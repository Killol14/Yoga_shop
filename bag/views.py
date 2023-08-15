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
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    colour = None
    if 'product_color' in request.POST:
        colour = request.POST['product_color']

    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size]['quantity'] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')
    if colour:
        if item_id in bag:
            if 'items_by_colour' in bag[item_id]:
                if colour in bag[item_id]['items_by_colour']:
                    bag[item_id]['items_by_colour'][colour]['quantity'] += quantity
                else:
                    bag[item_id]['items_by_colour'][colour] = {'quantity': quantity, 'size': None}
            else:
                bag[item_id]['items_by_colour'] = {colour: {'quantity': quantity, 'size': None}}
        else:
            bag[item_id] = {'items_by_colour': {colour: {'quantity': quantity, 'size': None}}}
    else:
        if item_id in bag:
            bag[item_id]['quantity'] += quantity
        else:
            bag[item_id] = {'quantity': quantity}


    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust Item"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    colour = None
    if 'product_color' in request.POST:
        colour = request.POST['product_color']

    bag = request.session.get('bag', {})

    if size and colour:
        if item_id in bag.keys():
            if size in bag[item_id]['items_by_size'].keys():
                if colour in bag[item_id]['items_by_size'][size]['colours'].keys():
                    bag[item_id]['items_by_size'][size]['colours'][colour] += quantity
                    messages.success(request, f'You have updated the {colour} {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]["colours"][colour]}')
                else:
                    bag[item_id]['items_by_size'][size]['colours'][colour] = quantity
                    messages.success(request, f'You have added a new {colour} {size.upper()} {product.name} to your shopping cart.')
            else:
                bag[item_id]['items_by_size'][size] = {
                    'colours': {
                        colour: quantity
                    }
                }
                messages.success(request, f'You have added a new {colour} {size.upper()} {product.name} to your shopping cart.')
        else:
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'colours': {
                            colour: quantity
                        }
                    }
                }
            }
            messages.success(request, f'You have added a new {colour} {size.upper()} {product.name} to your shopping cart.')
    elif size:
        messages.warning(request, 'Please select a color for the product.')
    else:
        if item_id in bag.keys():
            bag[item_id]['quantity'] += quantity  
            messages.success(request, f'You have updated {product.name} quantity to {bag[item_id]["quantity"]}')
        else:
            bag[item_id] = {
                'quantity': quantity,
                'colour': colour
            }
            messages.success(request, f'You have added {product.name} to your shopping cart.')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove the item from the bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        colour = None
        bag = request.session.get('bag', {})

        if item_id in bag.keys():
            if 'items_by_size' in bag[item_id]:
                size = request.POST.get('product_size')
                if size in bag[item_id]['items_by_size']:
                    colour = request.POST.get('product_color')
                    if colour in bag[item_id]['items_by_size'][size]['colours']:
                        del bag[item_id]['items_by_size'][size]['colours'][colour]
                        if not bag[item_id]['items_by_size'][size]['colours']:
                            del bag[item_id]['items_by_size'][size]
                            if not bag[item_id]['items_by_size']:
                                bag.pop(item_id)
                                messages.success(request, f'You Have Removed size {product.name} from your Shopping Cart.')
                            else:
                                messages.success(request, f'You Have Removed colour {colour} from size {product.name} in your Shopping Cart.')
                        else:
                            messages.success(request, f'You Have Removed colour {colour} from size {product.name} in your Shopping Cart.')
                    else:
                        messages.error(request, f'Colour {colour} not found in size {product.name}.')
                else:
                    bag.pop(item_id)
                    messages.success(request, f'You Have Removed the item {product.name} from your Shopping Cart.')
            else:
                bag.pop(item_id)
                messages.success(request, f'You Have Removed the item {product.name} from your Shopping Cart.')
        else:
            messages.error(request, f'Item {product.name} not found in your Shopping Cart.')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)