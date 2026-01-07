from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from dashboard.models import Course


# Create your views here.
def home(request):
    courses = Course.objects.order_by("-created_at")[:3]
    return render(request, 'index.html', {'courses': courses})



def about(request):
    return render(request, 'about.html')

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
