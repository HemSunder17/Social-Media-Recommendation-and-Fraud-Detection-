from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Post, Like, Comment
from fraud.utils import check_post_fraud, check_comment_fraud


@login_required
def feed_view(request):
    user_interests = request.user.interests.values_list('name', flat=True)

    if user_interests:
        posts = Post.objects.filter(
            category__in=user_interests,
            is_flagged=False
        ).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_flagged=False).order_by('-created_at')

    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'liked_posts': liked_posts,
    })


@login_required
def create_post(request):
    from accounts.models import INTEREST_CHOICES
    if request.method == 'POST':
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if not content or not category:
            messages.error(request, 'Content and category are required')
            return redirect('posts:create_post')

        post = Post(author=request.user, content=content, category=category)
        if image:
            post.image = image

        # Run fraud detection before saving
        is_fraud, reason = check_post_fraud(content, request.user)
        if is_fraud:
            post.is_flagged = True
            post.flag_reason = reason

        post.save()

        if is_fraud:
            messages.warning(request, f'Your post was flagged: {reason}')
        else:
            messages.success(request, 'Post created successfully!')

        return redirect('posts:feed')

    from accounts.models import INTEREST_CHOICES
    return render(request, 'posts/create_post.html', {'interests': INTEREST_CHOICES})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            is_fraud, reason = check_comment_fraud(content)
            comment = Comment.objects.create(
                user=request.user,
                post=post,
                content=content,
                is_flagged=is_fraud
            )
            if is_fraud:
                messages.warning(request, 'Your comment was flagged for review.')

    return redirect('posts:feed')


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('posts:feed')