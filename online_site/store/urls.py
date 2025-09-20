from .views import *
from  rest_framework import routers
from django.urls import path, include


router = routers.SimpleRouter()



urlpatterns = [
    path('', include(router.urls)),


    path('user_profile/', UserProfileListAPIView.as_view(), name='user_list'),

    path('home/', HomeListAPIView.as_view(), name='home_list'),

    path('who_course/', WhoCourseListAPIView.as_view(), name='who_course_list'),

    path('who_coursehighlight/', WhoCourseHighlightListAPIView.as_view(), name='who_coursehighlight_list'),

    path('accessiblecoursetitle/', AccessibleCourseTitleListAPIView.as_view(), name='accessiblecoursetitle_list'),

    path('email/', EmailListAPIView.as_view(), name='email_list'),

    path('titlecourse/', TitleCourseListAPIView.as_view(), name='user_list'),

    path('category/', CategoryListAPIView.as_view(), name='category_list'),

    path('course/', CourseListAPIView.as_view(), name='course_list'),

    path('coursereview/', CourseReviewListAPIView.as_view(), name='coursereview_list'),

    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),

    path('favorite/', FavoriteListAPIView.as_view(), name='favorite_list'),

    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
