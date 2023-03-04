from datetime import datetime

from django.db import models

class Category_group(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey('Category_group',on_delete=models.CASCADE)
    slug = models.SlugField('slug')

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

class ServiceReport(models.Model):

    date = models.DateTimeField(default=datetime.now())
    service = models.ForeignKey('Service',on_delete=models.CASCADE)
    userId = models.IntegerField()

    def __str__(self):
        return ''+self.service.name+': '+str(self.userId)
