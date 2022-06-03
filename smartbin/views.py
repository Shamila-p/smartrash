from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from booking.models import Booking
from smartbin.models import SmartBin

# Create your views here.
@login_required
def smartbin(request):
    if not (request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method=='GET':
        smartbin=SmartBin.objects.get(user_id=request.user.id)
        booking=Booking.objects.filter(smartbin_id=smartbin.id).exclude(status=Booking.VERIFIED).first()
        context={'title':'Smart Bin','smartbin':smartbin,'booking':booking}
        return render(request,'smartbin.html',context)

@login_required
def link_bin(request):
    if not (request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method=='GET':
        context={'title':'Link Bin'}
        return render(request,'link_bin.html',context)
    if request.method=='POST':
        bin_id=request.POST['bin_id']
        smartbin=SmartBin.objects.get(user_id=request.user.id)
        smartbin.bin_id=bin_id
        smartbin.fill_status=False
        smartbin.save()
        return redirect('smartbin')

def smartbin_collect_verify(request):
    if request.method=='POST':
        booking=Booking.objects.filter(smartbin__user_id=request.user.id).exclude(status=Booking.VERIFIED).first()
        booking.status=Booking.VERIFIED
        booking.save()
        smartbin=SmartBin.objects.get(user_id=request.user.id)
        smartbin.fill_status=False
        smartbin.save()
        return redirect('smartbin')



