# Generated by Django 5.0.6 on 2024-06-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0033_alter_candidate_encrypted_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='encrypted_data',
            field=models.CharField(max_length=64),
        ),
    ]
