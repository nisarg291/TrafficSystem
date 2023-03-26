from django.db import models

import datetime
# Create your models here.
DATE_INPUT_FORMATS = ["%d.%m.%Y"]
USE_L10N = False
defaultStart=datetime.date(2000,1,1);
defaultEnd=datetime.date(2000,1,3);

class Society(models.Model):
    societyId = models.AutoField(primary_key=True)
    societyName = models.CharField(max_length=200,unique=True)
    societyUsername = models.CharField(max_length=200,unique=True)
    societyEmail = models.EmailField() 
    totalNumberOfHouse = models.IntegerField()
    totalNumberOfBuilding = models.IntegerField()
    totalNumberOfFloors = models.IntegerField() 
    totalHouseInEachFloor = models.IntegerField()
    password = models.CharField(max_length=50)
    societyAddress = models.TextField()
    city = models.CharField(null=True,max_length=30)
    state = models.CharField(null=True,max_length=40)
    country = models.CharField(null=True,max_length=40)
    pincode = models.CharField(max_length=50)
    totalAvailableParkings= models.IntegerField(default=0)
    availableHouses = models.CharField(null=True,max_length=2000)
    
    class Meta: 
        db_table = "SocietyDetail"  
    def __str__(self):
        return str(self.societyName)


class House(models.Model):
    userId= models.AutoField(primary_key=True)
    houseNumber = models.CharField(max_length=100)
    blockNumber = models.CharField(max_length=50,default="A")
    username = models.CharField(max_length=200,unique=True)
    password=models.CharField(max_length=200,default='1234')
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(null=True)
    societyName= models.CharField(max_length=200)
    societyId= models.ForeignKey(Society,on_delete=models.CASCADE)
    totalDaysAvailable = models.IntegerField(default=0)
    startDate = models.DateField(default=defaultStart) 
    endDate = models.DateField(default=defaultEnd)
    available = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.username)
    
    def AvailabiltyCheck(self):
        from datetime import date
        if self.endDate<date.today() or self.startDate>date.today():
            self.available=False;
        elif self.startDate<=date.today() and self.endDate>=date.today():
            self.available=True;
        else:
            pass;


    @property
    def parkingStatus(self):
        from datetime import date
        if self.startDate<=date.today() and self.endDate>=date.today():
            return True;
        if self.startDate>date.today() or self.endDate<date.today():
            return False;

