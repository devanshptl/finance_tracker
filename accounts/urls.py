from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from accounts.views import *


urlpatterns = [
    path('login/', obtain_auth_token, name = "login"),
    path('signup/', user_registartion, name = 'signup'),
    path('logout/', logout_user, name = "logout"),
 ]