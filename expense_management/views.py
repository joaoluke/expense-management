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
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings

from expense_management.models import Expense, Category
from expense_management.serializers import ExpenseSerializer, CategorySerializer, MyTokenObtainPairSerializer


class GoogleLoginAPIView(APIView):
    def post(self, request, format=None):
        token = request.data.get('token', None)
        if not token:
            return Response({'error': 'Token missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Aqui você pode verificar se o usuário já existe no banco de dados, e criar um novo usuário se necessário
        try:
            user = User.objects.get(email=idinfo['email'])
        except User.DoesNotExist:
            # O usuário não existe, então vamos criar um novo
            user = User.objects.create_user(idinfo['email'], idinfo['email'])
            user.first_name = idinfo['given_name']
            user.last_name = idinfo['family_name']
            user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token})


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
    permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get(self, request, format=None):
        current_month = request.query_params.get('month')
        user_id = request.user.id
        expenses_paid = Expense.objects.filter(
            user=user_id, month_reference=current_month, column='PAID')
        expenses_to_pay = Expense.objects.filter(
            user=user_id, month_reference=current_month, column='TO_PAY')
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
