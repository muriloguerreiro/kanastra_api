from django.db import models
import uuid

class Debt(models.Model):
    name = models.CharField(max_length=255)
    governmentId = models.CharField(max_length=20)
    email = models.EmailField()
    debtAmount = models.DecimalField(max_digits=10, decimal_places=2)
    debtDueDate = models.DateField()
    debtId = models.UUIDField(unique=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.debtId}"