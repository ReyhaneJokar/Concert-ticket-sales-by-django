from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.loginView),
    path('logout/', views.logoutView),
    path('profile', views.profileView),
    path('profileRegister', views.profileRegisterView),
    path('profileEdit', views.ProfileEditView),
    path('registration_view', views.registration_view),
    path('login_view', views.login_view),
    ]