from django import forms


class RatingForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        label="Ваша оцінка (1-5)",
    )
    text = forms.CharField(
        required=False,
        label="Коментар (необов'язково)",
        widget=forms.Textarea(attrs={"rows": 3}),
    )


class NewsletterForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, label="Ім'я")
    email = forms.EmailField(required=True, label="Email")


class CheckoutForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('card', 'Банківська картка'),
    ]

    # Контактна інформація
    full_name = forms.CharField(
        max_length=200,
        required=True,
        label="Повне ім'я",
        widget=forms.TextInput(attrs={'placeholder': 'Іван Іванович Іваненко'})
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        label="Номер телефону",
        widget=forms.TextInput(attrs={'placeholder': '+380501234567'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'})
    )

    # Інформація про доставку
    delivery_address = forms.CharField(
        required=True,
        label="Адреса доставки",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'м. Київ, вул. Хрещатик, 1'})
    )
    delivery_date = forms.DateField(
        required=True,
        label="Дата доставки (забору автомобіля)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    delivery_time = forms.TimeField(
        required=True,
        label="Час доставки (забору автомобіля)",
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    # Спосіб оплати
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        required=True,
        label="Спосіб оплати",
        widget=forms.RadioSelect
    )

    # Додаткові примітки
    notes = forms.CharField(
        required=False,
        label="Додаткові примітки",
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Будь-які додаткові побажання...'})
    )

