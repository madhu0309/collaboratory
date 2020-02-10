from django.db import models

# Create your models here.


class Info(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)


class Programmer(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20)
    programmer = models.ForeignKey(Programmer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Book(models.Model):

    name = models.CharField(max_length=255)
    isbn_number = models.CharField(max_length=13)

    class Meta:
        db_table = "book"

    def __str__(self):
        return self.name
