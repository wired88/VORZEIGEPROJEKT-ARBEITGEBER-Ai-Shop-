import taggit
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import request
from django.utils.datetime_safe import datetime
from datetime import date
from .models import UserCredentials, UserAddPicture, SearchPictures
from taggit.forms import TagField


class SignInForm(AuthenticationForm):
    class Meta:
        fields = (
            'username',
            'password'
        )
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Your Username ...',
                       'class': 'form-control',
                       'id': 'login_username'
                       }

            ),
            'password': forms.PasswordInput(
                attrs={
                    'placeholder': 'Your Password ...',
                    'class': 'form-control',
                    'id': 'login_password'
                }
            ),
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserCredentials
        fields = [
            'username',
            'password1',
            'password2',

        ]

        # def __init__(self, *args, **kwargs):
        #  super().__init__(*args, **kwargs)
        #     self.fields['date_created'].widget.attrs['placeholder'] = datetime.now().strftime('%d/%m/%Y')  # 2
        #  2 so gibt man einem field - placeholder den wert einer Variable/ attributes. Man kann dies auch mit der Zuweisung eine modelattributes machen

        widgets = {
            'username': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Your Name ... ',
                       'id': 'value_field'
                       }
            ),

            'password1': forms.HiddenInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Choose a Strong Password!',
                       'id': 'value_field'
                       }
            ),
            'password2': forms.HiddenInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Confirm your Password ... ',
                       'id': 'value_field'
                       }
            ),

        }


class SearchPicturesForm(forms.ModelForm):
    class Meta:
        model = SearchPictures
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Search for Picture Tags ... ',
                    'class': 'search_field_home',
                    'id': 'name_field',
                    'label': ''
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ''  # So wird das default label nicht mehr angezeigt


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
                  'price',
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

            'price': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': '0.00',
                       'id': 'recipe_field'
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
        self.fields['price'].label = 'Price'  # So wird das default label nicht mehr angezeigt
        self.fields['category'].label = 'Category'  # So wird das default label nicht mehr
        self.fields['tag_field'].label = 'Tags'  # So wird das default label nicht mehr angezeigt
        self.fields['user_name'].label = 'From: '

'''
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='media')
    price = models.IntegerField()
    tag_field = models.CharField(max_length=180)
    user = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)  # 1 insanz der klasse wird gespeichert
    date = models.DateTimeField(auto_now_add=True)



'''
