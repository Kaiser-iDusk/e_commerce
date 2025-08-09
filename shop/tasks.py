from celery import shared_task
from django.core.mail import send_mail

from shop.models import Order

@shared_task
def send_order_confirmation_email(order_id):
    # Example task for order confirmation email
    order = Order.objects.get(id=order_id)
    send_mail(
        'Order Confirmation',
        f'Your order {order.id} has been confirmed.',
        'from@example.com',
        [order.user.email],
        fail_silently=False,
    )