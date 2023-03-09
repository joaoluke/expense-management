from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from expense_management.models import Expense, Color
from expense_management.serializers import ExpenseSerializer, ColorSerializer
from django.db.models import Sum


# Create your views here.
class ColorListView(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ExpenseListView(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ExpenseListAPIView(APIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get(self, request, format=None):
        current_month = request.query_params.get('month')
        expenses_paid = Expense.objects.filter(month_reference=current_month, column='PAID')
        expenses_to_pay = Expense.objects.filter(month_reference=current_month, column='TO_PAY')
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
