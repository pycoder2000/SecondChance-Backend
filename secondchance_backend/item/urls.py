from django.urls import path

from . import api


urlpatterns = [
    path("", api.items_list, name="api_items_list"),
    path("create/", api.create_item, name="api_create_item"),
    path("<uuid:pk>/", api.item_detail, name="api_items_detail"),
    path("<uuid:pk>/buy/", api.buy_item, name="api_buy_item"),
    path("<uuid:pk>/rentals/", api.item_rentals, name="api_item_rentals"),
    path("<uuid:pk>/toggle_favorite/", api.toggle_favorite, name="api_toggle_favorite"),
]
