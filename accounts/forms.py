from django import forms
from django.contrib.auth.models import User
from .models import Restaurant, FoodItem


# ============================================================
# REGISTER FORM
# ============================================================

class UserRegisterForm(forms.ModelForm):

    first_name = forms.CharField(
        label="Name",
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        label="Email",
        required=True
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "email",
            "username",
            "password",
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data


# ============================================================
# LOGIN FORM
# ============================================================

class UserLoginForm(forms.Form):

    username_or_email = forms.CharField(
        label="Username or Email",
        required=True
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True
    )


# ============================================================
# RESTAURANT FORM
# ============================================================

class RestaurantForm(forms.ModelForm):

    class Meta:

        model = Restaurant

        fields = [
            "name",
            "description",
            "cuisine",
            "rating",
            "delivery_time",
            "price_for_two",
            "image",
            "category",
            "is_active"
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

            "rating": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                    "max": "5"
                }
            ),
        }


# ============================================================
# FOOD ITEM FORM
# ============================================================

class FoodItemForm(forms.ModelForm):

    class Meta:

        model = FoodItem

        fields = [
            "restaurant",
            "name",
            "description",
            "price",
            "category",
            "image",
            "is_available"
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0"
                }
            ),
        }