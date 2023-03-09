from django.contrib import admin
from django.urls import path, include
from expense_management.views import ExpenseListView, ExpenseListAPIView, ColorListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('colors', ColorListView, basename='Color')
router.register('expenses-list', ExpenseListView, basename='Expense')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('expenses/', ExpenseListAPIView.as_view()),
]