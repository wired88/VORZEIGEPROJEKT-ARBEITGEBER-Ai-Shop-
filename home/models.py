import random


from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator, DecimalValidator
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from djangoProject.settings import MEDIA_URL, STATIC_URL, BASE_DIR
from django.contrib.auth.models import AbstractUser


class SearchPictures(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


#####################    AUTHENTICATION MODEL    #####################

class User(AbstractUser):
    profile_image = models.ImageField(
        default='media/user_img_default.png',
        blank=True,
        null=True,
        upload_to='media',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png']
        )
        ]
    )
    password2 = models.CharField(
        max_length=32,
        default=''
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    slug = models.SlugField(
        max_length=100,
        default=''
    )


    def __str__(self):
        return f' {self.username} {self.password} {self.email} {self.date_created}'

    def get_absolute_url(self):  # self.title wird als absoluter url returnt
        return reverse("home:profile")


'''
class ImageUpload(models.Model):
    class ImageType(models.TextChoices):
        PICTURE = 'Picture' 'Picture'
        GRAPHIC = 'Graphic' 'Graphic'
        VIDEO = 'Video' 'Video'

    base_role = ImageType.PICTURE

    image_type = models.CharField(
        default='Picture',
        max_length=50,
        choices=ImageType.choices,
    )

    def save(self, *args, **kwargs):
        if len(self.image_type) <= 4:
            self.role = self.base_role
            return super().save(*args, **kwargs)





'''



#########################        DATA UPLOAD MODELS        #########################
# CATEGORIES #
class PictureCategories(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True
    )
    p_cat_picture = models.ImageField(
        error_messages={'required': 'Load min 1 Graphic ...'},
        upload_to='media',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name_plural = 'p_categories'
        ordering = ['name']  # this sort the category names form a-z. if you want to sort by z-a than just write a
        # comma before

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # self.title wird als absoluter url returnt
        return reverse("home:category_single", kwargs={"slug": self.slug})

    def get_url_to_single(self):
        return reverse("home:customer_view", kwargs={"slug": self.slug})


class GraphicCategory(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True  # stellt einen index für den namen, sodass bei einer abfrage nciht jedes Mal die gesammte db
        # durchlaufen werden muss, wenn eine Anfrage gesendet wird
    )
    g_cat_picture = models.ImageField(
        error_messages={'required': 'Load min 1 Graphic ...'},
        upload_to='media',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    slug = models.SlugField(
        max_length=100,
        unique=True  # jeder slug darf nur einmal vorkommen
    )

    class Meta:
        verbose_name_plural = 'g_categories'
        # für instructions (für django)
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):  # self.title wird als absoluter url returnt

        return reverse("home:category_single", kwargs={"slug": self.slug})

    def get_url_to_single(self):
        return reverse("home:customer_g_view")



# UPLOAD MEDIA #

class UserAddPicture(models.Model):  # User Create new Picture

    title = models.CharField(  # der title wird im url dargestellt
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
    category = models.ForeignKey(
        PictureCategories,
        max_length=100,
        default='Category',
        related_name='picture',  # erklärung im GraphicsUpload model
        on_delete=models.CASCADE
    )

    tag_field = TaggableManager(
        blank=True,
        help_text='Choose some tags that people can find your Picture ...'
    )
    user_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # 1 insanz der klasse wird gespeichert
        related_name='user_name'  # so kann im Template einfacher auf den user zugegeriffen werden.
    )

    date = models.DateTimeField(
        auto_now_add=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=100
    )
    is_active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name_plural = 'picture'
        ordering = ['-date']  # wonach die Bilder geordnet werden sollen...

    def __str__(self):
        return f' {self.title}' \
               f' {self.picture}' \
               f' {int(self.price)}' \
               f' {self.tag_field}' \
               f' {self.user_name} ' \
               f' {self.date}'  # 1 jetzt kann jeder in der klasse definierter Wert über die return funktion abgerufen werden
        #        f'{self.currency}' \ später mit currency auswahl

    def get_absolute_url(self):  # self.title wird als absoluter url returnt
        # mit self.pk wird die id der instanz automatisch hinzugefügt
        return reverse("home:user-picture", kwargs={"pk": self.pk, "slug": self.slug})


################################

class GraphicUpload(models.Model):
    title = models.CharField(  # der title wird im url dargestellt
        error_messages={'required': 'Title is required'},
        max_length=100
    )
    picture = models.ImageField(
        error_messages={'required': 'Load min 1 Graphic ...'},
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
    category = models.ForeignKey(
        GraphicCategory,
        max_length=100,
        default='Category',
        related_name='graphic_category',
        # wird für den zugriff in zB views oder im template verwendet: Bsp: Model.graphics.all() statt Model.objects.all()
        on_delete=models.CASCADE
    )

    tag_field = TaggableManager(
        help_text='Choose some tags that people can find your Graphic ...'
    )
    g_username = models.ForeignKey(
        User,
        related_name='g_username',
        on_delete=models.CASCADE,  # wird der user gelöscht ird auh das produkt gelöscht
    )
    date = models.DateTimeField(
        auto_now_add=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
    )
    is_active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'graphics_upload'
        ordering = ['-date']  # wonach die graphic-Bilder geordnet werden sollen...

    def __str__(self):
        return f' {self.title}' \
               f' {self.picture}' \
               f' {int(self.price)}' \
               f' {self.tag_field}' \
               f' {self.g_username} ' \
               f' {self.date}'  # 1 jetzt kann jeder in der klasse definierter Wert über die return funktion abgerufen werden
        #        f'{self.currency}' \ später mit currency auswahl

    def get_absolute_url(self):  # self.title wird als absoluter url returnt
        # mit self.pk wird die id der instanz automatisch hinzugefügt
        return reverse("home:user-picture", kwargs={"pk": self.pk, "slug": self.slug})

    def get_edit_url(self):
        return reverse('home:edit-image', kwargs={"pk": self.pk, "slug": self.slug})


#############################################


class LoadVideoForPageCreation(models.Model):  # the model to load videos on the homepage
    video = models.FileField(upload_to='media')  # same like models.URLField()


class ProfileImage(models.Model):
    profile_image = models.ImageField()


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
