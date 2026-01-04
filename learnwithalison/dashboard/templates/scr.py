import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# List of HTML files to create
template_files = [
    "dashboard.html",
    "courses.html",
    "add_course.html",
    "categories.html",
    "students.html",
    "instructor_profile.html",
    "instructor_courses.html",
    "instructor_earnings.html",
    "orders.html",
    "transactions.html",
    "refunds.html",
    "pages.html",
    "faqs.html",
    "testimonials.html",
    "support_tickets.html",
    "settings.html",
    "profile.html",
]

# Template boilerplate content
template_content = """{% extends 'dashlayout.html' %}
{% load static %}
{% block content %}

{% endblock %}
"""

created = []
skipped = []

for filename in template_files:
    file_path = os.path.join(BASE_DIR, filename)

    if os.path.exists(file_path):
        skipped.append(filename)
        continue

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template_content)

    created.append(filename)

print("✅ Files created in current folder:")
for f in created:
    print(f"  - {f}")

print("\n⚠️ Files skipped (already exist):")
for f in skipped:
    print(f"  - {f}")
