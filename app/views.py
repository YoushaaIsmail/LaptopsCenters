from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("<h1>ljljlj</h1>")


from django.http import HttpResponse
from django_tenants.utils import schema_context
from centerappp.models import *
from app.models import center
import logging

logger = logging.getLogger(__name__)

def showallprodect(request):
    all_products_list = []

    # Get all tenants
    tenants = center.objects.exclude(schema_name='public') 
    print(tenants)
    for tenant in tenants:
        try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                products = prodect.objects.all()  # Fetch products for the current tenant
                print(products)
                all_products_list.extend(products)  # Add products to the list
        except Exception as e:
            logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            return HttpResponse("An error occurred while accessing products.")

    return HttpResponse(f"{[product.name for product in all_products_list]}")

def home(request):
    all_products_list = []

    # Get all tenants
    tenants = center.objects.exclude(schema_name='public') 
    print(tenants)
    for tenant in tenants:
        try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                products = prodect.objects.all()  # Fetch products for the current tenant
                print(products)
                all_products_list.extend(products)  # Add products to the list
        except Exception as e:
            logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            return HttpResponse("An error occurred while accessing products.")

    return HttpResponse(f"{[product.name for product in all_products_list]}")



def test(request):
             # Get all tenants
    allCenter=[]
    # Get all tenants
    tenants = center.objects.exclude(schema_name='public') 
    print(tenants)
    for tenant in tenants:
        try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                abouts1 = about.objects.first()  # Fetch products for the current tenant
                idtenant1=tenant.id
                countRat1=Rating.objects.count()
                countFa1=Favorite.objects.count()
              
                Center={
                     'abouts1':abouts1,
                     'idtenant1':idtenant1,
                     'countRat1':countRat1,
                     'countFa1':countFa1,
                  

                }
                allCenter.append(Center)
                print(allCenter)
                     
                
                  # Add products to the list
            
        except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
            return render(request, 'test.html',{'message':'you have a problem'})  
    return render(request, 'test.html',{'allCenter':allCenter}) 

def searchname(request):
             # Get all tenants
    allCenter=[]
    # Get all tenants
    if request.method == 'POST':
        name1=request.POST.get('name')

    tenants = center.objects.exclude(schema_name='public') 
    print(tenants)
    for tenant in tenants:
        try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                
               abouts1 = about.objects.first()  # Fetch products for the current tenant

               if abouts1.name ==name1 :
                idtenant1=tenant.id
                countRat1=Rating.objects.count()
                countFa1=Favorite.objects.count()
              
                Center={
                     'abouts1':abouts1,
                     'idtenant1':idtenant1,
                     'countRat1':countRat1,
                     'countFa1':countFa1,
                  

                }
                allCenter.append(Center)
                print(allCenter)
                     
                
                  # Add products to the list
            
        except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
            return render(request, 'test.html',{'message':'you have a problem'})  
    return render(request, 'test.html',{'allCenter':allCenter}) 
from django.db.models import Count, Avg
def filtertenant(request):
             # Get all tenants
    allCenter=[]
    # Get all tenants
    if request.method == 'POST':
        filter_type = request.POST.get('service')

    tenants = center.objects.exclude(schema_name='public') 
    print(tenants)
    for tenant in tenants:
            try:
                    with schema_context(tenant.schema_name):
                        abouts1 = about.objects.first()
                        idtenant1 = tenant.id
                        # Get Rating and Favorite counts
                        countRat1 = Rating.objects.count()
                        countFa1 = Favorite.objects.count()

                        # Optionally, you can calculate average rating here
                        avgStar = Rating.objects.aggregate(avg=Avg('Star'))['avg'] or 0

                        Center = {
                            'abouts1': abouts1,
                            'idtenant1': idtenant1,
                            'countRat1': countRat1,
                            'countFa1': countFa1,
                            'avgStar': avgStar,
                        }

                        allCenter.append(Center)

            except Exception as e:
                    return render(request, 'test.html', {'message': 'You have a problem'})

            # Apply filter based on filter_type
            if filter_type == 'MostRating':
                allCenter = sorted(allCenter, key=lambda x: x['countRat1'], reverse=True)
            elif filter_type == 'MostAdd':
                allCenter = sorted(allCenter, key=lambda x: x['countFa1'], reverse=True)
            elif filter_type == 'Last':
                allCenter = sorted(allCenter, key=lambda x: x['idtenant1'], reverse=True)

    return render(request, 'test.html', {'allCenter': allCenter})


def search_product_element(request):
    results = []

    if request.method == 'POST':
        search_product = request.POST.get('search_product_name')
        search_element = request.POST.get('search_element_name')

        tenants = center.objects.exclude(schema_name='public') 
        print(tenants)
        for tenant in tenants:
      
                try:
                    with schema_context(tenant.schema_name):
                        # Get tenant info
                        tenant_name = about.objects.first().name
                        tenant_photo = about.objects.first().photo.url 
                        tenant_Des = about.objects.first().Des
                        print('11')

                        # Search in prodect
                        if search_product:
                            products = prodect.objects.filter(name__icontains=search_product)
                            print(1)
                            print(products)
                            for product in products:
                                results.append({
                                    'type': 'Product',
                                    'name': product.name,
                                    'price': product.price,
                                    'count': product.count,
                                    'photo': product.photo.url if product.photo else '',
                                    'tenant_name': tenant_name,
                                    'tenant_photo': tenant_photo,
                                    'tenant_Des': tenant_Des,
                                })

                        # Search in element
                        if search_element:
                            elements = element.objects.filter(name__icontains=search_element)
                            print(elements)
                            for el in elements:
                                results.append({
                                    'type': 'Element',
                                    'name': el.name,
                                    'price': el.price,
                                    'count': el.count,
                                    'link': el.link,
                                    'tenant_name': tenant_name,
                                    'tenant_photo': tenant_photo,
                                    'tenant_Des': tenant_Des,
                                })

                except Exception as e:
                    return render(request, 'search_resultsp.html', {'message': 'There was a problem accessing data.'})

        return render(request, 'search_resultsp.html', {'results': results, 'search_product': search_product, 'search_element': search_element})

    return render(request, 'searchp.html', {})



def select_cpu(request):
             # Get all tenants
    allCenter=[]
    # Get all tenants
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)


    try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):

                
                if request.method == 'POST':
                   cpu_id = request.POST.get('cpu')
                   request.session['cpu_id'] = cpu_id
                   return redirect('select_gpu')
    
                cpus = CPU.objects.all()
                return render(request, 'select_cpu.html', {'cpus': cpus})
    except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
               return render(request, 'test.html',{'message':'you have a problem'})  

    
def select_gpu(request):
             # Get all tenants
    allCenter=[]
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)


    try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                
               if 'cpu_id' not in request.session:
                   return redirect('select_cpu')

               if request.method == 'POST':
                  gpu_id = request.POST.get('gpu')
                  request.session['gpu_id'] = gpu_id
                  return redirect('select_motherboard')

               gpus = GPU.objects.all()  # أو قم بتصفية حسب الـ CPU لو أردت
               return render(request, 'select_gpu.html', {'gpus': gpus})
    except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
               return render(request, 'test.html',{'message':'you have a problem'})  



    
    return render(request, 'test.html',{'allcenter':allCenter})   


    
def select_motherboard(request):
             # Get all tenants
    allCenter=[]
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)


    try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
               cpu_id = request.session.get('cpu_id')
               gpu_id = request.session.get('gpu_id')

               if not cpu_id or not gpu_id:
                 return redirect('select_cpu')  # الرجوع لاختيار CPU في حالة عدم وجود المعرفات

               cpu = get_object_or_404(CPU, pk=cpu_id)
               gpu = get_object_or_404(GPU, pk=gpu_id)

    # فلترة الماذربورد حسب التوافق مع CPU و GPU
               motherboards = Motherboard.objects.filter(
        socket_type=cpu.socket_type,
        # chipset__in=cpu.chipset,  # نفترض أن CPU.chipset هي قائمة (JSONField)
        pcie_version__gte=gpu.interface_version,
        supported_ram_type=cpu.supported_ram_type

    )
               print(cpu)
               print(gpu)
               print(motherboards)
               motherboards = [mb for mb in motherboards if mb.chipset in cpu.chipset]
               if request.method == 'POST':
                     motherboard_id = request.POST.get('motherboard')
                     request.session['motherboard_id'] = motherboard_id
                     return redirect('select_ram')  # أي صفحة تريدها بعد اختيار اللوحة

               return render(request, 'select_motherboard.html', {'motherboards': motherboards})

    except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
               return render(request, 'test.html',{'message':'you have a problem'})  

def select_ram(request):
    allCenter = []
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)
    try:
        with schema_context(tenant.schema_name):
            motherboard_id = request.session.get('motherboard_id')
            if not motherboard_id:
                return redirect('select_motherboard')

            motherboard = get_object_or_404(Motherboard, pk=motherboard_id)

            # فلترة الرامات المتوافقة
            compatible_rams = RAM.objects.filter(
                type=motherboard.supported_ram_type,
                speed__lte=motherboard.max_ram_speed,
                count__gt=0
            )

            rams = []
            for ram in compatible_rams:
                
                max_quantity = min(ram.count, (motherboard.ram_slots))
                rams.append({
                    'object': ram,
                    'max_quantity': max_quantity
                })

            if request.method == 'POST':
                selected_ram_id = request.POST.get('ram')
                selected_ram = get_object_or_404(RAM, pk=selected_ram_id)

                quantity = int(request.POST.get(f'ram_qty_{selected_ram_id}'))
                
                if quantity < 1 or quantity > min(selected_ram.count, motherboard.ram_slots):
                    return render(request, 'select_ram.html', {
                        'rams': rams,
                        'ram_slots': motherboard.ram_slots,
                        'error_message': 'Quantity exceeds allowed limits!'
                    })

                # احفظ الرام والكمية في السيشن
                request.session['ram_id'] = selected_ram_id
                request.session['ram_quantity'] = quantity

                return redirect('select_storage')

            return render(request, 'select_ram.html', {'rams': rams, 'ram_slots': motherboard.ram_slots})

    except Exception as e:
        return render(request, 'test.html', {'message': 'You have a problem'})


def select_storage(request):
             # Get all tenants
    allCenter=[]
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)

    try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                
                motherboard_id = request.session.get('motherboard_id')
                if not motherboard_id:
                    return redirect('select_motherboard')

                motherboard = get_object_or_404(Motherboard, pk=motherboard_id)

    # تصفية وحدات التخزين حسب المنافذ المتاحة على اللوحة الأم
                storage_options = Storage.objects.filter(
                type__in=[
            t for t in ['M.2 NVMe', 'SATA']
            if (t == 'M.2 NVMe' and motherboard.m2_slots > 0) or
               (t == 'SATA' and motherboard.sata_ports > 0)
        ]
    )

                if request.method == 'POST':
                  storage_id = request.POST.get('storage')
                  request.session['storage_id'] = storage_id
                  return redirect('select_psu')  # مثل select_psu أو select_monitor

                return render(request, 'select_storage.html', {'storages': storage_options})
    except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
               return render(request, 'test.html',{'message':'you have a problem'})  

def select_psu(request):
             # Get all tenants
    allCenter=[]
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)


    try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                 

               cpu_id = request.session.get('cpu_id')
               gpu_id = request.session.get('gpu_id')
               if not cpu_id or not gpu_id:
                  return redirect('select_cpu')

               cpu = get_object_or_404(CPU, pk=cpu_id)
               gpu = get_object_or_404(GPU, pk=gpu_id)

    # نحسب الحد الأدنى للطاقة المطلوبة
               min_wattage = cpu.tdp + gpu.power_draw + 100  # نضيف 100 كاحتياط

    # تصفية مزودات الطاقة التي تفي بالحد الأدنى
               psus = PSU.objects.filter(wattage__gte=min_wattage)

               if request.method == 'POST':
                 psu_id = request.POST.get('psu')
                 request.session['psu_id'] = psu_id
                 return redirect('select_cooler')  # الخطوة التالية

               return render(request, 'select_psu.html', {'psus': psus, 'min_wattage': min_wattage})
    except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
               return render(request, 'test.html',{'message':'you have a problem'})  


def select_cooler(request):
             # Get all tenants
    allCenter=[]
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)


    try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                    cpu_id = request.session.get('cpu_id')

                    if not cpu_id:
                       return redirect('select_cpu')

                    cpu = get_object_or_404(CPU, pk=cpu_id)

    # فلترة المبردات المتوافقة مع المعالج
                    coolers = Cooler.objects.filter(
        supported_sockets__contains=[cpu.socket_type],  # JSONField يحتوي على المقبس
        tdp_rating__gte=cpu.tdp  # يجب أن يكون قادراً على تحمل حرارة المعالج
    )

                    if request.method == 'POST':
                        cooler_id = request.POST.get('cooler')
                        request.session['cooler_id'] = cooler_id
                        return redirect('build_summary')  # الخطوة التالية التي تحددها

                    return render(request, 'select_cooler.html', {'coolers': coolers})

    except Exception as e:
            # logger.error(f"Error accessing tenant {tenant.schema_name}: {str(e)}")
            # return HttpResponse("An error occurred while accessing products.")
               return render(request, 'test.html',{'message':'you have a problem'})  


