from django.shortcuts import get_object_or_404, render

from .models import Brand, Car

def home(request):
    brands = Brand.objects.all()
    cars = Car.objects.select_related('brand').all()
    return render(request, 'index.html', {'brands': brands, 'cars': cars})


def category(request, brand_id: int):
    selected_brand = get_object_or_404(Brand, pk=brand_id)
    brands = Brand.objects.all()
    cars = Car.objects.select_related('brand').filter(brand=selected_brand)
    return render(
        request,
        'Car/category.html',
        {'brands': brands, 'cars': cars, 'selected_brand': selected_brand},
    )


def car_detail(request, pk: int):
    brands = Brand.objects.all()
    car = get_object_or_404(Car.objects.select_related('brand'), pk=pk)
    return render(request, 'Car/car_detail.html', {'brands': brands, 'car': car})

def page1(request):
    brands = Brand.objects.all()
    return render(request, 'Car/page1.html', {'text': 'Це сторінка 1', 'brands': brands})

def page2(request):
    brands = Brand.objects.all()
    return render(request, 'Car/page2.html', {'text': 'Це сторінка 2', 'brands': brands})
