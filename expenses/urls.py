# expenses/urls.py
from django.urls import path
from .views import ExpenseListView, AddExpenseView

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense_list'),
    path('add/', AddExpenseView.as_view(), name='add_expense'),
]