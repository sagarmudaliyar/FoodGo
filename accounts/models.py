from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):

    CATEGORY_CHOICES = [
        ('Pizza', 'Pizza'),
        ('Burgers', 'Burgers'),
        ('Indian', 'Indian'),
        ('Chinese', 'Chinese'),
        ('Desserts', 'Desserts'),
        ('Healthy', 'Healthy'),
        ('Beverages', 'Beverages'),
    ]

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    cuisine = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Pizza'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=4.5
    )

    delivery_time = models.CharField(
        max_length=50,
        default="20–30 min"
    )

    price_for_two = models.PositiveIntegerField(
        default=350
    )

    image = models.ImageField(
        upload_to='restaurants/',
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Pizza'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-rating', '-created_at']

    @property
    def price_info(self):
        return f"₹{self.price_for_two} for two"

    @property
    def reviews(self):
        return "100+ reviews"

    @property
    def badge(self):
        if self.rating >= 4.5:
            return "⭐ Popular"
        return "🍴 Recommended"

    @property
    def icon(self):
        icons = {
            'Pizza': '🍕',
            'Burgers': '🍔',
            'Indian': '🍛',
            'Chinese': '🥡',
            'Desserts': '🍰',
            'Healthy': '🥗',
            'Beverages': '🥤',
        }
        return icons.get(self.category, '🍴')

    @property
    def accent_color(self):
        colors = {
            'Pizza': '#e85d04',
            'Burgers': '#f59e0b',
            'Indian': '#dc2626',
            'Chinese': '#b91c1c',
            'Desserts': '#db2777',
            'Healthy': '#16a34a',
            'Beverages': '#2563eb',
        }
        return colors.get(self.category, '#0f766e')

    def __str__(self):
        return f"{self.name} ({self.cuisine})"


class FoodItem(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='food_items'
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    image = models.ImageField(
        upload_to='food_items/',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['restaurant', 'name']

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class CartItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'food_item'],
                name='unique_user_food_item'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name} ({self.quantity})"

    @property
    def subtotal(self):
        return self.quantity * self.food_item.price
