import taggit
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import models, FileField
from django.http import request
from django.utils.datetime_safe import datetime
from datetime import date
from .models import User, GraphicUpload, UserAddPicture
from taggit.forms import TagField
import string
from django.utils.safestring import mark_safe
from django.template import Template

from django.templatetags.static import static #to use my static-file-paths

class SignInForm(AuthenticationForm):
    class Meta:
        fields = [
            'username',
            'password'
        ]
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Your Username ...',
                       'class': 'login_form_field',
                       'id': 'login_username'
                       }

            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Your Password ...',
                    'class': 'login_form_field',
                    'id': 'login_password'
                }

            ),
        }

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if not data:
            raise forms.ValidationError('This Field is required ...')
        names = User.objects.values_list('username', flat=True)
        if data not in names:
            raise forms.ValidationError(f"The username '{data}' does not exist")
        return data

    def clean_password(self):
        data = self.cleaned_data.get('password')
        if not data:
            raise forms.ValidationError('This Field is required ...')
        return data









class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
            'profile_image',
        ]

        widgets = {
            'first_name': forms.TextInput(

                attrs={'class': 'input_form',
                       'placeholder': 'First Name',
                       'id': 'first_name_field'
                       }
            ),
            'last_name': forms.TextInput(

                attrs={'class': 'input_form',
                       'placeholder': 'Last Name',
                       'id': 'last_name_field'
                       }
            ),
            'username': forms.TextInput(

                attrs={'class': 'input_form',
                       'placeholder': 'Username ',
                       'id': 'value_field1'
                       }
            ),
            'email': forms.EmailInput(
                attrs={'class': 'input_form',
                       'placeholder': 'example@example.com ...',
                       'id': 'value_field2'
                       }
            ),

            'password': forms.PasswordInput(
                attrs={'class': 'input_form',
                       'placeholder': 'Choose a Strong Password!',
                       'id': 'value_field3'
                       }
            ),
            'password2': forms.PasswordInput(

                attrs={'class': 'input_form',
                       'placeholder': 'Confirm your Password ... ',
                       'id': 'value_field4'
                       }
            ),
            'profile_image': forms.FileInput(
                attrs={'id': 'profile_img_id',
                       'onchange': 'this.form.submit()',
                       'class': 'image_form'
                       }
            ),
        }

    def clean_email(self):
        data = self.cleaned_data.get('email')
        if not data:
            raise forms.ValidationError('Please enter a valid email address ...')
        elif '@' not in data:
            raise forms.ValidationError('The Form is not valid ...')
        return data

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if not data:
            raise forms.ValidationError('This Field is required ...')
        for unsupported_sign in string.punctuation:
            if unsupported_sign in data:
                raise forms.ValidationError(f'the following Signs are NOT allowed: {string.punctuation}')
        return data

    def clean_password(self):
        data = self.cleaned_data.get('password')
        if len(data) <= 6:
            raise forms.ValidationError('Your Password must be at least 6 characters ...')
        elif len(data) >= 32:
            raise forms.ValidationError('Max 32 Characters allowed ...')
        return data

    def clean_password2(self):
        data = self.cleaned_data.get('password2')
        if data != self.cleaned_data.get('password'):
            raise forms.ValidationError('These Passwords didnt match ...')
        return data


    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if len(data) == 0:
            raise forms.ValidationError('This Field is required ...')
        elif len(data) >= 100:
            raise forms.ValidationError('max 100 Characters allowed ...')
        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        if len(data) == 0:
            raise forms.ValidationError('This Field is required ...')
        elif len(data) >= 100:
            raise forms.ValidationError('max 100 Characters allowed ...')
        return data














    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'Wrong Username - Format. Please Try again ...'
        }
        self.fields['email'].error_messages = {
            'required': 'Wrong E-Mail Format. Please Try again ...'
        }
        self.fields['password'].error_messages = {
            'required': 'Wrong Password Format. Please try again ...'
        }
        self.fields['password2'].error_messages = {
            'required': 'These Passwords didnt match. Please try again ...'
        }
        self.fields['password2'].placeholder = {
            'Confirm your Password ...'
        }
        self.fields['password2'].label = 'Confirm '



class CustomTagWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs = {'class': 'form-control',
                      'id': 'tag_field_id',
                      'placeholder': ' ...',
                      'data-role': 'taginput',
                      'data-max-tags': '5',
                      'data-random-color': 'true',
                      }


class UsersAddPictureForm(forms.ModelForm):
    class Meta:
        model = UserAddPicture
        fields = ['title',
                  'picture',
                  'category',
                  'tag_field',
                  'user_name'
                  ]

        tag_field = taggit.forms.TagField(widget=CustomTagWidget)

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Title',
                       'class': 'form-control',
                       'id': "exampleFormControlInput1"
                       }
            ),
            'picture': forms.FileInput(
                attrs={'class': 'form-control',
                       "type": "file",
                       "id": "formFile",
                       }
            ),

            'category': forms.Select(
                attrs={'class': 'form-control',
                       'id': 'username_create_field',
                       'readonly': 'readonly'
                       }
            ),
            'user_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'user_name',
                    'readonly': 'readonly'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'  # So wird das default label nicht mehr angezeigt
        self.fields['picture'].label = 'Your Image'  # So wird das default label nicht mehr angezeigt
        self.fields['category'].label = 'Category'  # So wird das default label nicht mehr
        self.fields['tag_field'].label = 'Tags'  # So wird das default label nicht mehr angezeigt
        self.fields['user_name'].label = 'From: '


class UsersAddGraphicForm(forms.ModelForm):
    class Meta:
        model = GraphicUpload

        fields = ['title',
                  'picture',
                  'category',
                  'tag_field',
                  'g_username'
                  ]

        tag_field = taggit.forms.TagField(widget=CustomTagWidget)

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Title',
                       'class': 'form-control',
                       'id': "exampleFormControlInput1"
                       }
            ),
            'picture': forms.FileInput(
                attrs={'class': 'form-control',
                       "type": "file",
                       "id": "formFile",
                       }
            ),

            'category': forms.Select(
                attrs={'class': 'form-control',
                       'id': 'username_create_field',
                       'readonly': 'readonly'
                       }
            ),
            'g_username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'user_name',
                    'readonly': 'readonly'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'  # So wird das default label nicht mehr angezeigt
        self.fields['picture'].label = 'Your Image'  # So wird das default label nicht mehr angezeigt
        self.fields['category'].label = 'Category'  # So wird das default label nicht mehr
        self.fields['tag_field'].label = 'Tags'  # So wird das default label nicht mehr angezeigt
        self.fields['g_username'].label = 'From: '


'''
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='media')
    price = models.IntegerField()
    tag_field = models.CharField(max_length=180)
    user = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)  # 1 insanz der klasse wird gespeichert
    date = models.DateTimeField(auto_now_add=True)
'''
