from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model for both developers and businesses"""
    
    # User Type
    USER_TYPE_CHOICES = (
        ('developer', 'Developer'),
        ('business', 'Business'),
    )
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES,
        default='business',
        help_text="Are you a developer creating AI agents or a business looking to hire them?"
    )
    
    # Basic Information
    email = models.EmailField(_('email address'), unique=True)
    company_name = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Your company or organization name"
    )
    bio = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Tell us about yourself or your company"
    )
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True
    )
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Professional Information (for developers)
    github_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    skills = models.JSONField(default=list, blank=True)  # ["Python", "AI", "NLP"]
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    
    # Business Information (for businesses)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(
        max_length=20,
        choices=(
            ('1-10', '1-10 employees'),
            ('11-50', '11-50 employees'),
            ('51-200', '51-200 employees'),
            ('201-500', '201-500 employees'),
            ('501-1000', '501-1000 employees'),
            ('1000+', '1000+ employees'),
        ),
        blank=True
    )
    
    # Verification & Trust
    verified = models.BooleanField(
        default=False,
        help_text="Has this user been verified by Autra?"
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    trust_score = models.IntegerField(
        default=0,
        help_text="Trust score based on activity and reviews"
    )
    
    # Financial Information (for payment processing)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_account_id = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Connected Stripe account for receiving payments"
    )
    
    # Profile Completeness
    profile_completed = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)
    
    # Notifications & Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    newsletter_subscription = models.BooleanField(default=True)
    
    # Statistics
    total_spent = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Total amount spent on the platform (for businesses)"
    )
    total_earned = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Total amount earned on the platform (for developers)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(null=True, blank=True)
    
    # Profile Image
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        help_text="Profile picture"
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['user_type']),
            models.Index(fields=['verified']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        if self.company_name:
            return f"{self.username} - {self.company_name} ({self.get_user_type_display()})"
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_developer(self):
        return self.user_type == 'developer'
    
    @property
    def is_business(self):
        return self.user_type == 'business'
    
    @property
    def display_name(self):
        """Returns the best name to display for this user"""
        if self.company_name:
            return self.company_name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username
    
    def calculate_profile_completion(self):
        """Calculate profile completion percentage"""
        required_fields = ['email', 'first_name', 'last_name', 'bio']
        if self.is_developer:
            required_fields.extend(['github_username', 'skills'])
        else:
            required_fields.extend(['company_name', 'industry'])
        
        completed = sum([1 for field in required_fields if getattr(self, field)])
        return int((completed / len(required_fields)) * 100)
    
    def update_trust_score(self):
        """Update trust score based on various factors"""
        score = 0
        
        # Basic profile completion
        if self.profile_completed:
            score += 10
        
        # Verification
        if self.verified:
            score += 50
        
        # Activity-based scoring
        if self.is_developer:
            # Based on successful agents
            score += min(self.agents.filter(tested_by_platform=True).count() * 10, 100)
        else:
            # Based on successful hires
            score += min(int(self.total_spent / 1000), 100)
        
        self.trust_score = score
        self.save(update_fields=['trust_score'])


class DeveloperProfile(models.Model):
    """Extended profile for developers"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='developer_profile'
    )
    
    # Expertise
    specializations = models.JSONField(
        default=list,
        help_text="AI/ML specializations"
    )
    certifications = models.JSONField(
        default=list,
        help_text="Professional certifications"
    )
    
    # Work Preferences
    available_for_custom_work = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    preferred_project_size = models.CharField(
        max_length=20,
        choices=(
            ('small', 'Small (< $1,000)'),
            ('medium', 'Medium ($1,000 - $10,000)'),
            ('large', 'Large ($10,000+)'),
            ('any', 'Any size'),
        ),
        default='any'
    )
    
    # Statistics
    total_agents = models.IntegerField(default=0)
    successful_deployments = models.IntegerField(default=0)
    average_response_time = models.IntegerField(
        default=24,
        help_text="Average response time in hours"
    )
    
    def __str__(self):
        return f"Developer Profile: {self.user.username}"


class BusinessProfile(models.Model):
    """Extended profile for businesses"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='business_profile'
    )
    
    # Business Details
    tax_id = models.CharField(max_length=50, blank=True)
    billing_address = models.TextField(blank=True)
    billing_email = models.EmailField(blank=True)
    
    # Preferences
    preferred_budget_range = models.CharField(
        max_length=20,
        choices=(
            ('low', 'Low (< $500/month)'),
            ('medium', 'Medium ($500 - $5,000/month)'),
            ('high', 'High ($5,000+/month)'),
            ('enterprise', 'Enterprise (Custom)'),
        ),
        blank=True
    )
    interested_categories = models.JSONField(
        default=list,
        help_text="Categories of AI agents interested in"
    )
    
    # Statistics
    total_agents_hired = models.IntegerField(default=0)
    active_subscriptions = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Business Profile: {self.user.company_name or self.user.username}"