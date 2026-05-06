from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, NewsletterForm, RatingForm
from .models import Brand, Car, MailingSubscription, Order, Review


def _get_brands():
    return Brand.objects.all()


def _ensure_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def _get_cart(request):
    # cart: {car_id(str): quantity(int)}
    return request.session.get("cart", {})


def home(request):
    brands = _get_brands()
    cars = Car.objects.select_related("brand").all()
    return render(request, "index.html", {"brands": brands, "cars": cars})


def category(request, brand_id: int):
    selected_brand = get_object_or_404(Brand, pk=brand_id)
    brands = _get_brands()
    cars = Car.objects.select_related("brand").filter(brand=selected_brand)
    return render(
        request,
        "Car/category.html",
        {"brands": brands, "cars": cars, "selected_brand": selected_brand},
    )


def car_detail(request, pk: int):
    brands = _get_brands()
    car = get_object_or_404(Car.objects.select_related("brand"), pk=pk)

    # rating
    session_key = _ensure_session_key(request)
    reviews_qs = Review.objects.filter(car=car)
    review_count = reviews_qs.count()
    avg_rating = reviews_qs.aggregate(avg=Avg("rating"))["avg"]
    my_review = reviews_qs.filter(session_key=session_key).first()

    rating_form = RatingForm(
        initial={
            "rating": my_review.rating if my_review else 5,
            "text": my_review.text if my_review else "",
        }
    )

    # cart
    cart = _get_cart(request)
    cart_quantity = cart.get(str(car.pk), 0)

    return render(
        request,
        "Car/car_detail.html",
        {
            "brands": brands,
            "car": car,
            "review_count": review_count,
            "avg_rating": avg_rating,
            "my_review": my_review,
            "rating_form": rating_form,
            "cart_quantity": cart_quantity,
        },
    )


def rate_car(request, pk: int):
    if request.method != "POST":
        return redirect("car_detail", pk=pk)

    car = get_object_or_404(Car, pk=pk)
    session_key = _ensure_session_key(request)

    # Перевіряємо, чи вже існує оцінка від цієї сесії
    existing_review = Review.objects.filter(car=car, session_key=session_key).first()
    if existing_review:
        messages.warning(request, "Ви вже оцінили цей автомобіль. Неможливо змінити оцінку.")
        return redirect("car_detail", pk=pk)

    form = RatingForm(request.POST)
    if form.is_valid():
        Review.objects.create(
            car=car,
            session_key=session_key,
            rating=form.cleaned_data["rating"],
            text=form.cleaned_data["text"],
        )
        messages.success(request, "Дякуємо! Вашу оцінку збережено.")
    else:
        messages.error(request, "Не вдалося зберегти оцінку. Перевірте дані форми.")

    return redirect("car_detail", pk=pk)


def cart_view(request):
    brands = _get_brands()
    cart = _get_cart(request)

    cars_map = Car.objects.select_related("brand").in_bulk(cart.keys())

    cart_items = []
    total_price = 0
    for car_id, quantity in cart.items():
        car_obj = cars_map.get(int(car_id)) if isinstance(car_id, str) else cars_map.get(car_id)
        if not car_obj:
            continue
        subtotal = car_obj.price * quantity
        total_price += subtotal
        cart_items.append({"car": car_obj, "quantity": quantity, "subtotal": subtotal})

    return render(
        request,
        "Car/cart.html",
        {"brands": brands, "cart_items": cart_items, "total_price": total_price},
    )


def cart_add(request, pk: int):
    cart = _get_cart(request)
    car_id = str(pk)
    cart[car_id] = cart.get(car_id, 0) + 1
    request.session["cart"] = cart
    request.session.modified = True
    messages.success(request, "Товар додано в кошик.")
    return redirect("cart")


def cart_remove(request, pk: int):
    cart = _get_cart(request)
    car_id = str(pk)
    if car_id in cart:
        cart.pop(car_id, None)
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Товар видалено з кошика.")
    return redirect("cart")


def checkout(request):
    """Форма оформлення замовлення"""
    brands = _get_brands()
    cart = _get_cart(request)

    if not cart:
        messages.warning(request, "Кошик порожній. Додайте товари перед оформленням.")
        return redirect("cart")

    # Отримуємо інформацію про товари
    cars_map = Car.objects.select_related("brand").in_bulk(cart.keys())
    cart_items = []
    total_price = 0

    for car_id, quantity in cart.items():
        car_obj = cars_map.get(int(car_id)) if isinstance(car_id, str) else cars_map.get(car_id)
        if not car_obj:
            continue
        subtotal = car_obj.price * quantity
        total_price += subtotal
        cart_items.append({
            "car_id": car_obj.pk,
            "car_name": car_obj.name,
            "brand_name": car_obj.brand.name,
            "price": float(car_obj.price),
            "quantity": quantity,
            "subtotal": float(subtotal)
        })

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Створюємо замовлення
            order = Order.objects.create(
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data["phone"],
                email=form.cleaned_data["email"],
                delivery_address=form.cleaned_data["delivery_address"],
                delivery_date=form.cleaned_data["delivery_date"],
                delivery_time=form.cleaned_data["delivery_time"],
                payment_method=form.cleaned_data["payment_method"],
                total_price=total_price,
                cart_data=cart_items,
                notes=form.cleaned_data.get("notes", ""),
            )

            # Очищуємо кошик
            request.session["cart"] = {}
            request.session.modified = True

            return redirect("order_success", order_id=order.pk)
    else:
        form = CheckoutForm()

    return render(
        request,
        "Car/checkout.html",
        {
            "brands": brands,
            "form": form,
            "cart_items": cart_items,
            "total_price": total_price,
        },
    )


def order_success(request, order_id: int):
    """Сторінка підтвердження замовлення"""
    brands = _get_brands()
    order = get_object_or_404(Order, pk=order_id)

    return render(
        request,
        "Car/order_success.html",
        {
            "brands": brands,
            "order": order,
        },
    )


def page1(request):
    brands = _get_brands()
    return render(
        request, "Car/page1.html", {"text": "Це сторінка 1", "brands": brands}
    )


def page2(request):
    brands = _get_brands()
    return render(
        request, "Car/page2.html", {"text": "Це сторінка 2", "brands": brands}
    )


def subscribe(request):
    # Форма розсилки (вбудована в `base.html`)
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            name = form.cleaned_data.get("name", "")
            sub, created = MailingSubscription.objects.get_or_create(
                email=email, defaults={"name": name}
            )
            if not created and name and sub.name != name:
                sub.name = name
                sub.save(update_fields=["name"])
            messages.success(request, "Підписку оформлено. Дякуємо!")
        else:
            messages.error(request, "Перевірте форму підписки (email може бути некоректним).")

    return redirect("home")
