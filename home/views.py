from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import request, JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from PIL import Image
from django.views.generic import \
    FormView, \
    ListView, \
    TemplateView, \
    DetailView, \
    DeleteView, \
    CreateView, \
    UpdateView

'''
FormView, \  # eine vielw klasse zum rendern einer bestimmten form 
    ListView, \  #eine View Klasse für das geordnete rendern vieler bestimmter objekte
    TemplateView, \ # gibt einzig und eallein ein template zurück (zb für eine anleitung usw...)
    DetailView, \ # ein detailierter form-view
    DeleteView, \ # um eine bereits vorhandene form zu löschen
    CreateView, \ # um eine neue form zu erstellen zu können
    UpdateView,      # um bestehende objekte zu bearbeiten
    '''
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, forms

from django.shortcuts import render, redirect, get_object_or_404
from home.forms import SignUpForm, UsersAddPictureForm, SearchPicturesForm, UsersAddGraphicForm, SignInForm
from home.models import UserAddPicture, SearchPictures, LoadVideoForPageCreation, User, GraphicUpload, \
    GraphicCategory, PictureCategories

from taggit.models import Tag
from django.template.defaultfilters import slugify



class HomeView(FormView, ListView):
    form_class = SearchPicturesForm
    template_name = 'home/base.html'
    success_url = reverse_lazy('home:index')
    model = SearchPictures
    object_list = SearchPictures.objects.all()

    def get_boolean_free(self):
        if 'free_button' in self.request.POST:
            return True
        return False

    def get_context_data(self, **kwargs):
        user_add_pictures = []
        graphic_uploads = []
        context = super().get_context_data(**kwargs)
        for prod_id in self.request.session.get('skey', []):
            if UserAddPicture.objects.filter(id=prod_id).exists():
                user_add_pictures.append(UserAddPicture.objects.get(id=prod_id))
            else:
                graphic_uploads.append(GraphicUpload.objects.get(id=prod_id))
        user_add_pictures += graphic_uploads
        context['session_data'] = user_add_pictures
        context['video'] = LoadVideoForPageCreation.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'add_tag_searchfield' in request.POST:
            if form.is_valid():
                form.save()
                return super().form_valid(form)
            else:
                raise ValidationError('Not allowed signs. Please try again ...')

        elif 'search_pictures' in request.POST:  #
            return super().form_valid(form)  # sucht anhand der Eingabe Bidler mit passenden Tagsw

        elif 'profile_button' in request.POST:
            return reverse_lazy('home:profile', kwargs={'pk': self.request.user.id})

        # TOPBAR-DROPDOWN BUTTON ACTIONS #########################################################################
        # hier nicht reverse_lazy verwenden da diese methode nur einen als string url zurückgibt aber nicht
        # auf eine andere seite weiterleitet I was hier aber gewünscht ist)
        if 'pic_free_button' in request.POST:
            request.session['free'] = True
            request.session['picture'] = True
            return redirect('home:category')

        elif 'picture_categories' in request.POST:
            request.session['free'] = False
            request.session['picture'] = True
            return redirect('home:category')

        elif 'graphic_categories' in request.POST:
            request.session['free'] = False
            request.session['picture'] = False
            return redirect('home:category')

        elif 'graphic_free' in request.POST:
             request.session['picture'] = False
             request.session['free'] = True
             return redirect('home:category')

        elif 'basket_button' in request.POST:
            return redirect('basket:basket')
        return render(request, self.template_name)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oups... Invalid input! Please try again.')
        return super().form_invalid(form)



######################  From filter images for category to detail image-view - both models


class CustomerDetailView(DetailView):
    model = UserAddPicture
    template_name = 'home/random_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pictures'] = UserAddPicture.objects.filter(user_name=self.object.user_name.id)
        context['other'] = UserAddPicture.objects.filter(category=self.object.category)
        with Image.open(self.object.picture) as img: # read the size of the self.object image that i can render it in the template
            context['image_size'] = img.size
        return context

    def post(self, request, *args, **kwargs):
        if 'basket_button' in request.POST:
            return redirect('basket:basket')



