"""
Views for the articles application.
Handles the logic for article feeds, detail views, and the editorial approval process.
"""
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from articles.models import Article, Newsletter
from publishers.models import Publisher
from django.utils import timezone
from django.db.models import Q
import json
import os
from pathlib import Path


@permission_required("articles.view_article")
def pending_articles(request):
    """View articles and newsletters waiting for approval."""
    if request.user.role == "editor":
        # Get all publishers this editor belongs to
        user_publishers = Publisher.objects.filter(editors=request.user)
        articles = Article.objects.filter(
            approved=False,
            publisher__in=user_publishers,
            is_independent=False
        )
        newsletters = Newsletter.objects.filter(
            approved=False,
            publisher__in=user_publishers,
            is_independent=False
        )
    else:
        # Readers/Journalists shouldn't normally access this, but if they do:
        articles = Article.objects.filter(approved=False, is_independent=False)
        newsletters = Newsletter.objects.filter(approved=False, is_independent=False)
    
    return render(request, "articles/pending_articles.html", {
        "articles": articles,
        "newsletters": newsletters
    })



@permission_required("articles.change_article")
def approve_article(request, article_id):
    """Approve a pending article."""
    article = get_object_or_404(Article, id=article_id)
    
    # Check if user is an editor of the publisher
    if request.user.role == "editor" and article.publisher and request.user in article.publisher.editors.all():
        article.approve(request.user)
        from django.contrib import messages
        messages.success(request, f"Article '{article.title}' approved!")
    else:
        from django.contrib import messages
        messages.error(request, "You do not have permission to approve this article.")
        
    return redirect("pending-articles")


