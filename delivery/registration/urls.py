from django.urls import path
from registration import views

urlpatterns = [
    path('', views.default_path_redirect),
    path('signin', views.sign_in),
    path('signup', views.sign_up),
]