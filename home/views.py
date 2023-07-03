from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import request, JsonResponse
from django.urls import reverse_lazy, reverse
from django import forms
from django.views.generic import FormView, ListView, TemplateView, DetailView, DeleteView, CreateView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, forms

from django.shortcuts import render, redirect, get_object_or_404
from home.forms import SignUpForm, UsersAddPictureForm, SearchPicturesForm
from home.models import UserAddPicture, SearchPictures, LoadVideoForPageCreation, UserCredentials

from taggit.models import Tag
from django.template.defaultfilters import slugify


# Create your views here.

class HomeView(FormView, ListView):
    form_class = SearchPicturesForm
    template_name = 'home/base.html'
    success_url = reverse_lazy('home:index')
    model = SearchPictures
    object_list = SearchPictures.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video'] = LoadVideoForPageCreation.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'add_tag_searchfield' in request.POST:
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                raise ValidationError('Not allowed signs. Please try again ...')
        elif 'search_pictures' in request.POST:  #
            return redirect(self.get_success_url())  # sucht anhand der Eingabe Bidler mit passenden Tagsw

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oups... Invalid input! Please try again.')
        return super().form_invalid(form)


class RegisterView(FormView):  # for user registration
    form_class = SignUpForm
    template_name = 'home/register.html'
    success_url = reverse_lazy('home:index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'unhidden_mode' in request.POST:
            form.fields['password1'].widget = forms.PasswordInput()
            form.fields['password2'].widget = forms.PasswordInput()
            # später mit ajax im ui sichtbar machen

    def form_valid(self, form):
        form.save()  # wenn die form valid ist, wird sie gespeichert.
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        if user := authenticate(  # wenn der user authentifizert ist...
                self.request, username=username, password=password
        ):
            login(self.request, user)  # wird der user eingelogged,
            return redirect(self.get_success_url())  # er wird zum sucess_url weitergeleitetr.
        else:
            messages.error(self.request, 'Invalid input')  # ansonsten erhält der user diese Fhelermeldung
            return super().form_invalid(form)  # und diese


class UserLoginView(FormView):  # for user login
    form_class = AuthenticationForm
    template_name = 'home/login.html'
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')  # der Benutzername wird gespeichert
        password = form.cleaned_data.get('password')
        if user := authenticate(
                request, username=username, password=password
        ):
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, 'Invalid E-Mail or Password')  # ansonsten erhält der user diese Fhelermeldung
            return super().form_invalid(form)


class ProfileView(TemplateView):
    template_name = 'home/profile.html'


class SettingsView(TemplateView):
    template_name = 'home/settings.html'


class UserAddPictureView(CreateView):  # for user create a recipe
    template_name = 'home/user_add_image.html'  # in welchem template die form dargestellt werdfen soll
    form_class = UsersAddPictureForm
    success_url = reverse_lazy('home:my-pictures')

    # eine instanz der models wird erstellt und nach dem 'erscheinungsdatum' sortiert

    def get_context_data(self, **kwargs):

        # mit dieser definition der methode kann im html template über das schlüsselwort image_fields auf die
        # einzelnen attribute zugegriffen werden
        context = super().get_context_data(**kwargs)
        context['image_fields'] = UsersAddPictureForm(self.request.POST or None)

        # um einer form einen default wert zu geben, wird das parameter initiol verwendet. Jetzt rendert user_name - field
        # jedes mal bei einem upload den pk des users. (Der pk muss mitgegeben werden sonst kommt ein error.
        # Da aber nicht der pk sondern der username gerndert werden soll, wird der username im template sepperat
        # gerendert und username_field.user_name als.as_hidden (desplay:none) gesetzt)........
        context['username_field'] = UsersAddPictureForm(initial={'user_name': self.request.user.pk})

        # die 4 ersten Tags die geschrieben wurden, werden in tags gespeichert, sodass sie einfach im template gerendert
        # werden können # wichtig- hier nicht die Form, sondern das Model auswählen
        context['tags'] = UserAddPicture.tag_field.most_common()[:4]

        # eine instanz zum model wird erstellt und alle werte in model gespeichert damit darüber iteriert werden kann.
        context['model'] = UserAddPicture.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'add_picture_button' in request.POST:

            if form.is_valid():
                # get_form_save wird dda speicher der form übergeben
                get_form_save = form.save(commit=False)
                # slug wird der wert title übergeben
                get_form_save.slug = slugify(get_form_save.title)
                # die upgedatete form wird gespeichert
                get_form_save.save()
                # wichtig!!!
                form.save_m2m()
                # der user wird zur success_url weitergeleitet
                return redirect(self.get_success_url())
            else:
                # zeigt die fehler an die bei der
                print(form.errors)
                raise ValidationError('Not allowed signs. Please try again...')

    def form_valid(self, form):
        form.instance.author = self.request.user  # wenn die form valid ist, wird der benutzer der diese form erstellt hat, automatisch hinzugefügt.
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oups... Invalid input! Please try again.')
        return super().form_invalid(form)


