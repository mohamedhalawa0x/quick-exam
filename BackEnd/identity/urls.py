from django.urls import path
from . import views

app_name = "identity"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signout/", views.signout, name="signout"),
    path("activate/<code>/", views.activate_user_view, name="activate"),
]
