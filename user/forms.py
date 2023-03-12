from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User


class LoginUserForm(forms.ModelForm):
    email = forms.CharField(label=' ', required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}))
    password1 = forms.CharField(label=' ', required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ("email", "password1",)
        extra_kwargs = {
            'password1': {'write_only': True},
        }

    def clean(self):
        super(LoginUserForm, self).clean()

        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')

        if not email:
            self._errors['email'] = self.error_class([
                'Please provide valid email'])
            self.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})

        if not password1:
            self._errors['password1'] = self.error_class([
                'Please provide valid password1'])
            self.fields['password1'].widget.attrs.update({'class': 'form-control is-invalid'})

        return self.cleaned_data


class RegisterUserForm(forms.ModelForm):
    email = forms.CharField(label=" ", required=True,
                            widget=forms.TextInput(attrs={'class': 'shadow-sm form-control', 'placeholder': 'Почта'}))
    password1 = forms.CharField(label=" ", required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'shadow-sm form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label=" ", required=True, widget=forms.PasswordInput(
        attrs={'class': 'shadow-sm form-control', 'placeholder': 'Подтверждение пароля'}))

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True},
        }

    def clean(self):
        super(RegisterUserForm, self).clean()

        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not email:
            self._errors['email'] = self.error_class([
                'Please provide valid email'])
            self.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})

        if not password1:
            self._errors['password1'] = self.error_class([
                'Please provide valid password1'])
            self.fields['password1'].widget.attrs.update({'class': 'form-control is-invalid'})

        if not password2:
            self._errors['password2'] = self.error_class([
                'Please provide valid password1'])
            self.fields['password2'].widget.attrs.update({'class': 'form-control is-invalid'})

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=' ',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label=' ',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    image = forms.FileField(label=' ', widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Фото', 'type': 'file'}))
    birthdate = forms.DateField(label=' ', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата Рождения', 'type': 'date'}))
    class Meta:
        model = User
        fields = ("first_name", "last_name", "image", "birthdate")