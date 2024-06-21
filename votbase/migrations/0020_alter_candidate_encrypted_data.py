# Generated by Django 5.0.6 on 2024-06-21 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0019_alter_candidate_encrypted_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='encrypted_data',
            field=models.ForeignKey(blank=True, max_length=64, null=True, on_delete=django.db.models.deletion.CASCADE, to='votbase.block'),
        ),
    ]
