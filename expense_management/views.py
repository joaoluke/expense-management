from django.http import HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.db.models import Sum
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from expense_management.models import Expense, Category
from expense_management.serializers import ExpenseSerializer, CategorySerializer, MyTokenObtainPairSerializer
from expense_management.forms import LoginForm


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data, "<<<<<<<")
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
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
