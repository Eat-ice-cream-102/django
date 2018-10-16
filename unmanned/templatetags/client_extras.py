from django import template
import time
from unmanned.models import InOrOut

register = template.Library()


@register.filter(name='mul')
def mul(value, var):
    return round(float(value) * var)


@register.filter(name='time_tran')
def time_tran(in_time):
    ans_time = time.mktime(in_time.timetuple())
    return round(ans_time)


@register.filter(name='order_detail_total')
def order_detail_total(price, qut):
    return price*qut


@register.filter(name='avg_price')
def avg_price(time, price):
    return price/time


@register.filter(name='all_price')
def all_price(come_time):
    total = InOrOut.objects.raw("""
    select sum(quantity*price) as total ,inorout.come_time
    from inorout
    left join purchase
    on inorout.come_time=purchase.come_time
    left join product
    on purchase.product_id=product.product_id
    where inorout.come_time = "{}"
    group by inorout.come_time""".format(come_time))

    return total[0].total
