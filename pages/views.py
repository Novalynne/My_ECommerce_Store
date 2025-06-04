from django.shortcuts import render

# Create your views here.

def frontpage(request):
    return render(request, 'front_page.html')
def Login(request):
    return render(request, 'login.html')
