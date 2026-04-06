from django.db import models
from accounts.models import User
from posts.models import Post, Comment


class FraudReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('account', 'Account'),
    ]

    REASON_CHOICES = [
        ('hate_speech', 'Hate Speech'),
        ('abusive', 'Abusive Content'),
        ('spam', 'Spam'),
        ('irrelevant', 'Irrelevant Content'),
        ('fake_account', 'Fake Account'),
        ('harassment', 'Harassment'),
        ('misinformation', 'Misinformation'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_received')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    auto_detected = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} | {self.reason} | {self.status}"