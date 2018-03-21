# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
import time
import datetime
import jwt

#Contexts for OAuth Tokens
OAuthPost = 'post'
HASH_KEY = 'P4YL0Ad{34&ffs'
ALGORITHM = 'HS256'

#Singleton Tool Decorator
class Singleton:
    def __init__(self,decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Cannot Access. Try Acces from Intance Method')

    def __instancecheck__(self,inst):
        return isinstance(inst, self._decorated)

#Helper class used for Filter Request
class RequestFiltered:
    payload = {}
    headers = {}

    def __init__(self):
        self.namespace = "Demo"

    def insert(self,key,value):
        self.payload[key] = value

    def metaInsert(self,meta,value):
        self.headers[meta] = value

    def retrieve(self):
        return {'data':self.payload,'meta':self.headers}

#Asistente para generar la respuesta de las peticiones
class APIResponse:
    message = {}
    http_code = status.HTTP_200_OK

    def __init__(self):
        self.namespace = "Demo"

    #Default complete initializer after instance
    def initWith(self,code,msg=None,data=None):
        self.message['code'] = code
        self.message['message'] = msg
        self.message['data'] = data

    #Data Appender
    def insert(self,key,data=None):
        self.message['data'][key]=data

    #Configura el codigo de respuesta
    def setHttpCode(self,code):
        self.http_code = code

    #Configura el objeto de datos y custom en mensaje
    def setContent(self,msg=None,data=None):
        if data:
            self.message['data'] = data

        if msg:
            self.message['message'] = msg

    #Obtiene el objeto serializado
    def getSerialized(self):
        return self.message

    #Obtiene el status code
    def getHttpCode(self):
        return self.http_code

@Singleton
class APIMarshall():
    def __init__(self):
        self.namespace = "Demo"

    #Injection
    def containsInjectionData(self,data):
        return False

    #Inyecta CRUD data
    def injectCRUDInformation(self,model,entity='api'):
        if model:
            model.created_by = entity
            self.updateCRUDInformation(model,entity)

    #Actualiza CRUD data
    def updateCRUDInformation(self,model,entity='api'):
        if model:
            model.updated_on = datetime.datetime.today()
            model.updated_by = entity

    #Monitorea las conexiones entrantes
    def monitorIncomingStream(self,request,keys=None):
        filtered_request = RequestFiltered()

        if request.method != 'GET':
            for k in keys:
                filtered_request.insert(k,request.data[k])

        filtered_request.metaInsert('token',request.META.get('HTTP_FLKEY',''))
        filtered_request.metaInsert('auth',request.META.get('HTTP_AUTHKEY',''))
        filtered_request.metaInsert('type', request.method)

        return filtered_request.retrieve()

@Singleton
class Tokenizer:
    def __init__(self):
        self.namespace = "Demo"

    #Payload Generation
    def generatePayload(self, entity): #2 Days Validation
        orig = datetime.datetime.fromtimestamp(int(time.time()))
        new = orig + datetime.timedelta(days=1)
        payload = {'exp':int(time.mktime(new.timetuple())), 'entity': entity}

        return payload

    #OAuth Payload Generator
    def generateOAuthPayload(self,entity,context):
        orig = datetime.datetime.fromtimestamp(int(time.time()))
        new = orig + datetime.timedelta(days=1)
        payload = {'exp':int(time.mktime(new.timetuple())),'entity':entity,'ctx':context}

        return payload

    #Generate Encrypted Payload Data
    def maskSensitiveData(self, payload):
        return jwt.encode(payload,HASH_KEY,algorithm=ALGORITHM)

    #Generate Original Payload
    def unmaskSensitiveData(self, payload):
        try:
            return jwt.decode(encoded,HASH_KEY,algorithm=ALGORITHM)
        except jwt.ExpiredSignatureError:
            return {'exp':950797517,'entity':0,'ctx':'_'}

@Singleton
class OAuthManager:
    tokenizer = Tokenizer.Instance()
    valid_time_offset = 30

    def __init__(self):
        self.namespace = "Demo"

    #Generate OAuth Token
    def generateOauthToken(self,entity,context='auth'):
        payload = self.tokenizer.generateOAuthPayload(entity,context)
        return self.tokenizer.maskSensitiveData(payload)

    #Generate and keep hidden
    def generateToken(self,entity,ctx=0):
        if ctx == 1:
            return self.generateOauthToken(entity,OAuthPost)
        elif ctx == 2:
            return self.generateOauthToken(entity)

        return 'NO TOKEN FOR YOU'

    #Update OAuth Token
    def updateToken(self,token):
        if not self.isTokenValid(token):
            payload = self.tokenizer.unmaskSensitiveData(token)
            if payload['entity'] > 0:
                payload = self.tokenizer.generateOAuthPayload(payload['entity'],payload['ctx'])
                newToken = self.tokenizer.maskSensitiveData(payload)
            else:
                newToken = token
        else:
            newToken = token

        return newToken

    #Validate if OAuth Token is valid
    def isTokenValid(self,token):
        payload = self.tokenizer.unmaskSensitiveData(token)
        return (int(time.time()) > (int(payload['exp']) - self.valid_time_offset))

    #Verify if Token applies for context
    def isTokenValidForContext(self,token,context='auth'):
        if isTokenValid(token):
            payload = self.tokenizer.unmaskSensitiveData(token)
            return context == payload['ctx']

        return False
