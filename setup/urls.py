from django.contrib import admin
from django.urls import path, include
from expense_management.views import ExpenseListView, ExpenseListAPIView, CategoryListView, MyObtainTokenPairView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', CategoryListView, basename='Category')
router.register('expenses-list', ExpenseListView, basename='Expense')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('expenses/', ExpenseListAPIView.as_view()),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout')
]
