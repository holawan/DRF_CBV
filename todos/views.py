from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView
from todos.models import Todo

from todos.serializers import TodoSerializer
# Create your views here.
from rest_framework.permissions import IsAuthenticated


class TodosAPIView(ListCreateAPIView) :
    serializer_class =TodoSerializer
    permission_classes=(IsAuthenticated,)
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

# class CreateTodoAPIView(CreateAPIView) :
    
#     serializer_class =TodoSerializer
#     permission_classes=(IsAuthenticated,)
    
#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.user)
    
    
# class TodoListAPIView(ListAPIView) :
    
#     serializer_class = TodoSerializer
#     permission_classes=(IsAuthenticated,)
    
    
#     queryset=Todo.objects.all()
    
    
#     def get_queryset(self):
#         return Todo.objects.filter(owner=self.request.user)
