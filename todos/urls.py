# from todos.views import CreateTodoAPIView,TodoListAPIView,TodosAPIView
from todos.views import TodosAPIView
from django.urls import path
urlpatterns = [
    path("",TodosAPIView.as_view(),name="todos")
    # path('create',ListCreateAPIView.as_view(),name='create-todo'),
    # path('list',ListCreateAPIView.as_view(),name='list-todo'),
]
