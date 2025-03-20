from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from itertools import chain
import json
import os
from django.shortcuts import render
from .models import Review


# View to render abu.html
def abu_view(request):
    return render(request, "abu.html")


def load_reviews_from_json():
    """Load reviews from reviews.json file."""
    reviews_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reviews.json')
    
    try:
        with open(reviews_file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def reviews_view(request):
    # Load static reviews from the JSON file
    static_reviews = load_reviews_from_json()

    # Query dynamic reviews from the database
    queryset_reviews = Review.objects.all().order_by('-created_at')

    # Combine QuerySet and static reviews
    combined_reviews = list(queryset_reviews) + static_reviews
    total_reviews = len(combined_reviews)

    return render(request, 'reviews.html', {'reviews': combined_reviews, 'total_reviews': total_reviews})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create the new user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Authenticate and log the user in
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have signed up and logged in successfully!")
                return redirect('abu')  # Redirect to the desired page after signup and login

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('abu')  # Redirect to the 'abu' view after login
            else:
                # If user authentication fails (wrong username or password)
                messages.error(request, "Invalid username or password.")
        else:
            # If form is not valid (for other reasons)
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    # Clear messages related to non-login actions (e.g., review errors)
    if 'review' in request.GET:  # Only clear messages if it's a 'review' related page
        messages.get_messages(request).used = True  # Clears out old messages
        
    return render(request, 'registration/login.html', {'form': form})


# Custom login view
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('abu')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'registration/login.html')


# View to display all reviews
def reviews(request):
    all_reviews = Review.objects.all().order_by('-created_at')  # Sort reviews by created_at in descending order
    return render(request, 'reviews.html', {'reviews': all_reviews})

# views.py
@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('reviews')  # Redirect to reviews page after submission
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'form': form})


# Leave review view for rendering the form
@login_required
def leave_review(request):
    form = ReviewForm()
    return render(request, 'leave_review.html', {'form': form})


@login_required  # Ensure the user is logged in before accessing the profile page
def profile_view(request):
    # The logged-in user's data will be available in 'request.user'
    return render(request, 'profile.html', {'user': request.user})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
        messages.success(request, 'Your review has been deleted successfully!')
    else:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    return redirect('reviews')  # Redirect to reviews page after deletion



# Review list view using class-based view
class ReviewListView(ListView):
    model = Review
    template_name = 'reviews.html'
    context_object_name = 'reviews'


# Submit review view using class-based view
class SubmitReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['comment', 'rating']
    template_name = 'submit_review.html'
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your review has been submitted!")
        return super().form_valid(form)


