from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
import json

class Agent(models.Model):
    """AI Agent listing in the marketplace"""
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        help_text="Name of your AI agent"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly version of name"
    )
    description = models.TextField(
        help_text="Detailed description of what your agent does"
    )
    short_description = models.CharField(
        max_length=500,
        help_text="Brief description for listings"
    )
    
    # Ownership
    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agents',
        limit_choices_to={'user_type': 'developer'}
    )
    
    # Categories and Tags
    CATEGORY_CHOICES = (
        ('customer_service', 'Customer Service'),
        ('data_analysis', 'Data Analysis'),
        ('content_creation', 'Content Creation'),
        ('automation', 'Process Automation'),
        ('sales', 'Sales & Marketing'),
        ('coding', 'Coding & Development'),
        ('research', 'Research & Analysis'),
        ('education', 'Education & Training'),
        ('other', 'Other'),
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        db_index=True
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text='Tags like ["GPT-4", "Python", "API"]'
    )
    
    # Pricing Information
    PRICING_MODEL_CHOICES = (
        ('one_time', 'One-time Purchase'),
        ('monthly', 'Monthly Subscription'),
        ('annual', 'Annual Subscription'),
        ('usage', 'Pay Per Use'),
        ('freemium', 'Freemium'),
        ('custom', 'Custom Pricing'),
    )
    pricing_model = models.CharField(
        max_length=20,
        choices=PRICING_MODEL_CHOICES
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price in GBP"
    )
    usage_price = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Price per API call (for usage-based pricing)"
    )
    free_tier_limit = models.IntegerField(
        default=0,
        help_text="Free API calls per month (0 = no free tier)"
    )
    
    # Technical Details
    api_endpoint = models.URLField(
        blank=True,
        help_text="Your agent's API endpoint"
    )
    documentation_url = models.URLField(
        blank=True,
        help_text="Link to technical documentation"
    )
    github_url = models.URLField(
        blank=True,
        help_text="GitHub repository (if open source)"
    )
    
    # Integration Details
    INTEGRATION_CHOICES = (
        ('api', 'REST API'),
        ('webhook', 'Webhook'),
        ('sdk', 'SDK/Library'),
        ('plugin', 'Plugin'),
        ('standalone', 'Standalone App'),
    )
    integration_type = models.CharField(
        max_length=20,
        choices=INTEGRATION_CHOICES,
        default='api'
    )
    
    # Requirements
    requirements = models.JSONField(
        default=dict,
        blank=True,
        help_text='{"min_ram": "4GB", "python": "3.8+", "dependencies": ["numpy", "pandas"]}'
    )
    
    # Testing & Sandbox
    sandbox_available = models.BooleanField(
        default=False,
        help_text="Is a sandbox environment available for testing?"
    )
    sandbox_url = models.URLField(
        blank=True,
        help_text="Sandbox API endpoint for testing"
    )
    demo_url = models.URLField(
        blank=True,
        help_text="Live demo URL"
    )
    test_api_key = models.CharField(
        max_length=255,
        blank=True,
        help_text="Public test API key for sandbox"
    )
    
    # Trust & Safety
    risk_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text="1=Very Safe, 5=High Risk"
    )
    tested_by_platform = models.BooleanField(
        default=False,
        help_text="Has Autra tested and verified this agent?"
    )
    security_audit_date = models.DateField(
        null=True,
        blank=True,
        help_text="Last security audit date"
    )
    compliance_certifications = models.JSONField(
        default=list,
        blank=True,
        help_text='["GDPR", "HIPAA", "SOC2"]'
    )
    
    # Performance Metrics
    average_response_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Average response time in seconds"
    )
    uptime_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=99.9,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    rate_limit = models.IntegerField(
        default=1000,
        help_text="API calls per hour limit"
    )
    
    # Usage Statistics
    times_hired = models.IntegerField(default=0)
    total_api_calls = models.BigIntegerField(default=0)
    active_subscriptions = models.IntegerField(default=0)
    
    # Ratings
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(default=0)
    
    # Media
    logo = models.ImageField(
        upload_to='agent_logos/',
        blank=True,
        help_text="Agent logo or icon"
    )
    screenshots = models.JSONField(
        default=list,
        blank=True,
        help_text="List of screenshot URLs"
    )
    video_url = models.URLField(
        blank=True,
        help_text="Demo video URL (YouTube, Vimeo, etc.)"
    )
    
    # Status Flags
    is_active = models.BooleanField(
        default=True,
        help_text="Is this agent currently available?"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature on homepage?"
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Verified by Autra team?"
    )
    under_review = models.BooleanField(
        default=True,
        help_text="Pending platform review?"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the agent went live"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['developer', 'is_active']),
            models.Index(fields=['average_rating', '-times_hired']),
        ]
        
    def __str__(self):
        return f"{self.name} by {self.developer.username}"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug and set published date"""
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
            
        if self.is_active and not self.published_at:
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)
    
    def update_rating(self):
        """Recalculate average rating from reviews"""
        from django.db.models import Avg
        result = self.reviews.aggregate(avg=Avg('rating'))
        self.average_rating = result['avg'] or 0
        self.total_reviews = self.reviews.count()
        self.save(update_fields=['average_rating', 'total_reviews'])
    
    @property
    def monthly_revenue(self):
        """Calculate estimated monthly revenue"""
        if self.pricing_model == 'monthly':
            return self.price * self.active_subscriptions
        elif self.pricing_model == 'annual':
            return (self.price / 12) * self.active_subscriptions
        return 0
    
    @property
    def trust_score(self):
        """Calculate trust score based on multiple factors"""
        score = 50  # Base score
        
        if self.tested_by_platform:
            score += 20
        if self.is_verified:
            score += 15
        if self.security_audit_date:
            score += 10
        if self.uptime_percentage >= 99.9:
            score += 5
        
        # Subtract for risk
        score -= (self.risk_rating - 1) * 5
        
        return min(100, max(0, score))


class AgentVersion(models.Model):
    """Track different versions of an agent"""
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_number = models.CharField(
        max_length=20,
        help_text="e.g., 1.0.0, 2.1.3"
    )
    changelog = models.TextField(
        help_text="What changed in this version"
    )
    is_stable = models.BooleanField(default=True)
    release_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-release_date']
        unique_together = ['agent', 'version_number']
    
    def __str__(self):
        return f"{self.agent.name} v{self.version_number}"


class Transaction(models.Model):
    """Track all financial transactions"""
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sales'
    )
    
    # Financial Details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    platform_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Autra's commission"
    )
    seller_earning = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount seller receives"
    )
    
    # Transaction Type
    TRANSACTION_TYPE = (
        ('purchase', 'One-time Purchase'),
        ('subscription_start', 'Subscription Started'),
        ('subscription_renewal', 'Subscription Renewal'),
        ('usage', 'Usage-based Payment'),
        ('refund', 'Refund'),
    )
    transaction_type = models.CharField(
        max_length=25,
        choices=TRANSACTION_TYPE
    )
    
    # Status
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Payment Details
    stripe_payment_intent = models.CharField(
        max_length=255,
        blank=True
    )
    stripe_subscription_id = models.CharField(
        max_length=255,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.buyer.username} - {self.agent.name} - £{self.amount}"
    
    def calculate_fees(self):
        """Calculate platform fee (10% default)"""
        self.platform_fee = self.amount * 0.10
        self.seller_earning = self.amount - self.platform_fee
        

class Review(models.Model):
    """Reviews and ratings for agents"""
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    
    # Rating
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Review Content
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    # Review Categories
    ease_of_use = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    reliability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    support = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    value_for_money = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    
    # Metadata
    verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    reported = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-helpful_count', '-created_at']
        unique_together = ['agent', 'reviewer']
    
    def __str__(self):
        return f"{self.agent.name} - {self.rating}★ by {self.reviewer.username}"