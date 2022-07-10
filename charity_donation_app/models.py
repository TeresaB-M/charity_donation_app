#from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    @property
    def main_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.main_name


class Institution(models.Model):
    TYPE_INSTITUTION = (
        (1, "Fundacja"),
        (2, "Organizacja pozarządowa"),
        (3, "Zbiórka lokalna"),
    )
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    type = models.IntegerField(choices=TYPE_INSTITUTION, default=1)
    categories = models.ManyToManyField(Category)

    @property
    def main_name(self):
        return "{} {}".format(self.name, self.description, self.type, self.categories)

    def __str__(self):
        return self.main_name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    street = models.CharField(max_length=128)
    house_number = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=32)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    @property
    def main_name(self):
        return "{} {}".format(self.quantity, self.institution)

    def __str__(self):
        return self.main_name
