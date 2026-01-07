from django.db import models

class HomePage(models.Model):
    # ================= HERO SECTION =================
    hero_badge = models.CharField(
        max_length=100,
        default="Instructor Alison’s Tutorials"
    )
    hero_title = models.CharField(
        max_length=200,
        default="Learn Smarter, Achieve Greater"
    )
    hero_subtitle = models.TextField()
    hero_background = models.FileField(
        upload_to="home/hero/",
        blank=True,
        null=True
    )

    # ================= UNIVERSITY CARD SECTION =================
    card_intro = models.CharField(
        max_length=100,
        default="Discover your Potential"
    )
    card_heading = models.CharField(
        max_length=150,
        default="Alison's Tutorials"
    )
    card_button_text = models.CharField(
        max_length=50,
        default="View courses"
    )

    card1_title = models.CharField(
        max_length=100,
        default="Undergraduate"
    )
    card1_text = models.TextField(
        default="Higher education is designed for career professionals seeking"
    )

    card2_title = models.CharField(
        max_length=100,
        default="Postgraduate"
    )
    card2_text = models.TextField(
        default="Higher education is designed for career professionals seeking"
    )

    card3_title = models.CharField(
        max_length=100,
        default="Research Fellow"
    )
    card3_text = models.TextField(
        default="Higher education is designed for career professionals seeking"
    )

    # ================= WELCOME / ABOUT SECTION =================
    welcome_title = models.CharField(
        max_length=200,
        default="Welcome to Instructor Alison Learning Platform"
    )
    welcome_intro = models.TextField()
    welcome_body = models.TextField()

    # ================= INSTRUCTOR SECTION =================
    instructor_name = models.CharField(
        max_length=100,
        default="Alison"
    )
    instructor_bio = models.TextField()

    # ================= EXAMINATIONS & CURRICULA SECTION =================
    exams_section_title = models.CharField(
        max_length=200,
        default="Examinations & Curricula Covered"
    )
    exams_section_intro = models.TextField(
        default="We support learners across multiple countries and examination boards."
    )

    exams_nigeria_title = models.CharField(
        max_length=100,
        default="Nigeria & West Africa"
    )
    exams_nigeria_list = models.TextField(
        default="WAEC\nJAMB"
    )

    exams_uk_title = models.CharField(
        max_length=100,
        default="United Kingdom"
    )
    exams_uk_list = models.TextField(
        default=(
            "GCSE (Maths, Physics, Chemistry)\n"
            "IGCSE\n"
            "A-Level (Maths, Physics, Chemistry)\n"
            "AQA, Edexcel, OCR, Cambridge"
        )
    )

    exams_us_title = models.CharField(
        max_length=100,
        default="United States"
    )
    exams_us_list = models.TextField(
        default=(
            "SAT (Mathematics)\n"
            "AP Mathematics\n"
            "AP Physics 1\n"
            "AP Physics 2\n"
            "AP Physics C"
        )
    )

    exams_international_title = models.CharField(
        max_length=150,
        default="Canada & International Curricula"
    )
    exams_international_list = models.TextField(
        default=(
            "Provincial Secondary School Curricula\n"
            "IGCSE Pathways\n"
            "A-Level Pathways"
        )
    )
    why_choose_title = models.CharField(
        max_length=200,
        default="Why Choose Instructor Alison’s Tutorials"
    )

    why_choose_intro = models.TextField(
        default="We provide structured, results-driven learning built on strong academic foundations."
    )

    why_choose_points = models.TextField(
        default=(
            "Strong academic background in Theoretical and Mathematical Physics\n"
            "Clear, structured, and step-by-step teaching methodology\n"
            "Experience teaching both local and international students\n"
            "Curriculum-aligned instruction across multiple countries\n"
            "Flexible online delivery with global accessibility"
        )
    )
    exams_global_title = models.CharField(
        max_length=150,
        default="Global & Professional Exams"
    )
    exams_global_list = models.TextField(
        default=(
            "ASVAB (Mathematics & Science)\n"
            "GRE (Quantitative & Physics Foundations)\n"
            "IELTS (Academic Preparation Support)"
        )
    )

    # ================= SOCIAL TEXT ONLY =================
    instagram = models.CharField(max_length=100, blank=True)
    tiktok = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "Home Page Content"


