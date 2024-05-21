from django.urls import path
from .views import CreateCategoriesView, BalanceView, CategoryStatisticsView, NotifyView, CreateExpenseView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Expense Management API",
      default_version='v1',
      description="API for managing expenses",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@expenses.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('create-categories/', CreateCategoriesView.as_view(), name='create_categories'),
    path('balance/', BalanceView.as_view(), name='get_balance'),
    path('notify/', NotifyView.as_view(), name='send_notifications'),
    path('statistics/', CategoryStatisticsView.as_view(), name='get_statistics'),
    path('create-expense/', CreateExpenseView.as_view(), name='create_expense'),
    path('create-categories/', CreateCategoriesView.as_view(), name='create_categories'),

]
