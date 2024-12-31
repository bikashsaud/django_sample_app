from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Expense, Category

class ExpenseModelTest(TestCase):
    def setUp(self):
        # Setting up initial data for tests
        self.category = Category.objects.create(name="Food")
        self.expense = Expense.objects.create(
            date=date.today(),
            title="Lunch",
            description="Lunch with colleagues",
            amount=10.50,
            category=self.category
        )

    def test_expense_creation(self):
        """Test if the expense object is created with correct fields."""
        self.assertEqual(self.expense.title, "Lunch")
        self.assertEqual(self.expense.description, "Lunch with colleagues")
        self.assertEqual(self.expense.amount, 10.50)
        self.assertEqual(self.expense.category.name, "Food")

    def test_amount_in_cents(self):
        """Test the amount_in_cents property."""
        self.assertEqual(self.expense.amount_in_cents, 1050)

    def test_description_snippet(self):
        """Test the description_snippet property."""
        short_description = "Short desc"
        long_description = "This is a very long description that exceeds fifty characters."
        self.expense.description = short_description
        self.assertEqual(self.expense.description_snippet, short_description)

        self.expense.description = long_description
        self.assertEqual(self.expense.description_snippet, "This is a very long description that exceeds fi...")

    def test_total_expenses(self):
        """Test the total_expenses static method."""
        Expense.objects.create(
            date=date.today(),
            title="Dinner",
            description="Dinner with family",
            amount=20.00,
            category=self.category
        )
        self.assertEqual(Expense.total_expenses(), 30.50)

    def test_expenses_by_category(self):
        """Test the expenses_by_category static method."""
        another_category = Category.objects.create(name="Transport")
        Expense.objects.create(
            date=date.today(),
            title="Bus Ticket",
            description="Commute to work",
            amount=5.00,
            category=another_category
        )
        self.assertEqual(Expense.expenses_by_category(self.category.id).count(), 1)
        self.assertEqual(Expense.expenses_by_category(another_category.id).count(), 1)


class ExpenseViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.expense = Expense.objects.create(
            date=date.today(),
            title="Lunch",
            description="Lunch with colleagues",
            amount=10.50,
            category=self.category
        )

    def test_expense_list_view(self):
        """Test if the expense list view renders correctly."""
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lunch")
        self.assertContains(response, "$10.50")
        self.assertTemplateUsed(response, 'expenses/expense_list.html')

    def test_add_expense_view(self):
        """Test if the add expense view creates a new expense."""
        response = self.client.post(reverse('add_expense'), {
            'date': date.today(),
            'title': 'Dinner',
            'description': 'Dinner with friends',
            'amount': 20.00,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful form submission
        self.assertEqual(Expense.objects.count(), 2)
        new_expense = Expense.objects.last()
        self.assertEqual(new_expense.title, "Dinner")
        self.assertEqual(new_expense.description, "Dinner with friends")
        self.assertEqual(new_expense.amount, 20.00)
