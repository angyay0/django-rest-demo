# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
from api.demo.tools import OAuthManager,APIMarshall,OAuthPost,APIResponse
from api.demo.models import UserModel,UserStatus,Access
import datetime

#This Manager Base handles Access Rights Not public
class BaseManager:
    ctx = "None"
    OAuth = OAuthManager.Instance()

    def __init__(self):
        self.namespace = "DEMO"

    def Authorized(self,meta):
        isAuthorized = False
        try:
            if self.OAuth.isTokenValidForContext(meta):
                data = self.oauth.tokenizer.unmaskSensitiveData(meta)
                user = UserModel.objects.get(id=data['entity'])
                status = user.status.title

                if 'Suspended' in status:
                    isAuthorized = False
                else:
                    isAuthorized = True
        except Exception:
            isAuthorized = False

        return isAuthorized

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

class APIManager(BaseManager):
    marshall = APIMarshall.Instance()
    SignupKeys = ['name','last','email','password']
    AuthKeys = ['user','dev_id','dev_desc','password']

    def __init__(self):
        BaseManager.__init__(self)

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

    def isSignupValid(self,keys):
        count = 0
        for k in self.SignupKeys:
            for dk in keys:
                if k == dk:
                    count += 1
        #Regresa la cantidad de encuentros entre llaves
        return (count == len(self.SignupKeys))
