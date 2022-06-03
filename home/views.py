from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from home.models import WasteAmount


@login_required
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')


@login_required
def set_waste_amount(request):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        waste_amount = WasteAmount.objects.get(municipality_id=request.user.id)
        context = {'title': 'Set Amount', 'waste_amount': waste_amount}
        return render(request, 'set_waste_amount.html', context)
    if request.method == 'POST':
        amount = request.POST['waste_amount']
        waste_amount = WasteAmount.objects.get(municipality_id=request.user.id)
        waste_amount.amount = amount
        waste_amount.save()
        return redirect('set_waste_amount')
