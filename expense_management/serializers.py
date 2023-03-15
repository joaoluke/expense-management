from rest_framework import serializers
from expense_management.models import Expense, Category
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class CustomLoginSerializer(LoginSerializer):
    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseByMonthSerializer(serializers.Serializer):
    paid = ExpenseSerializer(many=True)
    to_pay = ExpenseSerializer(many=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
