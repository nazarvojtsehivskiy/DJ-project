from django.shortcuts import render

def home(request):
    return render(request, 'Car/index.html')

def page1(request):
    return render(request, 'Car/page1.html', {'text': 'Це сторінка 1'})

def page2(request):
    return render(request, 'Car/page2.html', {'text': 'Це сторінка 2'})