from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import person  # تأكد من أن المسار صحيح حسب تطبيقك

def loginuser(request):
    context = {}

    if request.method == "POST":
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')

        user1 = authenticate(request, username=username1, password=password1)
        print(user1)

        if user1:
            try:
                per = person.objects.get(user=user1)
                if per.is_verified:
                    login(request, user1)
                    return redirect('test')
                else:
                    context['error'] = "الحساب لم يتم التحقق منه بعد."
            except person.DoesNotExist:
                context['error'] = "لم يتم العثور على معلومات المستخدم."
        else:
            context['error'] = "اسم المستخدم أو كلمة المرور غير صحيحة."

    return render(request, 'loginuser.html', context)

from django.contrib import messages
from datetime import datetime, timedelta, time
from django.utils import timezone
from .emails import *
from django.contrib.auth.hashers import check_password, make_password
from .models import *

def otp_view(request):
    if request.method=="POST":
        iduser=request.POST['iduser']
        code=request.POST['code']
        user12=User.objects.get(id=iduser)
        user1=person.objects.get(user=user12)

        if user1.otp==code:
           user1.is_verified=True
           user1.save()
           return redirect('loginuser') 
        else:
            return render(request, 'OTP.html',{'iduser':iduser})
def registeruser(request):
    if request.method=="POST":

       first_name1=request.POST['firstname']
       last_name1=request.POST['lastname']
       password1=request.POST['password']
       Cpassword1=request.POST['Confirmpassword']
       email1=request.POST['email']
       Address1=request.POST['Address']
       Job1=request.POST['Work']
       Phone1=request.POST['phone']         
       UserName1=request.POST['username']   
       Birthday1=request.POST['Birthdate']    
       im=request.FILES.get('img')  
        
       X=request.POST['loction_x']   
       Y=request.POST['loction_y']                   
       if im:
           im1=im   
             
       search_date = timezone.datetime.strptime(Birthday1, "%Y-%m-%d")  # Adjust format as needed
                
       print(password1)
       print(Cpassword1)
        # Check if new passwords match
       if Cpassword1 != password1:
            print('11')
            messages.error(request, "New passwords do not match.")
            return redirect('register_show')
       
       paa=make_password(password1)
       u1=User.objects.create(username=UserName1,password=paa,email=email1,first_name=first_name1,last_name=last_name1)   
       person.objects.create(user=u1,phone=Phone1
                             ,work=Job1,BirthDate=search_date,photo=im1,Address=Address1,x=X,y=Y) 
       send_otp_via_email(email1)
       return render(request, 'OTP.html',{'iduser':u1.id})

    return render(request, 'registeruser.html')  


def showcenter(request):

    return render(request, 'centershow.html')  


from django.http import JsonResponse
from transformers import pipeline

model_save_path = "saved_models/sentiment_model"
sentiment_pipeline = pipeline("sentiment-analysis", model=model_save_path, tokenizer=model_save_path)

#         if request.method=="POST":

#            parent=request.user.id
#            puser=User.objects.get(id=parent)
#            commentNew = request.POST['commentNew']
#            if commentNew :
#                typeC = sentiment_pipeline(commentNew)[0]
#                print(typeC['label'])
         
#            current_date = datetime.now().date()
#            Comment.objects.create(HisParent=puser,Date=current_date,type=typeC['label'],Des=commentNew)
#            return redirect('Studentapp:homeparent')
#         return render(request,'Addcomment.html')
from django.contrib.auth.models import User
from django.shortcuts import render
from django_tenants.utils import schema_context


def showRating(request, idt):
    tenant = center.objects.get(id=idt)
    user1=request.user

    try:
        with schema_context(tenant.schema_name):
            if request.method=="POST":
                 stars = request.POST.get('stars')
                 ReviewC = request.POST.get('ReviewC')
                 typeC = sentiment_pipeline(ReviewC)[0]
                 Rating.objects.create(HisUser2=user1,text=ReviewC,Star=stars,Type=typeC['label'])
            toStar=0 
            ratings = Rating.objects.select_related('HisUser2').order_by('-Date')  # ترتيب الأحدث أولاً
            for i in ratings:
                 toStar +=i.Star
            Rcou=Rating.objects.count()

            sco=toStar/5      
            return render(request, 'showRating.html', {
                'ratings': ratings,
                'sco': sco,
                'tenant': tenant,
                'Rcou':Rcou
            })
             
    
    except Exception as e:
        return render(request, 'test.html', {'message': 'You have a problem'})


def showFav(request, idt):
    tenant = center.objects.get(id=idt)
    user1=request.user

    try:
        with schema_context(tenant.schema_name):
            Allfav = Favorite.objects.select_related('HisUser2').order_by('-Date')
            test=False
            for i in Allfav:
                      if i.HisUser2==user1:
                           testFa=i
                           test=True
            if request.method=="POST":

                 if test:
                      testFa.delete()
                 else:
                      Favorite.objects.create(HisUser2=user1)            
                 return redirect('test')

            fcou=Rating.objects.count()
      
            return render(request, 'showFav.html', {
                'Allfav': Allfav,
                
                'tenant': tenant,
                'fcou':fcou,'test':test
            })
             
    
    except Exception as e:
        return render(request, 'test.html', {'message': 'You have a problem'})

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required(login_url='loginuser')
def my_profile(request):
    user = request.user
    try:
        person_instance = person.objects.get(user=user)
    except person.DoesNotExist:
        return render(request, 'error.html', {'message': 'لم يتم العثور على ملفك الشخصي.'})

    if request.method == 'POST' and 'work' in request.POST:
        # تعديل معلومات الملف الشخصي
        person_instance.work = request.POST.get('work')
        person_instance.phone = request.POST.get('phone')
        person_instance.BirthDate = request.POST.get('BirthDate')
        person_instance.Address = request.POST.get('Address')
        person_instance.x = request.POST.get('x')
        person_instance.y = request.POST.get('y')
        if 'photo' in request.FILES:
            person_instance.photo = request.FILES['photo']
        person_instance.save()
        return redirect('my_profile')

    return render(request, 'my_profile.html', {'person': person_instance})

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # لتفادي تسجيل الخروج بعد تغيير كلمة السر
            return redirect('my_profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

def showcenterNewPc(request,idc):
    request.session['cen_id'] = idc
    tenant = center.objects.get(id=idc)    
    try:
        with schema_context(tenant.schema_name):
            about1=about.objects.all().first()
            laptop_ids = Laptop.objects.values_list('id', flat=True)
            NewComputers = NewComputer.objects.exclude(id__in=laptop_ids)
            countRat1=Rating.objects.count()
            countFa1=Favorite.objects.count()
      
            return render(request, 'centershow.html', {
                'about':about1,
                'NewCom':NewComputers,
                'countRat1':countRat1,
                'countFa1':countFa1,
                
                'tenant': tenant,
                
            })
             
    
    except Exception as e:
        return render(request, 'test.html', {'message': 'You have a problem'})

def showcenterLaptop(request):
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)    
    try:
        with schema_context(tenant.schema_name):
            about1=about.objects.all().first()
            laptops=Laptop.objects.all()
            countRat1=Rating.objects.count()
            countFa1=Favorite.objects.count()      
            return render(request, 'centershowL.html', {
                'about':about1,
                'laptops':laptops,
                'countRat1':countRat1,
                'countFa1':countFa1,
                
                'tenant': tenant,
                
            })
             
    
    except Exception as e:
        return render(request, 'test.html', {'message': 'You have a problem'})

