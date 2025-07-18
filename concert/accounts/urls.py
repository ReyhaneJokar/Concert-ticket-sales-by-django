from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


urlpatterns = [
    path('login/', views.loginView),
    path('logout/', views.logoutView),
    path('profile', views.profileView),
    path('profileRegister', views.profileRegisterView),
    path('profileEdit', views.ProfileEditView),
    path('registration_view', views.registration_view),
    path('login_view/', views.login_view),
    path('api/register/', views.register_view), 
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  #returns a new token
    path('api/logout/', views.LogoutView.as_view(), name='token_logout'),
    ]
