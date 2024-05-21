from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expense, Category, Budget, Notification
from .serializers import ExpenseSerializer, CategorySerializer, BudgetSerializer
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateCategoriesView(APIView):
    @swagger_auto_schema(
        operation_description="Создать несколько категорий",
        responses={201: 'Categories created successfully'}
    )
    def get(self, request):
        self.create_categories()
        return Response({'message': 'Categories created successfully'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Создать новую категорию",
        request_body=CategorySerializer,
        responses={201: CategorySerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_categories(self):
        Category.objects.create(name='Food')
        Category.objects.create(name='Transport')
        Category.objects.create(name='Entertainment')


class BalanceView(APIView):
    @swagger_auto_schema(
        operation_description="Получить баланс расходов за указанный период",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start Date", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End Date", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)
        ],
        responses={200: openapi.Response('Total expenses', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'total_expenses': openapi.Schema(type=openapi.TYPE_NUMBER)}))}
    )
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date or not end_date:
            return Response({'error': 'start_date and end_date are required'}, status=status.HTTP_400_BAD_REQUEST)

        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({'total_expenses': total_expenses})


class ExpenseCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Создать новый расход",
        request_body=ExpenseSerializer,
        responses={201: ExpenseSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = serializer.save()

            # Проверяем, превышает ли расход 100
            category = expense.category
            total_expenses = Expense.objects.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
            if total_expenses > 100:
                notification = f"Расходы в категории '{category.name}' превысили 100!"
                # Создаем уведомление
                create_notification(notification)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_notification(message):
    Notification.objects.create(message=message)


class CategoryStatisticsView(APIView):
    @swagger_auto_schema(
        operation_description="Получить статистику расходов по категориям",
        responses={200: openapi.Response('Category statistics', openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def get(self, request):
        categories = Category.objects.all()
        category_data = {}
        for category in categories:
            total_expenses = Expense.objects.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
            category_data[category.name] = total_expenses
        return Response(category_data)


class NotifyView(APIView):
    @swagger_auto_schema(
        operation_description="Отправить уведомления о превышении бюджета",
        responses={200: openapi.Response('Notifications', openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def get(self, request):
        categories = Category.objects.all()
        notifications = []

        for category in categories:
            total_expenses = Expense.objects.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0

            if total_expenses > 100:
                notifications.append({
                    'category': category.name,
                    'spent': total_expenses,
                    'message': 'Expenses exceeded 100!'
                })

        return Response({'notifications': notifications})


class CreateExpenseView(APIView):
    @swagger_auto_schema(
        operation_description="Создать новый расход",
        request_body=ExpenseSerializer,
        responses={201: ExpenseSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
