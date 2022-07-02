from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)

    @property
    def main_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.main_name
