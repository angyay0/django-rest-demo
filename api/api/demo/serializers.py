from rest_framework import serializers
from api.demo.models import *

'''
    Following Serializers are used to CRUD Operations in Admin Views
    Using Links instead of PKs
'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name','last_name','email','status','created_date')

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('author','title','entry','key','created_date')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment','author')

class AccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Access
        fileds = ('user','device','description')
'''
class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        exclude = ('id','created_date','active')
'''
