from django.shortcuts import render

from django.http import HttpResponse
from .models import prodect
# Create your views here.
from django.contrib.auth.decorators import login_required

import pyrebase
from datetime import datetime, timedelta, time
config = {
    
    "apiKey": "AIzaSyDVDzE3TvAzt1gSOx5TSWzYBfZMEMPU0wc",
    "authDomain": "workproject-f7fad.firebaseapp.com",
    "projectId": "workproject-f7fad",
    "databaseURL": "https://workproject-f7fad-default-rtdb.firebaseio.com",
    "storageBucket": "workproject-f7fad.firebasestorage.app",
    "messagingSenderId": "791273192526",
    "appId": "1:791273192526:web:9cad231e1775dad210171f",
    "measurementId": "G-835DXVDCZM"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()  # Initialize the Realtime Database


def index(request):
    allpro=prodect.objects.all()
    print(allpro)
    return HttpResponse(f"<h1>{allpro}</h1>")

def create_prodect(request,name):
    e=prodect(name=name)
    e.save()
    return HttpResponse(f"<h1>{request.tenant} created</h1>")





# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import TenantLoginForm,RegistrationForm
from django.contrib import messages
from app.models import TenantUser  # Ensure you import your TenantUser model


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Create the TenantUser instance
            tenant = request.tenant  # Assuming the tenant is already set in the request
            TenantUser.objects.create(user=user, tenant=tenant)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('Centerapp:tenant_login')  # Redirect to the login page
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})      
from django_tenants.utils import schema_context
from app.models import center
from .models import *

from django.contrib.auth.models import User
@login_required()
def show(request):
    return render(request, 'test.html')  

def create_about(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        Des1 = request.POST.get('Des')
        im1=request.FILES.get('Img1') 
        about.objects.create(name=name1,Des=Des1,photo=im1)
    
    return render(request, 'create_about.html')     



def test1(request):
    return render(request, 'therapist.html')  
@login_required()
def aboutadmin(request):

    tenant1=request.tenant 

    about1=about.objects.all().first()
    user1=request.user
 

    if request.method=="POST":
        name1 = request.POST.get('Name')
        name2 = request.POST.get('UserName')
        Des1 = request.POST.get('Description')
        Add1 = request.POST.get('Address') 
        prictrans1 = request.POST.get('pricetrans')         
        X = request.POST.get('X')
        Y = request.POST.get('Y')
        im1=request.FILES.get('Img') 
        im2=request.FILES.get('Img1') 
        PaymentInfo1=request.POST.get('PaymentInfo') 
        if about1:

              
          
          about1.name=name1
          about1.Des=Des1   
          about1.Address=Add1
          about1.x=X
          about1.y=Y
          about1.pricetrans=prictrans1
          about1.PaymentInfo=PaymentInfo1
          user1.username=name2
          if im1:
            about1.photo=im1
          if im2:
              about1.photo1=im2  
          user1.save()
          about1.save()    
        else:
            about.objects.create(name=name1,Des=Des1,photo=im1,x=X,y=Y,Address=Add1,pricetrans=prictrans1
                                 ,photo1=im2,PaymentInfo=PaymentInfo1)



    return render(request, 'aboutadmin.html',{'about':about1,'user':user1,'var':'about'})  

# def getAllRating(request):

#     ratings=Rating.objects.all()

#     return render(request, 'AllRating.html',{'Rating':ratings,'var':'Rating'})  


def tenant_login(request):
    if request.method == 'POST':
        form = TenantLoginForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate using the default backend
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                try:
                    print(user)
                    print(request.tenant)
                    print(TenantUser.objects.all())

                    tenant_user = TenantUser.objects.get(user=user, tenant=request.tenant)  # Get the TenantUser instance
                    print(tenant_user)
                    login(request, user)
                    print("ok")
                    return redirect('centerappp:aboutadmin')  # Change to your success URL
                except TenantUser.DoesNotExist:
                    print("User does not belong to the current tenant.")
            else:
                print("Authentication failed.")
    else:
        form = TenantLoginForm()
    return render(request, 'login.html', {'form': form})

def getAllCPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        socket_type1 = request.POST.get('socket_type')
        supported_ram_type1 = request.POST.get('supported_ram_type')
        max_ram_speed1 = request.POST.get('max_ram_speed')
        tdp1 = request.POST.get('tdp')
        chipset1 = request.POST.get('chipset')
        type1 = request.POST.get('type')
        CPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            socket_type=socket_type1,
            supported_ram_type=supported_ram_type1,
            max_ram_speed=max_ram_speed1,
            tdp=tdp1,
            chipset=chipset1,type=type1
        )
       

    CPUs=CPU.objects.all()

    return render(request, 'CPU.html',{'CPUS':CPUs,'var':'CPU'})  

