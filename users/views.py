from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import tourpackages
from .models import categories
from .models import enquiry
from .models import register,wishlist,addreview
from .models import payment
from .models import adminlogins
from django.core.mail import send_mail
from django.db.models import Q

# Create your views here.

# admin panel

def adminlog(request):
    if request.method=='POST':
        adlog=adminlogins()
        adlog.username=request.POST['username']
        adlog.password=request.POST['password']
        checK_ad=adminlogins.objects.get()
        if checK_ad:
            request.session['username']=checK_ad.username
            request.session['password']=checK_ad.password
            return render(request,'adminhome.html')
        else:
            messages.success(request,"invalid credentials") 
    return render(request,'adminlogin.html')

def adminhome(request):
    if request.method=='POST':
        create=tourpackages()
        create.Category=request.POST['Category']
        create.image=request.FILES['filetoupload']
        create.placename=request.POST['placename']
        create.actual_PRICE=request.POST['actual_price']
        create.special_price=request.POST['special_price']
        create.days=request.POST['days']
        create.travel_mode=request.POST['travelmode']
        create.slots=request.POST['slots']
        create.tour_themes=request.POST['tour_themes']
        create.save()
    messages.success(request,'tour packages created successfully')
    obj=tourpackages.objects.all()
    category=categories.objects.all()
    print(category)
    return render(request,'adminhome.html',{'obj':obj,'category':category})

def delete(request,id):
    obj=tourpackages.objects.get(id=id)
    obj.delete()
    return redirect('adminhome')

def edit(request,id):
    obj=tourpackages.objects.get(id=id)
    category=categories.objects.all()
    return render(request,'update.html',{'obj':obj,'category':category})

def insert(request):
    if request.method=='POST':
        id=request.POST['id']
        register=tourpackages.objects.get(id=id)
        register.Category=request.POST['Category']
        register.image=request.POST['filetoupload']
        register.placename=request.POST['placename']
        register.actual_PRICE=request.POST['actual_price']
        register.special_price=request.POST['special_price']
        register.days=request.POST['days']
        register.slots=request.POST['slots']  
        register.tour_themes=request.POST['tour_themes']
        register.save()
        messages.success(request,'update successfully')
    return redirect('adminhome')

def recommend(request):
    if request.method=='POST':
        show=categories()
        show.categoryimage=request.FILES['filetoupload']
        show.name=request.POST['name']
        show.save()
        messages.success(request,'submitted successfully')
    category=categories.objects.all()
    return render(request,'recommend.html',{'category':category})

def viewmore(request,id):
    if 'username' in request.session:
        print('present')
    else:
        print('not present')
        return redirect('userpage')
    user=request.session['username']
    pwd=request.session['password']
    usr=register.objects.get(username=user,password=pwd)
    obj=tourpackages.objects.filter(Q(Category=id))
    return render(request,'userhome.html',{'obj':obj,'id':id,'usr':usr})

def place(request,id):
    if 'username' in request.session:
        user=request.session['username']
        print('present')
    else:
        print('not present')
        return redirect('userpage')
    obj=tourpackages.objects.get(id=id) 
    view_reviews=addreview.objects.filter(product_id_id=obj.id).select_related('user_id')
    print(obj)
    return render(request,'place.html',{'obj':obj,'user':user,'view_reviews':view_reviews})

#def place_details_by_name(request, name):

    place = get_object_or_404(tourpackages,placename__iexact=name)

    return render(request,'placeinfo.html',{'msg': place})

def vieworders(request):
    return render(request,'view orders.html')

def completedorders(request):
    show=enquiry.objects.filter(Q(status='accept'))
    cash=payment.objects.all()
    return render(request,'completed orders.html',{'cash':cash,'show':show})

def book(request,id):
    if 'username' in request.session:
        print('present')
    else:
        print('not present')
        return redirect('userpage')
    user=request.session['username']
    pwd=request.session['password']
    usr=register.objects.get(username=user,password=pwd)
    obj=tourpackages.objects.get(id=id)
    return render(request,'userhome1.html',{'obj':obj,'usr':usr})

def booknow(request):
    if request.method=='POST':
        pay=enquiry()
        tripmode=request.POST['travel_mode']
        if tripmode=='group':
            print(request.POST['package_id'])
            up_tourpac=tourpackages.objects.get(id=request.POST['package_id'])
            pay.package_id=request.POST['package_id']
            pay.register_id_id=request.POST['register_id']
            pay.name=request.POST['name']
            pay.date=request.POST['date']
            pay.persons=request.POST['persons']
            pay.contact=request.POST['contact']
            pay.save()
            remaining=up_tourpac.slots - int(request.POST['persons'])
            up_tourpac.slots=remaining
            up_tourpac.save()
        else:
            pay.package_id=request.POST['package_id']
            pay.register_id_id=request.POST['register_id']
            pay.name=request.POST['name']
            pay.date=request.POST['date']
            pay.persons=request.POST['persons']
            pay.contact=request.POST['contact']
            pay.save()
    messages.success(request,"enquiry sent successfully")
    return redirect('userhome')

