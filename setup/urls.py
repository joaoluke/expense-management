from django.contrib import admin
from django.urls import path, include
from expense_management.views import ExpenseListView, ExpenseListAPIView, CategoryListView, MyObtainTokenPairView, LogoutView, UserProfileView, GoogleLoginAPIView
from expense_management.serializers import CustomLoginSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from dj_rest_auth.views import LoginView

router = routers.DefaultRouter()
router.register('category', CategoryListView, basename='Category')
router.register('expenses-list', ExpenseListView, basename='Expense')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('expenses/', ExpenseListAPIView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
        path('api/v1/auth/google-login/', GoogleLoginAPIView.as_view(), name='google-login'),
    path('api/v1/auth/login/',
         LoginView.as_view(serializer_class=CustomLoginSerializer)),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),

]
