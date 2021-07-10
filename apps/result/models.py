from django.core.exceptions import ValidationError
from django.db import models

from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass, Subject
from apps.students.models import Student

from .utils import score_grade

# Create your models here.
def validate_exam_score(value):
  if value<0 or value>10:
    raise ValidationError(('%(value)s must be greater than 0 and less than 10'),
      params={'value': value},
    )
def validate_test_score(value):
  if value<0 or value>10:
    raise ValidationError(('%(value)s must be greater than 0 and less than 10'),
      params={'value': value},
    )


class Result(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
  term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
  current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
  test_score = models.FloatField(default=0,verbose_name="điểm KT45'")
  exam_score = models.FloatField(default=0,verbose_name="điểm KT15'")

  class Meta:
    ordering = ['subject']

  def __str__(self):
    return f'{self.student} {self.session} {self.term} {self.subject}'

  def total_score(self):
    return (self.test_score + self.exam_score)/2

  def grade(self):
    return score_grade(self.total_score())


  # def save(self, *args, **kwargs):
  #   if self.current_class!=self.student.current_class:
  #     self.current_class=self.student.current_class
