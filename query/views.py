from django.shortcuts import render, redirect
from query.models import Query
from django.shortcuts import render, HttpResponse
from accounts.models import User

# Create your views here.


def ask_query(request):
    if not (request.user.role == User.COLLECTION_AGENT or request.user.role == User.CUSTOMER):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        context = {'title': 'ENQUIRY'}
        return render(request, 'ask_query.html', context)
    if request.method == 'POST':
        content = request.POST['content']
        Query.objects.create(content=content, user_id=request.user.id)
        return redirect('ask_query')


def display_query(request):
    if not (request.user.role == User.MUNICIPALITY):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'GET':
        queries = Query.objects.filter(user__municipality_id=request.user.id)
        context = {'title': 'DISPLAY QUERIES', 'queries': queries}
        return render(request, 'list_query.html', context)
