"""abu_driving_school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import abu_view, signup_view, reviews, leave_review, submit_review, custom_login_view, profile_view, delete_review, reviews_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', abu_view, name='abu'),  # Homepage view
    path('signup/', signup_view, name='signup'),  # Signup view
    path('login/', custom_login_view, name='login'),  # Custom login view
    path('logout/', auth_views.LogoutView.as_view(next_page='abu'), name='logout'),  # Logout view
    path('reviews/', reviews_view, name='reviews'),  # Reviews view
    path('reviews/submit/', leave_review, name='leave_review'),  # Leave a review
    path('submit_review/', submit_review, name='submit_review'),  # Submit review
    path('profile/', profile_view, name='profile'),
    path('reviews/delete/<int:review_id>/', delete_review, name='delete_review'),
]


