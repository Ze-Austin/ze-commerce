from django.db import models
from django.contrib.auth.models import User
from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)


class Item(
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel,
    Model
    ):

    """
    ecommerce.Item
    Stores a single item entry in the shop
    """

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ["id"]

    def __str__(self):
        return self.title
    
    stock = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    def amount(self):
        # converts price from cents to dollars
        amount = float(self.price / 100)
        return amount
    
    def manage_stock(self, qty):
        # reduce Item stock by order quantity
        new_stock = self.stock - int(qty)
        self.stock = new_stock
        self.save()

    def check_stock(self, qty):
        # check if order quantity exceeds stock level
        if int(qty) > self.stock:
            return False
        return True
    
    def place_order(self, user, qty):
        # place an order
        if self.check_stock(qty):
            order = Order.objects.create(
                item = self,
                quantity = qty,
                user = user
            )
            self.manage_stock(qty)
            return order
        else:
            return None


class Order(
    TimeStampedModel,
    ActivatorModel,
    Model
    ):
    """
    ecommerce.Order
    Stores a single order entry, related to :model:`ecommerce.Item` and :model:`auth.User`
    """

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ["id"]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.item.title}'