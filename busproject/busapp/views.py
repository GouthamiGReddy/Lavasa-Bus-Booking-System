from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import User, BusSlot, Booking
from .forms import SignupForm, LoginForm, StudentBookingForm, FacultyBookingForm, BusSlotForm


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
        return redirect('dashboard')
    return render(request, 'busapp/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect('dashboard')
    return render(request, 'busapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        return redirect('admin_dashboard')
    
    # Get upcoming active slots
    today = timezone.now().date()
    slots = BusSlot.objects.filter(is_active=True, date__gte=today).order_by('date', 'departure_time')
    
    # Get user's bookings
    my_bookings = Booking.objects.filter(user=user).select_related('slot').order_by('-booked_at')
    
    # Booked slot IDs for this user
    booked_slot_ids = list(my_bookings.values_list('slot_id', flat=True))
    
    context = {
        'slots': slots,
        'my_bookings': my_bookings,
        'booked_slot_ids': booked_slot_ids,
    }
    return render(request, 'busapp/dashboard.html', context)


@login_required
def book_slot(request, slot_id):
    user = request.user
    if user.role == 'admin':
        messages.error(request, 'Admins cannot book seats.')
        return redirect('admin_dashboard')

    slot = get_object_or_404(BusSlot, id=slot_id, is_active=True)

    # Check if already booked
    existing = Booking.objects.filter(user=user, slot=slot).first()
    if existing:
        messages.warning(request, 'You have already booked this slot.')
        return redirect('dashboard')

    # Check seat availability
    if slot.available_seats() <= 0:
        messages.error(request, 'Sorry, no seats available for this slot.')
        return redirect('dashboard')

    FormClass = StudentBookingForm if user.role == 'student' else FacultyBookingForm

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, slot=slot)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = user
            booking.slot = slot
            # Vacation service: always one-way
            if slot.service_type == 'vacation':
                booking.journey_type = 'oneway'
            booking.save()
            messages.success(request, 'Booking submitted successfully! Pending admin approval.')
            return redirect('dashboard')
    else:
        form = FormClass(slot=slot)

    context = {
        'slot': slot,
        'form': form,
    }
    template = 'busapp/book_student.html' if user.role == 'student' else 'busapp/book_faculty.html'
    return render(request, template, context)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Your booking has been withdrawn.')
    return redirect('dashboard')


# ─── ADMIN VIEWS ────────────────────────────────────────────────────────────────

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, 'Access denied. Admins only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    slots = BusSlot.objects.filter(is_active=True).order_by('date', 'departure_time')
    all_bookings = Booking.objects.select_related('user', 'slot').order_by('-booked_at')
    
    # Stats
    total_bookings = all_bookings.count()
    pending_bookings = all_bookings.filter(status='pending').count()
    approved_bookings = all_bookings.filter(status='approved').count()
    total_users = User.objects.exclude(role='admin').count()
    
    context = {
        'slots': slots,
        'all_bookings': all_bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'total_users': total_users,
        'today': today,
    }
    return render(request, 'busapp/admin_dashboard.html', context)


@admin_required
def admin_add_slot(request):
    form = BusSlotForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        slot = form.save(commit=False)
        slot.is_active = True
        # Vacation: disable return
        if slot.service_type == 'vacation':
            slot.has_return = False
        slot.save()
        messages.success(request, 'Slot created successfully!')
        return redirect('admin_dashboard')
    return render(request, 'busapp/admin_slot_form.html', {'form': form, 'action': 'Add'})


@admin_required
def admin_edit_slot(request, slot_id):
    slot = get_object_or_404(BusSlot, id=slot_id)
    form = BusSlotForm(request.POST or None, instance=slot)
    if request.method == 'POST' and form.is_valid():
        updated = form.save(commit=False)
        if updated.service_type == 'vacation':
            updated.has_return = False
        updated.save()
        messages.success(request, 'Slot updated successfully!')
        return redirect('admin_dashboard')
    return render(request, 'busapp/admin_slot_form.html', {'form': form, 'action': 'Edit', 'slot': slot})


@admin_required
def admin_delete_slot(request, slot_id):
    slot = get_object_or_404(BusSlot, id=slot_id)
    if request.method == 'POST':
        slot.delete()  # Permanent deletion
        messages.success(request, 'Slot permanently deleted.')
    return redirect('admin_dashboard')


@admin_required
def admin_booking_action(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('admin_note', '')
        if action == 'approve':
            booking.status = 'approved'
            booking.admin_note = note
            booking.save()
            messages.success(request, f'Booking by {booking.user.get_full_name()} approved.')
        elif action == 'cancel':
            booking.status = 'cancelled'
            booking.admin_note = note
            booking.save()
            messages.success(request, f'Booking by {booking.user.get_full_name()} cancelled.')
        elif action == 'revert':
            booking.status = 'pending'
            booking.admin_note = ''
            booking.save()
            messages.success(request, f'Booking reverted to pending.')
    return redirect('admin_dashboard')


@admin_required
def admin_users(request):
    users = User.objects.exclude(role='admin').order_by('role', 'last_name')
    return render(request, 'busapp/admin_users.html', {'users': users})


@admin_required
def admin_slot_bookings(request, slot_id):
    slot = get_object_or_404(BusSlot, id=slot_id)
    bookings = Booking.objects.filter(slot=slot).select_related('user').order_by('-booked_at')
    return render(request, 'busapp/admin_slot_bookings.html', {'slot': slot, 'bookings': bookings})
