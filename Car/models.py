from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

class Brand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.IntegerField()
    photo = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    # Використовуємо session_key, щоб анонімні користувачі теж могли
    # "оцінити самі" без логіну.
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    text = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.car.name}"

    class Meta:
        constraints = [
            # Забороняємо повторно створювати оцінку для одного авто в межах однієї сесії.
            models.UniqueConstraint(
                fields=["car", "session_key"],
                condition=Q(session_key__isnull=False),
                name="unique_review_per_car_session",
            )
        ]


class MailingSubscription(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('card', 'Банківська картка'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Очікує оплати'),
        ('paid', 'Оплачено'),
        ('processing', 'В обробці'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    # Контактна інформація
    full_name = models.CharField(max_length=200, verbose_name="Повне ім'я")
    phone = models.CharField(max_length=20, verbose_name="Номер телефону")
    email = models.EmailField(verbose_name="Email")

    # Інформація про доставку
    delivery_address = models.TextField(verbose_name="Адреса доставки")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Час доставки")

    # Оплата
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Спосіб оплати"
    )

    # Деталі замовлення
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна сума")
    cart_data = models.JSONField(verbose_name="Дані кошика")  # Зберігаємо інформацію про товари

    # Статус
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )

    # Додаткові примітки
    notes = models.TextField(blank=True, verbose_name="Додаткові примітки")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Замовлення #{self.pk} - {self.full_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
# Create your models here.
