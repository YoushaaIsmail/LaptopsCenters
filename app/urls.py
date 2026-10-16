from app.views import *
from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('admin/', admin.site.urls),
     path('',index),
     path('showallprodect',showallprodect),
     path('test',test,name="test"),
     path('select_cpu',select_cpu,name="select_cpu"),
     path('select_gpu',select_gpu,name="select_gpu"),
     path('select_motherboard',select_motherboard,name="select_motherboard"),
      path('select_ram',select_ram,name="select_ram"),
       path('select_storage',select_storage,name="select_storage"),
        path('select_psu',select_psu,name="select_psu"),
    path('select_cooler',select_cooler,name="select_cooler"),  
    path('show_cart',show_cart,name="show_cart"),    
     path('showcenter',showcenter),
       path('loginuser/',loginuser,name="loginuser"),
         path('registeruser/',registeruser,name="registeruser"),
           path('otp_view/',otp_view,name="otp_view"),
           path('showRating/<int:idt>',showRating,name="showRating"),
            path('showFav/<int:idt>',showFav,name="showFav"),
                path('profile/', my_profile, name='my_profile'),
    path('change-password/', change_password, name='change_password'),
            path('forgetpass',forgetpass, name='forgetpass'), 
            path('logout',logout_view,name='logout_view'), 
        path('resetpassword',resetpassword, name='resetpassword'), 
         path('show_otp1',show_otp1, name='show_otp1'), 
        path('showcenterNewPc/<int:idc>', showcenterNewPc, name='showcenterNewPc'),
        path('showcenterLaptop',showcenterLaptop, name='showcenterLaptop'),
        path('showcenterProdect',showcenterProdect, name='showcenterProdect'),
        path('showcenterNPC',showcenterNPC, name='showcenterNPC'),
        path('showcenterBC',showcenterBC, name='showcenterBC'),
           path('newcomputer/<int:id>/', new_computer_detail, name='new_computer_detail'),
           path('B_computer_detail/<int:id>/', B_computer_detail, name='B_computer_detail'),
           path('P_computer_detail/<int:id>/', P_computer_detail, name='P_computer_detail'),
           path('laptop/<int:id>/', laptop_detail, name='laptop_detail'),
           path('build-summary/', build_summary, name='build_summary'),
            path('show_cart/', show_cart, name='show_cart'),
            path('build_pc/', build_pc, name='build_pc'),
            path('searchname/', searchname, name='searchname'),
            path('filtertenant/', filtertenant, name='filtertenant'),
            path('MyFacenter/', MyFacenter, name='MyFacenter'),
            path('showlocation/<int:idt>/', showlocation, name='showlocation'),
            path('search_product_element/', search_product_element, name='search_product_element'),
                path('cart_detail/', cart_detail, name='cart_detail'),
    path('delete_item/', delete_item, name='delete_item'),
    path('cart_Pay/', cart_Pay, name='cart_Pay'),
    path('getnotif/', getnotif, name='getnotif'),
    path('orderbuild_pc/', orderbuild_pc, name='orderbuild_pc'),


           

            #  path('centeradmin/',include(('centerapp.urls', 'centerapp'),namespace='centerapp'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)