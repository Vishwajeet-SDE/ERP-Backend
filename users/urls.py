from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import get_user_profile, MyTokenObtainPairView
urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', get_user_profile, name='user_profile'),
]