class AboutPage(models.Model):
    # ================= PAGE INTRO =================
    page_title = models.CharField(
        max_length=200,
        default="About Instructor Alison"
    )

    page_intro = models.TextField(
        default=(
            "Instructor Alison is a STEM educator and education entrepreneur with "
            "a strong academic background and experience teaching students across "
            "diverse curricula and educational systems."
        )
    )

    # ================= ROLE =================
    role_title = models.CharField(
        max_length=150,
        default="Founder and Lead Educator"
    )

    # ================= ACADEMIC BACKGROUND =================
    academic_title = models.CharField(
        max_length=200,
        default="Academic Background and Qualifications"
    )

    academic_list = models.TextField(
        default=(
            "MSc in Theoretical and Mathematical Physics — Distinction\n"
            "PGD in Theoretical and Mathematical Physics — Distinction\n"
            "HND in Physics with Electronics\n"
            "Background in Science Laboratory Technology"
        ),
        help_text="One item per line"
    )

    academic_summary = models.TextField(
        default=(
            "This academic foundation informs a teaching style that emphasizes "
            "conceptual clarity, mathematical rigor, and practical problem-solving."
        )
    )

    # ================= TEACHING EXPERIENCE =================
    experience_title = models.CharField(
        max_length=200,
        default="Teaching Experience and Global Reach"
    )

    experience_body = models.TextField(
        default=(
            "Instructor Alison has taught and supported students preparing for local "
            "and international examinations, including learners from under-resourced "
            "communities and students following UK, US, and Canadian curricula.\n\n"
            "The goal is to make high-quality STEM education accessible, "
            "understandable, and effective for every learner."
        )
    )

    # ================= TEACHING PHILOSOPHY =================
    philosophy_title = models.CharField(
        max_length=200,
        default="Teaching Philosophy"
    )

    philosophy_list = models.TextField(
        default=(
            "Build strong foundations before advancing to complex topics\n"
            "Explain concepts clearly and systematically\n"
            "Adapt teaching to the learner’s level and curriculum\n"
            "Combine conceptual understanding with exam strategy"
        ),
        help_text="One principle per line"
    )

    # ================= BRAND VALUES =================
    values_title = models.CharField(
        max_length=200,
        default="Brand Values"
    )

    values_list = models.TextField(
        default=(
            "Academic excellence\n"
            "Clarity and simplicity\n"
            "Consistency and discipline\n"
            "Accessibility of quality education\n"
            "Global relevance"
        ),
        help_text="One value per line"
    )

    # ================= TUTORING SERVICES =================
    tutoring_title = models.CharField(
        max_length=200,
        default="Tutoring and Academic Services"
    )

    tutoring_services_title = models.CharField(
        max_length=200,
        default="Tutoring Services Offered"
    )

    tutoring_services_list = models.TextField(
        default=(
            "One-on-One Tutoring\n"
            "Small Group Tutoring\n"
            "Online Tutoring (Local and International)\n"
            "Exam-Focused Intensive Preparation"
        )
    )

    # ================= SUBJECT SUPPORT =================
    subjects_title = models.CharField(
        max_length=200,
        default="Subject-Specific Support"
    )

    math_support = models.TextField(
        default=(
            "Core mathematics\n"
            "Algebra, trigonometry, calculus foundations\n"
            "Exam-specific problem solving"
        )
    )

    physics_support = models.TextField(
        default=(
            "Mechanics\n"
            "Electricity and magnetism\n"
            "Waves and modern physics\n"
            "AP Physics and A-Level Physics"
        )
    )

    chemistry_support = models.TextField(
        default=(
            "Physical, organic, and inorganic chemistry\n"
            "Exam-aligned problem solving"
        )
    )

    programming_support = models.TextField(
        default=(
            "Python programming fundamentals\n"
            "Problem-solving and logical thinking"
        )
    )

    # ================= HOW TUTORING WORKS =================
    process_title = models.CharField(
        max_length=200,
        default="How Tutoring Works"
    )

    process_list = models.TextField(
        default=(
            "Initial academic assessment\n"
            "Curriculum-aligned learning plan\n"
            "Structured lesson delivery\n"
            "Continuous progress monitoring\n"
            "Exam readiness and revision support"
        )
    )

    # ================= LOCAL & INTERNATIONAL =================
    delivery_title = models.CharField(
        max_length=200,
        default="Local and International Tutoring"
    )

    delivery_list = models.TextField(
        default=(
            "Online sessions delivered via secure platforms\n"
            "Flexible scheduling across time zones\n"
            "Clear communication with students and parents"
        )
    )

    # ================= PRICING =================
    pricing_title = models.CharField(
        max_length=200,
        default="Pricing Structure"
    )

    pricing_body = models.TextField(
        default=(
            "Tutoring fees vary based on:\n"
            "Subject and academic level\n"
            "Exam type\n"
            "Session format (one-on-one or group)\n"
            "Location (local or international)"
        )
    )

    # ================= CTA =================
    cta_text = models.CharField(
        max_length=200,
        default="Book a Tutoring Session"
    )

    cta_subtext = models.CharField(
        max_length=200,
        default="Contact via WhatsApp for Pricing Details"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Page Content"


class InternationalAndProducts(models.Model):
    # ================= PAGE META =================
    page_title = models.CharField(
        max_length=200,
        default="Courses & Digital Products"
    )

    # ================= DIGITAL PRODUCTS =================
    digital_title = models.CharField(
        max_length=200,
        default="Courses and Digital Products"
    )
    digital_intro = models.TextField(
        default=(
            "Instructor Alison’s Tutorials provides self-paced learning resources "
            "designed for independent study and revision."
        )
    )

    digital_products_list = models.TextField(
        default=(
            "Online video courses\n"
            "E-books and study guides\n"
            "Practice workbooks\n"
            "Exam strategy materials"
        )
    )

    digital_audience_list = models.TextField(
        default=(
            "Students seeking flexible learning options\n"
            "Learners preparing for exams independently\n"
            "Parents looking for structured academic support"
        )
    )

    digital_access_list = models.TextField(
        default=(
            "Secure digital access via Selar\n"
            "Downloadable and on-demand resources"
        )
    )

    digital_cta_primary = models.CharField(
        max_length=50,
        default="View Courses"
    )
    digital_cta_secondary = models.CharField(
        max_length=50,
        default="Buy Now"
    )

    # ================= INTERNATIONAL STUDENTS =================
    intl_title = models.CharField(
        max_length=200,
        default="International Students"
    )

    uk_list = models.TextField(
        default=(
            "GCSE Mathematics, Physics, Chemistry\n"
            "IGCSE\n"
            "A-Level Mathematics and Physics\n"
            "AQA, Edexcel, OCR, Cambridge"
        )
    )

    us_list = models.TextField(
        default=(
            "SAT Mathematics\n"
            "AP Mathematics\n"
            "AP Physics (1, 2, C)"
        )
    )

    canada_list = models.TextField(
        default=(
            "Secondary school mathematics and sciences\n"
            "IGCSE and A-Level pathways"
        )
    )

    global_exams_list = models.TextField(
        default=(
            "ASVAB (Math and Science)\n"
            "GRE (Quantitative and Physics foundations)\n"
            "IELTS academic preparation"
        )
    )

    intl_why_list = models.TextField(
        default=(
            "Curriculum-specific tutoring\n"
            "Clear communication\n"
            "Flexible online delivery\n"
            "Results-focused instruction"
        )
    )

    intl_cta = models.CharField(
        max_length=100,
        default="Book an International Session"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Courses & International Students Page"