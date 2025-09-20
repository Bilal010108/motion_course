from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response



class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except  serializers.ValidationError:
            return Response({'detail': 'Малымат туура эмес берилди'}, status.HTTP_400_BAD_REQUEST)
        except NameError as e:
            return Response({'detail': f'{e}, Ошибка в коде'}, status.HTTP_500_INTERNAL_SERVER_ERROR)



class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'detail': f'Сервер ошибка {e}'}, status.HTTP_500_INTERNAL_SERVER_ERROR )

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'detail': 'Неправильный ключ'}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Сервер ошибка {e}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

@api_view(['POST'])
def verify_reset_code(request):
    serializer = VerifyResetCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class  HomeListAPIView(generics.ListCreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class WhoCourseListAPIView(generics.ListCreateAPIView):
    queryset = WhoCourse.objects.all()
    serializer_class = WhoCourseSerializer


class WhoCourseHighlightListAPIView(generics.ListCreateAPIView):
    queryset = WhoCourseHighlight.objects.all()
    serializer_class = WhoCourseHighlightSerializer


class AccessibleCourseTitleListAPIView(generics.ListCreateAPIView):
    queryset = AccessibleCourseTitle.objects.all()
    serializer_class = AccessibleCourseTitleSerializer


class EmailListAPIView(generics.ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class AboutUsListAPIView(generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer



class AboutUsImageListAPIView(generics.ListCreateAPIView):
    queryset = AboutUsImage.objects.all()
    serializer_class = AboutUsImageSerializer


class TitleCourseListAPIView(generics.ListCreateAPIView):
    queryset = TitleCourse.objects.all()
    serializer_class = TitleCourseSerializer




class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseListAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseReviewListAPIView(generics.ListCreateAPIView):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer


class LessonListAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class FavoriteListAPIView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer



