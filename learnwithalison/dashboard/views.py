from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.models import Profile


# Create your views here.

def course_list(request):
    return render(request, 'courses.html')


def course_detail(request, course_id):
    return render(request, "course-detail.html", {
        "course_id": course_id
    })

@login_required
def dashboard(request):
    user = request.user

    # ✅ Safely get or create profile
    profile, created = Profile.objects.get_or_create(user=user)

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

        # 🔁 Redirect back to same page (safe fallback)
        return redirect(request.META.get("HTTP_REFERER", "dashboard"))

    return render(request, "dashboard.html", {
        "profile": profile
    })