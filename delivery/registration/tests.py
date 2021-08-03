import bcrypt
import registration.services.dbservice as db
import logging

from django.http import QueryDict
from django.test import TestCase
from .models import Courier
from .forms import SignInForm, SignUpForm
from django.test import Client

c = Client()
signin_response = c.post('', {'email': 'test@gm.com', 'password': '123'})
signup_response = c.post('', {'email': 'test@gm.com', 'name': 'tester', 'surname': 'testov', 'password': '123'})


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.password = b'123'
        hashpassw = bcrypt.hashpw(self.password, bcrypt.gensalt())

        Courier.objects.create(name='tester', surname='testov',
                               email='test@gm.com', password_hash=hashpassw)

        self.courier = Courier.objects.filter(email='test@gm.com')[0]
        self.signinform = SignInForm(QueryDict('email=test@gm.com&password=123'))
        self.signupform = SignUpForm(QueryDict('email=test@gm.com&name=tester&surname=testov&password=123'))

        # чтобы было доступно поле cleared_data
        self.signinform.is_valid()
        self.signupform.is_valid()

    def test_get_user_id(self):
        self.assertEqual(db._get_user_id('test@gm.com'), self.courier.id)

    def test_get_user_pass_hash(self):
        self.assertEqual(db._get_user_pass_hash(self.courier.id), self.courier.password_hash)

    def test_get_data_from_signin_form(self):
        self.assertEqual(db._get_data_from_signin_form(self.signinform), ['test@gm.com', '123'])

    def test_get_data_from_signup_form(self):
        self.assertEqual(db._get_data_from_signup_form(self.signupform),
                         ['tester', 'testov', 'test@gm.com', '123'])

    def test_register_user(self):
        self.courier.delete()
        db._register_user(*db._get_data_from_signup_form(self.signupform))
        self.assertEqual(len(Courier.objects.filter(email='test@gm.com')), 1)

    def test_check_user_exists_from_form(self):
        self.assertEqual(db.check_user_exists_from_form(self.signinform), True)

    def test_get_user_id_from_form(self):
        self.assertEqual(db.get_user_id_from_form(self.signinform), self.courier.id)

