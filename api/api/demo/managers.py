# -*- coding: utf-8 -*-
from rest_framework import status
from api.demo.tools import OAuthManager,APIMarshall,OAuthPost,APIResponse
from api.demo.models import UserModel,UserStatus,Access,Entry,Comment
import datetime,traceback

#This Manager Base handles Access Rights Not public
class BaseManager:
    ctx = "None"
    OAuth = OAuthManager.Instance()

    def __init__(self):
        self.namespace = "DEMO"

    #Validate if has correct Auth Token for intereact with protected endpoints
    def Authorized(self,meta):
        isAuthorized = False
        try:
            if self.OAuth.isTokenValidForContext(meta):
                data = self.OAuth.tokenizer.unmaskSensitiveData(meta)
                user = UserModel.objects.get(id=data['entity'])
                status = user.status.title

                if 'Suspended' in status:
                    isAuthorized = False
                else:
                    isAuthorized = True
        except Exception:
            isAuthorized = False

        return isAuthorized

    #This method validates if can use protected endpoint
    def Context(self,meta):
        isAuthorized = False
        try:
            if self.OAuth.isTokenValidForContext(meta,self.ctx):
                data = self.OAuth.tokenizer.unmaskSensitiveData(meta)
                user = UserModel.objects.get(id=data['entity'])
                status = user.status.title

                if 'Suspended' in status:
                    isAuthorized = False
                else:
                    isAuthorized = True
        except Exception:
            isAuthorized = False

        return isAuthorized

#Manages public endpoints procedures
class APIManager(BaseManager):
    marshall = APIMarshall.Instance()
    SignupKeys = ['name','last','email','password']
    AuthKeys = ['user','dev_id','dev_desc','password']
    PostKeys = ['title','entry']

    def __init__(self):
        BaseManager.__init__(self)

    #Singn up request for new users
    def signupRequest(self,data):
        response = APIResponse()
        if data:
            if self.isSignupValid(data.keys()):
                try:
                    user = UserModel()
                    user.name = data['name']
                    user.last_name = data['last']
                    user.email = data['email']
                    user.password = data['password']
                    user.status = UserStatus.objects.get(title='Active')
                    self.marshall.injectCRUDInformation(user)
                    user.save()

                    response.initWith(0,'Successful') #Nothing to append
                except Exception as e:
                    print e
                    response.initWith(-1,'An error Occur')
                    response.setHttpCode(status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                response.initWith(100,'Invalid Data')
                response.setHttpCode(status.HTTP_406_NOT_ACCEPTABLE)
        else:
            response.initWith(100,'Invalid Data')
            response.setHttpCode(status.HTTP_400_BAD_REQUEST)

        return response

    #Authentication Requests for Registered Users
    def authenticationRequest(self, data):
        response = APIResponse()
        if data:
            try:
                user = UserModel.objects.get(email=data['user'])
                if 'Active' in user.status.title:
                    if user.password == data['password']:
                        access = Access()
                        access.user = user
                        access.device = data['dev_id']
                        access.description = data['dev_desc']
                        access.save()

                        response.initWith(0,'Welcome',{})
                        response.insert('user',{'name':user.name,'last':user.last_name,'email':user.email})
                        response.insert('api',self.OAuth.generateToken(user.id,1))
                        response.insert('auth',self.OAuth.generateToken(user.id,2))
                    else:
                        response.initWith(102,'Invalid Password')
                        response.setHttpCode(status.HTTP_403_FORBIDDEN)
                else:
                    response.initWith(101,'Account Suspended')
                    response.setHttpCode(status.HTTP_403_FORBIDDEN)

            except Exception as e:
                print e
                response.initWith(-1,'An error Occur')
                response.setHttpCode(status.HTTP_403_FORBIDDEN)
        else:
            response.initWith(100,'Invalid Data')
            response.setHttpCode(status.HTTP_400_BAD_REQUEST)

        return response

    #This Fetch all Post or One Post Depending on Key
    def fetchPosts(self,post=None):
        response = APIResponse()
        try:
            if post:
                data = self.getEntryData(post)
                response.initWith(0,'Successful',data)
            else:
                entries = []
                entryRaw = list(Entry.objects.all())
                for raw in entryRaw:
                    entries.append(self.getEntryData(raw.key))

                response.initWith(0,'Successful',entries)
        except Exception as e:
            print e
            response.initWith(-1,'Error on Posts')
            response.setHttpCode(status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    #This will create a post
    def postEntry(self,data,token):
        response = APIResponse()
        try:
            user = UserModel.objects.get(id=self.OAuth.tokenizer.unmaskSensitiveData(token)['entity'])
            entry = Entry()
            entry.author = user
            entry.title = data['title']
            entry.entry = data['entry']
            entry.updated_date = datetime.datetime.today()
            entry.save()
            response.initWith(0,'Successful',self.getEntryData(entry.key))
        except Exception as e:
            print e
            response.initWith(100,'An Error Occurs')
            response.setHttpCode(status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    #This will create a comment in the post
    def postComment(self,data,token):
        response = APIResponse()
        try:
            post = Entry.objects.get(key=data['post'])
            user = UserModel.objects.get(id=self.OAuth.tokenizer.unmaskSensitiveData(token)['entity'])
            comment = Comment()
            comment.comment = data['comment']
            comment.author = user
            comment.entry = post
            comment.save()

            response.initWith(0,'Successful')
        except Exception as e:
            respose.initWith(100,'An Error Occurs')
            response.setHttpCode(status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    #Retrieve one Entry Data
    def getEntryData(self,id):
        try:
            post=Entry.objects.get(key=id)
            comments = self.getComments(post.id)

            return {
                'author': post.author.name+' '+post.author.last_name,
                'id': post.key,
                'entry': post.entry,
                'title': post.title,
                'created': post.created_date,
                'edited': post.updated_date,
                'comments': comments
            }
        except Exception as e:
            print e
            return None

    #Retrieve Comments for a Post
    def getComments(self,key):
        try:
            comments = []
            raw_comments=list(Comment.objects.filter(entry=key))
            for com in comments:
                comments.append({
                    'comment':com.comment,
                    'author':com.author.name+' '+com.autho.last_name,
                    'date': com.created_date
                })

            return comments
        except Exception as e:
            print e
            return []


    #Validate Signup Keys
    def isSignupValid(self,keys):
        count = 0
        for k in self.SignupKeys:
            for dk in keys:
                if k == dk:
                    count += 1
        #Return True only if has the same keys
        return (count == len(self.SignupKeys))
