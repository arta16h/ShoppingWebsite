import random
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone

# Create your views here.

def generate_2fa(request): 
    request.session["2FA"] = random.randint(1000, 9999)
    request.session["2fa_expire"] = (timezone.now() + timedelta(minutes=1)).strftime("%d/%m/%Y, %H:%M:%S")
    print(f"generated:{request.session['2FA']}  exp:{request.session['2fa_expire']}")
    return request  