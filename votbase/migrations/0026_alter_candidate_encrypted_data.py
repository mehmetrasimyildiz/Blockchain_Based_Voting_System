# Generated by Django 5.0.6 on 2024-06-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0025_alter_candidate_encrypted_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='encrypted_data',
            field=models.CharField(blank=True, default=-1, max_length=64),
        ),
    ]
