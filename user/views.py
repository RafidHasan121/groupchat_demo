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
    return data


def get_projects(supabase, owner_id):
    response = supabase.table('projects').select(
        "name", count='exact').eq("owner", owner_id).execute()
    return response
# Create your views here.


def landing(request):
    if request.method == "POST" or get_user(supabase):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = login(email, password)
        project_list = get_projects(supabase, user.user.id)
        return render(request, "landing.html", context={"dropdown": project_list.data})
    else:
        return render(request, "landing.html")


def login_page(request):
    if get_user(supabase):
        return HttpResponseRedirect("/")
    else:
        return render(request, "login.html")


def logout(request):
    supabase.auth.sign_out()
    return HttpResponseRedirect("/login")
