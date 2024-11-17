from django.db import models


class Users(models.Model):
    """
    user's model for database
    """
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=12, blank=True, default='Не указан')
    birthday = models.DateField(blank=True)

    def __str__(self):
        return self.username


class Products(models.Model):
    """
    product's model for database
    """
    name_category = (
        ("jackets", "Куртки"),
        ("jeans", "Джинсы"),
        ("tshirts", "Футболки"),
        ("hoodies", "Худи"),
        ("shoes", "Кроссовки и кеды")
    )
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=7, choices=name_category, default='tshirts')
    description = models.TextField()
    price = models.IntegerField()
    image_product = models.ImageField(upload_to='images_product/')

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """
    cart's model for database
    """
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date_order = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} заказал {self.product.name}"
