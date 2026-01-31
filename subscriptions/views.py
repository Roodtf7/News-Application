"""
Views for the subscriptions application.
Implements the business logic for subscribing to and unsubscribing from publishers and journalists.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages
from .models import Subscription
from publishers.models import Publisher
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def subscription_list(request):
    """List all subscriptions for the current user."""
    subscriptions = Subscription.objects.filter(reader=request.user)
    return render(request, "subscriptions/subscription_list.html", {
        "subscriptions": subscriptions
    })

@login_required
def subscribe(request):
    """Subscribe to a publisher or journalist."""
    if request.method == "POST":
        publisher_id = request.POST.get("publisher_id")
        journalist_id = request.POST.get("journalist_id")
        
        try:
            if publisher_id:
                publisher = get_object_or_404(Publisher, id=publisher_id)
                Subscription.objects.get_or_create(reader=request.user, publisher=publisher)
                messages.success(request, f"Subscribed to {publisher.name}.")
                
            elif journalist_id:
                journalist = get_object_or_404(User, id=journalist_id)
                if journalist.role != "journalist":
                     messages.error(request, "User is not a journalist.")
                else:
                    Subscription.objects.get_or_create(reader=request.user, journalist=journalist)
                    messages.success(request, f"Subscribed to {journalist.username}.")
        except Exception as e:
            messages.error(request, f"Error subscribing: {e}")
            
    # Redirect back to where the user came from, or home
    next_url = request.POST.get("next") or "landing-page"
    return redirect(next_url)

@login_required
def unsubscribe(request, subscription_id):
    """Unsubscribe from a subscription."""
    subscription = get_object_or_404(Subscription, id=subscription_id, reader=request.user)
    
    if request.method == "POST":
        target = subscription.publisher or subscription.journalist
        subscription.delete()
        messages.success(request, f"Unsubscribed from {target}.")
        return redirect("subscription-list")
        
    return render(request, "subscriptions/unsubscribe.html", {
        "subscription": subscription
    })
