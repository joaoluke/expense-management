from django.contrib import admin
from django.urls import path
from expense_management.views import ExpenseListView

urlpatterns = [
    path('expenses/', ExpenseListView.as_view()),
    path('admin/', admin.site.urls),
]
