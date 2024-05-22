from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from supabase import create_client, Client
from .services import *
import os
import requests
# Create function here.

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_thread_id(body):
    project_id = body.get("project_id")
    data = supabase.table('chat_history').select('thread_id').eq('project_id', project_id).execute()
 
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
        self, shared = get_projects(supabase, user.user.id)
        return render(request, "landing.html", context={"self": self.data,
                                                        "shared": shared.data,
                                                        "url": url,
                                                        "key": key})
                                                        # "supabase": supabase})
    else:
        return login_page(request)


def invite(request):
    if request.method == "POST":
        email = request.POST.get("user_invite_email")
        project = request.POST.get("projectSelect")
        try:
            data = supabase.table('profiles').select(
                'id').eq('email', email).execute()
        except:
            raise Exception("User not found")
        try:
            project_id = supabase.table('projects').select(
                'id').eq('name', project).execute()
        except:
            raise Exception("Project not found")
        try:
            res = supabase.table('access_control').insert(
                {"id": project_id,
                "member": data.id,
                }).execute()
        except:
            raise Exception("Failed to invite user")
        return landing(request)

def history(request):
    thread_id = get_thread_id(request.POST)
    url == f"https://mysite-pnb5.onrender.com/chat/?thread_id={thread_id}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
    else:
        raise Exception("API request failed")

# below needs checking
def chatbot(request):
    thread_id = get_thread_id(request.POST)  # Replace with the actual thread id
    url = f"https://mysite-pnb5.onrender.com/chat/?thread_id={thread_id}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
    else:
        raise Exception("API request failed")
