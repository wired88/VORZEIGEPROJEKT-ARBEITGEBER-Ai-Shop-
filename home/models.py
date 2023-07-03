from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator, DecimalValidator
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from djangoProject.settings import MEDIA_URL
from django.contrib.auth.models import User


# Create your models here.
class SearchPictures(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class UserCredentials(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, help_text='Enter your email address', default='example@example.com')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.username} {self.password} {self.email} {self.date_created}'


from embed_video.fields import EmbedVideoField


class LoadVideoForPageCreation(models.Model):  # the model to load videos on the homepage
    video = models.FileField(upload_to='media')  # same like models.URLField()

    class Meta:
        managed = False


class ProfileImage(models.Model):
    profile_image = models.ImageField()


class UserAddPicture(models.Model):  # User Create new Picture
    class CategoryChoices(models.TextChoices):
        StarWars = 'Star Wars', 'Star Wars'
        Space = 'Space', 'Space'
        Nature = 'Nature', 'Nature'
        Cars = 'Cars', 'Cars'
        Animals = 'Animals', 'Animals'
        Architecture = 'Architecture', 'Architecture'
        Food = 'Food', 'Food'
        Travel = 'Travel', 'Travel'
        People = 'People', 'People'
        Sports = 'Sports', 'Sports'
        Fashion = 'Fashion', 'Fashion'
        Art = 'Art', 'Art'
        Technology = 'Technology', 'Technology'
        Landscapes = 'Landscapes', 'Landscapes'
        Cityscapes = 'Cityscapes', 'Cityscapes'
        Portraits = 'Portraits', 'Portraits'
        Other = 'Other', 'Other'
        Abstract = 'Abstract', 'Abstract'
        Comic = 'Comic', 'Comic'
        Monochrome = 'Monochrome', 'Monochrome'
        Macro = 'Macro', 'Macro'
        Streetyart = 'Street Art', 'Street Art'
        Documentary = 'Documentary', 'Documentary'
        Life = 'Life', 'Life'
        Underwater = 'Underwater', 'Underwater'
        Epic = 'Epic', 'Epic'

    title = models.CharField( # der title wird im url dargestellt
        error_messages={'required': 'Title is required'},
        max_length=100
    )
    picture = models.ImageField(
        error_messages={'required': 'Load min. 1 Picture ...'},
        upload_to='media',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )  # mit FileExtensioValidator können die erlaubten dateiformate festgelegt werden.
    price = models.DecimalField(
        error_messages={'required': 'Price in range 0 to 9999€ is required'},
        max_digits=6,
        max_length=6,
        decimal_places=2,
        help_text='Note: Price in EUR ...',
        validators=[
            MinValueValidator(0),  # mit validators kann min und max-value für das integerfield festgelegt werden.
            MaxValueValidator(9999),
            DecimalValidator(
                max_digits=6,
                decimal_places=2)
        ]
    )
    category = models.CharField(
        max_length=100,
        choices=CategoryChoices.choices,
        default='Category'
    )

    tag_field = TaggableManager(
        help_text='Choose some tags that people can find your Picture ...')
    user_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE)  # 1 insanz der klasse wird gespeichert
    date = models.DateTimeField(
        auto_now_add=True
    )
    slug = models.SlugField(
        default='',
        unique=True,
        max_length=100
    )

    def __str__(self):
        return f' {self.title}' \
               f' {self.picture}' \
               f' {int(self.price)}' \
               f' {self.tag_field}' \
               f' {self.user_name} ' \
               f' {self.date}'  # 1 jetzt kann jeder in der klasse definierter Wert über die return funktion abgerufen werden
        #        f'{self.currency}' \ später mit currency auswahl

    def get_absolute_url(self): # self.title wird als absoluter url returnt
        return reverse("user-picture", kwargs={"slug": self.title})

'''
class RecipeValueIngredients(models.Model):
    value = models.IntegerField(default=100)
    ingredients = models.TextField(default='', max_length=5000)

    class UnityChoices(models.TextChoices):  # um ein choicefiled(dropdownmenu mit verschiedenen auswahlmögl.)= zu erstellen, wird die Klasse textchoices verwendet
        GRAMM = 'g', 'Gramm'  # dieser klasse wird pro vairable ein tupel mit insgesammt 2 werten zugewiesen. der erste wert ist der in welcgher der zweite gespeichert wird.
        KILOGRAMM = 'kg', 'Kilogramm'  # der zweite Wert ist der, der dem Nutzer angezeigt wird.
        MILLILITER = 'ml', 'Milliliter'
        LITER = 'l', 'Liter'
        PINCH = 'p', 'Pinch'

    currency_choice_field = models.CharField(max_length=2, choices=UnityChoices.choices, default='g')  # 3

    # 3 = die auswahlmögl. werden als Charfield an die variable übergeben welche durch die choices methode als choicefield gerendert wird.

    def __str__(self):
        return f'{self.value} |' \
               f'{self.currency_choice_field}' \
               f'{self.ingredients} | '

'''
