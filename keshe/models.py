from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# 图书
class Book(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_name = models.CharField(max_length=30)
    b_author = models.CharField(max_length=20)
    b_isbn = models.CharField(max_length=40)
    b_public = models.CharField(max_length=30)
    b_total = models.IntegerField(default=0)
    b_lave = models.IntegerField(default=0)
    b_type = models.ForeignKey("BookType", on_delete=models.CASCADE)


# 老师
class Teacher(User):
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    borrow = models.IntegerField(default=0)


# 学生
class Student(User):
    max_borrow = models.IntegerField(default=5)
    borrow=models.IntegerField(default=0)


# 职称类型
class Type(models.Model):
    type = models.CharField(max_length=20)
    max_borrow = models.IntegerField(default=0)


# 老师借阅
class BorrowTeacher(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)


# 学生借阅
class BorrowStudent(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)


# 图书类型
class BookType(models.Model):
    bookType = models.CharField(max_length=20)
