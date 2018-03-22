# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import list_route
from api.demo.models import *
from api.demo.serializers import *
from api.demo.managers import APIManager
from api.demo.tools import APIResponse

'''
    These are CRUD Views
'''
class UserCRUD(viewsets.ModelViewSet):
    queryset = UserModel.objects.all().order_by('created_date')
    serializer_class = UserSerializer

class StatusCRUD(viewsets.ModelViewSet):
    queryset = UserStatus.objects.all()
    serializer_class = StatusSerializer

class EntryCRUD(viewsets.ModelViewSet):
    queryset = Entry.objects.all().order_by('created_date')
    serializer_class = EntrySerializer

class CommentCRUD(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_date')
    serializer_class = CommentSerializer

class AccessCRUD(viewsets.ModelViewSet):
    queryset = Access.objects.all().order_by('created_date')
    serializer_class = AccessSerializer

'''
class TokenCRUD(viewsets.ModelViewSet):
    queryset = Token.objects.all().filter(active=True).order_by('created_date')
    serializer_class = TokenSerializer
'''

'''
    These are Public endpoints
'''
class APIViewSet(viewsets.ViewSet):
    handler = APIManager()
    marshall = handler.marshall

    @list_route(methods=['post'])
    def signup(self,request):
        _content = self.marshall.monitorIncomingStream(
            request, self.handler.SignupKeys
        )
        _response = APIResponse()
        if _content['meta']['type'] == 'POST':
            _response = self.handler.signupRequest(_content['data'])
        else:
            _response.initWith(-1,'Ivalid Data')
            _response.setHttpCode(status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(_response.getSerialized(),status=_response.getHttpCode())

    @list_route(methods=['post'])
    def authenticate(self,request):
        _content = self.marshall.monitorIncomingStream(
            request, self.handler.AuthKeys
        )
        _response = APIResponse()
        if _content['meta']['type'] == 'POST':
            _response = self.handler.authenticationRequest(_content['data'])
        else:
            _response.initWith(-1,'Ivalid Data')
            _response.setHttpCode(status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(_response.getSerialized(),status=_response.getHttpCode())

    @list_route(methods=['get','post'])
    def post(self,request):
        _content = self.marshall.monitorIncomingStream(
            request, self.handler.PostKeys
        )
        _response = APIResponse()
        if self.handler.Authorized(_content['meta']['auth']):
            if _content['meta']['type'] == 'GET':
                key = request.GET.get('post')
                _response  = self.handler.fetchPosts(key)
            elif _content['meta']['type'] == 'POST':
                _response = self.handler.postEntry(_content['data'],_content['meta']['auth'])
            else:
                _response.initWith(-1,'Ivalid Data')
                _response.setHttpCode(status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            _response.initWith(-1,'Forbidden')
            _response.setHttpCode(status.HTTP_401_UNAUTHORIZED)

        return Response(_response.getSerialized(),status=_response.getHttpCode())

    @list_route(methods=['post'],url_path='post/comment')
    def comment(self,request):
        _content = self.marshall.monitorIncomingStream(
            request, ['post','comment']
        )
        _response = APIResponse()
        if self.handler.Authorized(_content['meta']['auth']):
            if _content['meta']['type'] == 'POST':
                _response = self.handler.postComment(_content['data'],_content['meta']['auth'])
            else:
                _response.initWith(-1,'Ivalid Data')
                _response.setHttpCode(status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            _response.initWith(-1,'Forbidden')
            _response.setHttpCode(status.HTTP_401_UNAUTHORIZED)

        return Response(_response.getSerialized(),status=_response.getHttpCode())
