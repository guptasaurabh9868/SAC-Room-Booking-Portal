from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer

from authentication.forms import AccountLoginForm, AccountSignupForm
from django.shortcuts import render, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login, logout

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def account_signup(request):
    if request.method == 'POST':
        form = AccountSignupForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data

            username = account['username']
            email = account['email']
            name = account['name']
            password = account['password']

            args = {'username': username, 'name': name}
            if not (Account.objects.filter(username=username).exists() or Account.objects.filter(email=email).exists()):
                account = Account.objects.create_user(email, password, **args)
                
                return HttpResponseRedirect('/auth/login')

            else:
                raise forms.ValidationError('User already exists')

    else:
        form = AccountSignupForm()

    return render(request, 'authentication/signup.html', {'form': form})

def account_login(request):
    if request.POST:
        form = AccountLoginForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data
            email = account['email']
            password = account['password']

            account = authenticate(request, email=email, password=password)

            if account is not None:
                login(request, account)

                return HttpResponseRedirect('/')

            return HttpResponseRedirect('/auth/login/')
        
    else:
        form = AccountLoginForm()

    return render(request, 'authentication/login.html', {'form': form})

def account_logout(request):
    logout(request)

    return HttpResponseRedirect('/')