@permission_required("articles.change_article")
def approve_newsletter(request, newsletter_id):
    """Approve a pending newsletter."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    
    # Check if user is an editor of the publisher
    if request.user.role == "editor" and newsletter.publisher and request.user in newsletter.publisher.editors.all():
        newsletter.approve(request.user)
        from django.contrib import messages
        messages.success(request, f"Newsletter '{newsletter.title}' approved!")
    else:
        from django.contrib import messages
        messages.error(request, "You do not have permission to approve this newsletter.")
        
    return redirect("pending-articles")






@login_required
def article_list(request):
    """
    Display a list of articles, newsletters, publishers, or journalists.
    Supports filtering by type and authorship.
    """
    content_type = request.GET.get("type", "articles")  # articles, newsletters, publishers, journalists, subscriptions
    filter_type = request.GET.get("filter", "all")
    author_id = request.GET.get('author')
    
    context = {
        "content_type": content_type,
        "filter_type": filter_type,
        "author_id": author_id,
    }

    # Base QuerySets for generic feed (Approved or Independent)
    articles_qs = Article.objects.filter(Q(is_independent=True) | Q(approved=True))
    newsletters_qs = Newsletter.objects.filter(Q(is_independent=True) | Q(approved=True)).distinct()

    if content_type == "newsletters":
        if request.user.is_authenticated and request.user.role == "journalist" and filter_type == "my":
            newsletters = request.user.journalist_newsletters
        else:
            newsletters = newsletters_qs
        
        context["newsletters"] = newsletters
        return render(request, "articles/article_list.html", context)
    
    elif content_type == "publishers":
        publishers = Publisher.objects.all()
        user_publishers = []
        if request.user.is_authenticated:
            if request.user.role == "editor":
                user_publishers = Publisher.objects.filter(editors=request.user)
            elif request.user.role == "journalist":
                user_publishers = Publisher.objects.filter(journalists=request.user)
            
        context["publishers"] = publishers
        context["user_publishers"] = user_publishers
        return render(request, "articles/article_list.html", context)

    elif content_type == "journalists":
        from django.contrib.auth import get_user_model
        User = get_user_model()
        journalists = User.objects.filter(role="journalist")
        context["journalists"] = journalists
        return render(request, "articles/article_list.html", context)

    elif content_type == "subscriptions":
        from subscriptions.models import Subscription
        sub_type = request.GET.get("sub_type", "all")
        subscriptions = Subscription.objects.filter(reader=request.user)
        
        if sub_type == "journalist":
            subscriptions = subscriptions.filter(journalist__isnull=False)
        elif sub_type == "publisher":
            subscriptions = subscriptions.filter(publisher__isnull=False)
            
        context["subscriptions"] = subscriptions
        context["sub_type"] = sub_type
        return render(request, "articles/article_list.html", context)

    # DEFAULT: Articles list
    articles = articles_qs
    if request.user.is_authenticated and request.user.role == "journalist" and filter_type == "my" and not author_id:
        articles = request.user.journalist_articles
    
    if author_id:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        selected_author = get_object_or_404(User, id=author_id)
        articles = articles.filter(author=selected_author)
        # Newsletters for this author must also be filtered by visibility for others
        author_newsletters = selected_author.newsletters.filter(Q(is_independent=True) | Q(approved=True)).distinct()
        context["newsletters"] = author_newsletters
        context["selected_author"] = selected_author

    context["articles"] = articles

    # Fetch user's subscription IDs for UI indicators
    from subscriptions.models import Subscription
    user_subs = Subscription.objects.filter(reader=request.user)
    context["subscribed_journalist_ids"] = list(user_subs.filter(journalist__isnull=False).values_list('journalist_id', flat=True))

    return render(request, "articles/article_list.html", context)


@login_required
def create_article(request):
    """
    Handle the creation of a new article by a journalist.
    Supports independent publishing or submission to a publisher for approval.
    """
    
    if request.user.role != "journalist":
        return redirect("article-list")

    # Get publishers this journalist belongs to
    user_publishers = Publisher.objects.filter(journalists=request.user)
    
    if request.method == "POST":
        publish_type = request.POST.get("publish_type")  # "independent" or "publisher"
        publisher_id = request.POST.get("publisher")
        
        article_data = {
            "title": request.POST["title"],
            "body": request.POST["content"],
            "author": request.user,
        }
        
        if publish_type == "independent":
            # Independent publishing - visible immediately to readers
            article_data["is_independent"] = True
            article_data["approved"] = True  # Independent articles are auto-approved
            article_data["published_at"] = timezone.now()
        else:
            # Publisher submission - requires approval
            article_data["is_independent"] = False
            article_data["approved"] = False
            if publisher_id:
                article_data["publisher_id"] = publisher_id
        
        article = Article.objects.create(**article_data)
        return redirect("article-list")

    return render(request, "articles/create_article.html", {
        "publishers": user_publishers
    })


@login_required
def article_detail(request, article_id):
    """
    Display the details of a specific article.
    Enforces visibility permissions for readers.
    """
    article = get_object_or_404(Article, id=article_id)
    
    # Check permissions: editors/journalists can see all, readers only see approved or independent
    if request.user.role == "reader" and not article.approved and not article.is_independent:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You don't have permission to view this article.")
    
    return render(request, "articles/article_detail.html", {"article": article})


@login_required
def update_article(request, article_id):
    """
    Update an existing article.
    Enforces permission: only the author or an editor can update.
    """
    article = get_object_or_404(Article, id=article_id)
    
    # Check permissions: editors can edit any, journalists only their own
    if request.user.role not in ["editor", "journalist"]:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You don't have permission to edit articles.")
    
    if request.user.role == "journalist" and article.author != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You can only edit your own articles.")
    
    if request.method == "POST":
        article.title = request.POST["title"]
        article.body = request.POST["content"]
        article.save()
        return redirect("article-detail", article_id=article.id)
    
    return render(request, "articles/update_article.html", {"article": article})


@login_required
def delete_article(request, article_id):
    """
    Delete an existing article.
    Enforces permission: only the author or an editor can delete.
    """
    article = get_object_or_404(Article, id=article_id)
    
    # Check permissions: editors can delete any, journalists only their own
    if request.user.role not in ["editor", "journalist"]:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You don't have permission to delete articles.")
    
    if request.user.role == "journalist" and article.author != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You can only delete your own articles.")
    
    if request.method == "POST":
        article.delete()
        return redirect("article-list")
    
    return render(request, "articles/delete_article.html", {"article": article})


@login_required
def create_newsletter(request):
    """Allow journalists to create newsletters."""
    if request.user.role != "journalist":
        return redirect("article-list")
    
    if request.method == "POST":
        publish_type = request.POST.get("publish_type")
        publisher_id = request.POST.get("publisher")
        
        newsletter = Newsletter.objects.create(
            title=request.POST["title"],
            body=request.POST["content"],
            author=request.user,
            is_independent=(publish_type == "independent"),
            approved=(publish_type == "independent"),
            published_at=timezone.now() if publish_type == "independent" else None,
            publisher_id=publisher_id if publish_type == "publisher" and publisher_id else None
        )
        return redirect(reverse("article-list") + "?type=newsletters")
    
    context = {
        "publishers": Publisher.objects.filter(journalists=request.user)
    }
    return render(request, "articles/create_newsletter.html", context)



@login_required
def newsletter_detail(request, newsletter_id):
    """View a newsletter in detail."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    return render(request, "articles/newsletter_detail.html", {"newsletter": newsletter})


@login_required
def update_newsletter(request, newsletter_id):
    """Update a newsletter (author or publisher editor)."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    
    is_author = request.user == newsletter.author
    is_editor = (
        request.user.role == "editor" and 
        newsletter.publisher and 
        newsletter.publisher.editors.filter(id=request.user.id).exists()
    )
    
    if not (is_author or is_editor):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You can only edit your own newsletters or those of your publisher.")
    
    if request.method == "POST":
        newsletter.title = request.POST["title"]
        newsletter.body = request.POST["content"]
        newsletter.save()
        from django.contrib import messages
        messages.success(request, "Newsletter updated successfully.")
        return redirect("newsletter-detail", newsletter_id=newsletter.id)
    
    return render(request, "articles/update_newsletter.html", {"newsletter": newsletter})


@login_required
def delete_newsletter(request, newsletter_id):
    """Delete a newsletter (author or publisher editor)."""
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    
    is_author = request.user == newsletter.author
    is_editor = (
        request.user.role == "editor" and 
        newsletter.publisher and 
        newsletter.publisher.editors.filter(id=request.user.id).exists()
    )
    
    if not (is_author or is_editor):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You can only delete your own newsletters or those of your publisher.")
    
    if request.method == "POST":
        newsletter.delete()
        from django.contrib import messages
        messages.success(request, "Newsletter deleted.")
        return redirect(reverse("article-list") + "?type=newsletters")
    
    return render(request, "articles/delete_newsletter.html", {"newsletter": newsletter})

