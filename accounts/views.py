from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .models import Restaurant, FoodItem, CartItem
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    RestaurantForm,
    FoodItemForm,
)


# ============================================================
# REGISTER
# ============================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.first_name = form.cleaned_data["first_name"]
            user.email = form.cleaned_data["email"]

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            messages.success(
                request,
                "Account created successfully! Please login."
            )

            return redirect("login")

    else:
        form = UserRegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = UserLoginForm(request.POST)

        if form.is_valid():

            username_or_email = form.cleaned_data[
                "username_or_email"
            ]

            password = form.cleaned_data["password"]

            # Try username login
            user = authenticate(
                request,
                username=username_or_email,
                password=password
            )

            # If username login fails, try email login
            if user is None:

                try:

                    user_obj = User.objects.get(
                        email__iexact=username_or_email
                    )

                    user = authenticate(
                        request,
                        username=user_obj.username,
                        password=password
                    )

                except User.DoesNotExist:

                    user = None

            # Successful login
            if user is not None:

                login(request, user)

                return redirect("home")

            # Failed login
            messages.error(
                request,
                "Invalid username/email or password. Please try again."
            )

    else:

        form = UserLoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect("login")


# ============================================================
# HOME
# ============================================================

@login_required
def home_view(request):

    restaurants = Restaurant.objects.all()

    foods = FoodItem.objects.all()

    return render(
        request,
        "accounts/home.html",
        {
            "restaurants": restaurants,
            "foods": foods,
        }
    )


# ============================================================
# RESTAURANT - READ / DETAILS
# ============================================================

@login_required
def restaurant_detail_view(request, restaurant_id):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    foods = FoodItem.objects.filter(
        restaurant=restaurant
    )

    return render(
        request,
        "accounts/restaurant_detail.html",
        {
            "restaurant": restaurant,
            "foods": foods,
        }
    )


# ============================================================
# RESTAURANT - CREATE
# ============================================================

@login_required
def restaurant_create_view(request):

    if request.method == "POST":

        form = RestaurantForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Restaurant added successfully!"
            )

            return redirect("home")

    else:

        form = RestaurantForm()

    return render(
        request,
        "accounts/restaurant_form.html",
        {
            "form": form,
            "title": "Add Restaurant"
        }
    )


# ============================================================
# RESTAURANT - UPDATE
# ============================================================

@login_required
def restaurant_update_view(request, restaurant_id):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    if request.method == "POST":

        form = RestaurantForm(
            request.POST,
            instance=restaurant
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Restaurant updated successfully!"
            )

            return redirect(
                "restaurant_detail",
                restaurant_id=restaurant.id
            )

    else:

        form = RestaurantForm(
            instance=restaurant
        )

    return render(
        request,
        "accounts/restaurant_form.html",
        {
            "form": form,
            "title": "Edit Restaurant",
            "restaurant": restaurant,
        }
    )


# ============================================================
# RESTAURANT - DELETE
# ============================================================

@login_required
def restaurant_delete_view(request, restaurant_id):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    if request.method == "POST":

        restaurant.delete()

        messages.success(
            request,
            "Restaurant deleted successfully!"
        )

        return redirect("home")

    return render(
        request,
        "accounts/restaurant_confirm_delete.html",
        {
            "restaurant": restaurant
        }
    )


# ============================================================
# FOOD - READ
# ============================================================

@login_required
def food_list_view(request):

    foods = FoodItem.objects.all()

    return render(
        request,
        "accounts/foods.html",
        {
            "foods": foods
        }
    )


# ============================================================
# FOOD - CREATE
# ============================================================

@login_required
def food_create_view(request):

    if request.method == "POST":

        form = FoodItemForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Food added successfully!"
            )

            return redirect("food_list")

    else:

        form = FoodItemForm()

    return render(
        request,
        "accounts/food_form.html",
        {
            "form": form,
            "title": "Add Food"
        }
    )


# ============================================================
# FOOD - UPDATE
# ============================================================

@login_required
def food_update_view(request, food_item_id):

    food = get_object_or_404(
        FoodItem,
        id=food_item_id
    )

    if request.method == "POST":

        form = FoodItemForm(
            request.POST,
            instance=food
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Food updated successfully!"
            )

            return redirect("food_list")

    else:

        form = FoodItemForm(
            instance=food
        )

    return render(
        request,
        "accounts/food_form.html",
        {
            "form": form,
            "title": "Edit Food",
            "food": food,
        }
    )


# ============================================================
# FOOD - DELETE
# ============================================================

@login_required
def food_delete_view(request, food_item_id):

    food = get_object_or_404(
        FoodItem,
        id=food_item_id
    )

    if request.method == "POST":

        food.delete()

        messages.success(
            request,
            "Food deleted successfully!"
        )

        return redirect("food_list")

    return render(
        request,
        "accounts/food_confirm_delete.html",
        {
            "food": food
        }
    )


# ============================================================
# CART - VIEW
# ============================================================

@login_required
def cart_view(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    total = sum(
        item.food_item.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        "accounts/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# ============================================================
# CART - ADD
# ============================================================

@login_required
def add_to_cart_view(request, food_item_id):

    food = get_object_or_404(
        FoodItem,
        id=food_item_id
    )

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        food_item=food,
        defaults={
            "quantity": 1
        }
    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    messages.success(
        request,
        f"{food.name} added to cart!"
    )

    return redirect("cart")


# ============================================================
# CART - UPDATE
# ============================================================

@login_required
def cart_update_view(request, cart_item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        user=request.user
    )

    if request.method == "POST":

        quantity = int(
            request.POST.get(
                "quantity",
                1
            )
        )

        if quantity > 0:

            cart_item.quantity = quantity

            cart_item.save()

        else:

            cart_item.delete()

    return redirect("cart")


# ============================================================
# CART - DELETE
# ============================================================

@login_required
def cart_delete_view(request, cart_item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        user=request.user
    )

    cart_item.delete()

    messages.success(
        request,
        "Item removed from cart."
    )

    return redirect("cart")