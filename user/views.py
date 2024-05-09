from django.http import HttpResponseRedirect
from django.shortcuts import render
from supabase import create_client, Client
from .services import *
import os
import requests
# Create function here.

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Create your views here.


def login_page(request):
    if get_user(supabase):
        return HttpResponseRedirect("/")
    else:
        return render(request, "login.html")


def logout(request):
    supabase.auth.sign_out()
    return HttpResponseRedirect("/login")


def landing(request):
    if request.method == "POST" or get_user(supabase):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = login(supabase, email, password)
        project_list = get_projects(supabase, user.user.id)
        return render(request, "landing.html", context={"dropdown": project_list.data})
    else:
        return login_page(request)


#below needs checking 
def chatbot(request):
    thread_id = "12345"  # Replace with the actual thread id
    url = f"https://mysite-pnb5.onrender.com/chat/?thread_id={thread_id}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
    else:
        raise Exception("API request failed")


def invite(request):
    if request.method == "POST":
        email = request.POST.get("email")
        project = request.POST.get("project")
        try:
            data = supabase.table('profiles').select(
                'id').eq('email', email).execute()
        except:
            raise Exception("User not found")
        try:
            res = supabase.table('access_control').insert(
                {"id": project,
                 "member": data.id,
                 }).execute()
            return res
        except:
            raise Exception("Failed to invite user")        
