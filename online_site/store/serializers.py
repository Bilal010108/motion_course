from django.contrib.auth import authenticate

from .models import *
from rest_framework import serializers
from rest_framework import serializers, generics
from rest_framework_simplejwt.tokens import RefreshToken

from django_rest_passwordreset.models import ResetPasswordToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
               'phone_number',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = UserProfile.objects.create_user(**validated_data)
            return user
        except Exception as e:
            return f'Ошибка сервере брат {e}'

    def to_representation(self, instance ):
        try:
            refresh = RefreshToken.for_user(instance)
            return {
                'user':{
                    'username': instance.username,
                    'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        except Exception as e:
            return f'{e}, Ошибка при создании токена'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['age','profile_picture','phone_number','user_role','image']

class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        reset_code = data.get('reset_code')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают.")

        try:
            token = ResetPasswordToken.objects.get(user__email=email, key=str(reset_code))
        except ResetPasswordToken.DoesNotExist:
            raise serializers.ValidationError("Неверный код сброса или email.")

        data['user'] = token.user
        data['token'] = token
        return data

    def save(self):
        user = self.validated_data['user']
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        # Удаляем использованный токен
        token.delete()

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['title','description','image']

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = ['id','home','title','iconka','description']



class WhoCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoCourse
        fields = ['id','title','description','title_number_one','number_one_description','title_number_two','number_two_description']


class WhoCourseHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoCourseHighlight
        fields = ['id','who_course','iconka','title','description',]


class AccessibleCourseTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoCourse
        fields = ['id','title','description',]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id','description',]
        ref_name = 'StoreEmailSerializer'


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id','title','title_author','author_image','author_bio']


class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = ['id','about_us','image',]

class TitleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleCourse
        fields = ['id','title','image','famous_course','famous_course_description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name',]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','owner','title','description','price',
                  'image','category','progress','title_fot_theme',
                  'description_for_theme','image_theme','title_one',
                  'description_one','title_two','description_two',
                  'title_three','description_three','title_four',
                  'description_four','user_role']


class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = ['id','user', 'course', 'city', 'region','rating','comment']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id','course','lesson_theme','title','video',
                  'video_time','status','created_date','views']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id','user','course']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','client_cart',]



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','cart','lesson_cart','quantity_cart']








