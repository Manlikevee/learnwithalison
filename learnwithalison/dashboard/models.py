from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    PRICE_TYPE_CHOICES = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    title = models.CharField(max_length=255)

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner'
    )

    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    thumbnail = models.FileField(
        upload_to='courses/thumbnails/',
        blank=True,
        null=True
    )

    price_type = models.CharField(
        max_length=10,
        choices=PRICE_TYPE_CHOICES,
        default='free'
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # 🔥 NEW COUNTERS
    view_count = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CourseView(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='views'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'user')  # 👈 unique per user

    def __str__(self):
        return f"{self.course.title} view"

class CoursePurchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_purchases'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='purchases'
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} → {self.course} ({self.status})"


class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} - {self.course}"

class CourseSection(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CourseLesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    section = models.ForeignKey(
        CourseSection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons'
    )

    title = models.CharField(max_length=255)

    video = models.FileField(
        upload_to='courses/videos/'
    )

    duration = models.CharField(
        max_length=50,
        blank=True
    )

    order = models.PositiveIntegerField(default=0)

    is_preview = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class SupportTicket(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    CATEGORY_CHOICES = (
        ('technical', 'Technical'),
        ('payment', 'Payment'),
        ('course', 'Course'),
        ('account', 'Account'),
        ('other', 'Other'),
    )

    ticket_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    subject = models.CharField(max_length=255)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='support_tickets'
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = f"TKT-{self.pk or ''}".upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"


class TicketMessage(models.Model):

    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    attachment = models.FileField(
        upload_to='support/attachments/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message on {self.ticket.ticket_id}"



from django.core.validators import MinValueValidator

class YearlyRevenueProjection(models.Model):
    business = models.ForeignKey(
        User,  # or Business model if you have one
        on_delete=models.CASCADE,
        related_name="revenue_projections"
    )

    year = models.PositiveIntegerField()

    monthly_projection = models.JSONField(
        default=dict,
        blank=True
    )

    # Optional: cached total for faster queries
    total_projected_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("business", "year")
        ordering = ["-year"]

    def __str__(self):
        return f"{self.business} - {self.year} Projection"