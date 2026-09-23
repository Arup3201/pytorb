from django.shortcuts import render

def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")

def profile(request):
    skills = "C, Python, Java, TypeScript, React, PostgreSQL, MySQL, Docker, AWS"
    profile_info = {
        'avatar_url': "https://lh3.googleusercontent.com/a/ACg8ocKqUa5riQe85OXVIEQxpHkmLVlWrpSZ4JCK4UxgyOubwuRxeb8t=s288-c-no",
        'display_name': "John", 
        'email': "john@example.com", 
        'username': "john", 
        'skills': skills.split(", "), 
        'total_projects': 12,
        'total_tasks_completed': 87,
        'task_completion_rate': f"{87/100:.2f}"
    }
    return render(request, 'profile.html', {'profile': profile_info})
