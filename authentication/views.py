from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer

from authentication.forms import AccountLoginForm, AccountSignupForm
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from roombooking import settings

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
                account.is_active = False
                account.is_verified = False
                account.save()
                login(request, account)

                current_site = get_current_site(request)

                mail_subject = "Approve indepedent body's registration"
                message = render_to_string('authentication/activation_email.html', {
                    'user': 'GSec',
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(account.pk)).decode(),
                    'token': account_activation_token.make_token(account),
                    'account': account,
                })         
                
                to_email = "rohitrp@iitb.ac.in"
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                print(email)
                email.send()

                return HttpResponseRedirect('/')

            else:
                raise forms.ValidationError('User already exists')

    else:
        form = AccountSignupForm()

    return render(request, 'authentication/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        account = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        account = None
    
    if account is not None and account_activation_token.check_token(account, token):
        account.is_active = True
        account.is_verified = True
        account.save()

        return HttpResponse('Account has been activated')
    else:
        return HttpResponse('Activtion link is invalid!')

def account_login(request):
    if request.POST:
        form = AccountLoginForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data
            email = account['email']
            password = account['password']

            account = authenticate(email=email, password=password)

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