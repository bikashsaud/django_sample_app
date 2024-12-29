# expenses/tests.py
from django.test import TestCase
from .models import Expense, Category
from django.urls import reverse
from datetime import date

class ExpenseModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.expense = Expense.objects.create(date=date.today(), description="Lunch", amount=10.50, category=self.category)

    def test_expense_creation(self):
        self.assertEqual(self.expense.description, "Lunch")
        self.assertEqual(self.expense.amount, 10.50)
        self.assertEqual(self.expense.category.name, "Food")

class ExpenseViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.expense = Expense.objects.create(date=date.today(), description="Lunch", amount=10.50, category=self.category)

    def test_expense_list_view(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lunch")
        self.assertTemplateUsed(response, 'expenses/expense_list.html')

    def test_add_expense_view(self):
        response = self.client.post(reverse('add_expense'), {
            'date': date.today(),
            'description': 'Dinner',
            'amount': 20.00,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.last().description, 'Dinner')