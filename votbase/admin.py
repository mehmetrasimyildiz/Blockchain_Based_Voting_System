from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Vote)
admin.site.register(models.Voter)
admin.site.register(models.Candidate)
admin.site.register(models.Voter_List)
admin.site.register(models.Vote_Auth)
admin.site.register(models.Voter_Pvt)
admin.site.register(models.Block)
