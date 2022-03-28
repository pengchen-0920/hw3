from django.db import models

# Create your models here.
class Order(models.Model):
    orderId = models.CharField(primary_key=True, max_length=20)
    customer = models.CharField(max_length=20)
    items = models.CharField(max_length=20)

    def __str__(self):
        return self.orderId + ':' + self.customer + ' orders ' + self.items
