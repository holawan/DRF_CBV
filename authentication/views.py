from django.shortcuts import render
from rest_framework.generics import GenericAPIView

from authentication.serializers import RegisterSerializer
from rest_framework import response,status
# Create your views here.
# Class Based View를 이용하는 이유 : Django의 많은 기능을 상속할 수 있기 때문

#serializer :사용자가 우리 프로그램에  json 데이터를 보낼 때 이를 파이썬 네이티브 객체로 바꾸는 역할을 한다.
# 왜냐하면 사용자가 JSON 데이터를 보낼 때 모댈 겍체처럼 매핑을 해야하기 때문 
#이것을 연결하는데 도움을 주는 것이 serializer이다. 
#또한 이를 python 객체를 json으로 변환하여유저에게 제공한다.  

class RegisterAPIView(GenericAPIView) :
    
    
    serializer_class=RegisterSerializer 
    
    
    def post(self,request) :
        serializers = self.serializer_class(data=request.data)  
        
        if serializers.is_valid() :
            serializers.save()
            return response.Response(serializers.data,status=status.HTTP_201_CREATED)
        return response.Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)