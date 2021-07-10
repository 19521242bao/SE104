from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class SiteConfig(models.Model):
  """ Site Configurations """
  key = models.SlugField()
  value = models.CharField(max_length=200)

  def __str__(self):
    return self.key


class AcademicSession(models.Model):
  """ Academic Session """
  name = models.CharField(max_length=200, unique=True,verbose_name="năm học")
  current = models.BooleanField(default=True)

  class Meta:
    ordering = ['-name']

  def __str__(self):
    return self.name


class AcademicTerm(models.Model):
  """ Academic Term """
  name = models.CharField(max_length=20, unique=True,verbose_name="học kì")
  current = models.BooleanField(default=True)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name


class Subject(models.Model):
  """ Subject """
  name = models.CharField(max_length=200, unique=True,verbose_name="môn học")

  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name


class StudentClass(models.Model):
  name = models.CharField(max_length=200, unique=True)
  class Meta:
    verbose_name = "Lớp"
    verbose_name_plural = "Lớp"
    ordering = ['name']

  def __str__(self):
    return self.name
