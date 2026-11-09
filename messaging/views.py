from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from listings.models import Item
from .models import Conversation, Message
from .forms import MessageForm, NewConversationForm


@login_required
def inbox(request):
    """List all conversations for the current user (as buyer or seller)."""
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).select_related('item', 'buyer', 'seller').annotate(
        unread_count=Count(
            'messages',
            filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user),
        )
    ).order_by('-updated_at')

    return render(request, 'messaging/inbox.html', {
        'conversations': conversations,
    })


@login_required
def conversation_detail(request, pk):
    """View and send messages within a conversation."""
    conversation = get_object_or_404(
        Conversation.objects.select_related('item', 'buyer', 'seller'),
        pk=pk,
    )

    # Only the buyer or seller can view the conversation
    if request.user not in (conversation.buyer, conversation.seller):
        raise Http404

    # Mark unread messages (sent by the other party) as read
    conversation.messages.filter(is_read=False).exclude(
        sender=request.user
    ).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            # Touch updated_at on the conversation
            conversation.save(update_fields=['updated_at'])
            return redirect('messaging:conversation_detail', pk=conversation.pk)
    else:
        form = MessageForm()

    messages_list = conversation.messages.select_related('sender').all()

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages_list': messages_list,
        'form': form,
    })


@login_required
def start_conversation(request, item_pk):
    """Start a new conversation about an item, or redirect to existing one."""
    item = get_object_or_404(Item.objects.select_related('seller'), pk=item_pk)

    # Seller cannot message themselves
    if request.user == item.seller:
        return redirect('listings:item_detail', pk=item.pk)

    # Check if conversation already exists
    existing = Conversation.objects.filter(item=item, buyer=request.user).first()
    if existing:
        return redirect('messaging:conversation_detail', pk=existing.pk)

    if request.method == 'POST':
        form = NewConversationForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(
                item=item,
                buyer=request.user,
                seller=item.seller,
            )
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=form.cleaned_data['message'],
            )
            return redirect('messaging:conversation_detail', pk=conversation.pk)
    else:
        form = NewConversationForm()

    return render(request, 'messaging/start_conversation.html', {
        'item': item,
        'form': form,
    })
