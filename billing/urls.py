from django.urls import path
from .views import UploadCSV, DebtList

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload_csv'),
    path('debts/', DebtList.as_view(), name='debt_list'),
]