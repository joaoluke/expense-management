from django.contrib import admin
from django.urls import path, include
from expense_management.views import ExpenseListView, ExpenseListAPIView, CategoryListView, CustomLoginView, ExpenseDeleteView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', CategoryListView, basename='Category')
router.register('expenses-list', ExpenseListView, basename='Expense')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('expenses/', ExpenseListAPIView.as_view()),
    path('login/', CustomLoginView.as_view()),
    path('expenses-list/<int:pk>/delete/',
         ExpenseDeleteView.as_view(), name='expense-delete'),

]
