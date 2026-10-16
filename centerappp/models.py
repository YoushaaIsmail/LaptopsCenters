from django.db import models
from app.models import center
from django_resized import ResizedImageField
import os
from django.contrib.auth.models import User,AbstractUser
def upload_to(inst,filename):
      base_path="profile"
      safe_filename=str(filename)
      final_path=os.path.join(base_path,safe_filename)
      return final_path

class element(models.Model):
       name=models.CharField(max_length=300)
       price=models.FloatField()
       count=models.IntegerField()
       link=models.CharField(null=True,blank=True)


class about(models.Model):
       name=models.CharField(max_length=1000)
       Des=models.CharField(max_length=5000)
       PaymentInfo=models.CharField(max_length=5000,null=True)
       photo=ResizedImageField(upload_to=upload_to,null=True,blank=True)
       photo1=ResizedImageField(upload_to=upload_to,null=True,blank=True)
       x=models.CharField(max_length=150)
       y=models.CharField(max_length=150)    
       Address=models.CharField(max_length=50)   
       pricetrans=models.FloatField() 

class Rating(models.Model):
     HisUser2 = models.ForeignKey(User, on_delete=models.DO_NOTHING)

     text=models.CharField(max_length=3000) 
     Star=models.FloatField()
     Date=models.DateField(auto_now=True)
     Type=models.CharField(max_length=200)



    




class Favorite(models.Model):
     HisUser2 = models.ForeignKey(User, on_delete=models.DO_NOTHING)
     Date=models.DateField(auto_now=True)
     

# class Motherboard(prodect):
             
from django.db import models

class CPU(element): 
     list3=(
            ('Low', 'Low'),
            ('High', 'High'),
            ('Medium', 'Medium'),
           
)

     type=models.CharField(max_length=20,choices=list3,null=True)      
     socket_type = models.CharField(max_length=500) 
     supported_ram_type = models.CharField(max_length=100)  # DDR4, DDR5 
     max_ram_speed = models.IntegerField() 
     tdp = models.IntegerField()  # Thermal Design Power in watts 
     chipset = models.JSONField()

class Motherboard(element): 
   
     socket_type = models.CharField(max_length=500) 
     chipset = models.CharField(max_length=500) 
     supported_ram_type = models.CharField(max_length=100) 
     max_ram_speed = models.IntegerField() 
     ram_slots = models.IntegerField() 
     pcie_version = models.DecimalField(max_digits=3,decimal_places=1) #GPU
     m2_slots = models.IntegerField() 
     sata_ports = models.IntegerField()

# class chipset(models.Model):
#      HisUser2=models.ForeignKey(CPU,on_delete=models.CASCADE,related_name='CPU_chipset') 
#      name=models.CharField(max_length=50)  

class RAM(element): 
  
     type = models.CharField(max_length=100)  # DDR4, DDR5 
     speed = models.IntegerField() 
     capacity = models.IntegerField(help_text="In GB") 
     modules = models.IntegerField()

class GPU(element): 
     list3=(
            ('Low', 'Low'),
            ('High', 'High'),
            ('Medium', 'Medium'),
           
)

     type=models.CharField(max_length=20,choices=list3,null=True)         
     interface_version = models.DecimalField(max_digits=3,decimal_places=1)  # e.g., PCIe x16 
     power_draw = models.IntegerField(help_text="In watts") 
     length_mm = models.IntegerField() 
     required_psu_wattage = models.IntegerField() 
     output_ports = models.JSONField()  # e.g., ["HDMI", "DisplayPort"]

class Storage(element): 
    
     type = models.CharField(max_length=200)  # SATA, M.2 NVMe 
     capacity = models.IntegerField(help_text="In GB") 
     interface_version = models.CharField(max_length=100)  # PCIe 3.0, 4.0

class PSU(element): 
     
     wattage = models.IntegerField() 
     efficiency_rating = models.CharField(max_length=100)  # 80+ Bronze, Gold, etc. 
     pcie_connectors = models.IntegerField() 
     eps_connector = models.BooleanField(default=True) 
     form_factor = models.CharField(max_length=10)  # ATX, SFX

class Cooler(element): 
   
     supported_sockets = models.JSONField()  # list of supported socket types 
     tdp_rating = models.IntegerField(help_text="Max TDP supported") 
     height = models.IntegerField(help_text="Cooler height in mm")

          

class prodect(models.Model):
     photo=ResizedImageField(upload_to=upload_to,null=True,blank=True)   
     name=models.CharField(max_length=300)
     count=models.IntegerField() 
     price=models.FloatField()



class Monitor(prodect): 
     
     resolution = models.CharField(max_length=200) 
     refresh_rate = models.IntegerField() 
     panel_type = models.CharField(max_length=200) 
     input_ports = models.JSONField()  # e.g., ["HDMI", "DisplayPort"]   

class BuildComputer(prodect):
     CPU=models.ForeignKey(CPU,on_delete=models.CASCADE,related_name='CPU_BuildComputer') 
     GPU=models.ForeignKey(GPU,on_delete=models.CASCADE,related_name='GPU_BuildComputer') 
     Cooler=models.ForeignKey(Cooler,on_delete=models.CASCADE,related_name='Cooler_BuildComputer')
     PSU=models.ForeignKey(PSU,on_delete=models.CASCADE,related_name='PSU_BuildComputer')
     Storage=models.ForeignKey(Storage,on_delete=models.CASCADE,related_name='Storage_BuildComputer')
     RAM=models.ForeignKey(RAM,on_delete=models.CASCADE,related_name='RAM_BuildComputer')
     Motherboard=models.ForeignKey(Motherboard,on_delete=models.CASCADE,related_name='Motherboard_BuildComputer')  
     countRam=models.DecimalField(max_digits=3,decimal_places=1) 

class NewComputer(prodect):
     list3=(
            ('Low', 'Low'),
            ('High', 'High'),
            ('Medium', 'Medium'),
           
)

     type=models.CharField(max_length=200,choices=list3,null=True)         

     CPU=models.CharField(max_length=300) 
     CPULink=models.CharField(max_length=300) 
     GPU=models.CharField(max_length=300) 
     GPULink=models.CharField(max_length=300) 
     Cooler=models.CharField(max_length=300)
     CoolerLink=models.CharField(max_length=300)
     PSU=models.CharField(max_length=300)
     PSULink=models.CharField(max_length=300)
     Storage=models.CharField(max_length=300)
     StorageLink=models.CharField(max_length=300)
     RAM=models.CharField(max_length=300)
     RAMLink=models.CharField(max_length=300)
     Motherboard=models.CharField(max_length=300)
     MotherboardLink=models.CharField(max_length=300)   
     company=models.CharField(max_length=250)


class Laptop(NewComputer):

     Battary=models.CharField(max_length=300)
     screen=models.CharField(max_length=300)




class onlyProdect(prodect):
     Des=models.CharField(max_length=2000)

class cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
     list3=(
            ('Faild', 'Faild'),
            ('Pendding', 'Pendding'),
            ('Complete', 'Complete'),
           
)

     shipping_cost=models.FloatField(null=True)
     photo=ResizedImageField(upload_to=upload_to,null=True,blank=True)
     Amount=models.FloatField(null=True)   
     State=models.CharField(max_length=20,choices=list3,null=True) 
class item(models.Model):
     his_prodect=models.ForeignKey(prodect,on_delete=models.CASCADE,related_name='item_prodect') 
     count=models.PositiveIntegerField() 
     Cart = models.ForeignKey(cart, related_name='cart_item', on_delete=models.CASCADE)

