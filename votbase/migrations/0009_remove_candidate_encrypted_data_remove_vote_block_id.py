# Generated by Django 5.0.6 on 2024-06-20 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0008_alter_candidate_encrypted_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='encrypted_data',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='block_id',
        ),
    ]