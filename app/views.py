from django.shortcuts import render,HttpResponse,redirect
# import pyttsx3 #pip install pyttsx3
# import speech_recognition as sr #pip install speechRecognition
from django.contrib import messages
#import datetime
# from bs4 import BeautifulSoup
import requests
import json
# import webbrowser
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# from verify_email.email_handler import send_verification_email
# from users.models import Profile


import os
from django.views.decorators.csrf import csrf_protect

# import smtplib

from app.models import Society,House

from datetime import datetime
# Create your views here.


# import schedule

# x=datetime.today()
# print(x)
# y = x.replace(day=x.day, hour=0, minute=5, second=0, microsecond=0) + timedelta(days=1)
# delta_t=y-x

# secs=delta_t.total_seconds()
# print(secs);

# from celery import shared_task
# @shared_task
# def run_daily_function():
#     schedule.every().day.at("10:00").do(UpdateAvailability)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


from datetime import datetime, timedelta


def every_monday_morning():
    print("This is run every Monday morning at 7:30")

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


def home(request):
    
    return render(request,'home.html')

def login(request):
    if request.method == "POST":
        loginName = request.POST['loginName']
        password = request.POST['password']
        logins = Society.objects.filter(societyName=loginName)
        availableHouses=[]
        if logins:
            if password == logins[0].password:
                request.session['ID'] = logins[0].societyId
                ID =  request.session['ID']
                buildings=logins[0].totalNumberOfBuilding;
                users= House.objects.filter(societyId=logins[0],available=True)
                if users:
                    TotalAvailableParking=users.count();
                    available={}

                    for i in range(0,buildings):
                        available[str(chr(65+i))]=0;

                    for user in users:
                        for i in range(0,buildings):
                            if user.blockNumber==str(chr(65+i)):
                                available[str(chr(65+i))]+=1;
                                availableHouses.append(user.houseNumber)
                                
                    
                    print(available)
                    print(availableHouses)

                    print(TotalAvailableParking)
                    logins[0].totalAvailableParkings=TotalAvailableParking;
                    logins[0].availableHouses=availableHouses;
                    logins[0].save()
                    return render(request,'home.html',{'available':available,'TotalAvailableParking':TotalAvailableParking,'availableHouses':availableHouses})

                else:
                    TotalAvailableParking=0
                    available={'A':0}
                return render(request,'home.html',{'available':available,'TotalAvailableParking':TotalAvailableParking})
            else:
                messages.warning(request,'Password Do not Match')
                return render(request,'login.html')
            
            
        else:
            logins = Society.objects.filter(societyUsername=loginName)
            if logins:
                if password == logins[0].password:
                    request.session['ID'] = logins[0].societyId
                    ID =  request.session['ID']
                    buildings=logins[0].totalNumberOfBuilding;
                users= House.objects.filter(societyId=logins[0],available=True)
                if users:
                    TotalAvailableParking=users.count();
                    available={}

                    for i in range(0,buildings):
                        available[str(chr(65+i))]=0;

                    for user in users:
                        for i in range(0,buildings):
                            if user.blockNumber==str(chr(65+i)):
                                available[str(chr(65+i))]+=1;
                                availableHouses.append(user.houseNumber)
                                
                    
                    print(available)
                    print(availableHouses)

                    print(TotalAvailableParking)
                    logins[0].totalAvailableParkings=TotalAvailableParking;
                    logins[0].availableHouses=availableHouses;
                    logins[0].save()
                    return render(request,'home.html',{'available':available,'TotalAvailableParking':TotalAvailableParking,'availableHouses':availableHouses})

                else:
                    messages.warning(request,'Password Do not Match')
                    return render(request,'login.html')
            
            else:
                messages.warning(request,'wrong Username or society name')
                return render(request,'login.html')
                        
    return render(request,'login.html')

