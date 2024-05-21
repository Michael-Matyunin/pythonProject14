

from rest_framework import serializers
from .models import Expense, Category, Budget, Balance

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category_name', 'description']

    def create(self, validated_data):
        category_name = validated_data.pop('category_name')
        category, created = Category.objects.get_or_create(name=category_name)
        validated_data['category'] = category
        return Expense.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['amount']
