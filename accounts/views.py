from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import CollectionAgent, User
from smartbin.models import SmartBin
from django.contrib import messages

from wallet.models import Wallet


# Create your views here.

@login_required
def profile(request):
    if not (request.user.role == User.CUSTOMER or request.user.role == User.COLLECTION_AGENT or request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        municipalities = User.objects.filter(role=User.MUNICIPALITY)
        if request.user.role == User.CUSTOMER:
            context = {'title': 'Profile',
                       'municipalities': municipalities}
        elif request.user.role == User.COLLECTION_AGENT:
            collection_agent = CollectionAgent.objects.get(
                user_id=request.user.id)
            context = {'title': 'Profile', 'municipalities': municipalities,
                       'collection_agent': collection_agent}
        elif request.user.role == User.MUNICIPALITY:
            context = {'title': 'Profile'}
        return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    if not (request.user.role == User.CUSTOMER or request.user.role == User.COLLECTION_AGENT or request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        if request.user.role == User.COLLECTION_AGENT or request.user.role == User.CUSTOMER:
            last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        if request.user.role == User.COLLECTION_AGENT or request.user.role == User.CUSTOMER:
            house_name = request.POST.get('house_name')
            place = request.POST.get('place')
            municipality_id = request.POST.get('municipality')
            profile_image = request.FILES.get('profile_image')
        postcode = request.POST.get('postcode')
        state = request.POST.get('state')
        country = request.POST.get('country')
        if request.user.role == User.COLLECTION_AGENT:
            aadhaar_number = request.POST.get('aadhaar')
            aadhaar_image = request.FILES.get('aadhaar_pic')
            license_number = request.POST.get('license')
            license_image = request.FILES.get('license_pic')
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        if request.user.role == User.COLLECTION_AGENT or request.user.role == User.CUSTOMER:
            user.last_name = last_name
        user.phone = phone
        user.email = email
        if request.user.role == User.COLLECTION_AGENT or request.user.role == User.CUSTOMER:
            user.housename = house_name
            user.place = place
            user.municipality_id = municipality_id
            if profile_image is not None:
                user.profile_image = profile_image
        user.postcode = postcode
        user.state = state
        user.country = country
        user.save()
        if request.user.role == User.COLLECTION_AGENT:
            collection_agent = CollectionAgent.objects.get(
                user_id=request.user.id)
            collection_agent.aadhaar_number = aadhaar_number
            collection_agent.license_number = license_number
            if aadhaar_image is not None:
                collection_agent.aadhaar_image = aadhaar_image
            if license_image is not None:
                collection_agent.license_image = license_image
            collection_agent.save()
        return redirect('profile')


@login_required
def change_password(request):
    if not (request.user.role == User.CUSTOMER or request.user.role == User.COLLECTION_AGENT or request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        current = request.POST['currentpoassword']
        new = request.POST['newpassword']
        confirm = request.POST['confirmpassword']
        user = User.objects.get(id=request.user.id)
        if new != confirm:
            messages.info(request, 'password not matching')
        elif not user.check_password(current):
            messages.info(request, 'wrong current password')
        else:
            user.set_password(new)
            user.save()
        return redirect('profile')


@login_required
def list_customer(request):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        users = User.objects.filter(
            role=User.CUSTOMER, municipality_id=request.user.id)
        context = {'title': 'Customers', 'add_button_name': 'ADD CUSTOMER',
                   'add_button_url_name': 'add_customer', 'users': users}
        return render(request, 'list_customer_agent.html', context)


@login_required
def add_customer(request):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        context = {'title': 'Add Customer'}
        return render(request, 'add_customer_agent.html', context)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        house_name = request.POST['house_name']
        place = request.POST['place']
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
                                     postcode=postcode, state=state,
                                     country=country, municipality_id=request.user.id, password=password1, profile_image=profile_image,
                                     role=User.CUSTOMER, is_active=False)
            SmartBin.objects.create(user_id=user.id)
            Wallet.objects.create(amount=0,user_id=user.id)
            return redirect('list_customer')
        return redirect('add_customer')


@login_required
def remove_customer(request, user_id):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('list_customer')


@login_required
def change_status_customer(request, user_id):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return redirect('list_customer')


@login_required
def list_agent(request):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        users = User.objects.filter(
            role=User.COLLECTION_AGENT, municipality_id=request.user.id)
        user_ids = []
        for user in users:
            user_ids.append(user.id)
        agents = CollectionAgent.objects.filter(user_id__in=user_ids)
        context = {'title': 'Collection Agents', 'add_button_name': 'ADD COLLECTION AGENT',
                   'add_button_url_name': 'add_agent', 'users': users, 'agents': agents, 'is_agent_page': True}
        return render(request, 'list_customer_agent.html', context)


@login_required
def add_agent(request):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        context = {'title': 'Add Agent', 'is_agent_page': True}
        return render(request, 'add_customer_agent.html', context)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        house_name = request.POST['house_name']
        place = request.POST['place']
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
                                            email=email, phone=phone, housename=house_name, place=place,
                                            postcode=postcode, state=state,
                                            country=country, municipality_id=request.user.id, password=password1, profile_image=profile_image,
                                            role=User.COLLECTION_AGENT, is_active=False)
            CollectionAgent.objects.create(aadhaar_number=aadhaar_number, license_number=license_number,
                                           aadhaar_image=aadhaar_image, license_image=license_image, user_id=user.id)
            return redirect('list_agent')
        return redirect('add_agent')


@login_required
def remove_agent(request, user_id):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        agent = CollectionAgent.objects.get(user_id=user_id)
        user.delete()
        agent.delete()
        return redirect('list_agent')


@login_required
def change_status_agent(request, user_id):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return redirect('list_agent')


@login_required
def list_municipalities(request):
    if not (request.user.role == User.ADMIN):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        users = User.objects.filter(role=User.MUNICIPALITY)
        context = {'title': 'Municipalities', 'add_button_name': 'ADD MUNICIPALITY',
                   'add_button_url_name': 'add_municipalities', 'users': users}
        return render(request, 'list_municipalities.html', context)


@login_required
def add_municipalities(request):
    if not (request.user.role == User.ADMIN):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        context = {'title': 'Add Municipality'}
        return render(request, 'add_municipality.html', context)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        phone = request.POST['phone']
        email = request.POST['email']
        postcode = request.POST['postcode']
        state = request.POST['state']
        country = request.POST['country']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1 == password2:
            messages.info(request, 'password incorrect')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
        elif User.objects.filter(phone=phone).exists():
            messages.info(request, 'phone number already registered')
        else:
            user=User.objects.create_user(first_name=first_name, username=email,
                                     email=email, phone=phone,
                                     postcode=postcode, state=state,
                                     country=country, password=password1, role=User.MUNICIPALITY)
            Wallet.objects.create(amount=0,user_id=user.id)
            return redirect('list_municipalities')
        return redirect('add_municipalities')


@login_required
def remove_municipalities(request, user_id):
    if not (request.user.role == User.ADMIN):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('list_municipalities')


@login_required
def change_status_municipalities(request, user_id):
    if not (request.user.role == User.ADMIN):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return redirect('list_municipalities')
