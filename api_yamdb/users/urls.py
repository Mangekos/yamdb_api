from .views import CustomUserViewSet, UsersMeApiView, get_token, signup
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register('users', CustomUserViewSet)

urlpatterns = [
    path('v1/users/me/', UsersMeApiView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', get_token, name='user_token'),
    path('v1/auth/signup/', signup, name='user-reg'),
]
