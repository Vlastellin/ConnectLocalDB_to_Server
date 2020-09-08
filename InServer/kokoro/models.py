from django.db import models


class Mens(models.Model):
    id=models.IntegerField(primary_key=True)
    value=models.CharField(max_length=255)
    
class Task_section(models.Model):
    id=models.IntegerField(primary_key=True)
    descript=models.CharField(max_length=255)  
    object = models.IntegerField()
    
class Object(models.Model):
    id=models.IntegerField(primary_key=True)
    adres=models.CharField(max_length=255)  

class Task(models.Model):
    id=models.IntegerField(primary_key=True)
    descript=models.CharField(max_length=255)  
    task_section = models.IntegerField()
    date = models.DateField()
    time1 = models.TimeField()
    time2 = models.TimeField()
    
class Operation(models.Model):
    id=models.IntegerField(primary_key=True)
    time1= models.TimeField()
    time2 = models.TimeField()
    description=models.CharField(max_length=255)
    place=models.CharField(max_length=255)
    mens = models.IntegerField()
    count = models.FloatField()
    price = models.FloatField()
    salary = models.FloatField()
    plan = models.IntegerField()
    
class Plan(models.Model):
    id=models.AutoField(primary_key=True)
    date = models.DateField()
    employee = models.IntegerField()
    task = models.IntegerField()
    take = models. BooleanField(null=True)
    comment = models.CharField(max_length=255) 
    
class Pass(models.Model):
    id=models.AutoField(primary_key=True)
    plan = models.IntegerField()
    operation = models.IntegerField()
    count = models.FloatField()    
    salary = models.FloatField()
    comment = models.CharField(max_length=255)
    

class Accept(models.Model):
    id=models.IntegerField(primary_key=True)
    operation = models.IntegerField()
    plan = models.IntegerField()
    count = models.FloatField()
    salary = models.FloatField()
    comment = models.CharField(max_length=255) 
    
class Employee(models.Model):
    id=models.IntegerField(primary_key=True)
    f=models.CharField(max_length=255)
    i=models.CharField(max_length=255)
    o=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=255)

    
    

    

    

    

