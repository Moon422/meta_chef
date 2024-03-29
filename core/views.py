from datetime import datetime, timezone, timedelta
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models import Avg, Q
from django.shortcuts import render, redirect

from .models import Food, FoodCategory, Profile, Rating, FoodViewed

def rating_rounder(rating: float):
    return 5 if rating > 4.5 else 4.5 if rating > 4 else 4 if rating > 3.5 else 3.5 if rating > 3 else 3 if rating > 2.5 else 2.5 if rating > 2 else 2 if rating > 1.5 else 1.5 if rating > 1 else 1 if rating > 0.5 else 0.5 if rating > 0 else 0

# Create your views here.
def index(request: HttpRequest):
    if request.method == "GET":
        newly_added = Food.objects.order_by("-date_created")[:5]
        ratings = [Rating.objects.filter(food=food).aggregate(Avg("rating", default=0))['rating__avg'] for food in newly_added]
        ratings = [rating_rounder(rating) for rating in ratings]
        
        hour_of_the_day = datetime.now(tz=timezone(timedelta(hours=6))).hour
        hour_of_the_day = 'BREAK_FAST' if 5 <= hour_of_the_day < 11 else 'LUNCH' if 12 < hour_of_the_day < 16 else 'DINNER' if 19 <= hour_of_the_day < 24 else 'SNACK'

        if hour_of_the_day == 'BREAK_FAST':
            hour_of_the_day_suggestions = [fc.food for fc in FoodCategory.objects.select_related('food').select_related('category').filter(category__title='breakfast')]
        elif hour_of_the_day == 'LUNCH':
            hour_of_the_day_suggestions = [fc.food for fc in FoodCategory.objects.select_related('food').select_related('category').filter(category__title='lunch')]
        elif hour_of_the_day == 'DINNER':
            hour_of_the_day_suggestions = [fc.food for fc in FoodCategory.objects.select_related('food').select_related('category').filter(category__title='dinner')]
        else:
            food_ids = (fc.food.id for fc in FoodCategory.objects.filter(Q(category__title='snack') | Q(category__title='fastfood')))
            hour_of_the_day_suggestions = list(Food.objects.filter(id__in=food_ids))
        
        hour_of_the_day_suggestions = [(food, rating_rounder(Rating.objects.filter(food=food).aggregate(Avg("rating", default=0))['rating__avg'])) for food in hour_of_the_day_suggestions]
        hour_of_the_day_suggestions.sort(key=lambda f: f[1], reverse=True)

        ctx = {
            "newly_added": list(zip(newly_added, ratings)),
            "hour_of_the_day": hour_of_the_day,
            "hour_of_the_day_suggestion": hour_of_the_day_suggestions
        }

        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            ctx['profile'] = profile
        except:
            pass

        return render(request, "core/index.html", ctx)
    else:
        return HttpResponseBadRequest()

def app_login(request: HttpRequest):
    if request.method == "GET":
        ctx = {
            "redirect": request.META.get("HTTP_REFERER")
        }

        return render(request, "core/login.html", ctx)
    elif request.method == "POST":
        redirect_to = request.POST.get("redirect")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            print(redirect_to)
            return redirect("core_index")
        else:
            return HttpResponse("fucked up")

def app_logout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect("core_index")

def profile(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            profile = Profile.objects.get(user=user)
            ctx = {
                "profile": profile,
                "edit_profile": False,
                "edit_email": False,
                "edit_password": False
            }
            return render(request, "core/profile.html", ctx)
        else:
            return HttpResponseBadRequest("fuck it...")
    else:
        return HttpResponse("bullshit", status=401)

def edit_profile(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            profile = Profile.objects.get(user=user)
            ctx = {
                "profile": profile,
                "edit_profile": True,
                "edit_email": False,
                "edit_password": False
            }
            return render(request, "core/profile.html", ctx)
        elif request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phonenumber = request.POST.get("phonenumber")
            user = get_user_model().objects.filter(id=request.user.id)
            user.update(first_name = first_name, last_name = last_name)
            
            profile = Profile.objects.get(user=user)
            profile.phonenumber = phonenumber
            profile.save()

            return redirect("core_profile")
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponse(status=401)

def edit_email(request: HttpRequest):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)

        if request.method == "GET":
            ctx = {
                "profile": profile,
                "edit_profile": False,
                "edit_email": True,
                "edit_password": False
            }
            return render(request, "core/profile.html", ctx)
        elif request.method == "POST":
            email = request.POST.get("email")
            get_user_model().objects.filter(id=request.user.id).update(email=email)

            return redirect("core_profile")
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponse(status=401)

def edit_password(request: HttpRequest):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)

        if request.method == "GET":
            ctx = {
                "profile": profile,
                "edit_profile": False,
                "edit_email": False,
                "edit_password": True
            }
            return render(request, "core/profile.html", ctx)
        elif request.method == "POST":
            current_password = request.POST.get("current_pass")
            new_password = request.POST.get("new_pass")
            if request.user.check_password(current_password):
                user = get_user_model().objects.get(id=request.user.id)
                user.set_password(new_password)
                user.save()
                user = authenticate(request, username=user.get_username(), password=new_password)

                if user:
                    login(request, user)
                    return redirect("core_profile")
                else:
                    return HttpResponse("fucked up")                
            else:
                return HttpResponseBadRequest("Password not matched")
        else:
            return HttpResponseBadRequest("method not implemented")
    else:
        return HttpResponse(status=401)

def food_view(request: HttpRequest, food_id: int):
    if request.method == "GET":
        try:
            food = Food.objects.get(id=food_id)
            rating = Rating.objects.filter(food=food).aggregate(Avg("rating", default=0))['rating__avg']
            rating = rating_rounder(rating)

            kitchen_suggestions = Food.objects.filter(Q(kitchen=food.kitchen) & ~Q(id=food.id))
            kitchen_suggestions = [(food, rating_rounder(Rating.objects.filter(food=food).aggregate(Avg("rating", default=0))['rating__avg'])) for food in kitchen_suggestions]        
            kitchen_suggestions.sort(key=lambda f: f[1], reverse=True)

            if request.user.is_authenticated:
                user = Profile.objects.get(user=request.user)
                recently_viewed = FoodViewed.objects.filter(Q(viewer=user) & ~Q(food=food)).order_by("-view_date")[:4]
                recently_viewed = [rv.food for rv in recently_viewed]
                recently_viewed = [(food, rating_rounder(Rating.objects.filter(food=food).aggregate(Avg("rating", default=0))['rating__avg'])) for food in recently_viewed]

                try:
                    fv = FoodViewed.objects.get(Q(viewer=user) & Q(food=food))
                    fv.view_date = datetime.now()
                    fv.view_count += 1
                    fv.save()
                except:
                    FoodViewed.objects.create(food=food, viewer=user, view_date=datetime.now())

            ctx = {
                'profile': user,
                'food': food,
                'rating': rating,
                'kitchen_suggestions': kitchen_suggestions,
                'recently_viewed': recently_viewed
            }
            return render(request, "core/food_details.html", ctx)
        except Exception as e:
            return HttpResponse("Food does not exist", status=404)
    else:
        return HttpResponseBadRequest("Method not implemented")
