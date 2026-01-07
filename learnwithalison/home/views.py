from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from dashboard.models import Course
from home.models import HomePage, AboutPage, InternationalAndProducts


def createhome(request):
    HomePage.objects.get_or_create(
        id=1,
        defaults={
            # ================= HERO =================
            "hero_badge": "Instructor Alison’s Tutorials",
            "hero_title": "Learn Smarter, Achieve Greater",
            "hero_subtitle": (
                "Simplified lessons in Mathematics, Physics, and Chemistry — "
                "crafted to make complex concepts easy to understand for learners at all levels."
            ),
            "why_choose_title": "Why Choose Instructor Alison’s Tutorials",
            "why_choose_intro": (
                "We provide structured, results-driven learning built on strong academic foundations."
            ),
            "why_choose_points": (
                "Strong academic background in Theoretical and Mathematical Physics\n"
                "Clear, structured, and step-by-step teaching methodology\n"
                "Experience teaching both local and international students\n"
                "Curriculum-aligned instruction across multiple countries\n"
                "Flexible online delivery with global accessibility"
            ),
            # ================= UNIVERSITY CARD SECTION =================
            "card_intro": "Discover your Potential",
            "card_heading": "Alison's Tutorials",
            "card_button_text": "View courses",

            "card1_title": "Undergraduate",
            "card1_text": "Higher education is designed for career professionals seeking",

            "card2_title": "Postgraduate",
            "card2_text": "Higher education is designed for career professionals seeking",

            "card3_title": "Research Fellow",
            "card3_text": "Higher education is designed for career professionals seeking",

            # ================= WELCOME / ABOUT =================
            "welcome_title": "Welcome to Instructor Alison Learning Platform",
            "welcome_intro": (
                "I am a tutor and Educational counselor with a demonstrated history "
                "of working in the education industry."
            ),
            "welcome_body": (
                "On this channel, I share simplified tutorials on Mathematics, Physics, "
                "and Chemistry. Subscribe and turn on your notification bell."
            ),

            # ================= INSTRUCTOR =================
            "instructor_name": "Alison",
            "instructor_bio": (
                "I always feel privileged and excited reading your comments, feedback, "
                "suggestions, and words of motivation."
            ),

            # ================= EXAMINATIONS & CURRICULA =================
            "exams_section_title": "Examinations & Curricula Covered",
            "exams_section_intro": (
                "We support learners across multiple countries, examination boards, "
                "and international curricula."
            ),

            "exams_nigeria_title": "Nigeria & West Africa",
            "exams_nigeria_list": (
                "WAEC\n"
                "JAMB"
            ),

            "exams_uk_title": "United Kingdom",
            "exams_uk_list": (
                "GCSE (Maths, Physics, Chemistry)\n"
                "IGCSE\n"
                "A-Level (Maths, Physics, Chemistry)\n"
                "AQA\n"
                "Edexcel\n"
                "OCR\n"
                "Cambridge"
            ),

            "exams_us_title": "United States",
            "exams_us_list": (
                "SAT (Mathematics)\n"
                "AP Mathematics\n"
                "AP Physics 1\n"
                "AP Physics 2\n"
                "AP Physics C"
            ),

            "exams_international_title": "Canada & International Curricula",
            "exams_international_list": (
                "Provincial Secondary School Curricula\n"
                "IGCSE Pathways\n"
                "A-Level Pathways"
            ),

            "exams_global_title": "Global & Professional Exams",
            "exams_global_list": (
                "ASVAB (Mathematics & Science)\n"
                "GRE (Quantitative Reasoning & Physics Foundations)\n"
                "IELTS (Academic Preparation Support)"
            ),

            # ================= SOCIALS =================
            "instagram": "@instructor_alison",
            "tiktok": "Instructor_Alison",
            "facebook": "Alison Zaccheaus",
            "twitter": "@Instructor_Alison",
        }
    )