def showcenterNPC(request):
    idc = request.session.get('cen_id')
    tenant = center.objects.get(id=idc)

    try:
        with schema_context(tenant.schema_name):
            about1 = about.objects.all().first()
            laptop_ids = Laptop.objects.values_list('id', flat=True)
            NewComputers = NewComputer.objects.exclude(id__in=laptop_ids)
            countRat1=Rating.objects.count()
            countFa1=Favorite.objects.count()
            return render(request, 'centershowN.html', {
                'about': about1,
                'NewComputers': NewComputers,
                'countRat1':countRat1,
                'countFa1':countFa1,
                'tenant': tenant,
            })

    except Exception as e:
        return render(request, 'test.html', {'message': 'You have a problem'})

def showcenterBC(request):
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)    
    try:
        with schema_context(tenant.schema_name):
            about1=about.objects.all().first()
            BComputers=BuildComputer.objects.all()
            countRat1=Rating.objects.count()
            countFa1=Favorite.objects.count()      
            return render(request, 'centershowB.html', {
                'about':about1,
                'NewComputers':BComputers,
                'countRat1':countRat1,
                'countFa1':countFa1,
                
                'tenant': tenant,
                
            })
             
    
    except Exception as e:
        print(e)
        return render(request, 'test.html', {'message': 'You have a problem'})



from django.contrib.contenttypes.models import ContentType    

def showcenterProdect(request):
    idc = request.session.get('cen_id')
    tenant = center.objects.get(id=idc)    
    try:
        with schema_context(tenant.schema_name):
           about1 = about.objects.all().first()
           all_products = onlyProdect.objects.all()
           countRat1=Rating.objects.count()
           countFa1=Favorite.objects.count()

           return render(request, 'centershowP.html', {
                'about': about1,
                'prodects1': all_products,
                'tenant': tenant,
                'countRat1':countRat1,
                'countFa1':countFa1,
            })
    except Exception as e:
        print(e)
        return render(request, 'test.html', {'message': 'You have a problem'})


def new_computer_detail(request, id):
    idc = request.session.get('cen_id')
    tenant = center.objects.get(id=idc)
    
    try:
        with schema_context(tenant.schema_name):
            computer = get_object_or_404(NewComputer, id=id)
            if request.method=="POST":
                his_prodect1=computer
                count1= int(request.POST.get('count'))
                cart1=cart.objects.filter(user=request.user,photo='').last()
                print(cart.objects.filter(user=request.user).last().photo)
                if cart1:
                     i1=item.objects.create(his_prodect=his_prodect1,count=count1,Cart=cart1)
                     
                else:    
                     cart1=cart.objects.create(user=request.user,Amount=0,photo='',State="pending") 
                     i1=item.objects.create(his_prodect=his_prodect1,count=count1,Cart=cart1)
                     cart1.Amount=0
                cart1.save()     
                cart1.Amount =cart1.Amount + i1.his_prodect.price * i1.count  
                cart1.save()
                computer.count =computer.count -count1
                computer.save()
                messages.success(request, "ِAdded to your cart Seccusfully .")
                return redirect('showcenterNPC')

            
            return render(request, 'newcomputer_detail.html', {
                'computer': computer,
                'tenant': tenant
            })
    except Exception as e:
        print(e)
        return render(request, 'test.html', {'message': str(e)})          

def forgetpass(request):
    if request.method=="POST":
       email1=request.POST['email'] 
       u1=User.objects.filter(email=email1).first()
       print(u1)
       if u1:
         send_otp_via_email(email1)
         return render(request, 'otp1.html',{'iduser':u1.id})

    return render(request, 'forgetpass.html')

def show_otp1(request):
    if request.method=="POST":
        iduser=request.POST['iduser']
        code=request.POST['code']
        user1=User.objects.get(id=iduser)
        if user1.otp==code:
           return render(request, 'resetpassword.html',{'iduser':user1.id})

        else:
            return render(request, 'otp.html',{'iduser':iduser})
        
def resetpassword(request):
    if request.method=="POST":
        iduser=request.POST['iduser']
        password1=request.POST['password']
        Cpassword1=request.POST['Cpassword']
        paa=make_password(password1)
        if Cpassword1 != password1:
            print('11')
        user1=User.objects.get(id=iduser)
        user1.set_password(password1)
        user1.save()
        messages.success(request, "Password is reseted")  
        return redirect("loginuser")
from django.contrib.auth import logout
def logout_view(request):

    logout(request)
    #  Option 1: Redirect to the login page:
    return redirect('loginuser') 