def queries(request):
    show=enquiry.objects.filter(Q(status='pending'))  
    can=enquiry.objects.filter(Q(CANCEL_request='yes'))
    print(can)
    return render(request,'queries.html',{'can':can,'show':show})

def rejection(request):
    if request.method=='POST':
        id=request.POST['id']
        show=enquiry.objects.get(id=id)
        show.reject=request.POST['reject']
        show.description=request.POST['description']
        show.status='reject'
        up_tourpac=tourpackages.objects.get(id=show.package_id)
        remaining=up_tourpac.slots + int(show.persons)
        up_tourpac.slots=remaining
        up_tourpac.save()
        show.save()
    return redirect('queries')

def confirm(request,id):
    show=enquiry.objects.get(id=id)
    show.status='accept'
    show.save()

    user_email=show.register_id.email
    user_name=show.register_id.name
     # send confirmation email
    send_mail(
        subject="🎉 Booking Confirmed - TripVox",
        message=(
            f"Hello {user_name},\n\n"
            "Great news! 🎉\n\n"
            "Your booking has been confirmed successfully.\n\n"
            "You can now complete your payment to finalize your booking.\n\n"
            "Please log in to your TripVox account and proceed with the payment process.\n\n"
            "Thank you for choosing TripVox. ✈️\n"
            "We wish you a wonderful and memorable journey! 🌍\n\n"
            "Best Regards,\n"
            "TripVox Team"
        ),
        from_email="tripvoxvox@gmail.com",
        recipient_list=[user_email],
        fail_silently=False
    )
    return redirect('queries')

def registration(request):
    if request.method=='POST':
        regis=register()
        regis.name=request.POST['name']
        regis.address=request.POST['address']
        regis.contact=request.POST['contact']
        regis.email=request.POST['email']
        regis.username=request.POST['username']
        regis.password=request.POST['password']
        regis.save()
        send_mail(
    subject="🎉 Registration Successful - Welcome to TripVox!",
    message=f"""
               Hello {request.POST['name']} 👋

               🎊 Welcome to TripVox!

               Your registration was completed successfully.

               🌍 Start exploring amazing destinations
               ✈️ Discover exciting tour packages
               💖 Save your favorite trips
              📅 Book your dream vacations easily

              We're excited to be part of your travel journey.

              "Travel isn't always about places; it's about experiences."

               Thank you for joining TripVox 🚀
               Happy Traveling! 🌴🏖️

              Need help?
              📧 Contact us: tripvoxvox@gmail.com

              Team TripVox ❤️
            """,
    from_email="tripvoxvox@gmail.com",
    recipient_list=[request.POST['email']],
    fail_silently=True
)
    return redirect('userpage')

def log(request):
    if request.method=='POST':

        username=request.POST['username']
        password=request.POST['password']
        verify_log=register.objects.filter(Q(username=username,password=password)).first()
        if verify_log:
            request.session['id']=verify_log.id
            request.session['username']=verify_log.username
            request.session['password']=verify_log.password
            obj=tourpackages.objects.all()
            messages.success(request,'login success')
            return render(request,'userhome.html',{'obj':obj})
        else:
            messages.success(request,'INVALID CREDENTIALS')
            return redirect('log')
    return render(request,'login.html')
              
def logout(request):
    print(request.session['username'])
    request.session.flush()
    return redirect('log')
    
#user views

def voicesearch(request):
    query = request.GET.get('q')

    if query:
        obj = tourpackages.objects.filter(
            Q(placename__icontains=query) |
            Q(Category__icontains=query) |
            Q(tour_themes__icontains=query)
        )
    else:
        obj = tourpackages.objects.all()

    user = request.session.get('username')

    return render(
        request,
        'userhome.html',
        {'obj': obj, 'user': user, 'query':query}
    )

def userpage(request):
    category=categories.objects.all()
    obj=tourpackages.objects.filter(Q(travel_mode='group'))
    print(obj)
    return render(request,'userpage.html',{'category':category,'obj':obj})
 
def userhome(request):
    #username=request.session
    if 'username' in request.session:
        user=request.session['username']
        print(request.session['username'])
        obj=tourpackages.objects.all()
        wishlist_products=[]
        if 'id'in request.session:
            user_id=request.session['id']
            wishlist_products=wishlist.objects.filter(user_id_id=user_id).values_list('product_id_id',flat=True)
        return render(request,'userhome.html',{'obj':obj,'user':user,'wishlist_products':wishlist_products})
    else:
        return redirect('log')
    

    
