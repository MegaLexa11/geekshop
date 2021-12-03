from django.db import models
from django.conf import settings
from basketapp.models import Product


# Create your models here.
class Order(models.Model):
    STATUS_FORMING = 'FM'
    STATUS_SENT_TO_PROCEED = 'STP'
    STATUS_PROCEEDING = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_READY = 'RDY'
    STATUS_CANCELED = 'CNC'

    ORDER_STATUS = {
        (STATUS_FORMING, 'формируется'),
        (STATUS_SENT_TO_PROCEED, 'отправлен в обрабоотку'),
        (STATUS_PROCEEDING, 'обрабатывается'),
        (STATUS_PAID, 'оплачен'),
        (STATUS_READY, 'готов к выдаче'),
        (STATUS_CANCELED, 'отменен'),
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    status = models.CharField(max_length=3, choices=ORDER_STATUS, default=STATUS_FORMING, verbose_name='статус')
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    @property
    def total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.product_cost, _items)))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
