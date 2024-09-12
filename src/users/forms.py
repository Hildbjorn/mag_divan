from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import Profile


class ProfileCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    """
    error_messages = {
        'password_mismatch': ('Введенные пароли не совпадают',),
    }

    email = forms.EmailField(label='E-mail:',
                             required=True,
                             widget=forms.TextInput(attrs={'id': 'id_username',
                                                           'aria-describedby': 'emailHelp'}, ),
                             error_messages={'unique': ("Пользователь с таким e-mail уже зарегистрирован",)})

    password1 = forms.CharField(label='Пароль:',
                                strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'new-password',
                                                                  'aria-describedby': 'password1Help'}),
                                help_text=password_validation.password_validators_help_text_html(),
                                )
    password2 = forms.CharField(label='Пароль еще раз:',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'autocomplete': 'new-password',
                                                                  'aria-describedby': 'password2Help'}),
                                strip=False,
                                help_text="Введите тот же пароль, что ввели выше.",
                                )

    class Meta:
        model = Profile
        fields = (
            'email',
            'password1',
            'password2'
        )


class ProfileChangeForm(UserChangeForm):
    """
    Форма изменения пользователя.
    """

    class Meta:
        model = Profile
        fields = ('email',)


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя в модели Profile.
    """

    last_name = forms.CharField(required=False,
                                label='Фамилия:',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'id': 'last_name',
                                                              'placeholder': 'Фамилия'}))

    first_name = forms.CharField(required=False,
                                 label='Имя:',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'id': 'first_name',
                                                               'placeholder': 'Имя'}))

    middle_name = forms.CharField(required=False,
                                  label='Отчество:',
                                  widget=forms.TextInput(attrs={'class': 'form-control ',
                                                                'id': 'middle_name',
                                                                'placeholder': 'Отчество'}))

    avatar = forms.ImageField(required=False,
                              label='Аватар:',
                              widget=forms.FileInput(attrs={'class': 'form-control form-control-sm field_hidden',
                                                            'id': 'avatar_field',
                                                            'accept': '.jpg, .png, .gif',
                                                            'input type': 'file'}))

    phone = forms.CharField(required=False,
                            label='Телефон:',
                            widget=forms.TextInput(attrs={'class': 'tel form-control',
                                                          'id': 'phone',
                                                          'placeholder': 'Телефон'}))

    email = forms.EmailField(label='E-mail:',
                             required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'id': 'email',
                                                           'placeholder': 'user@mail.ru'}),
                             error_messages={'unique': ("Пользователь с таким e-mail уже зарегистрирован"),
                                             'invalid': ("Введите корректное значение")})

    agreement = forms.BooleanField(required=True,
                                   label='',
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                     'type': 'checkbox',
                                                                     'role': 'switch',
                                                                     'id': 'agreement',
                                                                     'checked': ''}))

    class Meta:
        model = Profile
        fields = (
            'last_name',
            'first_name',
            'middle_name',
            'avatar',
            'phone',
            'email',
            'agreement',
        )
