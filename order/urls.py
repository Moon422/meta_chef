from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_orders, name='order_manage_orders'),
    path('add/<int:food_id>/', views.add_to_order, name='order_add_to_order'),
    path('remove/<int:order_id>/', views.remove_from_order, name='order_remove_from_order'),
    path('place/', views.place_order, name="order_place_order"),
    path('cancel/', views.cancel_order, name='order_cancel_order'),
    path('review/<int:order_item_id>/', views.submit_review, name='order_cancel_order')
]
