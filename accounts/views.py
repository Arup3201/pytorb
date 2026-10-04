import traceback
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from . import forms, services, selectors

def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if not form.is_valid() and form.errors.get("password2"):
            messages.add_message(request, messages.ERROR, "Passwords do not match.")
        else:
            try:
                services.create_user(email=form.data["email"], 
                                     username=form.data["username"], 
                                     first_name=form.data.get("first_name"), 
                                     last_name = form.data.get("last_name"), 
                                     password = form.data["password1"])
                messages.add_message(request, messages.SUCCESS, "You have been successfully registerd to Task Orbit!")
            except ValueError as ve:
                messages.add_message(request, messages.ERROR, str(ve))
            except Exception as e:
                traceback.print_exception(e)
                messages.add_message(request, messages.ERROR, "Something went wrong during registration. Please try again later.")
    else:
        form = forms.RegisterForm()
    
    return render(request, "register.html", context={'form': form})

def login(request):
    if request.method == "GET" and request.user.is_authenticated:
        next = request.GET["next"]
        return HttpResponseRedirect(next)

    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if not form.is_valid():
            error_messages = "\n".join([str(error) for error in form.non_field_errors()])
            messages.add_message(request, messages.ERROR, error_messages)
        else:
            try:
                services.login_user(request=request, 
                                    username=form.data["username"], 
                                    password=form.data["password"])
                return HttpResponseRedirect(reverse("accounts:profile"))
            except ValueError as v:
                messages.add_message(request, messages.ERROR, str(v))
    else:
        form = forms.LoginForm()

    return render(request, "login.html", {"form": form})

@login_required
def profile(request):
    profile = selectors.get_user_profile_data(user=request.user)
    edit_form = forms.AccountEditForm(instance=request.user)
    return render(request, 'profile.html', {'profile': profile, 'form': edit_form})

@login_required
def account_logout(request):
    services.logout_user(request=request)
    return HttpResponseRedirect(reverse('accounts:login'))

@login_required
def edit_account(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Request method POST is not allowed!")
        return HttpResponseRedirect(reverse('accounts:profile'))

    form = forms.AccountEditForm(request.POST)
    services.edit_account(user=request.user, 
                          first_name=form.data["first_name"], 
                          last_name=form.data["last_name"], 
                          skills=form.data["skills"])
    messages.add_message(request, messages.SUCCESS, "User profile data has been updated!")
    return HttpResponseRedirect(reverse('accounts:profile'))

@login_required
def upload_avatar(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Only POST method not allowed for this URL")
        return HttpResponseRedirect(reverse('accounts:profile'))

    file = request.FILES['avatar']
    try:
        services.save_user_avatar(user=request.user, file=file)
    except Exception as e:
        traceback.print_exception(e)
        messages.add_message(request, messages.ERROR, "Failed to edit the image! Please try again.")
        return HttpResponseRedirect(reverse('accounts:profile'))

    return HttpResponseRedirect(reverse('accounts:profile'))
