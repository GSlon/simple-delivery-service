from registration.models import Order, Courier


def get_orders_by_courier_id(id: int) -> list:
    return list(Order.objects.filter(courier=id))

