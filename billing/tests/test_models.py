from django.test import TestCase
from billing.models import Debt
import uuid

class DebtModelTest(TestCase):
    def setUp(self):
        self.debt = Debt.objects.create(
            name="John Doe",
            governmentId="11111111111",
            email="johndoe@kanastra.com.br",
            debtAmount=1000.00,
            debtDueDate="2024-07-07",
            debtId=uuid.uuid4()
        )

    def test_debt_creation(self):
        self.assertEqual(self.debt.name, "John Doe")
        self.assertEqual(self.debt.email, "johndoe@kanastra.com.br")
        self.assertEqual(self.debt.debtAmount, 1000.00)