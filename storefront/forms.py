from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from customer_relations.models import Customer

class UserLoginForm(forms.Form):
    username_or_email_or_phone = forms.CharField(label='Username or Email or Phone')
    password = forms.CharField(widget=forms.PasswordInput())

class UserRegistrationForm(UserCreationForm):
    # Additional fields from the Customer model
    phone_number = forms.IntegerField(label=None)
    phone_number_cc = forms.IntegerField(initial=91)
    email = forms.CharField(label='Email', max_length=201, required=False)  # Allow empty email field

    class Meta:
        model = User
        fields = [
                    'first_name',
                    'last_name',
                    'username',
                    'email',
                    'phone_number_cc',
                    'phone_number',
                    'password1',
                    'password2'
                ]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Add Customer model fields to the form
        self.fields['phone_number_cc'].required = True
        self.fields['phone_number'].required = True
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div('first_name', css_class='mb-3'),
                Div('last_name', css_class='mb-3'),
                Div('username', css_class='mb-3'),
                Div('phone_number_cc', 'phone_number', css_class='mb-3 flex space-x-4'),
                Div('email', css_class='mb-3'),
                Div('password1', css_class='mb-3'),
                Div('password2', css_class='mb-3'),
                css_class='grid grid-cols-2 gap-4'
            ),
            Submit('submit', 'Register', css_class='btn btn-primary')
        )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Create a Customer instance associated with the user
            Customer.objects.create(
                user=user,
                phone_number_cc=self.cleaned_data['phone_number_cc'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email']
            )

        return user