def searchEl(request):
   if request.method=="POST":
       fullname=request.POST.get('search')
       type=request.POST.get('type')
       if type=='CPU':
          CPUs=CPU.objects.filter(name=fullname)
          return render(request, 'CPU.html',{'CPUS':CPUs,'var':'CPU'}) 
       if type=='GPU':
          GPUs=GPU.objects.filter(name=fullname)
          return render(request, 'GPU.html',{'GPUS':GPUs,'var':'GPU'}) 
       if type=='RAM':
          RAMs=RAM.objects.filter(name=fullname)
          return render(request, 'RAM.html',{'RAMS':RAMs,'var':'RAM'}) 
       if type=='HARD':
          HARDS=Storage.objects.filter(name=fullname)
          return render(request, 'HARD.html',{'HARDS':HARDS,'var':'HARD'}) 
       if type=='Motherboard':
          Motherboards=Motherboard.objects.filter(name=fullname)
          return render(request, 'Motherboard.html',{'MotherboardS':Motherboards,'var':'Motherboard'}) 
       if type=='PSU':
          PSUs=PSU.objects.filter(name=fullname)
          return render(request, 'PSU.html',{'PSU':PSUs,'var':'PSU'}) 
       if type=='Cooler':
          Coolers=Cooler.objects.filter(name=fullname)
          return render(request, 'Cooler.html',{'Cooler':Coolers,'var':'Cooler'})   
def getHighCPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        socket_type1 = request.POST.get('socket_type')
        supported_ram_type1 = request.POST.get('supported_ram_type')
        max_ram_speed1 = request.POST.get('max_ram_speed')
        tdp1 = request.POST.get('tdp')
        chipset1 = request.POST.get('chipset')
        type1 = request.POST.get('type')
        CPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            socket_type=socket_type1,
            supported_ram_type=supported_ram_type1,
            max_ram_speed=max_ram_speed1,
            tdp=tdp1,
            chipset=chipset1,type=type1
        )
       

    CPUs=CPU.objects.filter(type='High')

    return render(request, 'CPU.html',{'CPUS':CPUs,'var':'CPU'})  

def getLowCPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        socket_type1 = request.POST.get('socket_type')
        supported_ram_type1 = request.POST.get('supported_ram_type')
        max_ram_speed1 = request.POST.get('max_ram_speed')
        tdp1 = request.POST.get('tdp')
        chipset1 = request.POST.get('chipset')
        type1 = request.POST.get('type')
        CPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            socket_type=socket_type1,
            supported_ram_type=supported_ram_type1,
            max_ram_speed=max_ram_speed1,
            tdp=tdp1,
            chipset=chipset1,type=type1
        )
       

    CPUs=CPU.objects.filter(type='Low')

    return render(request, 'CPU.html',{'CPUS':CPUs,'var':'CPU'})  

def getMediumCPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        socket_type1 = request.POST.get('socket_type')
        supported_ram_type1 = request.POST.get('supported_ram_type')
        max_ram_speed1 = request.POST.get('max_ram_speed')
        tdp1 = request.POST.get('tdp')
        chipset1 = request.POST.get('chipset')
        type1 = request.POST.get('type')
        CPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            socket_type=socket_type1,
            supported_ram_type=supported_ram_type1,
            max_ram_speed=max_ram_speed1,
            tdp=tdp1,
            chipset=chipset1,type=type1
        )
       

    CPUs=CPU.objects.filter(type='Medium')

    return render(request, 'CPU.html',{'CPUS':CPUs,'var':'CPU'})  


def deleteCPU(request):
    if request.method=="POST":
        idCPU = request.POST.get('iddoctor')
        CPU.objects.get(id=idCPU).delete()
    return redirect('centerappp:getAllCPU')


def EditCPU(request,idCPU):
    CPU1=CPU.objects.get(id=idCPU)
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        socket_type1 = request.POST.get('socket_type')
        supported_ram_type1 = request.POST.get('supported_ram_type')
        max_ram_speed1 = request.POST.get('max_ram_speed')
        tdp1 = request.POST.get('tdp')
        chipset1 = request.POST.get('chipset')
        type1 = request.POST.get('type')
        CPU1.name=name1
        CPU1.price=price1
        CPU1.count=count1
        CPU1.link=link1
        CPU1.socket_type=socket_type1
        CPU1.supported_ram_type=supported_ram_type1
        CPU1.max_ram_speed=max_ram_speed1
        CPU1.tdp=tdp1
        CPU1.chipset=chipset1
        CPU1.type=type1
        CPU1.save()
        return redirect('centerappp:getAllCPU')

    return render(request, 'CPU1.html',{'CPU':CPU1,'var':'CPU'})  
########################################################################################3
def getALLGPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        type1 = request.POST.get('type')
        interface_version1 = request.POST.get('interface_version')
        power_draw1 = request.POST.get('power_draw')
        length_mm1 = request.POST.get('length_mm')
        required_psu_wattage1 = request.POST.get('required_psu_wattage')
        output_ports1 = request.POST.get('output_ports')
        GPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            type=type1,
            interface_version=interface_version1,
            power_draw=power_draw1,
            length_mm=length_mm1,
            required_psu_wattage=required_psu_wattage1,output_ports=output_ports1
        )
       

    GPUs=GPU.objects.all()

    return render(request, 'GPU.html',{'GPUS':GPUs,'var':'GPU'})  
