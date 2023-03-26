from django.shortcuts import render

import requests
# import webbrowser
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# from verify_email.email_handler import send_verification_email
# from users.models import Profile
import os
# import smtplib

# Create your views here.

def user(request):
    return render(request,'user.html')
