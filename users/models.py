from django.db import models

# Create your models here.

class tourpackages(models.Model):
    id=models.AutoField(primary_key=True)
    Category=models.CharField(max_length=20)
    image=models.ImageField(upload_to='packages/')
    placename=models.CharField(max_length=25)
    actual_PRICE=models.IntegerField()
    special_price=models.IntegerField()
    days=models.CharField(max_length=20)
    travel_mode=models.CharField(max_length=20)
    slots=models.IntegerField()
    tour_themes=models.CharField(max_length=100)

class categories(models.Model):
    id=models.AutoField(primary_key=True)
    categoryimage=models.ImageField(upload_to='packages/')
    name=models.CharField(max_length=20)

class register(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    contact=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class enquiry(models.Model):
    id=models.AutoField(primary_key=True)
    register_id=models.ForeignKey(register,on_delete=models.CASCADE)
    package_id=models.IntegerField()
    name=models.CharField(max_length=20)
    date=models.CharField(max_length=20)
    persons=models.IntegerField()
    contact=models.CharField(max_length=10)
    reject=models.CharField(max_length=30)
    description=models.CharField(max_length=100)
    status=models.CharField(max_length=20,default='pending')
    CANCEL_request=models.CharField(max_length=20,default='no')
    cancel_REASON=models.CharField(max_length=90)

    
class login(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class addreview(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(register,on_delete=models.CASCADE)
    product_id=models.ForeignKey(tourpackages,on_delete=models.CASCADE)
    stars=models.CharField(max_length=40)
    description=models.CharField(max_length=100)

class payment(models.Model):
    id=models.AutoField(primary_key=True)
    register_id=models.ForeignKey(register,on_delete=models.CASCADE)
    enquiry_id=models.IntegerField()
    persons=models.IntegerField()
    total_amount=models.IntegerField()
    transactional_ID=models.CharField(max_length=30)
    payment_MODE=models.CharField(max_length=20)

class wishlist(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(register,on_delete=models.CASCADE)
    product_id=models.ForeignKey(tourpackages,on_delete=models.CASCADE)

class adminlogins(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
