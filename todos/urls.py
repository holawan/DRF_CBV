# from todos.views import CreateTodoAPIView,TodoListAPIView,TodosAPIView
from todos.views import TodosAPIView,TodoDetailAPIView
from django.urls import path
urlpatterns = [
    path("",TodosAPIView.as_view(),name="todos"),
    path("<int:id>",TodoDetailAPIView.as_view(),name="todo")
    # path('create',ListCreateAPIView.as_view(),name='create-todo'),
    # path('list',ListCreateAPIView.as_view(),name='list-todo'),
]
