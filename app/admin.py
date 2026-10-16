from django.contrib import admin
from .models import *
from django.contrib import admin, messages
from django_tenants.utils import schema_context, get_tenant_model
from django.db import connection
import psycopg2

from .models import center, Domain

@admin.action(description="حذف السكيمات المحددة يدويًا")
def delete_selected_schemas(modeladmin, request, queryset):
    for tenant in queryset:
        schema_name = tenant.schema_name
        if schema_name in ['public', 'template1']:
            messages.warning(request, f"لا يمكن حذف سكيمة {schema_name}")
            continue
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE')
            messages.success(request, f"تم حذف السكيمة: {schema_name}")
        except psycopg2.Error as e:
            messages.error(request, f"خطأ أثناء حذف {schema_name}: {e.pgerror}")

class CenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'schema_name', 'created_on']
    actions = [delete_selected_schemas]

admin.site.register(center, CenterAdmin)
admin.site.register(Domain)


admin.site.register(TenantUser)
from django.contrib import admin
from django.contrib.auth.models import User
from django_tenants.utils import schema_context

from centerappp.models import Rating ,Favorite,cart  # تأكد من الاستيراد الصحيح

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')  # حقول تظهر في جدول المستخدمين

    def delete_model(self, request, obj):
        # هنا كود حذف التقييمات والمعلومات المتعلقة بالمستخدم في كل tenant كما لديك
        tenants = center.objects.all()
        for tenant in tenants:
            with schema_context(tenant.schema_name):
                try:
                    Rating.objects.filter(HisUser2=obj).delete()
                 
                    Favorite.objects.filter(HisUser2=obj).delete()
                    cart.objects.filter(HisUser2=obj).delete()
                except Exception as e:
                    print(f"Error deleting Rating from tenant {tenant.schema_name}: {e}")
        
        # حذف المستخدم من public schema
        super().delete_model(request, obj)

# إلغاء تسجيل الادمن القديم
admin.site.unregister(User)
# تسجيل الادمن الجديد
admin.site.register(User, CustomUserAdmin)



class paymentMonthCo(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False 

    list_display = ('photo', 'Amount', 'Date','tenant','ispay') 
    readonly_fields = ('photo', 'Amount', 'Date','tenant') 
admin.site.register(paymentMonth, paymentMonthCo)

class personCo(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False 

    list_display = ('user', 'work', 'phone','BirthDate','photo', 'x', 'y','Address','is_verified','otp') 
    readonly_fields = ('user', 'work', 'phone','BirthDate','photo', 'x', 'y','Address','otp') 
admin.site.register(person, personCo)
