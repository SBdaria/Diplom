from django import forms


class UserRegisterForm(forms.Form):
    """
    form for registration
    """
    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    repeat_password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    phone = forms.CharField(max_length=12, required=False)
    birthday = forms.DateField(widget=forms.DateInput, required=False)


class UserAuthenticationForm(forms.Form):
    """
    form for authentication
    """
    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
