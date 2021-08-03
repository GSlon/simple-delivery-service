from django.db.models import QuerySet
from registration.models import Order, Courier


def get_orders_by_courier_id(id: int) -> QuerySet:
    return Order.objects.filter(courier=id)

