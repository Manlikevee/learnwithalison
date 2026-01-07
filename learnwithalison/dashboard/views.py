from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from dashboard.models import Category, Course, SupportTicket, YearlyRevenueProjection, CourseView, CoursePurchase, \
    CartItem
from home.forms import HomePageForm, AboutPageForm, InternationalProductsForm
from home.models import HomePage, AboutPage, InternationalAndProducts
from users.models import Profile
from django.utils.timezone import now

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Create your views here.

def course_list(request):
    courses = Course.objects.filter(status='published')
    return render(request, 'courses.html', {
        'courses': courses
    })

def ytcourse_list(request):
    return render(request, 'ytcourses.html')


def course_detail(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        status='published'
    )

    sections = course.sections.prefetch_related('lessons')

    # -----------------------------
    # VIEW TRACKING
    # -----------------------------
    if request.user.is_authenticated:
        view, created = CourseView.objects.get_or_create(
            course=course,
            user=request.user
        )
        if created:
            Course.objects.filter(id=course.id).update(
                view_count=F('view_count') + 1
            )
    else:
        Course.objects.filter(id=course.id).update(
            view_count=F('view_count') + 1
        )

    # -----------------------------
    # PURCHASE CHECK
    # -----------------------------
    has_purchased = False
    purchase = None

    if request.user.is_authenticated:
        purchase = CoursePurchase.objects.filter(
            user=request.user,
            course=course,
            # status='completed'
        ).first()

        has_purchased = purchase is not None
    print(has_purchased)
    return render(request, "course_detail.html", {
        "course": course,
        "sections": sections,
        "has_paid": has_purchased,
        "purchase": purchase,  # optional, useful later
    })

@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    # 🔹 Get or create profile safely
    profile, created = Profile.objects.get_or_create(user=user)

    # 🔹 Handle profile update
    if request.method == "POST" and request.POST.get("form_type") == "profile":

        # Update User model
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        user.username = request.POST.get("username", "").strip()
        user.email = request.POST.get("email", "").strip()

        # Update Profile model
        profile.phone = request.POST.get("phone", "").strip()
        profile.occupation = request.POST.get("occupation", "").strip()
        profile.bio = request.POST.get("bio", "").strip()

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect(request.META.get("HTTP_REFERER", "dashboard"))

    # =====================================================
    # 📊 DASHBOARD DATA
    # =====================================================

    # All purchases by user
    purchases = CoursePurchase.objects.filter(user=user)

    # Completed purchases = enrolled courses
    completed_purchases = purchases.filter(status="completed")

    # Active purchases (you can refine this later)
    active_purchases = purchases.filter(status="completed")

    # Counters
    enrolled_courses_count = completed_purchases.count()
    active_courses_count = active_purchases.count()
    completed_courses_count = completed_purchases.count()

    # Courses lists
    enrolled_courses = Course.objects.filter(
        purchases__user=user,
        purchases__status="completed"
    ).distinct()

    # Order history (all purchases)
    order_history = purchases.select_related("course").order_by("-created_at")

    return render(request, "dashboard.html", {
        "profile": profile,

        # Counters
        "enrolled_courses_count": enrolled_courses_count,
        "active_courses_count": active_courses_count,
        "completed_courses_count": completed_courses_count,

        # Lists
        "enrolled_courses": enrolled_courses,
        "active_courses": enrolled_courses,
        "completed_courses": enrolled_courses,
        "order_history": order_history,
    })


import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Course, CourseLesson, CourseSection

CHUNK_DIR = settings.MEDIA_ROOT  # /home/learesoa/public_html/chunk

