# Generated by Django 3.2.25 on 2024-07-02 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='debt',
            old_name='debt_amount',
            new_name='debtAmount',
        ),
        migrations.RenameField(
            model_name='debt',
            old_name='debt_due_date',
            new_name='debtDueDate',
        ),
        migrations.RenameField(
            model_name='debt',
            old_name='debt_id',
            new_name='debtId',
        ),
        migrations.RenameField(
            model_name='debt',
            old_name='government_id',
            new_name='governmentId',
        ),
    ]
