from django.db import models
from django.utils import timezone

class storyboard(models.Model):
    name = models.CharField(max_length=200, unique=False)
    length = models.IntegerField(default="0")
    initial_text = models.CharField(max_length=1024, unique=False, default="NULL")
    last_text = models.CharField(max_length=200, unique=False, default="NULL")
    start_text = models.CharField(max_length=200, unique=False, default="NULL")
    owner_id = models.IntegerField(default="0")
    publish_statut = models.BooleanField(default=False)
    date_publish = models.DateTimeField(default=timezone.now())
    owner_fav = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now())
    update_date = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default="0")
    fav = models.IntegerField(default="0")
    message = models.CharField(max_length=256, unique=False, default="NULL")

class storyboard_text(models.Model):
    storyboard = models.ForeignKey(storyboard, on_delete=models.CASCADE)
    case_id = models.IntegerField(default="0")
    text_order = models.IntegerField(default="0")
    text = models.CharField(max_length=1024, unique=False, default="NULL")
    owner_id = models.IntegerField(default="0")

class storyboard_picture(models.Model):
    storyboard = models.ForeignKey(storyboard, on_delete=models.CASCADE)
    case_id = models.IntegerField(default="0")
    text = models.CharField(max_length=1024, unique=False, default="NULL")
    picture = models.BinaryField(null=True, editable=True)
    owner_id = models.IntegerField(default="0")

class storyboard_publications(models.Model):
    storyboard = models.ForeignKey(storyboard, on_delete=models.CASCADE)
    owner_id = models.IntegerField(default="0")
    fav = models.BooleanField(default=False)
    like = models.BooleanField(default=False)