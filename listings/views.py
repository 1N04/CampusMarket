from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from django.http import HttpResponseForbidden

from .models import Item, Category
from .forms import ItemForm, ItemSearchForm


def item_list(request):
    """Home page: list all available items with search/filter support."""
    items = Item.objects.filter(is_available=True).select_related('category', 'seller')
    form = ItemSearchForm(request.GET or None)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        condition = form.cleaned_data.get('condition')

        if query:
            items = items.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            items = items.filter(category=category)
        if min_price is not None:
            items = items.filter(price__gte=min_price)
        if max_price is not None:
            items = items.filter(price__lte=max_price)
        if condition:
            items = items.filter(condition=condition)

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'listings/item_list.html', context)


def item_detail(request, pk):
    """Show item details and increment views count."""
    item = get_object_or_404(Item.objects.select_related('category', 'seller'), pk=pk)

    # Increment views count
    Item.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
    item.views_count += 1  # Update in-memory for the template

    context = {
        'item': item,
    }
    return render(request, 'listings/item_detail.html', context)


@login_required
def item_create(request):
    """Create a new item listing."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            messages.success(request, 'Item listed successfully!')
            return redirect(item.get_absolute_url())
    else:
        form = ItemForm()

    context = {
        'form': form,
        'title': 'Create Listing',
    }
    return render(request, 'listings/item_form.html', context)


@login_required
def item_edit(request, pk):
    """Edit an existing item listing. Only the seller can edit."""
    item = get_object_or_404(Item, pk=pk)

    if item.seller != request.user:
        return HttpResponseForbidden('You are not allowed to edit this item.')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect(item.get_absolute_url())
    else:
        form = ItemForm(instance=item)

    context = {
        'form': form,
        'item': item,
        'title': 'Edit Listing',
    }
    return render(request, 'listings/item_form.html', context)


@login_required
def item_delete(request, pk):
    """Delete an item listing. Only the seller can delete."""
    item = get_object_or_404(Item, pk=pk)

    if item.seller != request.user:
        return HttpResponseForbidden('You are not allowed to delete this item.')

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('listings:item_list')

    context = {
        'item': item,
    }
    return render(request, 'listings/item_delete.html', context)


@login_required
def item_toggle_availability(request, pk):
    """Toggle item availability. Only the seller can toggle."""
    item = get_object_or_404(Item, pk=pk)

    if item.seller != request.user:
        return HttpResponseForbidden('You are not allowed to modify this item.')

    item.is_available = not item.is_available
    item.save(update_fields=['is_available'])

    status = 'available' if item.is_available else 'unavailable'
    messages.success(request, f'Item marked as {status}.')
    return redirect(item.get_absolute_url())


def category_list(request):
    """Show all categories with item counts."""
    categories = Category.objects.annotate(
        item_count=Count('items', filter=Q(items__is_available=True))
    )

    context = {
        'categories': categories,
    }
    return render(request, 'listings/category_list.html', context)


def category_items(request, slug):
    """Show items filtered by category."""
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(
        category=category, is_available=True
    ).select_related('seller')

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'listings/category_items.html', context)
