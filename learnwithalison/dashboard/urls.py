from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('youtube_course_list/', views.ytcourse_list, name='youtube_course_list'),
    path("course/<str:course_id>/", views.course_detail, name="course_detail"),
    path('', views.dashboard, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin/courses/', views.admin_courses, name='admin_courses'),
    path('courses/creation/', views.admin_course_create, name='admin_course_create'),
    path('courses/<int:course_id>/curriculum/', views.admin_course_curriculum, name='admin_course_curriculum'),
    path(
        'courses/<int:course_id>/curriculum/',
        views.admin_course_curriculum,
        name='admin_course_curriculum'
    ),
    path(
        "admin/projections/yearly/",
        views.yearly_projection_view,
        name="yearly_projection"
    ),
    path(
        'courses/<int:course_id>/sections/create/',
        views.admin_course_section_create,
        name='admin_course_section_create'
    ),

    path(
        'courses/<int:course_id>/lessons/upload/',
        views.admin_course_lesson_upload,
        name='admin_course_lesson_upload'
    ),
    path(
        'dashboard/courses/<int:course_id>/lessons/upload/',
        views.resumable_lesson_upload,
        name='resumable_lesson_upload'
    ),
    path('courses/edit/<int:course_id>/', views.admin_course_edit, name='admin_course_edit'),
    path('courses/delete/<int:course_id>/', views.admin_course_delete, name='admin_course_delete'),
    path('categories/', views.admin_categories, name='admin_categories'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),


    # Students
    path('admin/students/', views.admin_students, name='admin_students'),
    path('students/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('students/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    # Instructor
    path('admin/instructor/profile/', views.instructor_profile, name='instructor_profile'),
    path('admin/instructor/courses/', views.instructor_courses, name='instructor_courses'),
    path('admin/instructor/earnings/', views.instructor_earnings, name='instructor_earnings'),

    # Payments
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin/refunds/', views.admin_refunds, name='admin_refunds'),

    # Website
    path('admin/pages/', views.admin_pages, name='admin_pages'),
    path('admin/faqs/', views.admin_faqs, name='admin_faqs'),
    path('admin/testimonials/', views.admin_testimonials, name='admin_testimonials'),

    # Support
    path('admin/support/', views.admin_support, name='admin_support'),

    # Settings & Profile
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path("cart/add/<int:course_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:course_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
]
