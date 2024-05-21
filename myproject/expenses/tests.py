from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Category, Expense


class CreateCategoriesViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_create_category(self):
        data = {'name': 'Health'}
        response = self.client.post(reverse('create_categories'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Health')


class BalanceViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Food')

    def test_get_balance(self):
        Expense.objects.create(category=self.category, amount=50, date='2024-01-01')
        Expense.objects.create(category=self.category, amount=60, date='2024-01-02')
        response = self.client.get(reverse('get_balance'), {'start_date': '2024-01-01', 'end_date': '2024-12-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_expenses'], 110)


class CategoryStatisticsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name='Food')
        self.category2 = Category.objects.create(name='Transport')
        Expense.objects.create(category=self.category1, amount=50, date='2024-01-01')
        Expense.objects.create(category=self.category2, amount=30, date='2024-01-02')

    def test_get_category_statistics(self):
        response = self.client.get(reverse('get_statistics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Food'], 50)
        self.assertEqual(response.data['Transport'], 30)


class NotifyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name='Food')
        self.category2 = Category.objects.create(name='Transport')

    def test_notify_view(self):
        Expense.objects.create(category=self.category1, amount=110, date='2024-01-01')
        Expense.objects.create(category=self.category2, amount=50, date='2024-01-02')
        response = self.client.get(reverse('send_notifications'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['notifications']), 1)
        self.assertEqual(response.data['notifications'][0]['category'], 'Food')
