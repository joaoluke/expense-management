from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse_lazy
from django.views.generic import DeleteView


from expense_management.models import Expense, Category
from expense_management.serializers import ExpenseSerializer, CategorySerializer
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from expense_management.forms import LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


class CategoryListView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]


class ExpenseListView(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    
class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('expense-list')


class ExpenseListAPIView(APIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get(self, request, format=None):
        current_month = request.query_params.get('month')
        expenses_paid = Expense.objects.filter(
            month_reference=current_month, column='PAID')
        expenses_to_pay = Expense.objects.filter(
            month_reference=current_month, column='TO_PAY')
        serializer_paid = ExpenseSerializer(expenses_paid, many=True)
        serializer_to_pay = ExpenseSerializer(expenses_to_pay, many=True)
        total_paid = expenses_paid.aggregate(Sum('value'))['value__sum']
        total_to_pay = expenses_to_pay.aggregate(Sum('value'))['value__sum']
        return Response({
            "expenses_paid": serializer_paid.data,
            "expenses_to_pay": serializer_to_pay.data,
            "total_paid": total_paid,
            "total_to_pay": total_to_pay,
        })
