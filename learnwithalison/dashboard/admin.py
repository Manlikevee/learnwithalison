from django.contrib import admin
from .models import (
    Category,
    Course,
    CourseView,
    CoursePurchase,
    CartItem,
    CourseSection,
    CourseLesson,
    SupportTicket,
    TicketMessage,
    YearlyRevenueProjection,
)

# =========================
# CATEGORY
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
    ordering = ("name",)


# =========================
# COURSE
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "level",
        "price_type",
        "price",
        "status",
        "view_count",
        "purchase_count",
        "created_at",
    )
    list_filter = ("status", "level", "price_type", "category")
    search_fields = ("title", "author__username")
    ordering = ("-created_at",)
    readonly_fields = ("view_count", "purchase_count")


# =========================
# COURSE VIEWS
# =========================
@admin.register(CourseView)
class CourseViewAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "ip_address", "created_at")
    list_filter = ("created_at",)
    search_fields = ("course__title", "user__username", "ip_address")
    ordering = ("-created_at",)


# =========================
# COURSE PURCHASES
# =========================
@admin.register(CoursePurchase)
class CoursePurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "user",
        "course",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("reference", "user__username", "course__title")
    ordering = ("-created_at",)


# =========================
# CART ITEMS
# =========================
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "created_at")
    search_fields = ("user__username", "course__title")
    ordering = ("-created_at",)


# =========================
# COURSE SECTIONS
# =========================
@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "created_at")
    list_filter = ("course",)
    search_fields = ("title", "course__title")
    ordering = ("course", "order")


# =========================
# COURSE LESSONS
# =========================
@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "section",
        "duration",
        "order",
        "is_preview",
        "created_at",
    )
    list_filter = ("course", "is_preview")
    search_fields = ("title", "course__title")
    ordering = ("course", "order")


# =========================
# SUPPORT TICKETS
# =========================
@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_id",
        "subject",
        "user",
        "category",
        "priority",
        "status",
        "created_at",
    )
    list_filter = ("status", "priority", "category")
    search_fields = ("ticket_id", "subject", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("ticket_id",)


# =========================
# TICKET MESSAGES
# =========================
@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ("ticket", "sender", "created_at")
    search_fields = ("ticket__ticket_id", "sender__username")
    ordering = ("-created_at",)


# =========================
# YEARLY REVENUE PROJECTION
# =========================
@admin.register(YearlyRevenueProjection)
class YearlyRevenueProjectionAdmin(admin.ModelAdmin):
    list_display = (
        "business",
        "year",
        "total_projected_amount",
        "created_at",
    )
    list_filter = ("year",)
    search_fields = ("business__username",)
    ordering = ("-year",)
