from django.urls import path

from user import views

urlpatterns = [path('', views.register, name='register'),
               path('register/', views.register, name='register'),
               path('login/', views.login, name='login'),
               path('logout/', views.logout, name='logout'),
               path('account/', views.account, name='account'),
               path('reset_password/', views.reset_password, name='reset_password'),
               path('change_password/<str:token>', views.change_password, name='change_password')
               ]