class SingleCategoyView(ListView): # filter images for category and model
    template_name = 'home/EVERY_single_pic_category_view.html'
    success_url = reverse_lazy('home:customer_detail_view')

    def get_queryset(self):
        # django will get the slug-parameter from the url
        slug = self.kwargs['slug']
        picture = self.request.session.get('picture', False)
        free = self.request.session.get('free', False)
        if picture and not free:
            # dont forget to get at first the categor with get_object_or_404-method and filter for slug
            category = get_object_or_404(PictureCategories, slug=slug)
            qs = UserAddPicture.objects.filter(category=category)
        elif picture and free:
            category = get_object_or_404(PictureCategories, slug=slug)
            qs = UserAddPicture.objects.filter(price__lt=0.01, category=category)
        elif not picture and not free:
            category = get_object_or_404(GraphicCategory, slug=slug)
            qs = GraphicUpload.objects.filter(category=category)
        else:
            category = get_object_or_404(GraphicCategory, slug=slug)
            qs = GraphicUpload.objects.filter(price__lt=0.01, category=category)
        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        picture = self.request.session.get('picture', False)
        free = self.request.session.get('free', False)
        slug = self.kwargs['slug']
        print(slug, free, picture)
        if picture and free:
            category = get_object_or_404(PictureCategories, slug=slug)
            context['image'] = UserAddPicture.objects.filter(price=0, category=category)
        elif picture and not free:
            category = get_object_or_404(PictureCategories, slug=slug)
            context['image'] = UserAddPicture.objects.filter(category=category)
        elif not picture and free:
            category = get_object_or_404(GraphicCategory, slug=slug)
            context['image'] = GraphicUpload.objects.filter(price=0, category=category)
        else:
            category = get_object_or_404(GraphicCategory, slug=slug)
            context['image'] = GraphicUpload.objects.filter(price=0, category=category)
        return context

    def get_success_url(self, slug):
        return reverse_lazy('home:customer_detail_view', kwargs={'slug': slug})


    def post(self, request, *args, **kwargs):
        if 'single_category_image' in request.POST:
            slug = request.POST.get('single_category_image')
            success_url = self.get_success_url(slug)
            return HttpResponseRedirect(success_url)
        elif 'basket_button' in request.POST:
            return redirect('basket:basket')



"""
    def post(self, request, *args, **kwargs):
        if 'single_category_image' in request.POST:
            object = self.get_context_data()['image']
            object_slug = object.slug
            product = get_object_or_404(object, slug=object_slug)
            return render(request, self.success_url, {'product': product})
        return render(request, self.template_name)
"""

    # Create your views here.
#################################  CATEGORY VIEWS ############################################
class CategoryView(ListView):
    template_name = 'home/categories.html'
    success_url = reverse_lazy('home:category_single')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_list = None

    def get_queryset(self):
        picture = self.request.session.get('picture', False)
        if picture:
            qs = PictureCategories.objects.all()
        else:
            qs = GraphicCategory.objects.all()
        return qs

    def get_success_url(self, slug):
        return reverse_lazy('home:category_single', kwargs={'slug': slug})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        picture = self.request.session.get('picture', False)
        if picture:
            context['model'] = PictureCategories
            context['image'] = PictureCategories.objects.all()
            context['imagemodel'] = UserAddPicture
        else:
            context['model'] = GraphicCategory
            context['image'] = GraphicCategory.objects.all()
            context['imagemodel'] = GraphicUpload
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_context_data()['image']
        if 'category_container' in request.POST:
            slug = request.POST.get('category_container')
            category = self.get_context_data()['model'].objects.get(slug=slug)
            final_object = self.get_context_data()['imagemodel'].objects.filter(category=category)

            # FALSCH return self.get_success_url(slug) dies würde einen fehler auslösen. versuche ->
            success_url = self.get_success_url(slug)
            return HttpResponseRedirect(success_url)
        elif 'basket_button' in request.POST:
            return redirect('basket:basket')


############## SINGLE CATEGORY VIEWS #################


class UsersImagesListView(ListView):
    template_name = 'home/my-images.html'
    model = UserAddPicture
    object_list = UserAddPicture.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture'] = UserAddPicture.objects.all()
        context['graphic'] = GraphicUpload.objects.all()
        context['free_image'] = UserAddPicture.objects.filter(price=0)
        context['free_graphic'] = GraphicUpload.objects.filter(price=0)

    def post(self, request, *args, **kwargs):
        # wenn ein button mit dem namen graphic_choice_button gedrückt wird, wird eine get-anfrage a den server gesendet.
        # in dieser wird dann die gewünschte form zurückgegeben.
        if 'graphic_choice_button' in request.POST:
            request.session['graphic'] = True
            self.model = GraphicUpload
            self.object_list = GraphicUpload.objects.filter(g_username=self.request.user.id)
            # sobald der user wieder den 'picture_choice_button' drückt, ...
        elif 'picture_choice_button' in request.POST:
            request.session['graphic'] = False
            # wird das model, die object_list und die restlichen kontextdaten benutzt ...
            self.model = UserAddPicture
            self.object_list = UserAddPicture.objects.filter(user_name=self.request.user.id)
            # und im template wiedergegeben.
        # statt der contextdats wird die object_list zurück gegeben um sie im templete zu rendern.
        elif 'basket_button' in request.POST:
            return redirect('basket:basket')
        return render(request, self.template_name, {'object_list': self.object_list})






