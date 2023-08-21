from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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
        if item_id in bag:
            if 'items_by_size' in bag[item_id]:
                if size in bag[item_id]['items_by_size']:
                    if colour:
                        if colour in bag[item_id]['items_by_size'][size]['colours']:
                            bag[item_id]['items_by_size'][size]['colours'][colour] += quantity
                        else:
                            bag[item_id]['items_by_size'][size]['colours'][colour] = quantity
                    else:
                        bag[item_id]['items_by_size'][size] = quantity
                    messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
                else:
                    bag[item_id]['items_by_size'][size] = {
                        'colours': {
                            colour: quantity
                        }
                    } if colour else quantity
                    messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
            else:
                bag[item_id]['items_by_size'] = {
                    size: {
                        'colours': {
                            colour: quantity
                        }
                    }
                } if colour else {
                    size: quantity
                }
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'colours': {
                            colour: quantity
                        }
                    }
                }
            } if colour else {
                'items_by_size': {
                    size: quantity
                }
            }
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in bag:
            if colour:
                if 'items_by_colour' in bag[item_id]:
                    if colour in bag[item_id]['items_by_colour']:
                        bag[item_id]['items_by_colour'][colour] += quantity
                    else:
                        bag[item_id]['items_by_colour'][colour] = quantity
                else:
                    bag[item_id]['items_by_colour'] = {
                        colour: quantity
                    }
            else:
                bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = {
                'quantity': quantity,
                'colour': colour
            } if colour else {
                'quantity': quantity
            }
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size')
    colour = request.POST.get('product_colour')  # Changed "color" to "colour"
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            if colour:
                if 'items_by_colour' not in bag[item_id]:
                    bag[item_id]['items_by_colour'] = {}
                bag[item_id]['items_by_colour'][colour] = quantity
            else:
                bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            if colour:
                if 'items_by_colour' in bag[item_id]:
                    del bag[item_id]['items_by_colour'][colour]
            else:
                bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = request.POST.get('product_size')
        colour = request.POST.get('product_colour')  # Changed "color" to "colour"
        bag = request.session.get('bag', {})

        if size:
            if colour in bag[item_id]['items_by_size'][size]['colours']:
                del bag[item_id]['items_by_size'][size]['colours'][colour]
                if not bag[item_id]['items_by_size'][size]['colours']:
                    del bag[item_id]['items_by_size'][size]
                    if not bag[item_id]['items_by_size']:
                        bag.pop(item_id)
                messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            if colour:
                if colour in bag[item_id]['items_by_colour']:
                    del bag[item_id]['items_by_colour'][colour]
                    if not bag[item_id]['items_by_colour']:
                        bag.pop(item_id)
                messages.success(request, f'Removed {product.name} from your bag')
            else:
                bag.pop(item_id)
                messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)