from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.db.models import Q
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings

from expense_management.models import Expense, Category
from expense_management.serializers import ExpenseSerializer, CategorySerializer, MyTokenObtainPairSerializer


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
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
    permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class ExpenseListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExpenseSerializer

    def get(self, request, format=None):
        current_month = request.query_params.get('month')
        user_id = request.user.id

        if current_month == 'null':
            expenses_paid = Expense.objects.filter(
                Q(month_reference__isnull=True) & Q(user=user_id) & Q(column='PAID')
            )
            expenses_to_pay = Expense.objects.filter(
                Q(month_reference__isnull=True) & Q(user=user_id) & Q(column='TO_PAY')
            )
        else:
            expenses_paid = Expense.objects.filter(
                Q(month_reference=current_month) & Q(user=user_id) & Q(column='PAID')
            )
            expenses_to_pay = Expense.objects.filter(
                Q(month_reference=current_month) & Q(user=user_id) & Q(column='TO_PAY')
            )

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

