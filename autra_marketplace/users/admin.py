from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, DeveloperProfile, BusinessProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 
        'email', 
        'user_type_badge', 
        'company_name', 
        'verified_badge',
        'trust_score',
        'created_at'
    ]
    list_filter = [
        'user_type', 
        'verified', 
        'is_active',
        'created_at'
    ]
    search_fields = [
        'username', 
        'email', 
        'company_name', 
        'first_name', 
        'last_name'
    ]
    
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {
            'fields': ('user_type',)
        }),
        ('Profile Information', {
            'fields': (
                'company_name', 
                'bio', 
                'phone_number', 
                'website', 
                'location',
                'avatar'
            )
        }),
        ('Developer Information', {
            'fields': (
                'github_username', 
                'linkedin_url', 
                'portfolio_url', 
                'skills',
                'years_of_experience'
            ),
            'classes': ('collapse',)
        }),
        ('Business Information', {
            'fields': (
                'industry', 
                'company_size'
            ),
            'classes': ('collapse',)
        }),
        ('Verification & Trust', {
            'fields': (
                'verified', 
                'verification_date', 
                'trust_score'
            )
        }),
        ('Payment Information', {
            'fields': (
                'stripe_customer_id', 
                'stripe_account_id',
                'total_spent',
                'total_earned'
            ),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': (
                'email_notifications', 
                'sms_notifications', 
                'newsletter_subscription'
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Type', {
            'fields': ('user_type', 'email')
        }),
    )
    
    def user_type_badge(self, obj):
        colors = {
            'developer': '#28a745',
            'business': '#007bff'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.user_type, '#6c757d'),
            obj.get_user_type_display()
        )
    user_type_badge.short_description = 'Type'
    
    def verified_badge(self, obj):
        if obj.verified:
            return format_html(
                '<span style="color: #28a745;">✓ Verified</span>'
            )
        return format_html(
            '<span style="color: #dc3545;">✗ Not Verified</span>'
        )
    verified_badge.short_description = 'Verified'


@admin.register(DeveloperProfile)
class DeveloperProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'available_for_custom_work', 
        'hourly_rate',
        'total_agents',
        'successful_deployments'
    ]
    list_filter = ['available_for_custom_work', 'preferred_project_size']
    search_fields = ['user__username', 'user__email']


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'preferred_budget_range',
        'total_agents_hired',
        'active_subscriptions'
    ]
    list_filter = ['preferred_budget_range']
    search_fields = ['user__username', 'user__company_name']
