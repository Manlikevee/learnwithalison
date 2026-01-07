from django import forms
from .models import HomePage, AboutPage, InternationalAndProducts


class BaseBootstrapForm(forms.ModelForm):
    """
    Base form that applies Bootstrap form-control to all fields
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # File inputs also support form-control in Bootstrap 5
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_class} form-control".strip()


class HomePageForm(BaseBootstrapForm):
    class Meta:
        model = HomePage
        fields = [
            # HERO
            "hero_badge",
            "hero_title",
            "hero_subtitle",
            "hero_background",

            # UNIVERSITY CARD
            "card_intro",
            "card_heading",
            "card_button_text",
            "card1_title",
            "card1_text",
            "card2_title",
            "card2_text",
            "card3_title",
            "card3_text",

            # WELCOME
            "welcome_title",
            "welcome_intro",
            "welcome_body",

            # INSTRUCTOR
            "instructor_name",
            "instructor_bio",

            # EXAMS
            "exams_section_title",
            "exams_section_intro",
            "exams_nigeria_title",
            "exams_nigeria_list",
            "exams_uk_title",
            "exams_uk_list",
            "exams_us_title",
            "exams_us_list",
            "exams_international_title",
            "exams_international_list",
            "exams_global_title",
            "exams_global_list",

            # WHY CHOOSE
            "why_choose_title",
            "why_choose_intro",
            "why_choose_points",

            # SOCIALS
            "instagram",
            "tiktok",
            "facebook",
            "twitter",
        ]

        widgets = {
            "hero_subtitle": forms.Textarea(attrs={"rows": 3}),
            "welcome_intro": forms.Textarea(attrs={"rows": 3}),
            "welcome_body": forms.Textarea(attrs={"rows": 4}),
            "instructor_bio": forms.Textarea(attrs={"rows": 4}),
            "why_choose_intro": forms.Textarea(attrs={"rows": 3}),
            "why_choose_points": forms.Textarea(attrs={"rows": 5}),
            "exams_nigeria_list": forms.Textarea(attrs={"rows": 4}),
            "exams_uk_list": forms.Textarea(attrs={"rows": 5}),
            "exams_us_list": forms.Textarea(attrs={"rows": 5}),
            "exams_international_list": forms.Textarea(attrs={"rows": 4}),
            "exams_global_list": forms.Textarea(attrs={"rows": 4}),
        }


# ================= ABOUT PAGE =================
class AboutPageForm(BaseBootstrapForm):
    class Meta:
        model = AboutPage
        fields = "__all__"
        widgets = {
            "academic_list": forms.Textarea(attrs={"rows": 4}),
            "experience_body": forms.Textarea(attrs={"rows": 5}),
            "philosophy_list": forms.Textarea(attrs={"rows": 4}),
            "values_list": forms.Textarea(attrs={"rows": 4}),
            "tutoring_services_list": forms.Textarea(attrs={"rows": 4}),
            "math_support": forms.Textarea(attrs={"rows": 3}),
            "physics_support": forms.Textarea(attrs={"rows": 4}),
            "chemistry_support": forms.Textarea(attrs={"rows": 3}),
            "programming_support": forms.Textarea(attrs={"rows": 3}),
            "process_list": forms.Textarea(attrs={"rows": 4}),
            "delivery_list": forms.Textarea(attrs={"rows": 3}),
            "pricing_body": forms.Textarea(attrs={"rows": 4}),
        }


# ================= INTERNATIONAL & PRODUCTS =================
class InternationalProductsForm(BaseBootstrapForm):
    class Meta:
        model = InternationalAndProducts
        fields = "__all__"
        widgets = {
            "digital_products_list": forms.Textarea(attrs={"rows": 4}),
            "digital_audience_list": forms.Textarea(attrs={"rows": 4}),
            "digital_access_list": forms.Textarea(attrs={"rows": 3}),
            "uk_list": forms.Textarea(attrs={"rows": 4}),
            "us_list": forms.Textarea(attrs={"rows": 3}),
            "canada_list": forms.Textarea(attrs={"rows": 3}),
            "global_exams_list": forms.Textarea(attrs={"rows": 3}),
            "intl_why_list": forms.Textarea(attrs={"rows": 4}),
        }
