from django.shortcuts import redirect, render

def home(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'home.html')