'''

def detail_view(request, slug): # bei klick auf ein
    picture = get_object_or_404(UserAddPicture, slug=slug)
    context = {
        'picture': picture,
    }
    return render(request, 'home/image_detail_view.html', context)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = UserAddPicture.tag_field.most_common()[:4]
    posts = UserAddPicture.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'common_tags':common_tags,
        'posts':posts,
    }
    return render(request, 'home/user_add_image.html', context)
'''


class PictureDetailView(DetailView):
    model = UserAddPicture
    template_name = 'home/image_detail_view.html'


class UsersImagesListView(ListView):  # all recipes that thre user creaTEd LISTED VIEW
    template_name = 'home/my_recipes.html'
    form_class = UsersAddPictureForm


class DeleteObjectView(DeleteView):
    model = SearchPictures
    success_url = reverse_lazy('home:index')
    template_name = 'home/base.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = get_object_or_404(SearchPictures, id=pk)
        context.name.delete()
        return context

    def post(self, request, pk=None, *args, **kwargs):
        print('Level0')
        if 'delete_tag' in request.POST:
            print('Level1')
            tag = get_object_or_404(SearchPictures, id=pk)
            tag.delete()
            return redirect(self.get_success_url())


# function based Views

def delete_object_view(request, pk):
    tag = get_object_or_404(SearchPictures, id=pk)
    tag.delete()
    return redirect(reverse('home:index'))  # der user wird zur my-recipes-page weitergeleitet.


def logout_view(request):
    logout(request)
    return redirect(reverse('home:index'))


'''
def user_add_image_view(request):
    # wohin der user später weitergeeitet werden soll
    success_url = 'home:my-pictures'
    # die form klasse welche im templete gerendert werden soll und die method über welche daten gesendet werden(
    # post/get)
    form = UsersAddPictureForm(request.POST)
    # die 4 ersten Tags die geschrieben wurden werden in tags gespeichert, sodass sie einfach im template gerendert
    # werden können
    tags = UsersAddPictureForm.tag_field.most_common()[:4]
    # eine instanz zum model wird erstellt und alle werte in model gespeichert damit darüber iteriert werden kann.
    model = UserAddPicture.objects.all()
    if 'add_picture_button' in request.POST:

        if form.is_valid():
            print('Success')
            # get_form_save wird dda speicher der form übergeben
            get_form_save = form.save(commit=False)
            # slug wird der wert title übergeben
            get_form_save.slug = slugify(get_form_save.title)
            # die upgedatete form wird gespeichert
            get_form_save.save()
            # wichtig!!!
            form.save_m2m()
            # der user wird zur success_url weitergeleitet
            return render(request, reverse_lazy(success_url))
        else:
            raise ValidationError('No Success')


    context = {
        'title': form.fields['title'],
        'picture': form.fields['picture'],
        'price': form.fields['price'],
        'category': form.fields['category'],
        'tags': tags,
        'posts': model,
        'form': form,
    }

    return render(request, 'home/user_add_image.html', context)
            '''