def createabout(request):
    AboutPage.objects.get_or_create(
        id=1,
        defaults={

            # ================= PAGE INTRO =================
            "page_title": "About Instructor Alison",
            "page_intro": (
                "Instructor Alison is a STEM educator and education entrepreneur with a "
                "strong academic background and experience teaching students across "
                "diverse curricula and educational systems."
            ),

            # ================= ROLE =================
            "role_title": "Founder and Lead Educator",

            # ================= ACADEMIC BACKGROUND =================
            "academic_title": "Academic Background and Qualifications",
            "academic_list": (
                "MSc in Theoretical and Mathematical Physics — Distinction\n"
                "PGD in Theoretical and Mathematical Physics — Distinction\n"
                "HND in Physics with Electronics\n"
                "Background in Science Laboratory Technology"
            ),
            "academic_summary": (
                "This academic foundation informs a teaching style that emphasizes "
                "conceptual clarity, mathematical rigor, and practical problem-solving."
            ),

            # ================= TEACHING EXPERIENCE =================
            "experience_title": "Teaching Experience and Global Reach",
            "experience_body": (
                "Instructor Alison has taught and supported students preparing for local "
                "and international examinations, including learners from under-resourced "
                "communities and students following UK, US, and Canadian curricula.\n\n"
                "The goal is to make high-quality STEM education accessible, "
                "understandable, and effective for every learner."
            ),

            # ================= TEACHING PHILOSOPHY =================
            "philosophy_title": "Teaching Philosophy",
            "philosophy_list": (
                "Build strong foundations before advancing to complex topics\n"
                "Explain concepts clearly and systematically\n"
                "Adapt teaching to the learner’s level and curriculum\n"
                "Combine conceptual understanding with exam strategy"
            ),

            # ================= BRAND VALUES =================
            "values_title": "Brand Values",
            "values_list": (
                "Academic excellence\n"
                "Clarity and simplicity\n"
                "Consistency and discipline\n"
                "Accessibility of quality education\n"
                "Global relevance"
            ),

            # ================= TUTORING SERVICES =================
            "tutoring_title": "Tutoring and Academic Services",
            "tutoring_services_title": "Tutoring Services Offered",
            "tutoring_services_list": (
                "One-on-One Tutoring\n"
                "Small Group Tutoring\n"
                "Online Tutoring (Local and International)\n"
                "Exam-Focused Intensive Preparation"
            ),

            # ================= SUBJECT SUPPORT =================
            "subjects_title": "Subject-Specific Support",
            "math_support": (
                "Core mathematics\n"
                "Algebra, trigonometry, calculus foundations\n"
                "Exam-specific problem solving"
            ),
            "physics_support": (
                "Mechanics\n"
                "Electricity and magnetism\n"
                "Waves and modern physics\n"
                "AP Physics and A-Level Physics"
            ),
            "chemistry_support": (
                "Physical, organic, and inorganic chemistry\n"
                "Exam-aligned problem solving"
            ),
            "programming_support": (
                "Python programming fundamentals\n"
                "Problem-solving and logical thinking"
            ),

            # ================= HOW TUTORING WORKS =================
            "process_title": "How Tutoring Works",
            "process_list": (
                "Initial academic assessment\n"
                "Curriculum-aligned learning plan\n"
                "Structured lesson delivery\n"
                "Continuous progress monitoring\n"
                "Exam readiness and revision support"
            ),

            # ================= DELIVERY =================
            "delivery_title": "Local and International Tutoring",
            "delivery_list": (
                "Online sessions delivered via secure platforms\n"
                "Flexible scheduling across time zones\n"
                "Clear communication with students and parents"
            ),

            # ================= PRICING =================
            "pricing_title": "Pricing Structure",
            "pricing_body": (
                "Tutoring fees vary based on:\n"
                "Subject and academic level\n"
                "Exam type\n"
                "Session format (one-on-one or group)\n"
                "Location (local or international)"
            ),

            # ================= CTA =================
            "cta_text": "Book a Tutoring Session",
            "cta_subtext": "Contact via WhatsApp for Pricing Details",
        }
    )

    return None

def create_courses_products_page(request):
    InternationalAndProducts.objects.get_or_create(
        id=1
    )

def courses_products_view(request):
    create_courses_products_page(request)
    content = InternationalAndProducts.objects.first()
    return render(
        request,
        "courses_products.html",
        {"content": content}
    )


# Create your views here.
def home(request):
    createhome(request)
    home = HomePage.objects.first()
    courses = Course.objects.order_by("-created_at")[:3]
    return render(request, 'index.html', {'courses': courses , 'home': home})


def about(request):
    createabout(request)
    about = AboutPage.objects.first()
    return render(request, 'about.html', {'about': about})


def contact(request):
    return render(request, 'contact.html')

def membership(request):
    return render(request, 'membership.html')


@login_required  # Ensure the user is authenticated
def check_superuser(request):
    if request.user.is_superuser:
        return JsonResponse({"is_superuser": "yes"})
    else:
        return JsonResponse({"is_superuser": "no"})


def custom_400(request, exception):
    return render(request, "error.html", {
        "code": 400,
        "title": "Bad Request",
        "message": "The request could not be understood by the server.",
    }, status=400)


def custom_403(request, exception):
    return render(request, "error.html", {
        "code": 403,
        "title": "Access Denied",
        "message": "You do not have permission to access this page.",
    }, status=403)


def custom_404(request, exception):
    return render(request, "error.html", {
        "code": 404,
        "title": "Page Not Found",
        "message": "Oops! That page can't be found.",
    }, status=404)


def custom_500(request):
    return render(request, "error.html", {
        "code": 500,
        "title": "Server Error",
        "message": "Something went wrong on our end. Please try again later.",
    }, status=500)


def custom_503(request):
    return render(request, "error.html", {
        "code": 503,
        "title": "Service Unavailable",
        "message": "The service is temporarily unavailable. Please try again shortly.",
    }, status=503)
