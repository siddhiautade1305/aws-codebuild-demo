from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin






class Career(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoadmapPhase(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.career.name} - {self.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=100)
    interests = models.CharField(max_length=200)
    time_commitment = models.IntegerField()

    def __str__(self):
        return self.user.username


class UserRoadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
