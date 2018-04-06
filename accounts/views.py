from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

from .models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to login:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists.com',
        [email],
    )
    messages.success(
        request,
        'Check your email, we have sent you a link you can use to login.'
    )
    return redirect('/')


def login(self):
    return redirect('/')
