from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
import ticketSales, accounts
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.forms import ProfileRegisterForm,ProfileEditForm,UserEditForm
from django.contrib.auth.models import User
from accounts.models import ProfileModel
from accounts.serializers import UserSerializer, UserLoginSerializer, LogoutSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import permissions


#----------- JWT output views ----------

@api_view(['POST'])
@permission_classes([]) 
def register_view(request):
    role = request.data.get('role', ProfileModel.USER)
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    profile, _ = ProfileModel.objects.get_or_create(user=user)
    profile.role = role
    profile.save()
    
    refresh = RefreshToken.for_user(user)
    refresh['role'] = profile.role
    access = refresh.access_token
    access['role'] = profile.role
    
    return Response({
        'user': UserSerializer(user).data,
        'role':    profile.role,       
        'refresh': str(refresh),
        'access': str(access),
    })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid or expired token."})

        return Response({"detail": "Logout successfully."})


#----------- api views ----------

@api_view(['GET','POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)    
        serializer.is_valid(raise_exception=True)
        
        data = {}
        user = serializer.save()
        data["message"] = "Register is done!"
        data['token'] = Token.objects.get(user=user).key 
        return Response(data)
    
    return Response({'detail': 'registarion check.'})

@api_view(['GET','POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials.'})

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'detail': 'login check.'})



#----------- ui views ----------

def loginView(request):
    #Post
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get("next"))
                
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            context = {
                "username": username,
                "errorMessage": "کاربری با این مشخصات یافت نشد"
            }
            return render(request, "accounts/login.html",context)
     #Get
    else:
        return render(request, "accounts/login.html",{})

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse(ticketSales.views.concertListView))

@login_required
def profileView(request):
    profile = request.user.profile

    context = {
        "profile": profile
    }

    return render(request,"accounts/profile.html",context)



def profileRegisterView(request):

    if request.method == "POST":
        profileRegisterForm = ProfileRegisterForm(request.POST, request.FILES)
        if profileRegisterForm.is_valid():

            user = User.objects.create_user(username=profileRegisterForm.cleaned_data["username"],
                                email=profileRegisterForm.cleaned_data['email'],
                                password=profileRegisterForm.cleaned_data['password'],
                                first_name=profileRegisterForm.cleaned_data['first_name'],
                                last_name=profileRegisterForm.cleaned_data['last_name'])

            user.save()

            profileModel=ProfileModel(user=user,
                                    ProfileImage=profileRegisterForm.cleaned_data['ProfileImage'],
                                    Gender=profileRegisterForm.cleaned_data['Gender'],
                                    Credit=profileRegisterForm.cleaned_data['Credit'])

            profileModel.save()

            return HttpResponseRedirect(reverse(ticketSales.views.concertListView))
    else:
        profileRegisterForm = ProfileRegisterForm()

    context = {
        "formData": profileRegisterForm
    }

    return render(request,"accounts/profileRegister.html",context)


def ProfileEditView(request):
    
    if request.method == "POST":
        profileEditForm = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        userEditForm = UserEditForm(request.POST, instance=request.user)
        
        if profileEditForm.is_valid and userEditForm.is_valid:
            profileEditForm.save()
            userEditForm.save()
            return HttpResponseRedirect(reverse(accounts.views.profileView))
    else:
        profileEditForm = ProfileEditForm(instance=request.user.profile)
        userEditForm = UserEditForm(instance=request.user)

    context = {
        "profileEditForm": profileEditForm,
        "userEditForm": userEditForm,
        "ProfileImage": request.user.profile.ProfileImage,
    }

    return render(request,"accounts/profileEdit.html",context)