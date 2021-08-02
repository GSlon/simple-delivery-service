import logging
from typing import Union
from ..forms import SignInForm, SignUpForm
from ..models import Courier
from .hasher import hash_password, check_equal_pass_and_hash

logger = logging.getLogger(__name__)


def _check_user_exists(email: str) -> bool:
    courier = Courier.objects.filter(email=email)
    if len(courier) != 0:
        return True
    else:
        return False


def _get_user_id(email: str) -> int:
    courier = Courier.objects.filter(email=email)
    return courier[0].id


def _get_user_pass_hash(id: int) -> str:
    courier = Courier.objects.filter(id=id)
    return courier[0].password_hash


def _register_user(name: str, surname: str, email: str, password: str) -> None:
    courier = Courier(name=name, surname=surname, email=email, password_hash=hash_password(password))
    courier.save()


def _get_data_from_signin_form(form: SignInForm) -> list:
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    return [email, password]


def _get_data_from_signup_form(form: SignUpForm) -> list:
    name = form.cleaned_data['name']
    surname = form.cleaned_data['surname']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    return [name, surname, email, password]


def check_user_exists_from_form(form: Union[SignInForm, SignUpForm]) -> bool:
    email = form.cleaned_data['email']
    return _check_user_exists(email)


def try_register_user(form: SignUpForm) -> bool:
    email = form.cleaned_data['email']
    if not _check_user_exists(email):
        _register_user(*_get_data_from_signup_form(form))
        return True
    else:
        return False


def authorize_user(form: SignInForm) -> bool:
    email, password = _get_data_from_signin_form(form)
    id = _get_user_id(email)
    user_hash = _get_user_pass_hash(id)
    return check_equal_pass_and_hash(password, user_hash)


def get_user_id_from_form(form: Union[SignInForm, SignInForm]) -> int:
    email = form.cleaned_data['email']
    return _get_user_id(email)
