from django import forms
from django.core.mail import send_mail

from users.models import CustomUser, Contact


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        # if user.email:
        #     send_mail(
        #         'Goodreads',
        #         f"Hi {user.username}, Welcome to Goodreads",
        #         'djangosend@mail.ru',
        #         [user.email]
        #     )

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_img')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')
