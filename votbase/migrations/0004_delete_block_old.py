# Generated by Django 5.0.6 on 2024-07-02 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0003_rename_block_new_block_old'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Block_old',
        ),
    ]
