# Generated by Django 5.0.6 on 2024-06-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0035_alter_merkletree_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='index',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='merkletree',
            name='blocks',
            field=models.ManyToManyField(to='votbase.block'),
        ),
    ]