def P_computer_detail(request, id):
    idc = request.session.get('cen_id')
    tenant = center.objects.get(id=idc)
    
    try:
        with schema_context(tenant.schema_name):
            computer = get_object_or_404(onlyProdect, id=id)
            if request.method=="POST":
                his_prodect1=computer
                count1= int(request.POST.get('count'))
                cart1=cart.objects.filter(user=request.user,photo='').last()
                if cart1:
                     i1=item.objects.create(his_prodect=his_prodect1,count=count1,Cart=cart1)
                     
                     
                else:    
                     cart1=cart.objects.create(user=request.user,Amount=0,State="pending") 
                     i1=item.objects.create(his_prodect=his_prodect1,count=count1,Cart=cart1)
                     cart1.Amount=0
                  
                cart1.Amount =cart1.Amount + i1.his_prodect.price * i1.count  
                cart1.save()
                computer.count =computer.count -count1
                computer.save()
                messages.success(request, "ِAdded to your cart Seccusfully.")
                return redirect('showcenterNPC')


            
            return render(request, 'P_detail.html', {
                'computer': computer,
                'tenant': tenant
            })
    except Exception as e:
        print(e)
        return render(request, 'test.html', {'message': str(e)})          


def B_computer_detail(request, id):
    idc = request.session.get('cen_id')
    tenant = center.objects.get(id=idc)
    
    try:
        with schema_context(tenant.schema_name):
            computer = get_object_or_404(BuildComputer, id=id)
            min_cou=computer.CPU.count
            if computer.GPU.count <=min_cou:
                  min_cou=computer.GPU.count
            if computer.Motherboard.count <= min_cou:
                  min_cou=computer.Motherboard.count
            if  computer.Storage.count <= min_cou:
                  min_cou=computer.Storage.count       
            if  computer.PSU.count<= min_cou:
                 min_cou=computer.PSU.count  
            if  computer.Cooler.count <= min_cou:
                 min_cou=computer.Cooler.count 
                               
            ram_possible_count = computer.RAM.count // computer.countRam
            if ram_possible_count <= min_cou:
                   min_cou = ram_possible_count
            print(min_cou)        
        
            computer.count=min_cou
            computer.save()
            if request.method=="POST":
                count1= int(request.POST.get('count'))
                his_prodect1=computer
                
                cart1=cart.objects.filter(user=request.user,photo='').last()
                if cart1:
                     i1=item.objects.create(his_prodect=his_prodect1,count=count1,Cart=cart1)
                        
                     
                else:    
                     cart1=cart.objects.create(user=request.user,Amount=0,State="pending") 
                     i1=item.objects.create(his_prodect=his_prodect1,count=1,Cart=cart1)
                     cart1.Amount=0
                 
                cart1.Amount =cart1.Amount + i1.his_prodect.price * i1.count  
                cpu =his_prodect1.CPU
                cpu.count =cpu.count -count1

                gpy =his_prodect1.GPU
                gpy.count =gpy.count -count1

                Ma =his_prodect1.Motherboard
                Ma.count =Ma.count -count1

                ram =his_prodect1.RAM
                ram.count =ram.count -count1

                st =his_prodect1.Storage
                st.count =st.count -count1
                psu =his_prodect1.PSU
                psu.count =psu.count -count1
                his_prodect1.save()
                cart1.save()
                messages.success(request, "ِ Added to your cart Seccusfully.")
                return redirect("showcenterBC")
          


            
            return render(request, 'Bcomputer_detail.html', {
                'computer': computer,
                'tenant': tenant
            })
    except Exception as e:
        print(e)
        return render(request, 'test.html', {'message': str(e)})          


def laptop_detail(request, id):
    idc = request.session.get('cen_id')
    tenant = center.objects.get(id=idc)
    
    try:
        with schema_context(tenant.schema_name):
            laptop = Laptop.objects.get(id=id)
            if request.method=="POST":
                his_prodect1=laptop
                count1= int(request.POST.get('count'))
                cart1=cart.objects.filter(user=request.user,photo='').last()
                if cart1:
                     i1=item.objects.create(his_prodect=his_prodect1,count=count1,Cart=cart1)
                     

                else:    
                     cart1=cart.objects.create(user=request.user,State="pending",photo=None) 
                     i1=item.objects.create(his_prodect=his_prodect1,count=count1,Cart=cart1)
                     cart1.Amount=0
                 
                cart1.Amount =cart1.Amount + i1.his_prodect.price * i1.count  
                cart1.save()
                laptop.count =laptop.count-count1
                laptop.save()
                messages.success(request, "ِAdded to your cart Seccusfully.")
                return redirect('showcenterNPC')
            return render(request, 'laptop_detail.html', {'laptop': laptop})
    except Exception as e:
        print(e)
        return render(request, 'test.html', {'message': str(e)})

def show_cart(request):

    tenants = center.objects.exclude(schema_name='public') 
    allcat=[]
    for tenant in tenants:
     try:
        with schema_context(tenant.schema_name):

            carts = cart.objects.filter(user=request.user).order_by('id')
            for i in carts:
                if i.State=="shipping":
                    i.State="shipping expect to recieve it within 48 hours "
            print(carts)
            for i in carts:
                i.idten=tenant.id
                print(i.idten)
            allcat.extend(carts)

               
        return render(request, 'cart_template.html', {'carts': allcat})
     except Exception as e:
        print(e)
        return redirect('test')          

