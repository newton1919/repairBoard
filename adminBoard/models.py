from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    desc = models.CharField(max_length=10000)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.name