from django.shortcuts import render
from .models import Rating
from django.db.models import Count, Q
from django.utils import timezone
def getALLRating(request):
    ratings = Rating.objects.all()

    positive_ratings = ratings.filter(Type='POSITIVE').values('Date').annotate(count=Count('Star')).order_by('Date')
    negative_ratings = ratings.filter(Type='NEGATIVE').values('Date').annotate(count=Count('Star')).order_by('Date')

    dates = sorted(list({r['Date'] for r in positive_ratings} | {r['Date'] for r in negative_ratings}))
    positive_counts = [0] * len(dates)
    negative_counts = [0] * len(dates)

    for r in positive_ratings:
        index = dates.index(r['Date'])
        positive_counts[index] = r['count']

    for r in negative_ratings:
        index = dates.index(r['Date'])
        negative_counts[index] = r['count']

    # تحويل التواريخ إلى سلسلة نصية
    dates = [d.strftime('%Y-%m-%d') for d in dates]

    context = {
        'Ratings': ratings,
        'dates': dates,
        'positive_counts': positive_counts,
        'negative_counts': negative_counts,
    }
    return render(request, 'Rating.html', context)




def getLowGPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        type1 = request.POST.get('type')
        interface_version1 = request.POST.get('interface_version')
        power_draw1 = request.POST.get('power_draw')
        length_mm1 = request.POST.get('length_mm')
        required_psu_wattage1 = request.POST.get('required_psu_wattage')
        output_ports1 = request.POST.get('output_ports')
        GPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            type=type1,
            interface_version=interface_version1,
            power_draw=power_draw1,
            length_mm=length_mm1,
            required_psu_wattage=required_psu_wattage1,output_ports=output_ports1
        )
       

    GPUs=GPU.objects.filter(type="Low")

    return render(request, 'GPU.html',{'GPUS':GPUs,'var':'GPU'})  

def getMediumGPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        type1 = request.POST.get('type')
        interface_version1 = request.POST.get('interface_version')
        power_draw1 = request.POST.get('power_draw')
        length_mm1 = request.POST.get('length_mm')
        required_psu_wattage1 = request.POST.get('required_psu_wattage')
        output_ports1 = request.POST.get('output_ports')
        GPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            type=type1,
            interface_version=interface_version1,
            power_draw=power_draw1,
            length_mm=length_mm1,
            required_psu_wattage=required_psu_wattage1,output_ports=output_ports1
        )
       

    GPUs=GPU.objects.filter(type="Medium")

    return render(request, 'GPU.html',{'GPUS':GPUs,'var':'GPU'})  

def getHighGPU(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        type1 = request.POST.get('type')
        interface_version1 = request.POST.get('interface_version')
        power_draw1 = request.POST.get('power_draw')
        length_mm1 = request.POST.get('length_mm')
        required_psu_wattage1 = request.POST.get('required_psu_wattage')
        output_ports1 = request.POST.get('output_ports')
        GPU.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            type=type1,
            interface_version=interface_version1,
            power_draw=power_draw1,
            length_mm=length_mm1,
            required_psu_wattage=required_psu_wattage1,output_ports=output_ports1
        )
       

    GPUs=GPU.objects.filter(type="High")

    return render(request, 'GPU.html',{'GPUS':GPUs,'var':'GPU'})  


def deleteGPU(request):
    if request.method=="POST":
        idGPU = request.POST.get('iddoctor')
        GPU.objects.get(id=idGPU).delete()
    return redirect('centerappp:getALLGPU')

def EditGPU(request,idGPU):
    GPU1=GPU.objects.get(id=idGPU)
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        interface_version1 = request.POST.get('interface_version')
        power_draw1 = request.POST.get('power_draw')
        length_mm1 = request.POST.get('length_mm')
        required_psu_wattage1 = request.POST.get('required_psu_wattage')
        output_ports1 = request.POST.get('output_ports')
        type1 = request.POST.get('type')
        GPU1.name=name1
        GPU1.price=price1
        GPU1.count=count1
        GPU1.link=link1
        GPU1.interface_version=interface_version1
        GPU1.power_draw=power_draw1
        GPU1.length_mm=length_mm1
        GPU1.required_psu_wattage=required_psu_wattage1
        GPU1.output_ports=output_ports1
        GPU1.type=type1
        GPU1.save()
        return redirect('centerappp:getALLGPU')

    return render(request, 'GPU1.html',{'GPU':GPU1,'var':'GPU'})  
###############################################################################################

def getAllRAM(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        type1 = request.POST.get('type')
        speed1 = request.POST.get('speed')
        capacity1 = request.POST.get('capacity')
        modules1 = request.POST.get('modules')

        RAM.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            type=type1,
            speed=speed1,
            capacity=capacity1,
            modules=modules1,
           
        )
       

    RAMs=RAM.objects.all()

    return render(request, 'RAM.html',{'RAMS':RAMs,'var':'RAM'})  


