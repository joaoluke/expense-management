from rest_framework import serializers
from expense_management.models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseByMonthSerializer(serializers.Serializer):
    paid = ExpenseSerializer(many=True)
    to_pay = ExpenseSerializer(many=True)