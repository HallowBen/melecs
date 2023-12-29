from django.shortcuts import render
from user_side import models
from melecs.settings import STATIC_URL, STATICFILES_DIRS
from django.http import HttpResponse, JsonResponse
from matplotlib import pyplot as plt
from django.template.defaultfilters import slugify
from datetime import datetime
from .models import measurement_data, measurement_list, measured_place, all_measurement
import os

# Create your views here.

def home(request):
    data={}
    if measurement_data.objects.exists() and measurement_data.objects.filter(Finished=False).exists():
        query = measurement_data.objects.filter(Finished=False).get()
        data['ID'] = query.ID.ID
        if query.Person != None:
            data['Person'] = query.Person.Name
        else:
            data['Person'] = "Ismeretlen"
        if query.Place != None:
            data['Place'] = query.Place.Name
            data['RequiredAmmount'] = query.Place.Required_ph
        else:
            data['Place'] = "Ismeretlen"
            data['RequiredAmmount'] = "Ismeretlen"
        data['StartTime'] = all_measurement.objects.last().time
        data['SUM'] = query.sum
        data['TimeSinceStart'] = query.runtime
        data['AmmountOfMeasurement'] = all_measurement.objects.count()
    else:
        data = None
        
        print(request)
    
    return render(request, 'sites/home.html', {'data':data,"title":"Home"})

def home_chart(request):
    data={}
    plt.switch_backend('agg')
    if os.path.exists(STATICFILES_DIRS[0]/'active.png'):
        os.remove(STATICFILES_DIRS[0]/'active.png')
        
    if measurement_data.objects.exists() and measurement_data.objects.filter(Finished=False).exists():
        active = measurement_data.objects.filter(Finished=False).get()
        if active != None:
            if measured_place.objects.exists() and active.Place != None:
                rpm = active.Place.Required_ph / 60
            else:
                rpm = 0.0
            if active.runtime != "unknown":
                apm = active.sum/ (active.runtime/60)
            else:
                apm = active.sum/60
            if apm<=(0.5*rpm):
                pdata = [apm,rpm-apm]
                plabel = ["teljesített", "hiányzok"]
            elif apm<rpm:
                pdata = [apm,apm-rpm]
                plabel = ["teljesített", "hiányzok"]
            else:
                pdata = [rpm,apm-rpm]
                plabel = ["elvárt", "többlet"]
            fig, pie = plt.subplots()
                
            pie.pie(pdata, explode=(0.1,0), labels=plabel, shadow=True, startangle=90)
            pie.axis('equal')
            fig.set_facecolor("#ffffff")
            plt.savefig(f'{STATIC_URL}/active.png', dpi=70)
            plt.close()
            data["chart"]=f"{STATIC_URL}active.png"
            data["val"] = False
            data["tapm"] = apm
            data["trpm"] = rpm
    
    else:
        data["tapm"] = 0
        data["trpm"] = 0      
    return JsonResponse({'data':data})

def test(request):
    data={}
    tapm = float(request.headers['Apm'])
    trpm = float(request.headers['Rpm'])
    if measurement_data.objects.exists() and measurement_data.objects.filter(Finished=False).exists():
        active = measurement_data.objects.filter(Finished=False).get()
        if active != None:
            if measured_place.objects.exists() and active.Place != None:
                rpm = active.Place.Required_ph / 60
            else:
                rpm = 0.0
            if active.runtime != 0:
                apm = active.sum/ (active.runtime/60)
            else:
                apm = active.sum/60
    else:
        rpm = 0
        apm = 0
    if tapm==apm and trpm==rpm:
        data["val"] = False
        data["tapm"] = apm
        data["trpm"] = rpm
    else:
        data["val"] = True
        data["tapm"] = apm
        data["trpm"] = rpm
    return JsonResponse({'data':data})
    
def allms(request):
        return render(request, "sites/measurements.html", {"title":"Mérési lista"})
    
def msdata(request):
    data = []
    querry = measurement_list.objects.all()
    for item in querry:
        tdata={
            "ID": item.ID,
            "Date": item.Date.strftime("%Y.%m.%d %H:%M"),
            "active": "Befejezett" if measurement_data.objects.filter(ID=item.ID).get().Finished else "Aktív" ,
        }
        data.append(tdata)
    return JsonResponse({"data":data})
    
def detailms(request, msid):
    data={}
    query = measurement_data.objects.filter(ID=msid).get()
    if query.Person !=None:
        data["person"]=query.Person.Name
    else:
         data["person"]="Ismeretlen"
    if query.Place !=None:
        data["place"]=query.Place.Name
        data["required"]=query.Place.Required_ph
    else:
        data["place"]="Ismeretlen"
        data["required"]="Ismeretlen"
    if query.Finished:
        data["SUM"]=query.SUM
        data["measuredtime"] = query.measured_time
        data["Endtime"] = query.End_Time.strftime("%Y.%m.%d %H:%M"),
        data["msammount"] = query.MSammount
    else:
        data["SUM"] = query.sum
        data["measuredtime"] = query.runtime
        data["Endtime"] = "Ismeretlen"
        data["msammount"] = query.msammount
    data["Start_Time"] = query.Start_Time.strftime("%Y.%m.%d %H:%M"),
    
    return JsonResponse({'data': data})
    
    
    
    
    
    
# def allms(request):
#     data = []
#     data.append({"name":"ID","val":"ID"})
#     data.append({"name":"Date","val":"Dátum"})
#     data.append({"name":"Place","val":"Hely"})
#     data.append({"name":"Person","val":"Személy"})
        
        
#     return render(request, "sites/measurements.html", {"data":data,"title":"Mérési lista"})

# def msdata(request, order):
#     data = []
#     querry = measurement_list.objects.all().order_by(order)
#     for item in querry:
#         tdata={
#             "ID": item.ID,
#             "date": item.Date.strftime("%Y.%m.%d %H:%M"),
#             "active": "Befejezett" if measurement_data.objects.filter(ID=item.ID).get().Finished else "Aktív" ,
#         }
#         data.append(tdata)
#     return JsonResponse({"data":data})


# def mssearch(request, where, what):
#     if where == "Place":
#         id_query = measurement_data.objects.filter(Place__Name__icontains = what).values_list('ID', flat = True)
#     if where == "Person":
#         id_query = measurement_data.objects.filter(Person__Name__icontains = what).values_list('ID', flat = True)
#     if where == "Date":
#         day = datetime.strptime(what,'%Y-%m-%d').day
#         id_query = [x.ID for x in measurement_data.objects.all() if x.get_day == int(day)]
    
#     if where == "ID":
#         what = slugify(what)
#         id_query = measurement_data.objects.filter(ID__ID__icontains = what).values_list('ID', flat = True)
    
#     query = measurement_list.objects.filter(ID__in = id_query)
#     data = []
#     for item in query:
#         tdata={
#             "ID": item.ID,
#             "date": item.Date.strftime("%Y.%m.%d %H:%M"),
#             "active": "Befejezett" if measurement_data.objects.filter(ID=item.ID).get().Finished else "Aktív" ,
#         }
#         data.append(tdata)
#     return JsonResponse({"data":data})