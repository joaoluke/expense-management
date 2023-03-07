from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from expense_management.models import Expense
from expense_management.serializers import ExpenseSerializer


# Create your views here.
# class ExpenseListView(generics.ListAPIView):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseSerializer

class ExpenseListView(APIView):
    def get(self, request, format=None):
        current_month = request.query_params.get('month')
        expenses_paid = Expense.objects.filter(month_reference=current_month, column='PAID')
        expenses_to_pay = Expense.objects.filter(month_reference=current_month, column='TO_PAY')
        serializer_paid = ExpenseSerializer(expenses_paid, many=True)
        serializer_to_pay = ExpenseSerializer(expenses_to_pay, many=True)
        return Response({
            "expenses_paid": serializer_paid.data,
            "expenses_to_pay": serializer_to_pay.data
        })
