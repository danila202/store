from django.db import models
from user.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUS = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен')
    )

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=62)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=150)
    basket_history = models.JSONField(default=dict)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id } {self.first_name} {self.last_name}'

