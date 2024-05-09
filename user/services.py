def login(supabase, email, password):
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

def invited_project(supabase, id):
    
    #probably need checking? 
    response = supabase.table('projects').select(
        "name").eq("access_control.member", id).execute()