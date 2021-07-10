from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import RegexValidator, EmailValidator

from apps.corecode.models import StudentClass, Subject


class Student(models.Model):

    GENDER = [
        ('nam', 'Nam'),
        ('nữ', 'Nữ')
    ]
    AGE=[
        ('15',"15"),
        ('16',"16"),
        ('17',"17"),
        ('18',"18"),
        ('19',"19"),
        ('20',"20"),

    ]

    name = models.CharField(max_length=200,verbose_name= "họ tên")
    gender = models.CharField(max_length=10, choices=GENDER, default='male',verbose_name="giới tính")
    date_of_birth = models.DateField(default=timezone.now,verbose_name="ngày sinh")
    #age=models.IntegerField(default=15,choices=AGE,verbose_name="tuổi")
    current_class = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, blank=True, null=True,verbose_name="Lớp")
    #date_of_admission = models.DateField(default=timezone.now,verbose_name="ngày nhập học")
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    parent_mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True,verbose_name="số điện thoại")
    email_regex=EmailValidator(message="Email is not valid")
    email=models.CharField(validators=[email_regex],max_length=30,default=None)
    address = models.TextField(blank=True,verbose_name="địa chỉ")
    #others = models.TextField(blank=True,verbose_name="thông tin thêm")
    passport = models.ImageField(blank=True, upload_to='students/passports/',verbose_name="ảnh đại diện")

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return f'{self.name} )'

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True,verbose_name="ngày cập nhật")
    csv_file = models.FileField(upload_to='students/bulkupload/')
