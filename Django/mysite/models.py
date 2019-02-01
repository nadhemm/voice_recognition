from django.db import models


class Keyword(models.Model):
    word = models.CharField(max_length=30)
    weight = models.IntegerField()
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.word + ' ' + self.language


class Algorithm(models.Model):
    name = models.CharField(max_length=30)
    language = models.CharField(max_length=30)
    tags = models.ManyToManyField(Keyword)
    implementation = models.TextField()

    def __str__(self):
        return self.name + ' ' + self.language
