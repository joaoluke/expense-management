from django.contrib import admin
from django.urls import path
from expense_management.views import ExpenseListView, ExpenseCreateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('students', ExpenseListView, basename='Students')

urlpatterns = [
    path('expenses/', ExpenseListView.as_view()),
    path('expenses/create/', ExpenseCreateView.as_view()),
    path('expense/<int:pk>/create/', ExpenseCreateView.as_view()),
    path('admin/', admin.site.urls),
]