def deleteRAM(request):
    if request.method=="POST":
        idRAM = request.POST.get('iddoctor')
        RAM.objects.get(id=idRAM).delete()
    return redirect('centerappp:getAllRAM')

def EditRAM(request,idRAM):
    RAM1=RAM.objects.get(id=idRAM)
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        speed1 = request.POST.get('speed')
        capacity1 = request.POST.get('capacity')
        modules1 = request.POST.get('modules')
        type1 = request.POST.get('type')
        RAM1.name=name1
        RAM1.price=price1
        RAM1.count=count1
        RAM1.link=link1


        RAM1.modules=modules1
        RAM1.capacity=capacity1
        RAM1.speed=speed1
        RAM1.type=type1
        RAM1.save()
        return redirect('centerappp:getAllRAM')
    return render(request, 'RAM1.html',{'RAM':RAM1,'var':'RAM'})    
#############################################################################################

def getAllMotherboard(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        socket_type1 = request.POST.get('socket_type')
        chipset1 = request.POST.get('chipset')
        supported_ram_type1 = request.POST.get('supported_ram_type')
        max_ram_speed1 = request.POST.get('max_ram_speed')
        ram_slots1 = request.POST.get('ram_slots')
        pcie_version1 = request.POST.get('pcie_version')
        m2_slots1 = request.POST.get('m2_slots')
        sata_ports1 = request.POST.get('sata_ports')

        Motherboard.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            socket_type=socket_type1,
            chipset=chipset1,
            supported_ram_type=supported_ram_type1,
            max_ram_speed=max_ram_speed1,
            ram_slots=ram_slots1,
            pcie_version=pcie_version1
            ,m2_slots=m2_slots1,
            sata_ports=sata_ports1
           
        )
       

    Motherboards=Motherboard.objects.all()

    return render(request, 'Motherboard.html',{'MotherboardS':Motherboards,'var':'Motherboard'})  


def deleteMotherboard(request):
    if request.method=="POST":
        idMotherboard = request.POST.get('iddoctor')
        Motherboard.objects.get(id=idMotherboard).delete()
    return redirect('centerappp:getAllMotherboard')

def EditMotherboard(request,idMo):
    Motherboard1=Motherboard.objects.get(id=idMo)
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        socket_type1 = request.POST.get('socket_type')
        chipset1 = request.POST.get('chipset')
        supported_ram_type1 = request.POST.get('supported_ram_type')
        max_ram_speed1 = request.POST.get('max_ram_speed')
        ram_slots1 = request.POST.get('ram_slots')
        pcie_version1 = request.POST.get('pcie_version')
        m2_slots1 = request.POST.get('m2_slots')
        sata_ports1 = request.POST.get('sata_ports')
        Motherboard1.name=name1
        Motherboard1.price=price1
        Motherboard1.count=count1
        Motherboard1.link=link1
        Motherboard1.socket_type=socket_type1
        Motherboard1.chipset=chipset1
        Motherboard1.supported_ram_type=supported_ram_type1
        Motherboard1.max_ram_speed=max_ram_speed1
        Motherboard1.ram_slots=ram_slots1
        Motherboard1.pcie_version=pcie_version1
        Motherboard1.m2_slots=m2_slots1
        Motherboard1.sata_ports=sata_ports1

        Motherboard1.save()
        return redirect('centerappp:getAllMotherboard')
    return render(request, 'Motherboard1.html',{'Motherboard':Motherboard1,'var':'Motherboard'})    



from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

MODEL_NAME = "unitary/toxic-bert"
LOCAL_DIR = "./saved_models/toxic_bert"

# # تحميل النموذج والتوكنيزر
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# # حفظ النموذج محليًا
# tokenizer.save_pretrained(LOCAL_DIR)
# model.save_pretrained(LOCAL_DIR)

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

LOCAL_DIR = "./saved_models/toxic_bert"

