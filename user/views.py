from django.http import HttpResponseRedirect
from django.shortcuts import render
from supabase import create_client, Client
import os
# Create function here.

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def login(email, password):
    data = supabase.auth.sign_in_with_password(
        {"email": email, "password": password})
    return data


def get_user(supabase):
    data = supabase.auth.get_user()
    print(data)
    return data
# Create your views here.


def landing(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        data = login(email, password)
        res = supabase.auth.get_session()
        return render(request, "landing.html")
    else:
        if get_user(supabase):
            return render(request, "landing.html")
        return login_page(request)

def login_page(request):
    if get_user(supabase):
        return landing(request)
    else:
        return render(request, "login.html")