import uuid
from django.db import models
from datetime import datetime


# Create your models here.

def get_time():
    return datetime.now().timestamp()


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    vote = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=get_time)
    block_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{}|{}|{}".format(self.id, self.vote, self.timestamp)


class Candidate(models.Model):
    candidate_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    profession = models.CharField(default=None,max_length=100)
    criminal_records = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Voter(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    public_key_n = models.CharField(max_length=100)
    public_key_e = models.IntegerField(default=0)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Voter_List(models.Model):
    username = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.username


class Voter_Pvt(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    salt = models.CharField(max_length=100)
    public_key_n = models.CharField(max_length=100)
    public_key_d = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Block(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    perv_hash = models.CharField(max_length=100, blank=True)
    merkle_hash = models.CharField(max_length=100, blank=True)
    self_hash = models.CharField(max_length=100, blank=True)
    nonce = models.IntegerField(null=True)
    timestamp = models.FloatField(default=get_time)

    def __str__(self):
        return str(self.self_hash)


class Vote_Auth(models.Model):
    username = models.CharField(max_length=100, primary_key=True, default='admin')
    start = models.DateTimeField()
    end = models.DateTimeField()
    result_Calculated = models.BooleanField(default=False)
    perv_hash = models.CharField(max_length=100, default='0' * 64)


