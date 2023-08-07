from django.shortcuts import render,redirect
from .models import User,Product
import requests
import random

# Create your views here.
def index(request):
	products=Product.objects.all()
	return render(request,'index.html',{'products':products})

def seller_index(request):
	return render(request,'seller-index.html')


def checkout(request):
	return render(request,'checkout.html')

def signup(request):
	
	if request.method=='POST':
		try:
			User.objects.get(email=request.POST['email'])
			msg='Email Already Registered'
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					profile_pic=request.FILES['profile_pic'],
					usertype=request.POST['usertype'],
					admin_access=admin_access,
					)
				msg='SignUp Suceesfully'
				return render(request,'signup.html',{'msg':msg})
			else:
				msg='Password & Confirm Password Does Not Match'
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="buyer":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return render(request,'index.html')
				else:
					if user.admin_access==True:
						request.session['email']=user.email
						request.session['fname']=user.fname
						request.session['profile_pic']=user.profile_pic.url
						return render(request,'seller-index.html')
					else:
						msg='Admin not accept your request'
						return render(request,'login.html',{'msg':msg})
			else:
				msg='Your Password is Incorrect'
				return render(request,'login.html',{'msg':msg})
		except:
			msg='Email Is Not Registered'
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'index.html')
	except:
		return render(request,'index.html')


def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		if user.password==request.POST['oldpassword']:
			if request.POST['npassword']==request.POST['cnpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg='New password and Confirm New password does not match'
				if user.usertype=='buyer':
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'seller-change-password.html',{'msg':msg})
		else:
				msg='Old password does not match'
				if user.usertype=='buyer':
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'seller-change-password.html',{'msg':msg})
	else:
		if user.usertype=='buyer':
			return render(request,'change-password.html')
		else:
			return render(request,'seller-change-password.html')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url
		msg='Profile Update Successfully'
		if user.usertype=='buyer':
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=='buyer':
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'seller-profile.html',{'user':user})

def forgot_password (request):
	if request.method=="POST":
		mobile=request.POST['mobile']
		try:
			user=User.objects.get(mobile=mobile)
			otp=random.randint(1000,9999)
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"M6sYpXnKx3t9I8zQJqwa2VNGdkjuCvPLrAybBRcifH7FESge5ZsYWunxdMrvy4X60L39hkJ5FbRACEgU","variables_values":str(otp),"route":"otp","numbers":str(mobile)}
			headers = { 'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			return render(request,'otp.html',{'otp':otp,'mobile':mobile})
		except:
			msg='Mobile Not Registered'
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	mobile=request.POST['mobile']
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	if otp==uotp:
		return render(request,'new-password.html',{'mobile':mobile})
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'msg':msg,'otp':otp,'mobile':mobile})

def new_password(request):
	mobile=request.POST['mobile']
	np=request.POST['npassword']
	cnp=request.POST['cnpassword']

	if np==cnp:
		user=User.objects.get(mobile=mobile)
		user.password=np
		user.save()
		msg="Password Update Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg='New password and Confirm new password does not match'
		return render(request,'new-password.html',{'mobile':mobile,'msg':msg})

def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		Product.objects.create(
			seller=seller,
			product_category=request.POST['product_category'],
			product_name=request.POST['product_name'],
			product_price=request.POST['product_price'],
			product_desc=request.POST['product_desc'],
			product_image=request.FILES['product_image']
			)
		msg='Product Added Successfully'
		return render(request,'seller-add-product.html',{'msg':msg})
	else:
		return render(request,'seller-add-product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-view-product.html',{'products':products})

def seller_product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller-product-details.html',{'product':product})

def seller_edit_product (request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_category=request.POST['product_category']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg='Product Update Successfully'
		return render(request,'seller-edit-product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller-edit-product.html',{'product':product})

def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')

def seller_view_laptops(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Laptop")
	return render(request,'seller-view-product.html',{'products':products})
	

def seller_view_cameras(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Camera")
	return render(request,'seller-view-product.html',{'products':products})
	

def seller_view_accessories(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Accessories")
	return render(request,'seller-view-product.html',{'products':products})

def product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'product-details.html',{'product':product})

def add_to_wishlist (request,pk):
	return render(request,'add-to-wishlist.html')

