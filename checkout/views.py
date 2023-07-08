from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your cart for Now!")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51NRh0NDezu7U4f762ZiUayuvAU3uTjnA0ln1o25qdxg5Vi10FouEHvFwAGj1zbSgp9kHEURVRnLI5MwzuZ6Xaj43009cz2qCSW',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)