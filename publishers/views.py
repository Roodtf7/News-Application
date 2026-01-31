"""
Views for the publishers application.
Handles organizational workflows including publisher creation and member management.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Publisher
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def create_publisher(request):
    """Allow editors to create a new publisher organization."""
    if request.user.role != "editor":
        raise PermissionDenied("Only editors can create publishers.")
    
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            publisher = Publisher.objects.create(name=name)
            # Add the creator as an editor
            publisher.editors.add(request.user)
            return redirect("publisher-detail", publisher_id=publisher.id)
    
    return render(request, "publishers/create_publisher.html")


@login_required
def publisher_list(request):
    """List all publishers."""
    publishers = Publisher.objects.all()
    user_publishers = None
    
    if request.user.role == "editor":
        user_publishers = Publisher.objects.filter(editors=request.user)
    elif request.user.role == "journalist":
        user_publishers = Publisher.objects.filter(journalists=request.user)
    
    return render(request, "publishers/publisher_list.html", {
        "publishers": publishers,
        "user_publishers": user_publishers or [],
    })


@login_required
def publisher_detail(request, publisher_id):
    """View details of a publisher and manage editors/journalists."""
    publisher = get_object_or_404(Publisher, id=publisher_id)
    is_editor = request.user.role == "editor" and request.user in publisher.editors.all()
    
    # Fetch content
    from articles.models import Article, Newsletter
    # Approved articles belonging to this publisher
    articles = Article.objects.filter(publisher=publisher, approved=True).order_by('-published_at')
    
    # Approved newsletters belonging to this publisher
    newsletters = Newsletter.objects.filter(publisher=publisher, approved=True).order_by('-published_at')
    
    # Check subscription status
    from subscriptions.models import Subscription
    subscription = Subscription.objects.filter(reader=request.user, publisher=publisher).first()

    return render(request, "publishers/publisher_detail.html", {
        "publisher": publisher,
        "is_editor": is_editor,
        "articles": articles,
        "newsletters": newsletters,
        "subscription": subscription,
    })


@login_required
def add_editor(request, publisher_id):
    """Add an editor to a publisher (only existing editors can do this)."""
    publisher = get_object_or_404(Publisher, id=publisher_id)
    
    if request.user.role != "editor" or request.user not in publisher.editors.all():
        raise PermissionDenied("Only editors of this publisher can add editors.")
    
    if request.method == "POST":
        editor_id = request.POST.get("editor_id")
        try:
            user = User.objects.get(id=editor_id, role="editor")
            publisher.editors.add(user)
            return redirect("publisher-detail", publisher_id=publisher.id)
        except User.DoesNotExist:
            available_editors = User.objects.filter(role="editor").exclude(id__in=publisher.editors.values_list('id', flat=True))
            return render(request, "publishers/add_editor.html", {
                "publisher": publisher,
                "error": "Editor not found.",
                "available_editors": available_editors
            })
    
    # Get editors not already assigned to this publisher
    available_editors = User.objects.filter(role="editor").exclude(id__in=publisher.editors.values_list('id', flat=True))
    
    return render(request, "publishers/add_editor.html", {
        "publisher": publisher,
        "available_editors": available_editors
    })



@login_required
def join_publisher(request, publisher_id):
    """Allow journalists to join a publisher."""
    if request.user.role != "journalist":
        raise PermissionDenied("Only journalists can join publishers.")
    
    publisher = get_object_or_404(Publisher, id=publisher_id)
    
    if request.method == "POST":
        publisher.journalists.add(request.user)
        return redirect("publisher-detail", publisher_id=publisher.id)
    
    return render(request, "publishers/join_publisher.html", {"publisher": publisher})