def register(request):
    if request.method == "POST":
        societyName = request.POST['societyName']
        societyUsername =  request.POST['societyUsername']
        societyEmail = request.POST['societyEmail']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        totalNumberOfHouses = int(request.POST['totalNumberOfHouses'])
        totalNumberOfBuildings = int(request.POST['totalNumberOfBuildings'])
        totalNumberOfFloor = int(request.POST['totalNumberOfFloor'])
        totalHouseInEachFloor = int(request.POST['totalHouseInEachFloor'])
        societyAddress = request.POST['societyAddress']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        if password == confirmPassword:
            add_society = Society(societyName=societyName,societyUsername=societyUsername,societyEmail=societyEmail,password=password,totalNumberOfHouse=totalNumberOfHouses,totalNumberOfBuilding=totalNumberOfBuildings,totalNumberOfFloors=totalNumberOfFloor,totalHouseInEachFloor=totalHouseInEachFloor,societyAddress=societyAddress,city=city,state=state,country=country,pincode=pincode)
            add_society.save()
            soc=Society.objects.filter(societyUsername=societyUsername,password=password)
            societyId=soc[0].societyId;
            for i in range(0,totalNumberOfBuildings):
                for j in range(1,totalNumberOfFloor+1):
                    for k in range(1,totalHouseInEachFloor+1):
                        houseNumber=str(chr(65+i)+str(j)+str('0')+str(k))
                        blockNumber=str(chr(65+i))
                        username= str(societyName)+houseNumber
                        password=societyUsername+houseNumber
                        add_user=House(houseNumber=houseNumber,username=username,blockNumber=blockNumber,societyName=societyName,password=password,societyId=add_society)
                        add_user.save()
        return redirect('login')
    return render(request,'register.html')
def parking(request):
    if request.method == "POST":
        totalDaysAvailable=request.POST['totalDaysAvailable']
        startDate=request.POST['startDate']
        endDate=request.POST['endDate']
        username=request.session.get('user')
        
        users=House.objects.filter(username=username)
        if users:
            users[0].available=True
            users[0].totalDaysAvailable=int(totalDaysAvailable)
            users[0].startDate=startDate
            users[0].endDate=endDate
            users[0].save()
            messages.success(request,'Parking Status successfully Updated')
            return render(request,'userHome.html')
    return render(request,'parking.html')

def userLogin(request):
    if request.method == "POST":
        loginUsername = request.POST["loginUsername"]
        loginPassword = request.POST["loginPassword"]
        users=House.objects.filter(username=loginUsername)
        if users:
            if loginPassword == users[0].password:
                print("login successful");
                messages.success(request,'Login successful welcome to home page')
                request.session['user']=users[0].username
                return render(request,'userHome.html',{'user':users[0]})   
            else:
                messages.warning(request,'enter correct password')  
                return render(request,'login.html')
        else:
            users=House.objects.filter(email=loginUsername)
            if users:
                if loginPassword == users[0].password:
                    print("login successful");
                    messages.success(request,'Login successful welcome to home page')
                    request.session['user']=users[0].username;
                    return render(request,'userHome.html',{'user':users[0]})   
                else:
                    messages.warning(request,'enter correct password')   
                    return render(request,'login.html')
            else:
                messages.warning(request,'enter correct username or email')
                return render(request,'login.html')

    return render(request,'login.html')

def societyDetails(request):
    pass;

def availableParkings(request):
    if request.session.has_key('user'):
        username=request.session['user'];
        users=House.objects.filter(username=username);
        societyName=str(users[0].societyName);
        socities=Society.objects.filter(societyName=societyName);
        societyName=socities[0].societyName;
        totalNumberOfBuilding = int(socities[0].totalNumberOfBuilding);
        totalAvailableParkings=str(socities[0].totalAvailableParkings);
        availableHouses=(socities[0].availableHouses);
        print(availableHouses);
        availableHouses=availableHouses.strip('][').replace("'",'').split(',');
        print(availableHouses);
        
        av_dct={};
        for h in availableHouses:
            av_dct[h.strip(' ')[0]]=[];
        for i in range(0,len(availableHouses)):
            block=str(availableHouses[i].strip(' ')[0]);    
            av_dct[block].append(availableHouses[i]);
                
        


        # for i in range(0,totalNumberOfBuilding):
        #     blocks.find
        #     av_dct[chr(65+i)]=blocks.count(chr(65+i));

        print(av_dct);
        print(type(availableHouses));
        
        
        return render(request,'AvailableParkings.html',{'societyName':societyName,'av_dct':av_dct,'totalNumberOfBuilding':totalNumberOfBuilding, 'availableHouses':availableHouses,'totalAvailableParkings':totalAvailableParkings})
    else:
        return render(request,'AvailableParkings.html')

    