# تحميل من التخزين المحلي
tokenizer = AutoTokenizer.from_pretrained(LOCAL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(LOCAL_DIR)

# إنشاء التصنيف
toxicity_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def is_toxic(comment, threshold=0.2):
    result = toxicity_classifier(comment)[0]
    label = result["label"]
    score = result["score"]
    print(score)
    print(label)
    if score > threshold:
        return True
    # قد يكون "LABEL_1" هو السام و "LABEL_0" هو الآمن حسب النموذج
    else:
        return False



#############################################################################################################

def getAllHARD(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        type1 = request.POST.get('type')
        capacity1 = request.POST.get('capacity')
        interface_version1 = request.POST.get('interface_version')
        Storage.objects.create(
            name=name1,
            price=price1,
            count=count1,
            link=link1,
            type=type1,
            capacity=capacity1,
            interface_version=interface_version1,

           
        )
       

    HARDS=Storage.objects.all()

    return render(request, 'HARD.html',{'HARDS':HARDS,'var':'HARD'})  


def deleteHARD(request):
    if request.method=="POST":
        idS = request.POST.get('iddoctor')
        Storage.objects.get(id=idS).delete()
    return redirect('centerappp:getAllHARD')

def EditHARD(request,idHARD):
    HARD1=Storage.objects.get(id=idHARD)
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        type1 = request.POST.get('type')
        capacity1 = request.POST.get('capacity')
        interface_version1 = request.POST.get('interface_version')

        HARD1.name=name1
        HARD1.price=price1
        HARD1.count=count1
        HARD1.link=link1
        HARD1.type=type1
        HARD1.capacity=capacity1
        HARD1.interface_version=interface_version1



        HARD1.save()
        return redirect('centerappp:getAllHARD')
    return render(request, 'HARD1.html',{'HARD':HARD1,'var':'HARD'})    

#############################################################################################################

def getAllPS(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        wattage1 = request.POST.get('wattage')
        efficiency_rating1 = request.POST.get('efficiency_rating')
        pcie_connectors1 = request.POST.get('pcie_connectors')
        eps_connector1 = request.POST.get('eps_connector')
        form_factor1 = request.POST.get('form_factor')
        
        PSU.objects.create(
             name=name1,
             price=price1,
             count=count1,
             link=link1,
             wattage=wattage1,
             efficiency_rating=efficiency_rating1,
             pcie_connectors=pcie_connectors1,
             eps_connector=eps_connector1,
             form_factor=form_factor1,
            
            

           
        )
       

    PSUs=PSU.objects.all()

    return render(request, 'PSU.html',{'PSU':PSUs,'var':'PSU'})  


def deletePS(request):
    if request.method=="POST":
        idS = request.POST.get('iddoctor')
        PSU.objects.get(id=idS).delete()
    return redirect('centerappp:getAllPS')

def EditPS(request,idPS):
    PSU1=PSU.objects.get(id=idPS)
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        wattage1 = request.POST.get('wattage')
        efficiency_rating1 = request.POST.get('efficiency_rating')
        pcie_connectors1 = request.POST.get('pcie_connectors')
        eps_connector1 = request.POST.get('eps_connector')
        form_factor1 = request.POST.get('form_factor')
        PSU1.name=name1
        PSU1.price=price1
        PSU1.count=count1
        PSU1.link=link1
        PSU1.wattage=wattage1
        PSU1.efficiency_rating=efficiency_rating1
        PSU1.pcie_connectors=pcie_connectors1
        PSU1.eps_connector=eps_connector1
        PSU1.form_factor=form_factor1



        PSU1.save()
        return redirect('centerappp:getAllPS')
    return render(request, 'PSU1.html',{'PSU':PSU1,'var':'PSU'})    

#############################################################################################################

def getAllCooler(request):
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        supported_sockets1 = request.POST.get('supported_sockets')
        tdp_rating1 = request.POST.get('tdp_rating')
        height1 = request.POST.get('height')
        Cooler.objects.create(
             name=name1,
             price=price1,
             count=count1,
             link=link1,
             supported_sockets=supported_sockets1,
             tdp_rating=tdp_rating1,
             height=height1,
        )
    Coolers=Cooler.objects.all()
    return render(request, 'Cooler.html',{'Cooler':Coolers,'var':'Cooler'})  


def deleteCooler(request):
    if request.method=="POST":
        idS = request.POST.get('iddoctor')
        Cooler.objects.get(id=idS).delete()
    return redirect('centerappp:getAllCooler')

def EditCooler(request,idCo):
    Cooler1=Cooler.objects.get(id=idCo)
    if request.method=="POST":
        name1 = request.POST.get('name')
        price1 = request.POST.get('price')
        count1 = request.POST.get('count')
        link1 = request.POST.get('link')
        supported_sockets1 = request.POST.get('supported_sockets')
        tdp_rating1 = request.POST.get('tdp_rating')
        height1 = request.POST.get('height')
        Cooler1.name=name1
        Cooler1.price=price1
        Cooler1.count=count1
        Cooler1.link=link1
        Cooler1.supported_sockets=supported_sockets1
        Cooler1.tdp_rating=tdp_rating1
        Cooler1.height=height1
        Cooler1.save()
        return redirect('centerappp:getAllCooler')
    return render(request, 'Cooler1.html',{'Cooler':Cooler1,'var':'Cooler'})    

#############################################################################################################


# def getAllRa(request):
#     user1=request.user
#     print(user1)
#     Ra=Rating.objects.all()

#     return render(request, 'RatingA.html',{'Ratings':Ra})  

def getAllFa(request):
    user1=request.user
    print(user1)
  
    Fas=Favorite.objects.all()

    return render(request, 'FavoriteA.html',{'Favorites':Fas,'var':'Favorite'})  

#############################################################################################################

def getAllMonitor(request):
    if request.method=="POST":
        photo1=request.FILES.get('photo') 
        name1 = request.POST.get('name')
        count1 = request.POST.get('count')
        resolution1 = request.POST.get('resolution')
        refresh_rate1 = request.POST.get('refresh_rate')
        panel_type1 = request.POST.get('panel_type')
        input_ports1 = request.POST.get('input_ports')
        Monitor.objects.create(
             photo=photo1,
             name=name1,
             count=count1,
             resolution=resolution1,
             refresh_rate=refresh_rate1,
             panel_type=panel_type1,
             input_ports=input_ports1,
        )
    Monitors=Monitor.objects.all()
    return render(request, 'Monitor.html',{'Monitors':Monitors,'var':'Monitor'})  


def deleteMonitor(request):
    if request.method=="POST":
        idS = request.POST.get('iddoctor')
        Monitor.objects.get(id=idS).delete()
    return redirect('centerappp:getAllMonitor')

def EditMonitor(request,idMo):
    Monitor1=Monitor.objects.get(id=idMo)
    if request.method=="POST":
        photo1=request.FILES.get('photo') 

        name1 = request.POST.get('name')
        count1 = request.POST.get('count')
        resolution1 = request.POST.get('resolution')
        refresh_rate1 = request.POST.get('refresh_rate')
        panel_type1 = request.POST.get('panel_type')
        input_ports1 = request.POST.get('input_ports')
        if photo1:
         Monitor1.photo=photo1
        Monitor1.name=name1
        Monitor1.count=count1
        Monitor1.resolution=resolution1
        Monitor1.refresh_rate=refresh_rate1
        Monitor1.panel_type=panel_type1
        Monitor1.input_ports=input_ports1
        Monitor1.save()
        return redirect('centerappp:getAllMonitor')
    return render(request, 'Monitor1.html',{'Monitor':Monitor1,'var':'Monitor'})    

#############################################################################################################

# def getAllNComputer(request):
#     if request.method=="POST": 
#         name1 = request.POST.get('type')
#         count1 = request.POST.get('CPU')
#         resolution1 = request.POST.get('CPULink')
#         refresh_rate1 = request.POST.get('GPU')
#         panel_type1 = request.POST.get('GPULink')
#         input_ports1 = request.POST.get('Monitor')
#         input_ports1 = request.POST.get('MonitorLink')
#         input_ports1 = request.POST.get('Cooler')
#         input_ports1 = request.POST.get('CoolerLink')
#         input_ports1 = request.POST.get('PSU')
#         input_ports1 = request.POST.get('PSULink')
#         input_ports1 = request.POST.get('Storage')
#         input_ports1 = request.POST.get('StorageLink')
#         input_ports1 = request.POST.get('RAM')
#         input_ports1 = request.POST.get('RAMLink')
#         input_ports1 = request.POST.get('Motherboard')
#         input_ports1 = request.POST.get('MotherboardLink')
#         input_ports1 = request.POST.get('Motherboard')
#         input_ports1 = request.POST.get('Motherboard')
#         input_ports1 = request.POST.get('Motherboard')


#         Monitor.objects.create(
#              photo=photo1,
#              name=name1,
#              count=count1,
#              resolution=resolution1,
#              refresh_rate=refresh_rate1,
#              panel_type=panel_type1,
#              input_ports=input_ports1,
#         )
#     Monitors=Monitor.objects.all()
#     return render(request, 'Monitor.html',{'Monitors':Monitors,'var':'Monitor'})  

from django.shortcuts import render, redirect, get_object_or_404

def getAllNewComputer(request):
    if request.method == "POST":
        # Collect form data
        photo = request.FILES.get('photo')
        name = request.POST.get('name')
        count = request.POST.get('count')
        type_choice = request.POST.get('type')
        CPU = request.POST.get('CPU')
        CPULink = request.POST.get('CPULink')
        GPU = request.POST.get('GPU')
        GPULink = request.POST.get('GPULink')

        Cooler = request.POST.get('Cooler')
        CoolerLink = request.POST.get('CoolerLink')
        PSU = request.POST.get('PSU')
        PSULink = request.POST.get('PSULink')
        Storage = request.POST.get('Storage')
        StorageLink = request.POST.get('StorageLink')
        RAM = request.POST.get('RAM')
        RAMLink = request.POST.get('RAMLink')
        Motherboard = request.POST.get('Motherboard')
        MotherboardLink = request.POST.get('MotherboardLink')
        company = request.POST.get('company')
        price1 = request.POST.get('price')
        
        NewComputer.objects.create(
            photo=photo,
            name=name,
            count=count,
            type=type_choice,
            CPU=CPU,
            CPULink=CPULink,
            GPU=GPU,
            GPULink=GPULink,
   
            Cooler=Cooler,
            CoolerLink=CoolerLink,
            PSU=PSU,
            PSULink=PSULink,
            Storage=Storage,
            StorageLink=StorageLink,
            RAM=RAM,
            RAMLink=RAMLink,
            Motherboard=Motherboard,
            MotherboardLink=MotherboardLink,
            company=company,
            price=price1
        )
        for i in Favorite.objects.all():
           now = datetime.now()
           print(i.HisUser2)
           message_data = {
                'sender':str(request.tenant.name),
                'receiver': str(i.HisUser2),
                'message': f'{request.tenant.name} Add new Computer.',
                'time': now.strftime("%Y-%m-%d %H:%M:%S"),  # This will set the current server timestamp
                'read': False
            }
            
            # # Send the message to Firebase Realtime Database
           db.child("messages").push(message_data)  # Store the message in the 'messages' node
           print("ok1")

    laptop_ids = Laptop.objects.values_list('id', flat=True)
    computers = NewComputer.objects.exclude(id__in=laptop_ids)
    return render(request, 'NewComputer.html', {'computers': computers, 'var': 'NewComputer'})

def deleteNewComputer(request):
    if request.method == "POST":
        idS = request.POST.get('iddoctor')
        print(idS)
        n=NewComputer.objects.get(id=idS).delete()
        print(n)
       
    return redirect('centerappp:getAllNewComputer')

def EditNewComputer(request, idNc):
    new_pc = NewComputer.objects.get(id=idNc)

    if request.method == "POST":
        photo = request.FILES.get('photo')
        name = request.POST.get('name')
        count = request.POST.get('count')
        type1 = request.POST.get('type')
        CPU = request.POST.get('CPU')
        CPULink = request.POST.get('CPULink')
        GPU = request.POST.get('GPU')
        GPULink = request.POST.get('GPULink')
        Monitor = request.POST.get('Monitor')
        MonitorLink = request.POST.get('MonitorLink')
        Cooler = request.POST.get('Cooler')
        CoolerLink = request.POST.get('CoolerLink')
        PSU = request.POST.get('PSU')
        PSULink = request.POST.get('PSULink')
        Storage = request.POST.get('Storage')
        StorageLink = request.POST.get('StorageLink')
        RAM = request.POST.get('RAM')
        RAMLink = request.POST.get('RAMLink')
        Motherboard = request.POST.get('Motherboard')
        MotherboardLink = request.POST.get('MotherboardLink')
        company = request.POST.get('company')
        price1 = request.POST.get('price')

        if photo:
            new_pc.photo = photo

        new_pc.name = name
        new_pc.price=price1
        new_pc.count = count
        new_pc.type = type1
        new_pc.CPU = CPU
        new_pc.CPULink = CPULink
        new_pc.GPU = GPU
        new_pc.GPULink = GPULink
        new_pc.Monitor = Monitor
        new_pc.MonitorLink = MonitorLink
        new_pc.Cooler = Cooler
        new_pc.CoolerLink = CoolerLink
        new_pc.PSU = PSU
        new_pc.PSULink = PSULink
        new_pc.Storage = Storage
        new_pc.StorageLink = StorageLink
        new_pc.RAM = RAM
        new_pc.RAMLink = RAMLink
        new_pc.Motherboard = Motherboard
        new_pc.MotherboardLink = MotherboardLink
        new_pc.company = company

        new_pc.save()
        return redirect('centerappp:getAllNewComputer')

    return render(request, 'edit_new_computer.html', {'new_pc': new_pc, 'var': 'NewComputer'})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Laptop
def getAllLaptop(request):
    if request.method == "POST":
        Laptop.objects.create(
            photo=request.FILES.get('photo'),
            name=request.POST.get('name'),
            count=request.POST.get('count'),
            CPU=request.POST.get('CPU'),
            GPU=request.POST.get('GPU'),
            RAM=request.POST.get('RAM'),
            price=request.POST.get('price'),
            Storage=request.POST.get('Storage'),
            PSU=request.POST.get('PSU'),
            Cooler=request.POST.get('Cooler'),
            Motherboard=request.POST.get('Motherboard'),
            CPULink=request.POST.get('CPULink'),
            GPULink=request.POST.get('GPULink'),
            RAMLink=request.POST.get('RAMLink'),
           
            StorageLink=request.POST.get('StorageLink'),
            PSULink=request.POST.get('PSULink'),
            CoolerLink=request.POST.get('CoolerLink'),
            MotherboardLink=request.POST.get('MotherboardLink'),
            company=request.POST.get('company'),
            type=request.POST.get('type'),
            Battary=request.POST.get('Battary'),
            screen=request.POST.get('screen'),
        )
    laptops = Laptop.objects.all()
    return render(request, 'Laptop.html', {'Laptops': laptops})

def deleteLaptop(request):
    if request.method == "POST":
        idL = request.POST.get('iddoctor')
        Laptop.objects.get(id=idL).delete()
    return redirect('centerappp:getAllLaptops')


def editLaptop(request, id):
    laptop = get_object_or_404(Laptop, id=id)
    if request.method == "POST":
        photo = request.FILES.get('photo')
        if photo:
            laptop.photo = photo
        laptop.name = request.POST.get('name')
        laptop.count = request.POST.get('count')
        laptop.type = request.POST.get('type')
        laptop.CPU = request.POST.get('CPU')
        laptop.CPULink = request.POST.get('CPULink')
        laptop.GPU = request.POST.get('GPU')
        laptop.GPULink = request.POST.get('GPULink')
        laptop.Monitor = request.POST.get('Monitor')
        laptop.MonitorLink = request.POST.get('MonitorLink')
        laptop.Cooler = request.POST.get('Cooler')
        laptop.CoolerLink = request.POST.get('CoolerLink')
        laptop.PSU = request.POST.get('PSU')
        laptop.PSULink = request.POST.get('PSULink')
        laptop.Storage = request.POST.get('Storage')
        laptop.StorageLink = request.POST.get('StorageLink')
        laptop.RAM = request.POST.get('RAM')
        laptop.RAMLink = request.POST.get('RAMLink')
        laptop.Motherboard = request.POST.get('Motherboard')
        laptop.MotherboardLink = request.POST.get('MotherboardLink')
        laptop.company = request.POST.get('company')
        laptop.Battary = request.POST.get('Battary')
        laptop.screen = request.POST.get('screen')

        laptop.save()
        return redirect('centerappp:getAllLaptops')
    return render(request, 'EditLaptop.html', {'laptop': laptop})



def getAllProdects(request):
    if request.method == "POST":
        name = request.POST.get('name')
        count = request.POST.get('count')
        photo = request.FILES.get('photo')
        Des1 = request.POST.get('Des')
        onlyProdect.objects.create(name=name, count=count, photo=photo,Des=Des1)

    prodects = onlyProdect.objects.all()
    return render(request, 'prodects.html', {'prodects': prodects})


def deleteProdect(request):
    if request.method == "POST":
        idP = request.POST.get('iddoctor')
        onlyProdect.objects.get(id=idP).delete()
    return redirect('centerappp:getAllProdects')

def editProdect(request, idP):
    item = onlyProdect.objects.get(id=idP)
    if request.method == "POST":
        item.name = request.POST.get('name')
        item.Des = request.POST.get('Des')
        item.count = request.POST.get('count')
        if request.FILES.get('photo'):
            item.photo = request.FILES.get('photo')
        item.save()
        return redirect('centerappp:getAllProdect')
    return render(request, 'editProdect.html', {'prodect': item})

def get_product_type(product):
          if hasattr(product, 'monitor'):
             return 'Monitor'
          elif hasattr(product, 'buildcomputer'):
             return 'BuildComputer'
          elif hasattr(product, 'newcomputer'):
             return 'NewComputer'
          elif hasattr(product, 'laptop'):
             return 'Laptop'
          elif hasattr(product, 'onlyprodect'):
             return 'OnlyProdect'
          else:
             return 'Unknown'

def getAllCarts(request):
    carts = cart.objects.all()
    return render(request, 'cart.html', {'carts': carts, 'var': 'Cart'})

def getBC(request):
    BC = BuildComputer.objects.all()
    return render(request, 'BC.html', {'BC': BC, 'var': 'BC'})

def deleteBC(request):
    if request.method=="POST":
        idCPU = request.POST.get('iddoctor')
        BuildComputer.objects.get(id=idCPU).delete()
    return redirect('centerappp:getBC')

def getUserCarts(request,iduser):
    carts = cart.objects.filter(user=iduser)
    return render(request, 'cart.html', {'carts': carts, 'var': 'Cart'})


def cartDetails(request, cart_id):
    try:



        selected_cart = cart.objects.get(id=cart_id)
        items = item.objects.filter(Cart=selected_cart)
        if request.method =="POST":
            state = request.POST.get('state')
            selected_cart.State=state
            selected_cart.save()
        for i in items:
            i.HisType=get_product_type(i.his_prodect)
    except cart.DoesNotExist:
        return HttpResponse("Cart not found", status=404)
    
    return render(request, 'cart_details.html', {
        'cart': selected_cart,
        'items': items
    })
from app.models import paymentMonth
def getAllPaymentMonth(request):
    if request.method == "POST":
        photo = request.FILES.get('photo')
        amount = request.POST.get('Amount')
        date = request.POST.get('Date')
        paymentMonth.objects.create(photo=photo, Amount=amount, Date=date,tenant=request.tenant)

    payments = paymentMonth.objects.filter(tenant=request.tenant)
    return render(request, 'paymentMonth.html', {'payments': payments, 'var': 'paymentMonth'})

def deletePaymentMonth(request):
    if request.method == "POST":
        id_payment = request.POST.get('iddoctor')
        paymentMonth.objects.filter(id=id_payment).delete()
    return redirect('centerappp:getAllPaymentMonth')
from django.contrib.auth import logout

def logout_view(request):

    logout(request)
    #  Option 1: Redirect to the login page:
    return redirect('centerappp:tenant_login') 

def getuserloction(request,iduser):
    user1=User.objects.get(id=iduser).person
    return render(request,'map.html',{'latitude':user1.x,'longitude':user1.y})