def build_summary(request):
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)
    try:
        with schema_context(tenant.schema_name):
            # Retrieve all selected IDs from the session
            cpu_id = request.session.get('cpu_id')
            gpu_id = request.session.get('gpu_id')
            motherboard_id = request.session.get('motherboard_id')
            ram_id = request.session.get('ram_id')
            storage_id = request.session.get('storage_id')
            psu_id = request.session.get('psu_id')
            ram_quantity = request.session.get('ram_quantity')
            cooler_id = request.session.get('cooler_id', None)  # Optional: in case you allow skipping cooler
            monitor_id = request.session.get('monitor_id', None)  # Optional: if you added monitor selection

            if not all([cpu_id, gpu_id, motherboard_id, ram_id, storage_id, psu_id]):
                return redirect('select_cpu')  # In case the user skipped steps by mistake

            # Fetch selected objects
            cpu = CPU.objects.get(pk=cpu_id)
            gpu = GPU.objects.get(pk=gpu_id)
            motherboard = Motherboard.objects.get(pk=motherboard_id)
            ram = RAM.objects.get(pk=ram_id)
            storage = Storage.objects.get(pk=storage_id)
            psu = PSU.objects.get(pk=psu_id)
            cooler = Cooler.objects.get(pk=cooler_id) if cooler_id else None
            print(ram.capacity * ram_quantity)
            min_cou=cpu.count
            if gpu.count <=min_cou:
                min_cou=gpu.count
            if motherboard.count <= min_cou:
                min_cou=motherboard.count
            if  storage.count <= min_cou:
                min_cou=storage.count       
            if  psu.count <= min_cou:
                min_cou=psu.count   
            if  cooler.count <= min_cou:
                min_cou=storage.count 
            ram_possible_count = ram.count // ram_quantity    
            if ram_possible_count <= min_cou:
                   min_cou = ram_possible_count      
                       
            import random
            import string
            total_price = (
                cpu.price +
                gpu.price +
                cooler.price +
                psu.price +
                storage.price +
                ram.price * ram_quantity +
                motherboard.price 
    )

            if request.method == "POST":
                CountOr = request.POST.get('countOrder')
    # حساب السعر الإجمالي للمكونات + 50

    
    # توليد اسم عشوائي مكون من 10 أحرف
                random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # إنشاء BuildComputer مع القيم المطلوبة
                B1=BuildComputer.objects.create(
                name=random_name,
                count=CountOr,
                price=total_price,
                CPU=cpu,
                GPU=gpu,
                Cooler=cooler,
                PSU=psu,
                Storage=storage,
                RAM=ram,
                Motherboard=motherboard,
                countRam=ram_quantity
    )           
                CountOr =int(CountOr)
                cpu.count -=CountOr
                cpu.save()
                gpu.count -= CountOr
                gpu.save()
                cooler.count -= CountOr
                cooler.save()
                psu.count -=CountOr
                psu.save()
                storage.count -=CountOr
                storage.save()
                motherboard.count -=CountOr
                motherboard.save()
                ram.count -=(CountOr * ram_quantity)
                ram.save()
                
                cart1=cart.objects.filter(user=request.user,photo='').last()
                if cart1:
                     i1=item.objects.create(his_prodect=B1,count=CountOr,Cart=cart1)
                     
                else:    
                     print('11')
                     cart1=cart.objects.create(user=request.user,Amount=0,State="pending") 
                     i1=item.objects.create(his_prodect=B1,count=CountOr,Cart=cart1)
                     cart1.Amount=0
                     
                cart1.Amount += i1.his_prodect.price * i1.count  
                cart1.save()
                messages.success(request, "ِAdded to your cart Seccusfully.")
                return redirect('showcenterNewPc',idc=idc)

                

            return render(request, 'build_summary.html', {
        'cpu': cpu,
        'gpu': gpu,
        'motherboard': motherboard,
        'ram': ram,
        'storage': storage,
        'psu': psu,
        'cooler': cooler,
        'ram_quantity': ram.capacity * ram_quantity,
        'total_price': total_price,
         'min_cou': min_cou,
        
    })
    except Exception as e:
        print(e)
        return render(request, 'test.html', {'message': 'An error occurred while loading the summary.'})
from django.shortcuts import render
from django_tenants.utils import schema_context

from django.shortcuts import render
from django_tenants.utils import schema_context
from django.shortcuts import render
from django_tenants.utils import schema_context

