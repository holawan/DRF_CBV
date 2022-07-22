from rest_framework.authentication import get_authorization_header,BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings

from authentication.models import User

class JWTAuthentications(BaseAuthentication) :
    
    def authenticate(self, request):
        # print(request.data)
        #요청에서 header를 가져온다. 
        auth_header = get_authorization_header(request)
        # print(auth_header)
        #받은 header를 utf-8로 디코딩한다. 
        auth_data = auth_header.decode('utf-8')
        # print(auth_data)
        #token 형식이 Bearer + Token 이므로, ' '로 나눈다. 
        auth_token = auth_data.split(' ')
        # print(auth_token)
        
        #토큰이 있는 리스트 길이가 2여야 하는데, 그렇지 않으면 유효하지 않은 토큰 
        if len(auth_token)!=2 :
            raise exceptions.AuthenticationFailed('Token not valid')
        
        #토큰만 취한다. 
        token=auth_token[1]
        
        try:
            #토큰과 SECRET_KEY, 발급시 사용한 알고리즘을 이용해서 디코딩한다. 
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            # print(payload)
            #디코딩 결과로 얻은 username으로 유저 정보를 가져온다. 
            username=payload['username']
            
            
            user=User.objects.get(username=username)
            
            return (user,token)
            
        #만료된 토큰일경우 예외처리 
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token is expired, login again')
        
        #디코딩 에러일 경우 예외처리 
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Token is invalid')
        
        #토큰 정보로 가져온 User가 존재하지 않을 경우 예외처리 
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed(
                'No Search user'
            )
        
        
        return super().authenticate(request)