@csrf_exempt
@login_required
def resumable_lesson_upload(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        author=request.user
    )

    # ===== RESUME CHECK (GET) =====
    if request.method == "GET":
        identifier = request.GET.get("resumableIdentifier")
        chunk_number = request.GET.get("resumableChunkNumber")

        chunk_path = os.path.join(
            CHUNK_DIR, f"{identifier}_{chunk_number}.part"
        )

        if os.path.exists(chunk_path):
            return JsonResponse({}, status=200)
        return JsonResponse({}, status=204)

    # ===== CHUNK UPLOAD (POST) =====
    if request.method == "POST":

        identifier = request.POST.get("resumableIdentifier")
        filename = request.POST.get("resumableFilename")
        chunk_number = int(request.POST.get("resumableChunkNumber"))
        total_chunks = int(request.POST.get("resumableTotalChunks"))

        section_id = request.POST.get("section")
        title = request.POST.get("title")
        duration = request.POST.get("duration", "")

        video_chunk = request.FILES.get("file")

        if not video_chunk:
            return JsonResponse({"error": "Missing chunk"}, status=400)

        os.makedirs(CHUNK_DIR, exist_ok=True)

        chunk_path = os.path.join(
            CHUNK_DIR, f"{identifier}_{chunk_number}.part"
        )

        with open(chunk_path, "wb+") as dest:
            for chunk in video_chunk.chunks():
                dest.write(chunk)

        # ===== CHECK IF ALL CHUNKS EXIST =====
        uploaded = [
            os.path.exists(
                os.path.join(CHUNK_DIR, f"{identifier}_{i}.part")
            )
            for i in range(1, total_chunks + 1)
        ]

        if all(uploaded):

            final_dir = os.path.join(
                settings.MEDIA_ROOT, "courses/videos"
            )
            os.makedirs(final_dir, exist_ok=True)

            final_path = os.path.join(final_dir, filename)

            with open(final_path, "wb") as final:
                for i in range(1, total_chunks + 1):
                    with open(
                        os.path.join(CHUNK_DIR, f"{identifier}_{i}.part"),
                        "rb"
                    ) as part:
                        final.write(part.read())

            # cleanup
            for i in range(1, total_chunks + 1):
                os.remove(
                    os.path.join(CHUNK_DIR, f"{identifier}_{i}.part")
                )

            section = None
            if section_id:
                section = get_object_or_404(
                    CourseSection,
                    id=section_id,
                    course=course
                )

            lesson = CourseLesson.objects.create(
                course=course,
                section=section,
                title=title,
                video=f"courses/videos/{filename}",
                duration=duration,
            )

            return JsonResponse({
                "success": True,
                "lesson_id": lesson.id
            })

        return JsonResponse({"chunk_received": True})

    return JsonResponse({"error": "Invalid request"}, status=400)




