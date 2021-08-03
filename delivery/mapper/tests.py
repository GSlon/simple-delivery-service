import mapper.services.dbservice as db
import mapper.services.mapapi as mp

from django.db.models import QuerySet
from django.test import TestCase
from registration.models import Order, Courier



class MapperTestCase(TestCase):
    def setUp(self):
        Courier.objects.create(name='tester', surname='testov',
                               email='test@gm.com', password_hash='123')

        self.courier = Courier.objects.filter(email='test@gm.com')[0]
        Order.objects.create(courier=self.courier, description='Moscow',
                             places={'end': '37.767, 55.6761', 'start': '37.784, 55.6674'})

        self.order = Order.objects.filter(courier=self.courier.id)[0]

    def test_get_orders_by_courier_id(self):
        self.assertEqual(db.get_orders_by_courier_id(self.courier.id)[0], self.order)

    def test__parse_orders_json(self):
        self.assertEqual(mp._parse_orders_json([self.order]), [(mp.Point(x=37.784, y=55.6674),
                                                               mp.Point(x=37.767, y=55.6761))])
