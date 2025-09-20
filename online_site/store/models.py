from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django .contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(12), MaxValueValidator(80)], null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    ROLE_CHOICES = (
        ('student', 'student'),
        ('teacher', 'teacher'),

    )
    user_role = models.CharField(max_length=17, choices=ROLE_CHOICES, default='student')
    image = models.ImageField(upload_to='image/', null=True, blank=True)


    def __str__(self):
        return f'{self.first_name}, {self.user_role}'



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Укажи свой реальный домен
    frontend_url = "https://example.com"  # Заменить на адрес твоего сайта или фронтенда

    # Генерация полного URL сброса пароля
    reset_url = "{}{}?token={}".format(
        frontend_url,
        reverse('password_reset:reset-password-request'),  # Django-обработчик, можно заменить
        reset_password_token.key
    )

    # Отправка письма
    send_mail(
        subject="Password Reset for Some Website",  # Тема
        message=f"Use the following link to reset your password:\n{reset_url}",  # Текст
        from_email="noreply@example.com",  # Отправитель
        recipient_list=[reset_password_token.user.email],  # Получатель
        fail_silently=False,
    )


# Add reset password logic


class Home(models.Model):
    title =  models.CharField(max_length = 227,null = True,blank = True)
    description = models.TextField(null =True,blank = True)
    image = models.ImageField(upload_to = 'home_image')

    def __str__(self):
        return f'{self.title}'

class Highlight(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='home_h')
    title = models.CharField(max_length = 227,null =True,blank = True)
    iconka = models.ImageField(upload_to ='iconka_h')
    description = models.TextField(null =True,blank = True)

    def __str__(self):
        return f'{self.title}'


class WhoCourse(models.Model):
    title = models.CharField(max_length = 227,null = True, blank= True)
    description =models.TextField(null = True, blank = True)
    title_number_one = models.CharField(max_length = 7)
    number_one_description = models.TextField(null =True,blank =True)
    title_number_two  = models.CharField(max_length=7)
    number_two_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class WhoCourseHighlight(models.Model):
    who_course = models.ForeignKey(WhoCourse, on_delete=models.CASCADE, related_name='who_courses')
    iconka = models.ImageField(upload_to ='iconka_who_course_h')
    title = models.CharField(max_length = 227,null = True,blank = True)
    description = models.TextField(null = True,blank = True)

    def __str__(self):
        return f'{self.title}'




class AccessibleCourseTitle(models.Model):
    title = models.CharField(max_length = 227,null = True,blank = True)
    description = models.TextField(null = True,blank = True)

    def __str__(self):
        return f'{self.title}'





class Email(models.Model):
    description = models.TextField(null =True,blank =True)

    def __str__(self):
        return f'{self.description}'


class AboutUs(models.Model):
    title = models.CharField(max_length=300)
    title_author = models.CharField(max_length=32)
    author_image = models.ImageField(upload_to='author_image/')
    author_bio = models.TextField(null = True,blank = True)

    def __str__(self):
        return self.title

class AboutUsImage(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name='aboutus_images')
    image = models.ImageField(upload_to='aboutus_image/')

    def __str__(self):
        return f'{self.image}'

class TitleCourse(models.Model):
    title = models.CharField(max_length=227)
    image = models.ImageField(upload_to='course_list_image/')
    famous_course = models.CharField(max_length=227)
    famous_course_description = models.TextField(null = True,blank = True)

    def __str__(self):
        return f'{self.title}'

class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.category_name}'


class Course(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null = True,blank = True)
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='course_images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    progress = models.CharField(max_length=32)
    title_fot_theme = models.CharField(max_length=255)
    description_for_theme = models.TextField()
    image_theme = models.ImageField(upload_to='theme_images/')
    title_one = models.TextField(null = True,blank = True)
    description_one = models.TextField(null = True,blank = True)
    title_two = models.TextField(null = True,blank = True)
    description_two = models.TextField(null = True,blank = True)
    title_three = models.TextField(null = True,blank = True)
    description_three = models.TextField(null = True,blank = True)
    title_four = models.TextField(null = True,blank = True)
    description_four = models.TextField(null = True,blank = True)

    STATUS_COURSE = (
        ('Бесплатно', 'Бесплатно'),
        ('Платно', 'Платно'),

    )
    user_role = models.CharField(max_length=17, choices=STATUS_COURSE, default='Бесплатно')

    def __str__(self):
        return self.title


class CourseReview(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    city = models.CharField(max_length=43)
    region = models.CharField(max_length=43)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user},{self.course}'

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons')
    lesson_theme = models.TextField(null =True,blank = True)
    title = models.CharField(max_length=227,null = True,blank = True)
    video = models.FileField(upload_to='lesson_video/')
    video_time = models.DurationField()
    STATUS_LESSONS = (
        ('Открытый', 'Открытый'),
        ('Закрытый', 'Закрытый')
    )
    status = models.CharField(max_length=27, choices=STATUS_LESSONS, default='Открытый')
    created_date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.course},{self.lesson_theme}'



class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorites')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='favorites')



    def __str__(self):
        return f'{self.user},{self.course}'

class Cart(models.Model):
    client_cart = models.ForeignKey(UserProfile,related_name='client_cart',on_delete=models.CASCADE)


    def __str__(self):
       return str(self.client_cart)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart', on_delete=models.CASCADE,)
    lesson_cart = models.ForeignKey(Lesson,related_name='product_cart',on_delete=models.CASCADE)
    quantity_cart =models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.lesson_cart)


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile,)
    created_date = models.DateField(auto_now_add=True)


class Massage(models.Model):
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chatimages', null=True, blank=True)
    video = models.FileField(upload_to='chatvideos', null=True, blank=True  )
    created_date = models.DateField(auto_now_add=True)





