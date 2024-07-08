import hashlib
import uuid
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import json


# Create your models here.

def get_time():
    return datetime.now().timestamp()


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(default=18, validators=[MinValueValidator(18), MaxValueValidator(120)])
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    criminalRecords = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vote_to_who = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    has_voted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}|{}|{}".format(self.id, self.user, self.timestamp)


class Block_new(models.Model):
    index = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField(default=0)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.hash = self.calculate_hash()
        super(Block_new, self).save(*args, **kwargs)

    def calculate_hash(self):
        block_dict = {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def create_genesis_block():
        return Block_new(index=0, data="Genesis Block", previous_hash="0")

    @staticmethod
    def get_latest_block():
        return Block_new.objects.last()

    @staticmethod
    def add_block(data, user_id):
        previous_block = Block_new.get_latest_block()
        previous_hash = previous_block.hash if previous_block else '0'
        new_block = Block_new(index=previous_block.index + 1 if previous_block else 0, data=data,
                              previous_hash=previous_hash, user=user_id)
        new_block.save()
        return new_block

    @staticmethod
    def is_chain_valid():
        blocks = Block_new.objects.all()
        for i in range(1, len(blocks)):
            current_block = blocks[i]
            previous_block = blocks[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


class Block(models.Model):
    index = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField(default=0)
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.hash = self.calculate_hash()
        super(Block, self).save(*args, **kwargs)

    def calculate_hash(self):
        block_dict = {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def create_genesis_block():
        return Block(index=0, data="Genesis Block", previous_hash="0")

    @staticmethod
    def get_latest_block():
        return Block.objects.last()

    @staticmethod
    def add_block(data, user):
        previous_block = Block.get_latest_block()
        previous_hash = previous_block.hash if previous_block else '0'
        new_block = Block(index=previous_block.index + 1 if previous_block else 0, data=data,
                          previous_hash=previous_hash, user=user)
        new_block.save()
        return new_block

    @staticmethod
    def is_chain_valid():
        blocks = Block.objects.all()
        for i in range(1, len(blocks)):
            current_block = blocks[i]
            previous_block = blocks[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


'''
class MerkleTree:
    def __init__(self, data_list):
        self.data_list = data_list
        self.tree = self.build_merkle_tree(data_list)

    def build_merkle_tree(self, data_list):
        if len(data_list) == 1:
            return data_list

        new_level = []
        for i in range(0, len(data_list), 2):
            left = data_list[i]
            right = data_list[i + 1] if i + 1 < len(data_list) else left
            new_level.append(self.hash_pair(left, right))

        return self.build_merkle_tree(new_level)

    @staticmethod
    def hash_pair(left, right):
        return hashlib.sha256((left + right).encode()).hexdigest()

    def get_root(self):
        return self.tree[0] if self.tree else None
        
'''
