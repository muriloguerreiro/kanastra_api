from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Debt
from .serializers import DebtSerializer
from .utils.email_service import EmailService
from .utils.boleto_service import BoletoService
import csv
from io import TextIOWrapper
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
logger.addHandler(handler)

class UploadCSV(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file_data = TextIOWrapper(file.file, encoding='utf-8')
            reader = csv.DictReader(file_data)
            
            processed_debts = []
            for row in reader:
                # Verificar se existe um registro processado com o mesmo debtId
                existing_debt = Debt.objects.filter(debtId=row['debtId'], processed=True).first()
                if existing_debt:
                    logger.warning(f"Boleto with ID {row['debtId']} has already been generated previously")
                    continue

                serializer = DebtSerializer(data=row)
                if serializer.is_valid():
                    debt = serializer.save()
                    processed_debts.append(debt)

                    BoletoService.generate_boleto(debt)
                    EmailService.send_email(debt.email, "Your Boleto", f"Here is your boleto for {debt.debtAmount} due on {debt.debtDueDate}")

                    debt.processed = True
                    debt.save()

                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
            return Response({"message": "File processed successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DebtList(generics.ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer