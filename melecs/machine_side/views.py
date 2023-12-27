from django.shortcuts import render
from user_side.models import measurement_list,measured_place,measurement_data, user, all_measurement
from django.http import HttpResponse
from Archive import Archivation
import datetime

# Create your views here.


def start(request):
    new_measurement = measurement_list(Comment="new measurement")
    new_measurement.save()
    response = HttpResponse(
        status=204, 
        headers={
            'msid': f"{new_measurement.pk}",
    })
    new_measurement_data = measurement_data(ID=new_measurement)
    if "place" in request.headers:
        searched_place= request.headers.get("place")
        places = measured_place.objects.all()
        for place in places:
            if searched_place == place.Name:
                new_measurement_data.Place = place

    if "person" in request.headers:
        searched_person= request.headers.get("person")
        users = user.objects.all()
        for person in users:
            if searched_person == person.Name:
                new_measurement_data.Person = person
    new_measurement_data.save()
    return response

def add(request, msid, nammount):
    ms = measurement_list.objects.filter(ID=msid).get()
    new_data = all_measurement(ID=ms, ammount=nammount)
    new_data.save()
    response = HttpResponse(
        status=204, 
        headers={
            "status":"Ok",
    })
    return response

def end(request, msid, nammount):
    data = measurement_data.objects.filter(ID = msid).get()
    new_data = all_measurement(ID=measurement_list.objects.filter(ID=msid).get(), ammount=nammount)
    new_data.save()
    
    Archivation("measaurement_datas", msid, [1])
    
    data.Finished=True
    data.save()
    response = HttpResponse(
        status=204, 
        headers={
            "status":"Ok",
    })
    return response

def archive(request):
    response = HttpResponse(
        status=204, 
        headers={
            "status":"Ok",
    })
    
    date = str(datetime.date.today().year)+"_"+str(datetime.date.today().month)+"_"+str(datetime.date.today().day)
    Archivation("monthly archive",date, [1,2,3,4,5])
    
    querry = all_measurement.objects.all()
    for data in querry:
        data.delete()
    querry = measurement_data.objects.all()
    for data in querry:
        data.delete()
    querry = measurement_list.objects.all()
    for data in querry:
        data.delete()
    
    return response