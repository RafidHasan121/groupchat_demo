from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from supabase import create_client, Client
from .services import *
import os
import requests
import json
# Create function here.

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_thread_id(body):
    project_id = body.get("project_id")
    data = supabase.table('chat_history').select(
        'thread_id').eq('project_id', project_id).execute()

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
    if get_user(supabase):
        user = get_user(supabase)
        self, shared = get_projects(supabase, user.user.id)
        return render(request, "landing.html", context={"self": self.data,
                                                        "shared": shared.data,
                                                        "url": url,
                                                        "key": key})
    else:
        if request.method == "POST":
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
        url = "https://cogo.creatego.io/add/"
        data = {
            "email": email,
            "project_id": project
        }
        data = json.dumps(data)
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
        else:
            raise Exception(response.text)
        return landing(request)


def history(request):
    thread_id = get_thread_id(request.POST)
    url == f"https://cogo.creatego.io/chat/?thread_id={thread_id}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
    else:
        raise Exception("API request failed")


"""
schema for table access control:

id: int8, incremental, non primary key
created_at: timestamp default
member: user.id foreign key, primary key( part of composite key)
project: project.id foreign key, primary key( part of composite key)

"""
