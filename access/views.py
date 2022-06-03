from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from accounts.models import User, CollectionAgent
from smartbin.models import SmartBin
from wallet.models import Wallet


def index(request):
    return render(request, 'index.html')


def customer(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.CUSTOMER:
            return redirect('home')
        else:
            return redirect('customer_login')


def customer_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.CUSTOMER:
            return redirect('home')
        context = {'title': 'Customer Login',
                   'signup_url_name': 'customer_signup', 'show_forgot_password': True}
        return render(request, 'login.html', context)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        print(email,password,user)
        if user is not None and user.role == User.CUSTOMER:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('customer_login')


def agent(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.COLLECTION_AGENT:
            return redirect('home')
        else:
            return redirect('agent_login')


def agent_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.COLLECTION_AGENT:
            return redirect('home')
        context = {'title': 'Agent Login',
                   'signup_url_name': 'agent_signup', 'show_forgot_password': True}
        return render(request, 'login.html', context)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.COLLECTION_AGENT:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('agent_login')


def municipality(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.MUNICIPALITY:
            return redirect('home')
        else:
            return redirect('municipality_login')


def municipality_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.MUNICIPALITY:
            return redirect('home')
        context = {'title': 'Municipality Login',
                   'signup_url_name': None, 'show_forgot_password': True}
        return render(request, 'login.html', context)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.MUNICIPALITY:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('municipality_login')


def admin(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.ADMIN:
            return redirect('home')
        else:
            return redirect('admin_login')


def admin_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == User.ADMIN:
            return redirect('home')
        context = {'title': 'Admin Login',
                   'signup_url_name': None, 'show_forgot_password': False}
        return render(request, 'login.html', context)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None and user.role == User.ADMIN:
            auth.login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong credentials!!!')
        return redirect('admin_login')


def logout(request):
    auth.logout(request)
    return redirect('index')


def customer_signup(request):
    if request.method == 'GET':
        municipalities = User.objects.filter(role=User.MUNICIPALITY)
        context = {'title': 'Customer signup',
                   'login_url_name': 'customer_login', 'municipalities': municipalities, 'is_agent_page': False}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        house_name = request.POST['house_name']
        place = request.POST['place']
        municipality_id = request.POST['municipality']
        postcode = request.POST['postcode']
        state = request.POST['state']
        country = request.POST['country']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        profile_image = request.FILES['profile_image']

        if not password1 == password2:
            messages.info(request, 'password incorrect')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
        elif User.objects.filter(phone=phone).exists():
            messages.info(request, 'phone number already registered')
        else:
            user=User.objects.create_user(first_name=first_name, last_name=last_name, username=email,
                                     email=email, phone=phone, housename=house_name, place=place,
                                      municipality_id=municipality_id, postcode=postcode, state=state,
                                       country=country, password=password1,profile_image=profile_image, 
                                       role=User.CUSTOMER, is_active=False)
            SmartBin.objects.create(user_id=user.id)
            Wallet.objects.create(amount=0,user_id=user.id)
            return redirect('customer_login')
        return redirect('customer_signup')


def agent_signup(request):
    if request.method == 'GET':
        municipalities = User.objects.filter(role=User.MUNICIPALITY)
        context = {'title': 'Agent signup',
                   'login_url_name': 'agent_login', 'municipalities': municipalities, 'is_agent_page': True}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        house_name = request.POST['house_name']
        place = request.POST['place']
        municipality_id = request.POST['municipality']
        postcode = request.POST['postcode']
        state = request.POST['state']
        country = request.POST['country']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        aadhaar_number = request.POST['aadhaar']
        license_number = request.POST['license']
        aadhaar_image = request.FILES['aadhaar_pic']
        license_image = request.FILES['license_pic']
        profile_image = request.FILES['profile_image']

        if not password1 == password2:
            messages.info(request, 'password incorrect')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
        elif User.objects.filter(phone=phone).exists():
            messages.info(request, 'phone number already registered')
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=email,
                                            email=email, phone=phone, housename=house_name, place=place, municipality_id=municipality_id,
                                            postcode=postcode, state=state, country=country, password=password1,profile_image=profile_image, role=User.COLLECTION_AGENT, is_active=False)
            CollectionAgent.objects.create(aadhaar_number=aadhaar_number, license_number=license_number,
                                           aadhaar_image=aadhaar_image, license_image=license_image, user_id=user.id)
            return redirect('agent_login')
        return redirect('agent_signup')


