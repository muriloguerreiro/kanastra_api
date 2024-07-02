from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from billing.models import Debt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import io
import csv
import uuid
import logging

class DebtTests(APITestCase):
    def test_upload_csv(self):
        url = reverse('upload_csv')

        # Configuração do logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger.addHandler(handler)

        # Criar arquivo CSV em memória
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['name', 'governmentId', 'email', 'debtAmount', 'debtDueDate', 'debtId'])
        writer.writerow(['John Doe', '11111111111', 'johndoe@kanastra.com.br', '1000.00', '2024-07-07', str(uuid.uuid4())])
        csv_data.seek(0)

        # Simular upload de arquivo
        uploaded = SimpleUploadedFile("test.csv", csv_data.getvalue().encode('utf-8'), content_type="text/csv")

        # Envia a requisição POST e a garante a criação de um registro
        response = self.client.post(url, {'file': uploaded}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Debt.objects.count(), 1)

        # Verificar se os logs contêm as mensagens geradas pelos serviços de email e boleto
        log_contents = log_stream.getvalue()
        self.assertIn("Simulated generating boleto for John Doe", log_contents)
        self.assertIn("Simulated sending email to johndoe@kanastra.com.br", log_contents)

    def test_list_debts(self):
        url = reverse('debt_list')

        # Envia a requisição GET e garante o status de listagem como OK
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_csv_duplicate_debt_id(self):
        url = reverse('upload_csv')

        # Configuração do logger
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.WARNING)
        logger.addHandler(handler)

        # Criar arquivo CSV em memória com um registro duplicado
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['name', 'governmentId', 'email', 'debtAmount', 'debtDueDate', 'debtId'])
        debt_id = str(uuid.uuid4())
        writer.writerow(['John Doe', '11111111111', 'johndoe@kanastra.com.br', '1000.00', '2024-07-07', debt_id])
        writer.writerow(['Jane Doe', '22222222222', 'janedoe@kanastra.com.br', '1500.00', '2024-08-06', debt_id])
        csv_data.seek(0)

        # Simular upload de arquivo
        uploaded = SimpleUploadedFile("test.csv", csv_data.getvalue().encode('utf-8'), content_type="text/csv")

        # Enviar requisição POST e garantir a geração de apenas um boleto
        response = self.client.post(url, {'file': uploaded}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Debt.objects.count(), 1)

        # Verificar se os logs contêm a mensagem de duplicidade
        log_contents = log_stream.getvalue()
        self.assertIn(f"Boleto with ID {debt_id} has already been generated previously", log_contents)