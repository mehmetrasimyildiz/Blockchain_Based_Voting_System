# Generated by Django 5.0.6 on 2024-06-21 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votbase', '0038_alter_merkletree_root_hash'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MerkleTree',
        ),
    ]