from django.contrib import admin
from .models import FraudReport

@admin.register(FraudReport)
class FraudReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'reason', 'status', 'reported_by', 'reported_user', 'auto_detected', 'created_at')
    list_filter = ('report_type', 'reason', 'status', 'auto_detected')
    search_fields = ('reported_by__username', 'reported_user__username')