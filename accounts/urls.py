from django.urls import path

from . import views


urlpatterns = [

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),


    # ============================================================
    # HOME
    # ============================================================

    path(
        '',
        views.home_view,
        name='home'
    ),


    # ============================================================
    # RESTAURANT
    # ============================================================

    # Restaurant details / READ
    path(
        'restaurant/<int:restaurant_id>/',
        views.restaurant_detail_view,
        name='restaurant_detail'
    ),

    # Create restaurant
    path(
        'restaurants/create/',
        views.restaurant_create_view,
        name='restaurant_create'
    ),

    # Update restaurant
    path(
        'restaurants/update/<int:restaurant_id>/',
        views.restaurant_update_view,
        name='restaurant_update'
    ),

    # Delete restaurant
    path(
        'restaurants/delete/<int:restaurant_id>/',
        views.restaurant_delete_view,
        name='restaurant_delete'
    ),


    # ============================================================
    # FOOD
    # ============================================================

    # Food list / READ
    path(
        'foods/',
        views.food_list_view,
        name='food_list'
    ),

    # Create food
    path(
        'foods/create/',
        views.food_create_view,
        name='food_create'
    ),

    # Update food
    path(
        'foods/update/<int:food_item_id>/',
        views.food_update_view,
        name='food_update'
    ),

    # Delete food
    path(
        'foods/delete/<int:food_item_id>/',
        views.food_delete_view,
        name='food_delete'
    ),


    # ============================================================
    # CART
    # ============================================================

    # View cart
    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

    # Add to cart
    path(
        'cart/add/<int:food_item_id>/',
        views.add_to_cart_view,
        name='add_to_cart'
    ),

    # Update cart
    path(
        'cart/update/<int:cart_item_id>/',
        views.cart_update_view,
        name='cart_update'
    ),

    # Delete cart item
    path(
        'cart/delete/<int:cart_item_id>/',
        views.cart_delete_view,
        name='cart_delete'
    ),

]