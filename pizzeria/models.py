import decimal
from decimal import Decimal
from django.db import models
from django.urls import reverse


class Customer(models.Model):
    """ Model for Customer """

    name = models.CharField(max_length=64)
    number = models.IntegerField()
    address = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("root")


class Size(models.Model):
    """ Model for Pizza Size """

    name = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Topping(models.Model):
    """ Model for Pizza Topping """

    name = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return self.name


# class Pizza(models.Model):
#     name = models.CharField(max_length=24)
#     size = models.ForeignKey(Size, null=True, on_delete=models.CASCADE, default=1)
#     price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

#     def save(self, *args, **kwargs):
#         if not Pizza.objects.filter(id=self.id):
#             super(Pizza, self).save(*args, **kwargs)
#         else:
#             price = Decimal("0.00")
#             if self.size:
#                 price = self.size.price
#                 print(price)

#             self.price = decimal.Decimal(str(price)).quantize(quant)
#             super(Pizza, self).save(*args, **kwargs)

#     def __str__(self):
#         if self.size.name:
#             name = self.size.name + " Pizza"
#         else:
#             name = "Pizza"
#         return name


# class Order(models.Model):
#     customer = models.ForeignKey(
#         Customer, on_delete=models.CASCADE, related_name="orders"
#     )
#     # total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
#     is_made = models.BooleanField(default=False)
#     is_dispatched = models.BooleanField(default=False)
#     is_collected = models.BooleanField(default=False)
#     is_delivered = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(f"{self.id}, (Customer: {self.customer.name})")

#     def get_absolute_url(self):
#         return reverse("new_customer", kwargs={"pk": self.id})


class Order(models.Model):
    """ Model for order """

    STATUS_CHOICES = (
        ("pending", "pending"),
        ("ready", "ready"),
        ("dispatched", "dispatched"),
        ("delivered", "delivered"),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    # total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.id}, (Customer: {self.customer.name})")

    def get_absolute_url(self):
        return reverse("new_customer", kwargs={"pk": self.id})


class OrderItem(models.Model):
    """ Model class for order item """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    topping = models.ForeignKey(
        Topping, on_delete=models.CASCADE, related_name="toppings"
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=5, null=True, blank=True, decimal_places=2)
    size = models.ForeignKey(
        Size, null=True, on_delete=models.CASCADE, default=1, related_name="sizes"
    )
    notes = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.size} {self.topping.name}")

    def save(self, *args, **kwargs):
        decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
        self.price = Decimal("0.00")
        total = (self.size.price + self.topping.price) * self.quantity
        # print("total Price for item is:", total)
        self.price = total
        super(OrderItem, self).save(*args, **kwargs)