from django.db import models


class Courier(models.Model):
    name = models.CharField(max_length=40, null=False)
    surname = models.CharField(max_length=40, null=False)
    email = models.EmailField(max_length=40, null=False, unique=True)
    password_hash = models.CharField(max_length=80, null=False)

    def __str__(self):
        return 'Courier {0}'.format(self.id)


class Order(models.Model):
    # нельзя удалить курьера, пока его заказы не переназначены
    courier = models.ForeignKey(Courier, on_delete=models.PROTECT)
    description = models.CharField(max_length=40, null=True)
    places = models.JSONField(null=False)

    def __str__(self):
        return 'Order {0}'.format(self.id)
