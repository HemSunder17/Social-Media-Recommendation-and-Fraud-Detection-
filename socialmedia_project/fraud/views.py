from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FraudReport
from posts.models import Post
from accounts.models import User


@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')

        # Prevent reporting your own post
        if post.author == request.user:
            messages.error(request, 'You cannot report your own post')
            return redirect('posts:feed')

        # Prevent duplicate reports
        already_reported = FraudReport.objects.filter(
            reported_by=request.user,
            post=post
        ).exists()

        if already_reported:
            messages.warning(request, 'You have already reported this post')
            return redirect('posts:feed')

        FraudReport.objects.create(
            report_type='post',
            reason=reason,
            reported_by=request.user,
            reported_user=post.author,
            post=post,
            auto_detected=False,
        )

        # If a post gets 3 or more reports, auto flag it
        report_count = FraudReport.objects.filter(post=post).count()
        if report_count >= 3:
            post.is_flagged = True
            post.flag_reason = 'Reported by multiple users'
            post.save()

        messages.success(request, 'Post reported successfully. Our team will review it.')
        return redirect('posts:feed')

    return render(request, 'fraud/report.html', {'post': post})


@login_required
def fraud_dashboard(request):
    # Only superusers can access the dashboard
    if not request.user.is_superuser:
        messages.error(request, 'Access denied')
        return redirect('posts:feed')

    reports = FraudReport.objects.all().order_by('-created_at')
    flagged_posts = Post.objects.filter(is_flagged=True).order_by('-created_at')
    flagged_users = User.objects.filter(is_flagged=True).order_by('-date_joined')

    total_reports = reports.count()
    pending_reports = reports.filter(status='pending').count()
    auto_detected = reports.filter(auto_detected=True).count()

    return render(request, 'fraud/dashboard.html', {
        'reports': reports,
        'flagged_posts': flagged_posts,
        'flagged_users': flagged_users,
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'auto_detected': auto_detected,
    })