from wsgiref import validate
from rest_framework import serializers 
from authentication.models import User
# 모델 시리어라이저를 상속받는 이유는 이미 모델이 있기 때문이다. 
class RegisterSerializer(serializers.ModelSerializer) :
    
    password = serializers.CharField(max_length=128,min_length=6,write_only=True)
    
    class Meta() :
        model=User
        fields = ('username','email','password')
        
    
    def create(create,validated_data) :

        return User.objects.create_user(**validated_data)
    
    
class LoginSerializer(serializers.ModelSerializer) :
    
    password = serializers.CharField(max_length=128,min_length=6,write_only=True)
    
    class Meta() :
        model=User
        fields = ('email','password','token',)
        
        read_only_fields = ['token']
        
    