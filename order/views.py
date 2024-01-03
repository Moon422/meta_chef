from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import redirect, render
from core import models

# Create your views here.
def manage_orders(request: HttpRequest):
    if request.user.is_authenticated:
        ctx = {}
        try:
            open_order = models.Order.objects.get(Q(customer=request.user) & Q(orderstatus=models.OrderStatus.NOT_PLACED))
            order_items = models.OrderItem.objects.filter(order=open_order)
            prices = [item.quantity * item.food.price for item in order_items]

            different_kitchens = len(set(item.food.kitchen.id for item in order_items))
            delivery_charge = different_kitchens * 20 + 20
            
            total_cost = sum(prices) + delivery_charge            

            ctx['order_items'] = list(zip(order_items, prices))
            ctx['order'] = open_order
            ctx['total_cost'] = total_cost            
        except:
            pass
        
        delivered_orders = models.Order.objects.filter(orderstatus=models.OrderStatus.DELIVERED)
        reviewed_delivered_order_items = []
        unreviewed_delivered_order_items = []

        for order in delivered_orders:
            _order_items = models.OrderItem.objects.filter(order=order)
            for item in _order_items:
                if item.review_submitted:
                    reviewed_delivered_order_items.append(item)
                else:
                    unreviewed_delivered_order_items.append(item)
        
        ctx['reviewed_delivered_order_items'] = reviewed_delivered_order_items
        ctx['unreviewed_delivered_order_items'] = unreviewed_delivered_order_items            
            
        return render(request, "order/order.html", ctx)            
    else:
        return HttpResponse("Please login to manage orders. <a href='/login'>Login</a>", status=401)

def add_to_order(request: HttpRequest, food_id: int):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                open_order = models.Order.objects.get(Q(customer=request.user) & Q(orderstatus=models.OrderStatus.NOT_PLACED))
            except:
                open_order = models.Order.objects.create(customer=request.user, phonenumber='01748689039', discount=0, delivery_charge=20)
            try:
                food = models.Food.objects.get(id=food_id)
                quantity = int(request.POST.get('quantity'))

                if quantity:
                    try:
                        open_order_item = models.OrderItem.objects.get(Q(order=open_order) & Q(food=food))
                        open_order_item.quantity += quantity
                        open_order_item.save()
                    except:
                        models.OrderItem.objects.create(food=food, quantity=quantity, order=open_order)
                    
                    return redirect(request.META.get("HTTP_REFERER"))
                else:
                    return HttpResponseBadRequest('quantity is zero')
            except:
                return HttpResponseBadRequest("food does not exist")
        else:
            return HttpResponseBadRequest("method not implemented")
    else:
        return HttpResponse("Please login to manage orders. <a href='/login'>Login</a>", status=401)

def remove_from_order(request: HttpRequest, order_id: int):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                open_order = models.Order.objects.get(Q(customer=request.user) & Q(orderstatus=models.OrderStatus.NOT_PLACED))
                order_item = models.OrderItem.objects.get(Q(id=order_id) & Q(order=open_order))
                order_item.delete()
                return redirect(request.META.get("HTTP_REFERER"))
            except:
                return HttpResponseBadRequest("no pending orders")
        else:
            return HttpResponseBadRequest("method not implemented")
    else:
        return HttpResponse("Please login to manage orders. <a href='/login'>Login</a>", status=401)

def place_order(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                open_order = models.Order.objects.get(Q(customer=request.user) & Q(orderstatus=models.OrderStatus.NOT_PLACED))
                open_order.orderstatus = models.OrderStatus.ORDER_PLACED
                open_order.save()
                return redirect(request.META.get("HTTP_REFERER"))
            except:
                return HttpResponseBadRequest("no pending orders")
        else:
            return HttpResponseBadRequest("method not implemented")
    else:
        return HttpResponse("Please login to manage orders. <a href='/login'>Login</a>", status=401)
    
def cancel_order(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                open_order = models.Order.objects.get(Q(customer=request.user) & Q(orderstatus=models.OrderStatus.NOT_PLACED))
                open_order.delete()
                return redirect(request.META.get("HTTP_REFERER"))
            except:
                return HttpResponseBadRequest("no pending orders")
        else:
            return HttpResponseBadRequest("method not implemented")
    else:
        return HttpResponse("Please login to manage orders. <a href='/login'>Login</a>", status=401)
