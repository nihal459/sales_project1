from django.db import models

# Create your models here.
class Salesman(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_join = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    unit_type = models.CharField(max_length=50, unique=True)  # e.g., kg, g, liter

    def __str__(self):
        return self.unit_type

class Inventory(models.Model):
    product_name = models.CharField(max_length=255)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Stock available
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit

    def __str__(self):
        return f"{self.product_name} - {self.product_category.name}"



class AddToCart(models.Model):
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    product_quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=True, default=0.00)

    def __str__(self):
        return f"{self.product.product_name} added on {self.date_added}"

class Checkout(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    checkout_date = models.DateTimeField(auto_now_add=True)
    salesman = models.CharField(max_length=100, null=True, blank=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Checkout for {self.customer_name}"

    def save(self, *args, **kwargs):
        if self.total_price is not None and self.amount_received is not None:
            self.amount_remaining = self.total_price - self.amount_received
            if self.amount_remaining == 0:
                self.payment_status = True
        super().save(*args, **kwargs)
    
class OrderedProduct(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='ordered_products')
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    product_quantity = models.FloatField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, editable=True, null=True, blank=True)

    def __str__(self):
        return f"{self.checkout.customer_name}"

