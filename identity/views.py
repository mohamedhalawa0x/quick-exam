from django.shortcuts import render
from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponseRedirect, Http404
from .forms import UserCreationForm, UserLoginForm
from .models import EmailActivation

User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        # redirect admins to admin panel !
        if request.user.is_admin:
            return HttpResponseRedirect("/admin/")
        # redirect normal users to thier dashboard
        return HttpResponseRedirect("/courses/")
    # anonymous users should Sign-in / Sign-up first
    return signin(request)


def signin(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email_ = form.cleaned_data.get('email')
        # get the user object
        user_obj = User.objects.get(email=email_)
        # login !
        login(request, user_obj)
        # admins will be redirected to the admin panel, otherwise redirect to dashboard
        if user_obj.is_admin:
            return HttpResponseRedirect("/admin/")
        return HttpResponseRedirect("/courses/")
    return render(request, "index.html", {'form': form})


def signup(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        # After Registeration Redirect to Welcome Page
        return HttpResponseRedirect("/")
    return render(request, "identity/signup.html", context)


def signout(request, *args, **kwargs):
    logout(request)
    # return to homepage !
    return HttpResponseRedirect("/")

    # activating accounts based on activation code sent via mail !


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        act_profile_qs = EmailActivation.objects.filter(key=code)
        if act_profile_qs.exists() and act_profile_qs.count() == 1:
            act_obj = act_profile_qs.first()
            if not act_obj.expired:
                user_obj = act_obj.user

                user_obj.is_active = True
                user_obj.save()

                act_obj.expired = True
                act_obj.save()
            return HttpResponseRedirect("/")
    raise Http404
