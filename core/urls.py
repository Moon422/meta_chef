from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="core_index"),
    path("login/", views.app_login, name="core_login"),
    path("logout/", views.app_logout, name="core_logout"),
    path("profile/", views.profile, name="core_profile"),
    path("profile/edit", views.edit_profile, name="core_edit_profile"),
    path("profile/edit/email", views.edit_email, name="core_edit_email"),
    path("profile/edit/password", views.edit_password, name="core_edit_password"),
    path("food/<int:food_id>", views.food_view, name="core_food_view"),
]
