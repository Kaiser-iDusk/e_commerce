from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, CartItem, Order, OrderItem, ReturnRequest
from accounts.models import Address
from accounts.forms import AddressForm, DeliveryTimeForm, ReturnRequestForm
from django.core.mail import send_mail
from django.conf import settings
import uuid
from datetime import datetime
from django.utils import timezone
from celery import shared_task

@shared_task
def send_delivery_notification(order_id):
    order = Order.objects.get(order_id=order_id)
    if timezone.now() >= order.preferred_delivery_time:
        send_mail(
            'Your Order is Out for Delivery',
            f'Order {order.order_id} is out for delivery to {order.address}.',
            settings.EMAIL_HOST_USER,
            [order.user.email],
            fail_silently=False,
        )

@login_required
def home(request):
    products = Product.objects.all()
    recommendations = Product.objects.order_by('?')[:4]
    return render(request, 'shop/home.html', {'products': products, 'recommendations': recommendations})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def update_cart_quantity(request, pk, action):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
            return redirect('cart')
    cart_item.save()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'{item.product.name} is out of stock.')
            recommendations = Product.objects.exclude(pk=item.product.pk).order_by('?')[:4]
            return render(request, 'shop/out_of_stock.html', {'product': item.product, 'recommendations': recommendations})

    if request.method == 'POST':
        address_form = AddressForm(request.user, request.POST)
        delivery_form = DeliveryTimeForm(request.POST)
        if address_form.is_valid() and delivery_form.is_valid():
            if address_form.cleaned_data['use_existing'] and address_form.cleaned_data['existing_address']:
                address = address_form.cleaned_data['existing_address']
            else:
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()

            total_amount = sum(item.product.price * item.quantity for item in cart_items)
            order = Order.objects.create(
                user=request.user,
                order_id=str(uuid.uuid4()),
                address=address,
                preferred_delivery_time=delivery_form.cleaned_data['preferred_delivery_time'],
                payment_method='Pending',
                total_amount=total_amount,
                status='confirmed'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                item.product.stock -= item.quantity
                if item.product.stock <= 0:
                    item.product.delete()
                else:
                    item.product.save()
                item.delete()

            request.session['order_id'] = order.order_id
            return redirect('payment')
        else:
            # Log form errors for debugging
            print(address_form.errors, delivery_form.errors)
    else:
        address_form = AddressForm(user=request.user)
        delivery_form = DeliveryTimeForm()

    return render(request, 'shop/checkout.html', {
        'address_form': address_form,
        'delivery_form': delivery_form,
        'cart_items': cart_items
    })

@login_required
def payment(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, 'No order found.')
        return redirect('cart')

    order = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order.payment_method = payment_method
        order.status = 'Confirmed'
        order.save()
        send_delivery_notification.delay(order.order_id)
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success', order_id=order.order_id)
    
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery']
    return render(request, 'shop/payment.html', {'order': order, 'payment_methods': payment_methods})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})

@login_required
def return_request(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if request.method == 'POST':
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.order = order
            return_request.save()
            send_mail(
                'Return Request Submitted',
                f'Your return request for Order {order.order_id} has been submitted. Description: {return_request.description}',
                settings.EMAIL_HOST_USER,
                [order.user.email],
                fail_silently=False,
            )
            messages.success(request, 'Return request submitted.')
            return redirect('profile')
    else:
        form = ReturnRequestForm()
    return render(request, 'shop/return_request.html', {'form': form, 'order': order})

@login_required
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'shop/search.html', {'products': products, 'query': query})