def add_to_checklist(request,id):
    if 'id' in request.session:
        user_id=request.session['id']
        product=id
        addtowishlist=wishlist(user_id_id=user_id,product_id_id=product)
        addtowishlist.save()
        return redirect('userhome')
    else:
        return redirect('userpage')
    
def checklist(request):
    if 'username' in request.session:
        user=request.session['username']
        user_id=request.session['id']
        checklistproducts=wishlist.objects.filter(user_id=user_id).select_related('product_id')
        print(checklistproducts)
    return render(request,'checklist.html',{'checklistproducts':checklistproducts,'user':user})

def delete_checklist(request,id):
    delete_items=wishlist.objects.get(id=id)
    delete_items.delete()
    return redirect('checklist')


def usercompletedorders(request):
    user=request.session['username']
   # show=enquiry.objects.filter(Q(status='accept'))
    cash=payment.objects.all()  
    only_user=enquiry.objects.filter(register_id=request.session['id'],status='accept')
    paid_orders = payment.objects.values_list('enquiry_id',flat=True)
    reviewed=addreview.objects.filter(user_id_id=request.session['id']).values_list('product_id_id',flat=True)
    return render(request,'usercompleted orders.html',{'cash':cash,'user':user,'only_user':only_user,'paid_orders':paid_orders,'reviewed':reviewed})

def review(request,id):
    if 'username' in request.session:
        user=request.session['username']
    tour=tourpackages.objects.get(id=id)
    return render(request,'review.html',{'tour':tour,'user':user,})

def add_review(request):
    if request.method == 'POST':
        reviews=addreview()
        reviews.user_id_id=request.session['id']
        reviews.product_id_id=request.POST['tour_id']
        reviews.stars=request.POST['rating']
        reviews.description=request.POST['review']
        reviews.save()
    viewreviews=addreview.objects.all()
    return redirect('usercompletedorders')

def admin_view_review(request):
    view_reviews=addreview.objects.select_related('user_id','product_id')
    return render(request,'adminviewreview.html',{'view_reviews':view_reviews})

def myorders(request):
    user=request.session['username']
    pwd=request.session['password']
    usr=register.objects.get(username=user,password=pwd)
    show=enquiry.objects.filter(Q(register_id=usr.id))
    print(show)
    paid_orders=payment.objects.values_list('enquiry_id',flat=True)
    obj=tourpackages.objects.all()
    return render(request,'my orders.html',{'show':show,'usr':usr,'obj':obj,'user':user,'paid_orders':paid_orders})

def makepayment(request):
    if request.method=='POST':
        user=request.session['username']
        id=request.POST['id']
        show=enquiry.objects.get(id=id)
        persons=int(request.POST['persons'])
        price=int(request.POST['price']) 
        total_amount = persons * price
        return render(request,'enquiry form.html',{'show':show,'total_amount':total_amount,'user':user})
    
def pay(request):
    if request.method=='POST':
        money=payment()
        money.enquiry_id=request.POST['id']
        money.persons=request.POST['persons']
        money.total_amount=request.POST['total_amount']
        money.transactional_ID=request.POST['transactional_ID']
        money.payment_MODE=request.POST['payment_MODE']
        money.save()
        messages.success(request,'payment successfull')
        cash=payment.objects.all()
        return render(request,'enquiry form.html',{'cash':cash})

def cancel(request):
    if request.method=='POST':
        id=request.POST['id']
        show=enquiry.objects.get(id=id)
        show.cancel_REASON=request.POST['cancel']
        show.CANCEL_request='yes'
        show.save()
    return redirect('myorders')

from django.shortcuts import redirect, get_object_or_404
from .models import tourpackages


# OPEN DETAILS PAGE
def voice_open_place(request, place):
    obj = get_object_or_404(
        tourpackages,
        placename__iexact=place
    )

    return redirect('place', id=obj.id)


# OPEN BOOKING PAGE
def voice_book_place(request, place):
    obj = get_object_or_404(
        tourpackages,
        placename__iexact=place
    )

    return redirect('book', id=obj.id)


from django.shortcuts import redirect, get_object_or_404
from .models import tourpackages, wishlist


def voice_add_checklist(request, place):

    if 'id' not in request.session:
        return redirect('userpage')

    user_id = request.session['id']

    package = get_object_or_404(
        tourpackages,
        placename__iexact=place
    )

    # Avoid duplicate checklist entries
    already_added = wishlist.objects.filter(
        user_id_id=user_id,
        product_id_id=package.id
    ).exists()

    if not already_added:
        wishlist.objects.create(
            user_id_id=user_id,
            product_id_id=package.id
        )

    return redirect('checklist')