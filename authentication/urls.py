from authentication import views
from django.urls import path,include



urlpatterns=[
    path('register',views.RegisterAPIView.as_view(),name='register'),
    path('login',views.LoginAPIView.as_view(),name='login'),
]