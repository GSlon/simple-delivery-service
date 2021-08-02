from django import forms


class SignInForm(forms.Form):
    email = forms.EmailField(required=True, max_length=40, label=False,
                             widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(required=True, max_length=20, label=False,
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    required_css_class = "signin"


class SignUpForm(forms.Form):
    email = forms.EmailField(required=True, max_length=40, label=False,
                             widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    name = forms.CharField(required=True, max_length=20, label=False,
                           widget=forms.TextInput(attrs={'placeholder': 'name'}))
    surname = forms.CharField(required=True, max_length=20, label=False,
                              widget=forms.TextInput(attrs={'placeholder': 'surname'}))
    password = forms.CharField(required=True, max_length=20, label=False,
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    required_css_class = "signin"  # применим один css файл на обе формы
