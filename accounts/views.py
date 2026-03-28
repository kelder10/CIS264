from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy

from reservations.models import Reservation
from reviews.models import Review
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Welcome to Indian Creek Cycles, {user.first_name}! Your account has been created.'
            )
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Create Account'
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                messages.success(request, f'Welcome back, {user.first_name or username}!')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'title': 'Sign In'
    }
    return render(request, 'accounts/login.html', context)


@login_required
def user_logout(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """User profile view with reservations and reviews."""
    # Get user's reservations
    reservations = Reservation.objects.filter(
        user=request.user
    ).select_related('bike').order_by('-created_at')[:5]
    
    # Get user's reviews
    reviews = Review.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'reservations': reservations,
        'reviews': reviews,
        'reservation_count': Reservation.objects.filter(user=request.user).count(),
        'review_count': Review.objects.filter(user=request.user).count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'title': 'Edit Profile'
    }
    return render(request, 'accounts/edit_profile.html', context)
