from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    desc = models.CharField(max_length=10000)
    country = models.CharField(max_length=50)
    website = models.URLField()
    contact_people = models.CharField(max_length=10)
    telphone = models.CharField(max_length=20)

    class Meta:
        ordering = ["-name"]

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.name
    
class Appliance(models.Model):
    type = models.CharField(max_length=20)
    title = models.CharField(max_length=80)
    thumbnail = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    create_at = models.CharField(max_length=50)
    update_at = models.CharField(max_length=50)
      
    class Meta:
        pass
  
    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.title
    
class Appliance_type(models.Model):
    type = models.CharField(max_length=20)
    desc = models.CharField(max_length=80)
    icon = models.CharField(max_length=20)
    create_at = models.CharField(max_length=50)
    update_at = models.CharField(max_length=50)
      
    class Meta:
        pass
  
    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.type