from django.contrib import admin

# Register your models here.
# marketplace/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Agent, AgentVersion, Transaction, Review

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'developer_link',
        'category',
        'pricing_display',
        'rating_display',
        'status_display',
        'created_at'
    ]
    list_filter = [
        'category',
        'pricing_model',
        'is_active',
        'is_featured',
        'is_verified',
        'tested_by_platform',
        'risk_rating',
    ]
    search_fields = [
        'name',
        'description',
        'developer__username',
        'developer__company_name'
    ]
    readonly_fields = [
        'slug',
        'times_hired',
        'total_api_calls',
        'average_rating',
        'total_reviews',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'slug',
                'developer',
                'category',
                'tags',
                'short_description',
                'description'
            )
        }),
        ('Pricing', {
            'fields': (
                'pricing_model',
                'price',
                'usage_price',
                'free_tier_limit'
            )
        }),
        ('Technical Details', {
            'fields': (
                'api_endpoint',
                'documentation_url',
                'github_url',
                'integration_type',
                'requirements'
            )
        }),
        ('Testing & Sandbox', {
            'fields': (
                'sandbox_available',
                'sandbox_url',
                'demo_url',
                'test_api_key'
            )
        }),
        ('Trust & Safety', {
            'fields': (
                'risk_rating',
                'tested_by_platform',
                'is_verified',
                'security_audit_date',
                'compliance_certifications'
            )
        }),
        ('Performance', {
            'fields': (
                'average_response_time',
                'uptime_percentage',
                'rate_limit'
            )
        }),
        ('Statistics', {
            'fields': (
                'times_hired',
                'total_api_calls',
                'active_subscriptions',
                'average_rating',
                'total_reviews'
            )
        }),
        ('Media', {
            'fields': (
                'logo',
                'screenshots',
                'video_url'
            )
        }),
        ('Status', {
            'fields': (
                'is_active',
                'is_featured',
                'under_review',
                'published_at'
            )
        })
    )
    
    def developer_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.developer.pk])
        return format_html('<a href="{}">{}</a>', url, obj.developer.username)
    developer_link.short_description = 'Developer'
    
    def pricing_display(self, obj):
        if obj.pricing_model == 'usage':
            return f"${obj.usage_price}/call"
        return f"${obj.price}/{obj.get_pricing_model_display()}"
    pricing_display.short_description = 'Pricing'
    
    def rating_display(self, obj):
        avg = obj.average_rating or 0
        stars = '★' * int(avg)
        avg_str = f"{avg:.1f}"             # do numeric formatting first
        reviews = obj.total_reviews or 0

        return format_html(
            '<span style="color: gold;">{}</span> {} ({} reviews)',
            stars, avg_str, reviews
        )
    rating_display.short_description = 'Rating'
    
    def status_display(self, obj):
        statuses = []
        if obj.is_active:
            statuses.append('<span style="color: green;">✓ Active</span>')
        if obj.is_featured:
            statuses.append('<span style="color: blue;">★ Featured</span>')
        if obj.is_verified:
            statuses.append('<span style="color: purple;">✓ Verified</span>')
        if obj.under_review:
            statuses.append('<span style="color: orange;">⚠ Under Review</span>')
        return format_html(' '.join(statuses))
    status_display.short_description = 'Status'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'agent',
        'buyer',
        'seller',
        'amount',
        'platform_fee',
        'status',
        'transaction_type',
        'created_at'
    ]
    list_filter = [
        'status',
        'transaction_type',
        'created_at'
    ]
    search_fields = [
        'agent__name',
        'buyer__username',
        'seller__username',
        'stripe_payment_intent'
    ]
    readonly_fields = [
        'created_at',
        'completed_at'
    ]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('agent', 'buyer', 'seller')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'agent',
        'reviewer',
        'rating_stars',
        'title',
        'verified_purchase',
        'helpful_count',
        'created_at'
    ]
    list_filter = [
        'rating',
        'verified_purchase',
        'reported',
        'created_at'
    ]
    search_fields = [
        'agent__name',
        'reviewer__username',
        'title',
        'comment'
    ]
    readonly_fields = [
        'created_at',
        'updated_at'
    ]
    
    def rating_stars(self, obj):
        return format_html(
            '<span style="color: gold;">{}</span>',
            '★' * obj.rating
        )
    rating_stars.short_description = 'Rating'


@admin.register(AgentVersion)
class AgentVersionAdmin(admin.ModelAdmin):
    list_display = [
        'agent',
        'version_number',
        'is_stable',
        'release_date'
    ]
    list_filter = [
        'is_stable',
        'release_date'
    ]
    search_fields = [
        'agent__name',
        'version_number',
        'changelog'
    ]