class RegisterView(FormView):  # for user registration
    form_class = SignUpForm
    template_name = 'home/register.html'
    success_url = reverse_lazy('home:index')

    # die dispatch methode ist die erste die bei einer anfrage verarbeotet wird. Wenn man also einen user unter irgendwelchen Bedingungen
    # direkt auf eine andere Webpage umleiten will, sollte man das hier tun.
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.user.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            username = form.cleaned_data.get('username')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully registered")
                return self.form_valid(form)
            else:
                messages.error(request, "We were unable to log you in at this time")
        else:
            image = form.cleaned_data.get('profile_image')
            if image:
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


'''
        if self.request.accepts("text/html"): # wenn die foem invlid ist wird de user auf eine seite weitergeleitet.(irgndiwe rausfinden wie mann eine webpage mit einem counter bauen kann=)
            return response
        else:
'''


class UserLoginView(FormView):  # for user login
    form_class = SignInForm
    template_name = 'home/login.html'
    success_url = reverse_lazy('home:index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'login_button' in request.POST and form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return self.form_valid(form)
            else:
                raise ValidationError('Invalid Password or Username')
        elif 'basket_button' in request.POST:
            return redirect('basket:basket')
        else:
            return self.form_invalid(form)


####################### PROFILE VIEWS #######################

class ProfileView(UpdateView):
    template_name = 'home/profile.html'
    model = User
    success_url = reverse_lazy('home:profile')
    form_class = SignUpForm

    def get_initial(self):
        # MIT get_initial KANN DER VALUE WERT EINES INPUT FELDES VERÄNDERT WERDEN, DA DIESER AUF DEFAULT BEI EINEM
        # UPDATEVIEW DEN TATSÄCHLICHEN BISHERIGEN WERT DES FELDES ANZEIGT, WAS BEI PASSWORD DER GEHASHTE WERT IST
        initial = super(ProfileView, self).get_initial()
        initial['password'] = ''
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = User.objects.filter(id=self.request.user.id)
        return context

    def get_success_url(self):
        pass

    def dispatch(self, request, pk, *args, **kwargs):
        # zum init immer zuerst die super methode aufrufen !!! (nicht vergessen!!)
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated and pk == self.request.user.id:
            return response
        else:
            return HttpResponseRedirect(reverse_lazy('home:login'))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'profile_edit_button' in request.POST:
            return render(request, self.template_name, {'object': self.get_context_data()['object']})
        elif 'confirm_edit_button' in request.POST:
            if form.is_valid():
                form.save()
                return render(request, self.template_name, {'object': self.get_context_data()['object']})
        elif 'basket_button' in request.POST:
            return redirect('basket:basket')
        return render(request, self.template_name, {'object': self.get_context_data()['object']})


# erben lassen


class SettingsView(TemplateView):
    template_name = 'home/settings.html'


class UserAddPictureView(CreateView):  # for user create a recipe
    template_name = 'home/user_add_image.html'  # in welchem template die form dargestellt werdfen soll
    form_class = UsersAddPictureForm

    def get_success_url(self):
        # ein custom success url wird erstellt um beim Weiterleiten slug und pk im url mitgeben zu können
        # wenn der fehler 'ViewClass has no attribute self.object' auftritt schau dir die form_valid mathode an.
        # WICHTIG-Nicht den success url in der post methode returnen sonder die iform_valid methode.
        return reverse_lazy('home:user-picture', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    def get_context_data(self, **kwargs):

        # mit dieser definition der methode kann im html template über das schlüsselwort image_fields auf die
        # einzelnen attribute zugegriffen werden
        context = super().get_context_data(**kwargs)
        context['image_fields'] = UsersAddPictureForm(self.request.POST or None)

        # eine zweite form für das uploadden von graphics wird gesetzt.
        context['upload_graphic'] = UsersAddGraphicForm(self.request.POST or None)

        # um einer form einen default wert zu geben, wird das parameter initiol verwendet. Jetzt rendert user_name - field
        # jedes Mal bei einem upload den pk des users. (Der pk muss mitgegeben werden sonst kommt ein error.
        # Da aber nicht der pk, sondern der username gerndert werden soll, wird der username im template sepperat
        # gerendert und username_field.user_name als.as_hidden (desplay:none) gesetzt).
        context['username_field'] = UsersAddPictureForm(initial={'user_name': self.request.user.pk})

        # die 4 ersten Tags die geschrieben wurden, werden in tags gespeichert, sodass sie einfach im template gerendert
        # werden können # wichtig- hier nicht die Form, sondern das Model auswählen
        context['tags'] = UserAddPicture.tag_field.most_common()[:4]

        # eine instanz zum model wird erstellt und alle werte in model gespeichert damit darüber iteriert werden kann.
        context['model'] = UserAddPicture.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        # Dies gibt eine Liste aller Titel in der UserAddPicture-Tabelle zurück. flat=True gibt hierbei an,
        # dass das Ergebniss als liste zurückgegeben werden soll.

        if 'add_picture_button' in request.POST:
            form = self.get_form()
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
                return self.form_valid(form)
            else:
                return super().form_invalid(form)
        elif 'basket_button' in request.POST:
            return redirect('basket:basket')
        elif 'add_graphic_button' in request.POST:

            # der form variable wird der zugewiesene con´text von graphic zugewiesen um dqrüber iterieren zu können
            form = self.get_context_data()['upload_graphic']

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
                return self.form_valid(form)
            else:
                return super().form_invalid(form)

    def form_valid(self, form):
        # Erstellen Sie das neue Objekt und speichern Sie es in der Datenbank
        self.object = form.save()
        # Setzen Sie die Instanzvariable self.object
        self.object = form.instance
        # Rufen Sie die ursprüngliche form_valid-Methode auf
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Oups... Invalid input! Please try again.')
        return super().form_invalid(form)


class PictureDetailView(DetailView):
    model = UserAddPicture
    template_name = 'home/image_detail_view.html'



class CustomerGraphicDetailView(DetailView):
    model = GraphicUpload
    template_name = 'home/random_detail_view.html'


class PictureUpdateView(UpdateView):
    fields = ['title', 'picture', 'tag_field', 'category', 'price']
    template_name = 'home/edit.html'


    def get_queryset(self):
        graphic_edit = self.request.session.get('graphic', False)
        if graphic_edit:
            qs = GraphicUpload.objects.all()
        else:
            qs = UserAddPicture.objects.all()
        return qs


class ProfileUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'email', 'profile_image']
    success_url = reverse_lazy('home:profile')
    template_name = 'home/profile.html'


# LoginRequiredMixin???












class DeleteObjectView(DeleteView):
    model = SearchPictures
    success_url = reverse_lazy('home:index')
    template_name = 'home/base.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = get_object_or_404(SearchPictures, id=pk)
        return context

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(pk=pk, **kwargs)
        if 'delete_tag' in request.POST:
            context.name.delete()
            # jetzt muss nur noch pk im template übergeben werden dann funktioniert es
            return redirect(self.get_success_url())
        elif 'basket_button' in request.POST:
            return redirect('basket:basket')


# function based Views

def delete_object_view(request, pk):
    tag = get_object_or_404(SearchPictures, id=pk)
    tag.delete()
    return redirect(reverse('home:index'))  # der user wird zur my-recipes-page weitergeleitet.


def logout_view(request):
    logout(request)
    return redirect(reverse('home:index'))


























































































'''
    def get_success_url(self, pk=None, slug=None, **kwargs):
        self.object = get_object_or_404(UserAddPicture, id=pk, slug=slug)
        return reverse_lazy('home:user-picture', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


'''

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

'''
    def get_success_url(self):
        # ein custom success url wird erstellt um beim Weiterleiten slug und pk im url mitgeben zu können
        # wenn der fehler 'ViewClass has no attribute self.object' auftritt schau dir die form_valid mathode an.
        # WICHTIG-Nicht den success url in der post methode returnen sonder die iform_valid methode.
        return reverse_lazy('home:user-picture', kwargs={'pk': self.object.pk, 'slug': self.object.slug})
'''
