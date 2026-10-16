from django.db import models
from django_tenants.models import TenantMixin,DomainMixin
# Create your models here.
import os
from django.contrib.auth.models import User,AbstractUser

from django.db import connection
from django_tenants.models import TenantMixin
from django_resized import ResizedImageField
def upload_to(inst,filename):
      base_path="profile"
      safe_filename=str(filename)
      final_path=os.path.join(base_path,safe_filename)
      return final_path



class center(TenantMixin):
    name=models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)


    def delete(self, *args, **kwargs):
        schema_to_drop = self.schema_name
        super().delete(*args, **kwargs)

        if schema_to_drop != 'public':
            with connection.cursor() as cursor:
                cursor.execute(f'DROP SCHEMA IF EXISTS "{schema_to_drop}" CASCADE')

class Domain(DomainMixin):
    pass    




class TenantUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(center, on_delete=models.CASCADE)

class person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    work=models.CharField(max_length=30)
    phone=models.CharField(max_length=315)    
    BirthDate=models.DateField()
    photo=ResizedImageField(upload_to=upload_to,null=True,blank=True)
    x=models.CharField(max_length=15)
    y=models.CharField(max_length=15)    
    Address=models.CharField(max_length=50)           
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)


class paymentMonth(models.Model):
     photo=ResizedImageField(upload_to=upload_to,null=True,blank=True)
     Amount=models.FloatField()
     Date=models.DateField(auto_created=True)
     ispay=models.BooleanField(default=False) 
     tenant=models.ForeignKey(center,on_delete=models.CASCADE,related_name='center_tenant') 