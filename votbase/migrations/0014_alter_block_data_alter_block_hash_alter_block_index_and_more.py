# Generated by Django 5.0.6 on 2024-06-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0013_candidate_encrypted_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='data',
            field=models.TextField(default=0),
        ),
        migrations.AlterField(
            model_name='block',
            name='hash',
            field=models.CharField(default=0, max_length=64),
        ),
        migrations.AlterField(
            model_name='block',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='block',
            name='previous_hash',
            field=models.CharField(default=0, max_length=64),
        ),
        migrations.AlterField(
            model_name='merkletree',
            name='blocks',
            field=models.ManyToManyField(to='votbase.block'),
        ),
        migrations.AlterField(
            model_name='merkletree',
            name='root_hash',
            field=models.CharField(default=0, max_length=64),
        ),
    ]