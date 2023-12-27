from collections.abc import Iterable
from django.db import models
import random, string
from django.template.defaultfilters import slugify
from django.utils import timezone

# Create your models here.

class permission_set(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.Name)
    
    def save(self,*args, **kwargs):
        super(permission_set, self).save(*args, **kwargs)

class measurement_list(models.Model):
    ID = models.SlugField(editable=False, primary_key=True, unique=True, default="")
    Date = models.DateTimeField( auto_now=True, auto_now_add=False)
    Comment = models.TextField()
    
    def save(self):
        if self.ID=="":
            self.ID=slugify(''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(6)))
        super(measurement_list, self).save()
    
    def __str__(self):
        return str(self.ID)
            
class user(models.Model):
    ID = models.SlugField(editable=False, primary_key=True, unique=True, default="")
    Date = models.DateTimeField( auto_now=True, auto_now_add=False, editable=False)
    Name = models.CharField(max_length=50)
    Permission = models.ManyToManyField(permission_set)
    
    def __str__(self):
        return str(self.Name)
    
    def save(self,*args, **kwargs):
        if self.ID=="":
            self.ID=slugify(self.Name)
        super(user, self).save(*args, **kwargs)
        
class measured_place(models.Model):
    ID = models.SlugField(editable=False, primary_key=True, unique=True, default="")
    Date = models.DateTimeField( editable=False, auto_now=True, auto_now_add=False)
    Name = models.CharField(max_length=50)
    Person = models.ForeignKey(user, on_delete=models.SET_NULL, null = True, blank=True, default=None)
    Required_ph = models.IntegerField()
    
    def __str__(self):
        return str(self.Name)
    
    def save(self):
        if self.ID=="":
            self.ID=slugify(self.Name)
        super(measured_place, self).save()
        
class all_measurement(models.Model):
    ID = models.ForeignKey(measurement_list, on_delete=models.CASCADE)
    ammount = models.IntegerField(blank = False, default = 0)
    time = models.DateTimeField( auto_now=True, auto_now_add=False)
    
    def save(self):
        super(all_measurement, self).save()
    
    def __str__(self):
        return str(self.ID)+":"+str(self.time)
        
class measurement_data(models.Model):
    ID = models.ForeignKey(measurement_list, on_delete=models.CASCADE)
    Place = models.ForeignKey(measured_place, on_delete=models.SET_NULL, null = True, blank=True, default=None, db_constraint=False)
    Person = models.ForeignKey(user, on_delete=models.SET_NULL, null = True, blank=True, default=None, db_constraint=False)
    Start_Time = models.DateTimeField( auto_now=False, auto_now_add=False, editable=False, null=True,  blank=True, default=None)
    Finished = models.BooleanField(default=False)
    SUM = models.IntegerField(editable=False, blank=True, null=True)
    MSammount = models.IntegerField(editable=False, blank=True, null = True)
    measured_time = models.IntegerField(editable=False, blank=True, null=True)
    End_Time = models.DateTimeField(auto_now=False, auto_now_add=False, editable=False, null=True,  blank=True)
    
    def __str__(self):
        return str(self.ID)
    
    def save(self, *args, **kwargs):
        if self.Start_Time==None:
            self.Start_Time = timezone.now()
        if self.Finished and self.End_Time==None:
            self.End_Time = timezone.now()
            self.SUM=self.sum
            
            last = all_measurement.objects.filter(ID = self.ID).last()
            duration = last.time-self.Start_Time
            self.measured_time = duration.seconds
            
            query=all_measurement.objects.filter(ID = self.ID)
            self.MSammount = query.count()
            for data in query:
                data.delete()
            
            
        elif not self.Finished:
            self.End_Time = None
        super(measurement_data, self).save(*args, **kwargs)
        
    @property
    
    def sum(self):
        query = all_measurement.objects.filter(ID = self.ID)
        rsum = 0
        for data in query:
            rsum += data.ammount
        
        return rsum 
    @property
    def runtime(self):
        if all_measurement.objects.filter(ID = self.ID).exists():
            last = all_measurement.objects.filter(ID = self.ID).last()
            duration = last.time-self.Start_Time
            return duration.seconds
        else:
            return "unknown"
        
    @property
    def msammount(self):
        if all_measurement.objects.filter(ID = self.ID).exists():
            return all_measurement.objects.filter(ID = self.ID).count()
        else:
            return "unknown"
        
    
class Archive(models.Model):
    Name = models.CharField( max_length=30)
    type = models.CharField( max_length=20)
    File_Location = models.CharField( max_length=50)
    date = models.DateTimeField( auto_now=False, auto_now_add=False, default = None )
    
    def __str__(self):
        return str( self.Name )

    def save(self,*args, **kwargs):
        if self.date == None:
            self.date = timezone.now()
        return super(Archive, self).save(*args, **kwargs)