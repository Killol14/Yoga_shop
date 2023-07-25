from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

from .contexts import bag_contents

def view_bag(request):
    context = bag_contents(request) 
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """ Adding Item to Bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size')
    color = request.POST.get('product_color')

    bag = request.session.get('bag', {})

    if size:
        if item_id in bag.keys():
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size]['quantity'] += quantity
                messages.success(request, f'You have updated the size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]["quantity"]}')
            else:
                bag[item_id]['items_by_size'][size] = {
                    'quantity': quantity,
                    'color': color 
                }
                messages.success(request, f'You have added a new size {size.upper()} {product.name} to your shopping cart.')
        else:
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'quantity': quantity,
                        'color': color  
                    }
                }
            }
            messages.success(request, f'You have added a new size {size.upper()} {product.name} to your shopping cart.')
    else:
        if item_id in bag.keys():
            bag[item_id]['quantity'] += quantity
            messages.success(request, f'You have updated {product.name} quantity to {bag[item_id]["quantity"]}')
        else:
            bag[item_id] = {
                'quantity': quantity,
                'color': color  # Add the selected color to the bag
            }
            messages.success(request, f'You have added {product.name} to your shopping cart.')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust Item"""

    product = get_object_or_404(Product, pk=item_id)
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    color = request.POST.get('product_color')
    bag = request.session.get('bag', {})

    if size and color:
        if item_id in bag.keys():
            if size in bag[item_id]['items_by_size'].keys():
                if color in bag[item_id]['items_by_size'][size]['colors'].keys():
                    bag[item_id]['items_by_size'][size]['colors'][color] += quantity
                    messages.success(request, f'You have updated the {color} {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]["colors"][color]}')
                else:
                    bag[item_id]['items_by_size'][size]['colors'][color] = quantity
                    messages.success(request, f'You have added a new {color} {size.upper()} {product.name} to your shopping cart.')
            else:
                bag[item_id]['items_by_size'][size] = {
                    'colors': {
                        color: quantity
                    }
                }
                messages.success(request, f'You have added a new {color} {size.upper()} {product.name} to your shopping cart.')
        else:
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'colors': {
                            color: quantity
                        }
                    }
                }
            }
            messages.success(request, f'You have added a new {color} {size.upper()} {product.name} to your shopping cart.')
    elif size:
        messages.warning(request, 'Please select a color for the product.')
        
    else:
        quantity = request.POST.get('quantity')
        if quantity is not None:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    bag[item_id] = quantity
                    messages.success(request, f'You have updated {product.name} quantity to {bag[item_id]}')
                else:
                    bag.pop(item_id)
                    messages.success(request, f'You have removed the item {product.name} from your shopping cart.')
            except ValueError:
                messages.error(request, 'Invalid quantity value.')
        else:
            messages.error(request, 'Quantity not provided.')
        

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove the"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'You Have Removed size {product.name} from your Shopping Cart.')
        else:
            bag.pop(item_id)
            messages.success(request, f'You Have Removed the item {product.name} from your Shopping Cart.')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        message.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)