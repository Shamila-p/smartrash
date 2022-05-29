from django.shortcuts import render,HttpResponse
from accounts.models import  User
from wallet.models import Wallet
from django.http import JsonResponse


# Create your views here.
def wallet(request):
    if not (request.user.role == User.MUNICIPALITY or request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method=='GET':
        wallet=Wallet.objects.get(user_id=request.user.id)
        context={'title': 'Wallet','wallet':wallet}
        return render(request,'wallet.html',context)

def add_wallet(request):
    if not (request.user.role == User.MUNICIPALITY or request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method=='POST':
        amount=request.POST['amount']
        wallet=Wallet.objects.get(user_id=request.user.id)
        wallet.amount += float(amount)
        wallet.save()
        return JsonResponse(
            {'amount':wallet.amount,},
            safe=False
        )
       

    

