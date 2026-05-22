#!/usr/bin/env python
"""
Setup script for LavPune Bus Booking System.
Run this once after setting up the project:
    python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busproject.settings')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 55)
    print("  LavPune Bus Booking System — Setup")
    print("=" * 55)

    # Run migrations
    print("\n[1/3] Running database migrations...")
    from django.core.management import call_command
    call_command('migrate', verbosity=0)
    print("      ✓ Migrations complete")

    django.setup()
    from busapp.models import User

    # Create default admin
    print("\n[2/3] Creating default admin account...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@lavpune.edu',
            first_name='Admin',
            last_name='User',
            role='admin',
            is_staff=True,
        )
        print("      ✓ Admin created: username=admin  password=admin123")
    else:
        print("      ! Admin already exists, skipping.")

    # Create sample slots
    print("\n[3/3] Creating sample bus slots...")
    from busapp.models import BusSlot
    import datetime

    if BusSlot.objects.count() == 0:
        today = datetime.date.today()
        # Find next Sunday
        days_until_sunday = (6 - today.weekday()) % 7 or 7
        next_sunday = today + datetime.timedelta(days=days_until_sunday)

        BusSlot.objects.create(
            service_type='weekend',
            date=next_sunday,
            departure_time=datetime.time(10, 0),
            from_location='Lavasa',
            to_location='Pune',
            total_seats=45,
            description='Regular Sunday morning bus. Pick-up from Main Gate.',
            has_return=True,
            return_time=datetime.time(18, 0),
            return_from='Pune',
            return_to='Lavasa',
            return_seats=45,
            is_active=True,
        )
        print(f"      ✓ Weekend slot created for {next_sunday} (Lavasa→Pune 10AM / Pune→Lavasa 6PM)")

        vacation_date = today + datetime.timedelta(days=14)
        BusSlot.objects.create(
            service_type='vacation',
            date=vacation_date,
            departure_time=datetime.time(8, 0),
            from_location='Lavasa',
            to_location='Pune',
            total_seats=45,
            description='Vacation break bus service. Limited seats — book early!',
            has_return=False,
            is_active=True,
        )
        print(f"      ✓ Vacation slot created for {vacation_date} (Lavasa→Pune 8AM)")
    else:
        print("      ! Slots already exist, skipping sample data.")

    print("\n" + "=" * 55)
    print("  Setup complete! Run the server with:")
    print("  python manage.py runserver")
    print("\n  Then visit:  http://127.0.0.1:8000/")
    print("  Admin login: username=admin  password=admin123")
    print("=" * 55 + "\n")


if __name__ == '__main__':
    # Bootstrap Django before calling main
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'busproject.settings')
    import django
    django.setup()
    main()