def build_pc(request):
    idc = request.session.get('cen_id')
    tenant = center.objects.get(id=idc)

    performance_profiles = {
        'Low': {'CPU': 0.3, 'GPU': 0.2, 'Motherboard': 0.2, 'RAM': 0.2, 'Storage': 0.1},
        'Medium': {'CPU': 0.35, 'GPU': 0.3, 'Motherboard': 0.15, 'RAM': 0.15, 'Storage': 0.05},
        'High': {'CPU': 0.4, 'GPU': 0.35, 'Motherboard': 0.1, 'RAM': 0.1, 'Storage': 0.05},
    }

    type_priority = {'Low': 1, 'Medium': 2, 'High': 3}

    if request.method == 'POST':
        total_budget = float(request.POST.get('budget', 0))
        performance = request.POST.get('performance', 'Medium')

        if total_budget <= 0:
            return render(request, 'build_pc_input.html', {'error': 'يرجى إدخال ميزانية صحيحة'})

        ratios = performance_profiles.get(performance, performance_profiles['Medium'])
        allowed_types = [t for t, p in type_priority.items() if p >= type_priority[performance]]

        try:
            with schema_context(tenant.schema_name):

                def select_cheapest(model, filters=None):
                    queryset = model.objects.filter(count__gt=0)
                    if filters:
                        queryset = queryset.filter(**filters)
                    return queryset.order_by('price').first()
                def select_cheapest1(queryset, filters=None):
                    queryset = queryset.filter(count__gt=0)
                    if filters:
                      queryset = queryset.filter(**filters)
                    return queryset.order_by('price').first()


                def select_best_within_budget(model, budget, filters=None):
                    queryset = model.objects.filter(count__gt=0)
                    if filters:
                        queryset = queryset.filter(**filters)
                    return queryset.filter(price__lte=budget).order_by('-price').first()
                CPU1=CPU.objects.filter(type=performance)
                GPU1=GPU.objects.filter(type=performance)
                # الخطوة 1: نحجز أرخص القطع الممكنة مع فلترة النوع
                cpu = select_cheapest1(CPU1, {'type': performance})
                gpu = select_cheapest1(GPU1, {'type': performance})

                motherboard = select_cheapest(Motherboard, {'socket_type': cpu.socket_type})

                ram = RAM.objects.filter(
                    type=motherboard.supported_ram_type,
                    speed__lte=motherboard.max_ram_speed,
                    count__gt=0
                ).order_by('price').first()
                if not ram:
                        return render(request, 'build_pc_input.html', {
        'error': motherboard.supported_ram_type
    })
                max_modules = min(motherboard.ram_slots, ram.count)
                ram_modules_used = max_modules 
                # min(2, max_modules)
                ram_total_price = ram.price * ram_modules_used

                storage_types = []
                if motherboard.m2_slots > 0:
                    storage_types.append('M.2 NVMe')
                if motherboard.sata_ports > 0:
                    storage_types.append('SATA')

                storage = Storage.objects.filter(type__in=storage_types, count__gt=0).order_by('price').first()

                total_tdp = cpu.tdp + gpu.power_draw + 100
                required_psu_wattage = int(total_tdp * 1.2)

                psu = PSU.objects.filter(wattage__gte=required_psu_wattage, count__gt=0).order_by('price').first()

                cooler = Cooler.objects.filter(
                    supported_sockets__contains=[cpu.socket_type],
                    tdp_rating__gte=cpu.tdp,
                    count__gt=0
                ).order_by('price').first()

                current_price = cpu.price + gpu.price + motherboard.price + ram_total_price + storage.price + psu.price + cooler.price
                remaining_budget = total_budget - current_price

                if remaining_budget > 0:
                    upgrade_order = ['GPU', 'CPU', 'Motherboard', 'RAM', 'Storage', 'Cooler', 'PSU']
                    for component in upgrade_order:
                        if remaining_budget <= 0:
                            break

                        if component == 'GPU':
                            better_gpu = GPU.objects.filter(
                                count__gt=0,
                                price__gt=gpu.price,
                                price__lte=gpu.price + remaining_budget,
                                type=performance
                            ).order_by('-price').first()
                            if better_gpu:
                                remaining_budget -= (better_gpu.price - gpu.price)
                                gpu = better_gpu

                        elif component == 'CPU':
                            better_cpu = CPU.objects.filter(
                                count__gt=0,
                                price__gt=cpu.price,
                                price__lte=cpu.price + remaining_budget,
                                type=performance
                            ).order_by('-price').first()
                            if better_cpu:
                                remaining_budget -= (better_cpu.price - cpu.price)
                                cpu = better_cpu

                        elif component == 'Motherboard':
                            better_mb = Motherboard.objects.filter(
                                socket_type=cpu.socket_type,
                                count__gt=0,
                                price__gt=motherboard.price,
                                price__lte=motherboard.price + remaining_budget
                            ).order_by('-price').first()
                            if better_mb:
                                remaining_budget -= (better_mb.price - motherboard.price)
                                motherboard = better_mb

                        elif component == 'RAM':
                            better_ram = RAM.objects.filter(
                                type=motherboard.supported_ram_type,
                                speed__lte=motherboard.max_ram_speed,
                                count__gt=0,
                                price__gt=ram.price,
                                price__lte=ram.price + remaining_budget
                            ).order_by('-price').first()
                            if better_ram:
                                remaining_budget -= (better_ram.price - ram.price) * ram_modules_used
                                ram = better_ram
                                ram_total_price = ram.price * ram_modules_used

                        elif component == 'Storage':
                            better_storage = Storage.objects.filter(
                                type__in=storage_types,
                                count__gt=0,
                                price__gt=storage.price,
                                price__lte=storage.price + remaining_budget
                            ).order_by('-price').first()
                            if better_storage:
                                remaining_budget -= (better_storage.price - storage.price)
                                storage = better_storage

                        elif component == 'Cooler':
                            better_cooler = Cooler.objects.filter(
                                supported_sockets__contains=[cpu.socket_type],
                                tdp_rating__gte=cpu.tdp,
                                count__gt=0,
                                price__gt=cooler.price,
                                price__lte=cooler.price + remaining_budget
                            ).order_by('-price').first()
                            if better_cooler:
                                remaining_budget -= (better_cooler.price - cooler.price)
                                cooler = better_cooler

                        elif component == 'PSU':
                            better_psu = PSU.objects.filter(
                                wattage__gte=required_psu_wattage,
                                count__gt=0,
                                price__gt=psu.price,
                                price__lte=psu.price + remaining_budget
                            ).order_by('-price').first()
                            if better_psu:
                                remaining_budget -= (better_psu.price - psu.price)
                                psu = better_psu

                total_price = cpu.price + gpu.price + motherboard.price + ram_total_price + storage.price + psu.price + cooler.price
                min_cou=cpu.count
                if gpu.count <=min_cou:
                  min_cou=gpu.count
                print(min_cou)
                if motherboard.count <= min_cou:
                  min_cou=motherboard.count
                print(min_cou)
                if  storage.count <= min_cou:
                  min_cou=storage.count    
                print(min_cou)   
                if  psu.count <= min_cou:
                  min_cou=psu.count 
                print(min_cou)   
                if  cooler.count <= min_cou:
                  min_cou=cooler.count
                print(min_cou)    
                ram_possible_count = ram.count // ram_modules_used
                if ram_possible_count <= min_cou:
                   min_cou = ram_possible_count
                print(min_cou)    
                context = {
                    'cpu': cpu,
                    'gpu': gpu,
                    'motherboard': motherboard,
                    'ram': ram,
                    'ram_modules_used': ram_modules_used,
                    'ram_total_capacity': ram.capacity * ram_modules_used,
                    'ram_total_price': ram_total_price,
                    'storage': storage,
                    'psu': psu,
                    'cooler': cooler,
                    'total_budget': total_budget,
                    'performance': performance,
                    'total_price': total_price,
                    'min_cou':min_cou
                }
                return render(request, 'build_pc_result.html', context)

        except Exception as e:
            print(cpu)
            print(gpu)
            print(cpu)

            return render(request, 'build_pc_input.html', {'error': f'حدث خطأ: {str(e)}'})

    return render(request, 'build_pc_input.html')
import random
import string
def orderbuild_pc(request):
    idc=request.session.get('cen_id')
    tenant = center.objects.get(id=idc)
    try:
     with schema_context(tenant.schema_name):
      if request.method=="POST":
        
        cpu = request.POST.get('cpu')
        gpu = request.POST.get('gpu')
        motherboard = request.POST.get('motherboard')
        ram = request.POST.get('ram')
        ram_modules_used = int(request.POST.get('ram_modules_used'))
        storage = request.POST.get('storage')
        psu = request.POST.get('psu')
        cooler = request.POST.get('cooler')
        count = int(request.POST.get('count'))
        min_cou = int(request.POST.get('min_cou'))
        price1 = float(request.POST.get('total_price'))
        c=CPU.objects.get(id=cpu)
        print(c)
        print(count)
        c.count = c.count-count
        c.save()
        print(gpu)
        g=GPU.objects.get(id=gpu)
        g.count =g.count -count
        g.save()
        print(c)
        m=Motherboard.objects.get(id=motherboard)
        m.count =m.count -count
        m.save()
        print(c)
        s=Storage.objects.get(id=storage)
        print(s.count)
        s.count =s.count -count
        s.save()
        print(c)
        co=Cooler.objects.get(id=cooler)
        co.count =co.count -count
        co.save()
        print(c)
        p=PSU.objects.get(id=psu)
        p.count =p.count -count
        p.save()
        print(c)
        r=RAM.objects.get(id=ram)

        r.count =r.count -ram_modules_used
        r.save()
        print(r)
            # توليد اسم عشوائي مكون من 10 أحرف
        random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # إنشاء BuildComputer مع الق
        BC=BuildComputer.objects.create(CPU=c,GPU=g,Cooler=co,PSU=p,
                                        Storage=s,RAM=r,Motherboard=m
                                        ,countRam=ram_modules_used,count=min_cou-count,price=price1,name=random_name)
        cart1=cart.objects.filter(user=request.user,photo='').last()
        if cart1:
            i1=item.objects.create(his_prodect=BC,count=count,Cart=cart1)
            
                     
        else:    
            print('11')
            cart1=cart.objects.create(user=request.user,Amount=0,State="pending") 
            i1=item.objects.create(his_prodect=BC,count=count,Cart=cart1)
            cart1.Amount=0
        
        cart1.save()    
        cart1.Amount =cart1.Amount+ i1.his_prodect.price * i1.count  
        cart1.save()
        messages.success(request, "ِAdded to your cart Seccusfully.")
        return redirect('showcenterNewPc',idc=idc)
    except Exception as e:
            print(e)
            return render(request, 'build_pc_input.html', {'error': f'حدث خطأ: {str(e)}'})        
        

       
    return redirect('centerappp:showcenterBC')