@login_required
def admin_dashboard(request):
    current_year = now().year
    userslistcount = User.objects.select_related('profile').all().count()
    coursescount = Course.objects.all().count()
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    # ================= PROJECTIONS =================
    projection = YearlyRevenueProjection.objects.filter(
        business=request.user,
        year=current_year
    ).first()

    monthly_projection = []
    if projection and projection.monthly_projection:
        for m in months:
            monthly_projection.append(
                float(projection.monthly_projection.get(m, 0))
            )
    else:
        monthly_projection = [0.0] * 12

    total_projected_amount = sum(monthly_projection)

    # ================= PURCHASES PER MONTH =================
    monthly_purchases = []

    for month_index in range(1, 13):
        total = CoursePurchase.objects.filter(
            status="completed",
            created_at__year=current_year,
            created_at__month=month_index
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        monthly_purchases.append(float(total))

    # ================= DASHBOARD STATS =================
    top_courses = Course.objects.order_by("-view_count")[:10]
    purchases = Course.objects.order_by("-purchase_count")[:10]

    total_cart_items = CartItem.objects.count()
    purchase_count = CoursePurchase.objects.filter(status="completed").count()
    awaiting_confirmation = CoursePurchase.objects.exclude(status="completed").count()

    return render(request, "admindash.html", {
        "current_year": current_year,

        # Charts
        "monthly_projection": monthly_projection,
        "monthly_purchases": monthly_purchases,

        # Totals
        "total_projected_amount": total_projected_amount,

        # Lists
        "CourseView": top_courses,
        "purchases": purchases,

        # Counters
        "purchase_count": purchase_count,
        "total_cart_items": total_cart_items,
        "awaiting_confirmation": awaiting_confirmation,
        'userslistcount':userslistcount,
        'coursescount':coursescount
    })
@login_required
def admin_courses(request):
    courses = Course.objects.select_related('category', 'author').order_by('-created_at')
    categories = Category.objects.filter(status='active')

    return render(request, 'all_courses.html', {
        'courses': courses,
        'categories': categories
    })
@login_required
def admin_course_create(request):
    categories = Category.objects.filter(status='active')

    if request.method == "POST":
        price_type = request.POST.get('price_type')
        price = request.POST.get('price')

        course = Course.objects.create(
            author=request.user,
            title=request.POST.get('title'),
            category_id=request.POST.get('category'),
            level=request.POST.get('level'),
            short_description=request.POST.get('short_description'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            price_type=price_type,
            price=price if price_type == 'paid' else None,
            status=request.POST.get('status'),
        )

        messages.success(
            request,
            "Course created successfully. Please add sections and videos."
        )

        # 👉 REDIRECT TO VIDEO UPLOAD / CURRICULUM PAGE
        return redirect('admin_course_curriculum', course.id)

    return render(request, 'add_course.html', {
        'categories': categories
    })



@login_required
def admin_course_curriculum(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        # author=request.user
    )

    return render(request, 'course_curriculum.html', {
        'course': course,
        'sections': course.sections.all(),
        'lessons': course.lessons.all(),
    })

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Course, CourseSection, CourseLesson


@login_required
def admin_course_lesson_upload(request, course_id):
    """
    Handles single video upload per request.
    Frontend can clone inputs & submit multiple times.
    """

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    course = get_object_or_404(
        Course,
        id=course_id,
        # author=request.user
    )

    section_id = request.POST.get('section')
    title = request.POST.get('title')
    order = request.POST.get('order', 0)
    duration = request.POST.get('duration', '')
    is_preview = request.POST.get('is_preview') == 'true'
    video_file = request.FILES.get('video')

    if not video_file or not title:
        return JsonResponse(
            {"error": "Title and video are required"},
            status=400
        )

    section = None
    if section_id:
        section = get_object_or_404(
            CourseSection,
            id=section_id,
            course=course
        )

    lesson = CourseLesson.objects.create(
        course=course,
        section=section,
        title=title,
        video=video_file,
        duration=duration,
        order=order,
        is_preview=is_preview,
    )

    return JsonResponse({
        "success": True,
        "lesson_id": lesson.id,
        "title": lesson.title,
        "section": section.title if section else None
    })

@login_required
def admin_course_section_create(request, course_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    course = get_object_or_404(
        Course,
        id=course_id,
        # author=request.user
    )

    title = request.POST.get('title')
    order = request.POST.get('order', 0)

    if not title:
        return JsonResponse({"error": "Section title required"}, status=400)

    section = CourseSection.objects.create(
        course=course,
        title=title,
        order=order
    )

    return JsonResponse({
        "success": True,
        "section_id": section.id,
        "title": section.title
    })


@login_required
def admin_course_edit(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        # author=request.user
    )

    categories = Category.objects.filter(status='active')

    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.category_id = request.POST.get('category')
        course.level = request.POST.get('level')
        course.short_description = request.POST.get('short_description')
        course.description = request.POST.get('description')
        course.status = request.POST.get('status')

        price_type = request.POST.get('price_type')
        price = request.POST.get('price')

        course.price_type = price_type
        course.price = price if price_type == 'paid' else None

        if request.FILES.get('thumbnail'):
            course.thumbnail = request.FILES['thumbnail']

        course.save()

        messages.success(request, "Course updated successfully")

        # 👉 REDIRECT TO CURRICULUM / VIDEO UPLOAD PAGE
        return redirect('admin_course_curriculum', course.id)

    return render(request, 'edit_course.html', {
        'course': course,
        'categories': categories
    })

@login_required
def admin_course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if course.author != request.user:
        messages.error(request, "You are not allowed to delete this course.")
        return redirect('admin_courses')

    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('admin_courses')


def admin_categories(request):
    categories = Category.objects.all().order_by('-created_at')

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')

        Category.objects.create(
            name=name,
            description=description,
            status=status
        )

        messages.success(request, "Category added successfully.")
        return redirect('admin_categories')

    return render(request, 'categories.html', {
        'categories': categories
    })

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.status = request.POST.get('status')
        category.save()

        messages.success(request, "Category updated successfully.")
        return redirect('admin_categories')

    return render(request, 'edit_category.html', {
        'category': category
    })

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted.")
    return redirect('admin_categories')
# ======================
# STUDENTS
# ======================

@login_required
def admin_students(request):
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    return render(request, 'students.html', {
        'users': users,
        'total_users': users.count()
    })


@login_required
def edit_user(request, user_id):
    # messages.success(request, "Email sent successfully.")
    user = get_object_or_404(User, id=user_id)

    # ❌ Protect superuser
    if user.is_superuser:
        messages.error(request, "Superuser cannot be edited.")
        return redirect('admin_students')

    # -----------------------------
    # UPDATE USER + PROFILE
    # -----------------------------
    if request.method == "POST":
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone', '').strip()
        profile.occupation = request.POST.get('occupation', '').strip()
        profile.bio = request.POST.get('bio', '').strip()
        profile.save()

        messages.success(request, "User updated successfully.")
        return redirect('admin_students')

    # -----------------------------
    # USER RELATED DATA
    # -----------------------------

    # Cart items
    cart_items = CartItem.objects.filter(
        user=user
    ).select_related('course')

    # Purchases
    purchases = CoursePurchase.objects.filter(
        user=user
    ).select_related('course').order_by('-created_at')

    # Support tickets
    support_tickets = SupportTicket.objects.filter(
        user=user
    ).order_by('-created_at')

    # Optional counts (useful in UI)
    cart_count = cart_items.count()
    purchase_count = purchases.count()
    ticket_count = support_tickets.count()

    return render(request, 'edit_user.html', {
        'user_obj': user,

        # profile already available via user.profile
        'profile': user.profile,

        # related data
        'cart_items': cart_items,
        'purchases': purchases,
        'support_tickets': support_tickets,

        # counts
        'cart_count': cart_count,
        'purchase_count': purchase_count,
        'ticket_count': ticket_count,
    })

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        messages.error(request, "Superuser cannot be deleted.")
        return redirect('admin_students')

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('admin_students')
# ======================
# INSTRUCTOR
# ======================
@login_required
def instructor_profile(request):
    return render(request, 'instructor_profile.html')


@login_required
def instructor_courses(request):
    return render(request, 'instructor_courses.html')


@login_required
def instructor_earnings(request):
    return render(request, 'instructor_earnings.html')


# ======================
# PAYMENTS
# ======================
@login_required
def admin_orders(request):
    orders = CoursePurchase.objects.select_related(
        "user", "course"
    ).order_by("-created_at")

    return render(request, "orders.html", {
        "transactions": orders
    })


@login_required
def admin_transactions(request):
    transactions = CoursePurchase.objects.filter(
        status__in=["completed", "pending"]
    ).select_related(
        "user", "course"
    ).order_by("-created_at")

    return render(request, "orders.html", {
        "transactions": transactions
    })


@login_required
def admin_refunds(request):
    refunds = CoursePurchase.objects.filter(
        status="refunded"
    ).select_related(
        "user", "course"
    ).order_by("-created_at")

    return render(request, "refunds.html", {
        "refunds": refunds
    })

# ======================
# WEBSITE CONTENT
# ======================
@login_required
def admin_pages(request):
    return render(request, 'pages.html')


@login_required
def admin_faqs(request):
    return render(request, 'faqs.html')


@login_required
def admin_testimonials(request):
    return render(request, 'testimonials.html')


@login_required
def admin_home(request):
    home, _ = HomePage.objects.get_or_create(id=1)

    if request.method == "POST":
        form = HomePageForm(request.POST, request.FILES, instance=home)

        if form.is_valid():
            # ✅ Preserve existing hero image if none uploaded
            if not request.FILES.get("hero_background"):
                form.instance.hero_background = home.hero_background

            form.save()
            messages.success(request, "Home page updated successfully.")
            return redirect("admin_home")

        else:
            # ✅ Show readable validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(request, error)
                    else:
                        messages.error(
                            request,
                            f"{field.replace('_', ' ').title()}: {error}"
                        )

    else:
        form = HomePageForm(instance=home)

    return render(request, "admin_home.html", {"form": form})


@login_required
def admin_about(request):
    about, _ = AboutPage.objects.get_or_create(id=1)

    if request.method == "POST":
        form = AboutPageForm(request.POST, instance=about)

        if form.is_valid():
            form.save()
            messages.success(request, "About page updated successfully.")
            return redirect("admin_about")
        else:
            # ✅ Show why it failed
            # ✅ Show readable validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(request, error)
                    else:
                        messages.error(
                            request,
                            f"{field.replace('_', ' ').title()}: {error}"
                        )

    else:
        form = AboutPageForm(instance=about)

    return render(
        request,
        "admin_about.html",
        {
            "form": form,
        }
    )


def admin_products(request):
    products, _ = InternationalAndProducts.objects.get_or_create(id=1)
    form = InternationalProductsForm(request.POST or None, instance=products)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Products page updated successfully.")
        return redirect("admin_products")

    return render(request, "admin_products.html", {"form": form})


@login_required
def admin_send_marketing_email(request, user_id):
    if request.method != "POST":
        return redirect("admin_students")

    user = get_object_or_404(User, id=user_id)

    # ✅ Ensure user has email
    if not user.email:
        messages.error(request, "User does not have an email address.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    message = request.POST.get("message", "").strip()

    # ✅ Validate message
    if not message:
        messages.error(request, "Message cannot be empty.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    subject = "Message from Instructor Alison’s Tutorials"

    # ✅ Render HTML email
    html_content = render_to_string(
        "marketing_email.html",
        {
            "subject": subject,
            "header_title": "Instructor Alison’s Tutorials",
            "user_name": user.first_name or user.username,
            "message": message,
            "year": now().year,
        }
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,  # plain-text fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.attach_alternative(html_content, "text/html")

    # ✅ FAIL SILENTLY BUT CHECK RESULT
    sent_count = email.send(fail_silently=True)

    if sent_count == 0:
        messages.error(
            request,
            "Email could not be sent. Please check email configuration and try again."
        )
    else:
        messages.success(
            request,
            f"Email sent successfully to {user.email}."
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))
# ======================
# SUPPORT
# ======================
@login_required
def admin_support(request):
    """
    View all support tickets (admin view)
    """

    tickets = SupportTicket.objects.select_related('user').order_by('-created_at')

    context = {
        'tickets': tickets
    }

    return render(request, 'support_tickets.html', context)

@login_required
def support_ticket_detail(request, ticket_id):
    """
    View a single support ticket details
    """

    ticket = get_object_or_404(SupportTicket, id=ticket_id)

    # Optional: non-admins can only view their own tickets
    if not request.user.is_staff and ticket.user != request.user:
        messages.error(request, "You are not allowed to view this ticket.")
        return redirect('admin_support')

    context = {
        'ticket': ticket
    }

    return render(request, 'ticket_detail.html', context)



@login_required
def support_ticket_resolve(request, ticket_id):
    """
    Mark a support ticket as resolved
    """

    ticket = get_object_or_404(SupportTicket, id=ticket_id)

    # Only admins can resolve tickets
    if not request.user.is_staff:
        messages.error(request, "You are not allowed to resolve tickets.")
        return redirect('admin_support')

    ticket.status = 'resolved'
    ticket.save(update_fields=['status'])

    messages.success(request, f"Ticket #{ticket.ticket_id} marked as resolved.")

    return redirect('admin_support')

# ======================
# SETTINGS & PROFILE
# ======================
@login_required
def admin_settings(request):
    return render(request, 'settings.html')


from django.contrib.auth import update_session_auth_hash


@login_required
def admin_profile(request):
    user = request.user

    if request.method == "POST":

        # UPDATE PROFILE INFO
        if request.POST.get("form_type") == "profile":
            user.first_name = request.POST.get("first_name", "")
            user.last_name = request.POST.get("last_name", "")
            user.email = request.POST.get("email", "")
            user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("admin_profile")

        # UPDATE PASSWORD
        if request.POST.get("form_type") == "password":
            current = request.POST.get("current_password")
            new = request.POST.get("new_password")
            confirm = request.POST.get("confirm_password")

            if not user.check_password(current):
                messages.error(request, "Current password is incorrect.")
                return redirect("admin_profile")

            if new != confirm:
                messages.error(request, "New passwords do not match.")
                return redirect("admin_profile")

            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password updated successfully.")
            return redirect("admin_profile")

    return render(request, "profile.html")


@login_required
def yearly_projection_view(request):
    current_year = datetime.now().year

    # Get or create projection for this year
    projection, created = YearlyRevenueProjection.objects.get_or_create(
        business=request.user,
        year=current_year,
        defaults={
            "monthly_projection": {month: 0 for month in MONTHS}
        }
    )
    total = sum(
        projection.monthly_projection.values()
    )

    # Ensure missing months are added (safety check)
    updated = False
    for month in MONTHS:
        if month not in projection.monthly_projection:
            projection.monthly_projection[month] = 0
            updated = True

    if updated:
        projection.save()

    # HANDLE UPDATE
    if request.method == "POST":
        monthly_data = {}

        for month in MONTHS:
            value = request.POST.get(month, 0)
            monthly_data[month] = float(value) if value else 0

        projection.monthly_projection = monthly_data
        projection.save()

        messages.success(request, f"{current_year} projections updated successfully.")
        return redirect("yearly_projection")

    return render(request, "yearly_projection.html", {
        "projection": projection,
        "months": MONTHS,
        "year": current_year,
        "total_projected_amount": total
    })

@login_required
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id, status="published")

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        course=course
    )

    if created:
        messages.success(request, "Course added to cart.")
    else:
        messages.info(request, "Course already in your cart.")

    # ✅ Redirect back to the same page
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def remove_from_cart(request, course_id):
    cart_item = CartItem.objects.filter(
        user=request.user,
        course_id=course_id
    ).first()

    if cart_item:
        cart_item.delete()
        messages.success(request, "Course removed from cart.")
    else:
        messages.warning(request, "Course not found in your cart.")

    # ✅ Redirect back to the same page
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("course")

    subtotal = Decimal("0.00")
    for item in cart_items:
        if item.course.price_type == "paid" and item.course.price:
            subtotal += item.course.price

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": subtotal,  # same for now (no tax/shipping)
    }

    return render(request, "cart.html", context)



@login_required
def checkout(request):
    cart_items = CartItem.objects.select_related("course").filter(
        user=request.user
    )

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect("cart")

    # Calculate total
    total_amount = sum(
        (item.course.price or Decimal("0.00")) for item in cart_items
    )

    if request.method == "POST":
        with transaction.atomic():
            for item in cart_items:
                course = item.course
                amount = course.price or Decimal("0.00")

                purchase, created = CoursePurchase.objects.get_or_create(
                    user=request.user,
                    course=course,
                    defaults={
                        "amount": amount,
                        "status": "completed",
                        "reference": f"PUR-{get_random_string(10)}",
                    }
                )

                # Increment purchase count ONLY once
                if created:
                    Course.objects.filter(id=course.id).update(
                        purchase_count=F("purchase_count") + 1
                    )

            # Clear cart after successful purchase
            cart_items.delete()

        messages.success(
            request,
            "Payment successful. You are now enrolled in your courses."
        )
        return redirect("dashboard")  # or dashboard

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total_amount": total_amount
    })