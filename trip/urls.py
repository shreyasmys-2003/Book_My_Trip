"""
URL configuration for trip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlog/',views.adminlog,name='adminlog'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('view orders',views.vieworders,name='view orders'),
    path('completed orders',views.completedorders,name='completed orders'),
    path('delete/<int:id>',views.delete,name='delete'), 
    path('edit/<int:id>',views.edit,name='edit'),
    path('insert',views.insert,name='insert'),
    path('recommend',views.recommend,name='recommend'),
    path('viewmore/<int:id>',views.viewmore,name='viewmore'),
    path('place/<int:id>',views.place,name='place'),
    path('book/<int:id>',views.book,name='book'),
    path('booknow',views.booknow,name='booknow'),
    path('queries',views.queries,name='queries'),
    path('rejection',views.rejection,name='rejection'),
    path('confirm/<int:id>',views.confirm,name='confirm'),
    path('registration',views.registration,name='registration'),
    path('log',views.log,name='log'),
    path('logout',views.logout,name='logout'),
    path('voicesearch/',views.voicesearch,name='voicesearch'),
    path('userpage',views.userpage,name='userpage'),
    path('userhome',views.userhome,name='userhome'),

    path('add_to_checklist/<int:id>',views.add_to_checklist,name='add_to_checklist'),
    
    path('checklist',views.checklist,name='checklist'),

    path('delete_checklist/<int:id>',views.delete_checklist,name='delete_checklist'),

    path('review/<int:id>',views.review,name='review'),

    path('add_review',views.add_review,name='add_review'),

    path('admin_view_review',views.admin_view_review,name='admin_view_review'),

    #path('place-details/<str:name>/',views.place_details_by_name,name='place_details_by_name'),

    path('voice-open/<str:place>/',views.voice_open_place,name='voice_open_place'),

    path('voice-book/<str:place>/',views.voice_book_place,name='voice_book_place'),

    path('voice-checklist/<str:place>/',views.voice_add_checklist,name='voice_add_checklist'),

    path('adminlogout',views.adminlogout,name='adminlogout'),


    path('usercompletedorders',views.usercompletedorders,name='usercompletedorders'),
    path('myorders',views.myorders,name='myorders'),
    path('makepayment',views.makepayment,name='makepayment'),
    path('pay',views.pay,name='pay'),
    path('cancel',views.cancel,name='cancel'),
    #path('cancels',views.cancels,name='cancels'),

   
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