def showlocation(request,idt):
        tenant=center.objects.get(id=idt)
        try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                latitude=about.objects.first().x
                longitude=about.objects.first().y
                return render(request,'map.html',{'latitude':latitude,'longitude':longitude})
        except Exception as e:
            return render(request, 'test.html', {'error': f'حدث خطأ: {str(e)}'})    

def MyFacenter(request):
    tenants = center.objects.exclude(schema_name='public') 
    allcat=[]
    for tenant in tenants:
     try:
            # Use tenant context to switch to the tenant's schema
            with schema_context(tenant.schema_name):
                R1=Favorite.objects.filter(HisUser2=request.user)
                if R1:
                    a1=about.objects.all().first()
                    a1.idten=tenant.id
                    allcat.append(a1)



     except Exception as e:
            return render(request, 'test.html', {'error': f'حدث خطأ: {str(e)}'})    
    return render(request, 'MyFaCenter.html',{'allcat':allcat}) 

from django.shortcuts import render, get_object_or_404, redirect

import requests

def cart_detail(request):
    u1 = request.user.person
    xuser = u1.x
    yuser = u1.y

    if request.method == "POST":
        idt = request.POST.get('idt')
        idca = request.POST.get('idca')

        if not idt or not idca:
            return render(request, 'cart_detail.html', {'error': 'Cart ID or Tenant ID is missing.'})

        tenant = center.objects.get(id=idt)

        try:
            with schema_context(tenant.schema_name):
                try:
                    about_center = about.objects.all().first()
                    xcenter = about_center.x
                    ycenter = about_center.y
                    price_per_km = about_center.pricetrans

                    my_cart = cart.objects.get(id=idca)
                    items = my_cart.cart_item.all()

                    # Calculate item totals
                    for i in items:
                        i.sum = i.his_prodect.price * i.count

                    # Calculate distance using TomTom API
                    url = f"https://api.tomtom.com/routing/1/calculateRoute/{xcenter},{ycenter}:{xuser},{yuser}/json?key=wncqPXyuwK1DoGAegYSHAJ5SyE3ATzh7"

                    response = requests.get(url)
                    result = response.json()

                    distance_meters = result['routes'][0]['summary']['lengthInMeters']
                    distance_km = distance_meters / 1000

                    # Calculate shipping cost
                    shipping_cost = distance_km * price_per_km
                    my_cart.shipping_cost = shipping_cost
                    my_cart.save()

                except cart.DoesNotExist:
                    return render(request, 'cart_detail.html', {'error': 'Cart not found.'})

                return render(request, 'cart_detail.html', {
                    'items': items,
                    'my_cart': my_cart,
                    'cart_id': idca,
                    'idt': idt,
                    'PaymentInfo':about_center.PaymentInfo,
                    'shipping_cost': round(shipping_cost, 2),
                    'distance': round(distance_km, 2)
                })

        except Exception as e:
            print(e)
            return render(request, 'test.html', {'error': f'حدث خطأ: {str(e)}'})

    return render(request, 'cart_detail.html', {'error': 'Please submit the form to view cart details.'})

def cart_Pay(request):
    u1 = request.user.person


    if request.method == "POST":
        idt = request.POST.get('idt')
        idca = request.POST.get('idca')
       
        Photo1 = request.FILES.get('photo1')
        shipping_value = request.POST.get('add_shipping')


        if not idt or not idca:
            return render(request, 'cart_detail.html', {'error': 'Cart ID or Tenant ID is missing.'})

        tenant = center.objects.get(id=idt)

        try:
            with schema_context(tenant.schema_name):
                    print(Photo1)
                
                    cart1=cart.objects.get(id=idca)
                    cart1.photo=Photo1
                    if shipping_value:
                      cart1.shipping_cost=shipping_value
                    else:
                        cart1.shipping_cost=0  
                    cart1.save()
                    return redirect('show_cart')
                    
                        

        except Exception as e:
            print(e)
            return render(request, 'test.html', {'error': f'حدث خطأ: {str(e)}'})

    return redirect('show_cart')
def delete_item(request):
    if request.method == "POST":
        idt = request.POST.get('idc')
        iditem = request.POST.get('iditem')  
        tenant = center.objects.get(id=idt)

        try:
            with schema_context(tenant.schema_name):  
                item_to_delete = get_object_or_404(item, id=iditem)
                cart_id = request.POST.get('idica') 
                
                product = item_to_delete.his_prodect
                item_count = item_to_delete.count
                build_computer = BuildComputer.objects.get(id=product.id)

                # إذا كان المنتج من نوع BuildComputer
                if build_computer:
                    # استرجع كل القطع وزد عددها
                    build_computer.CPU.count += item_count
                    build_computer.CPU.save()

                    build_computer.GPU.count += item_count
                    build_computer.GPU.save()

                    build_computer.Motherboard.count += item_count
                    build_computer.Motherboard.save()

                    build_computer.Storage.count += item_count
                    build_computer.Storage.save()

                    build_computer.PSU.count += item_count
                    build_computer.PSU.save()

                    build_computer.Cooler.count += item_count
                    build_computer.Cooler.save()

                    # للـ RAM نضرب بالعدد المستخدم في التجميع
                    ram_total = int(item_count * build_computer.countRam)
                    build_computer.RAM.count += ram_total
                    build_computer.RAM.save()

                else:
                    # منتج عادي: فقط زد عدد المخزون
                    product.count += item_count
                    product.save()

                # خصم السعر من السلة
                cart_instance = cart.objects.get(id=cart_id)
                cart_instance.Amount -= item_count * product.price
                cart_instance.save()

                # حذف العنصر
                item_to_delete.delete()

                return redirect("show_cart")

        except Exception as e:
            print(e)
            return render(request, 'test.html', {'message': str(e)})


def getnotif(request):
    return render(request,'notif.html')