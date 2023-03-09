from rest_framework import serializers
from expense_management.models import Expense, Color

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseByMonthSerializer(serializers.Serializer):
    paid = ExpenseSerializer(many=True)
    to_pay = ExpenseSerializer(many=True)

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'