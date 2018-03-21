from rest_framework import serializers
from api.demo.models import *

'''
    Following Serializers are used to CRUD Operations in Admin Views
    Using Links instead of PKs
'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('id','created_date','created_by')

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        exclude = ('id','created_date')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        exclude = ('id','created_date')

class AccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Access
        exclude = ('id','created_date')
'''
class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        exclude = ('id','created_date','active')
'''
