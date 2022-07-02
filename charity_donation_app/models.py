from django.db import models

TYPE_INSTITUTION = (
    (1, "Fundacja"),
    (2, "Organizacja pozarządowa"),
    (3, "Zbiórka lokalna"),
)

class Category(models.Model):
    name = models.CharField(max_length=128)

    @property
    def main_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.main_name

class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    type = models.IntegerField(choices=TYPE_INSTITUTION, default=1)
    categories = models.ManyToManyField(Category)

    @property
    def main_name(self):
        return "{} {}".format(self.name, self.description, self.type, self.categories)

    def __str__(self):
        return self.main_name
