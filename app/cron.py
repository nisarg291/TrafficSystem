
from app.models import Society,House

import time
from datetime import datetime
# Create your views here.


# import schedule


def UpdateAvailability():
    Societies=Society.objects.all();
    print(Societies);
    for society in Societies:
        availableHouses=[];
        users= House.objects.filter(societyId=society,available=True)
        if users:
            TotalAvailableParking=0;
            available={}

            for i in range(0,society.totalNumberOfBuilding):
                available[str(chr(65+i))]=0;

            for user in users:

                if user.parkingStatus==True:
                    TotalAvailableParking+=1;
                    for i in range(0,society.totalNumberOfBuilding):
                        if user.blockNumber==str(chr(65+i)):
                            available[str(chr(65+i))]+=1;
                            availableHouses.append(user.houseNumber)
            print(society.societyName)    
            print(available)
            print(availableHouses)
            print(TotalAvailableParking)
            society.totalAvailableParkings=TotalAvailableParking;
            society.availableHouses=availableHouses;
            society.save()


