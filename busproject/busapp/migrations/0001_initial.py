from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(
                    error_messages={'unique': 'A user with that username already exists.'},
                    max_length=150,
                    unique=True,
                    validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                    verbose_name='username',
                )),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('student', 'Student'), ('faculty', 'Faculty'), ('admin', 'Admin')], default='student', max_length=10)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('year_of_study', models.CharField(blank=True, choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year'), ('5', '5th Year')], max_length=1)),
                ('groups', models.ManyToManyField(blank=True, related_name='busapp_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='busapp_user_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BusSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('weekend', 'Weekend Bus Service'), ('vacation', 'Vacation Bus Service')], default='weekend', max_length=10)),
                ('date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('from_location', models.CharField(max_length=100)),
                ('to_location', models.CharField(max_length=100)),
                ('total_seats', models.PositiveIntegerField(default=45)),
                ('description', models.TextField(blank=True)),
                ('has_return', models.BooleanField(default=False)),
                ('return_time', models.TimeField(blank=True, null=True)),
                ('return_from', models.CharField(blank=True, max_length=100)),
                ('return_to', models.CharField(blank=True, max_length=100)),
                ('return_seats', models.PositiveIntegerField(default=45)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['date', 'departure_time'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journey_type', models.CharField(choices=[('oneway', 'One Way'), ('bothway', 'Both Ways')], default='oneway', max_length=10)),
                ('reason', models.TextField(blank=True)),
                ('proof', models.FileField(blank=True, null=True, upload_to='proofs/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('admin_note', models.TextField(blank=True)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='busapp.busslot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='busapp.user')),
            ],
            options={
                'ordering': ['-booked_at'],
                'unique_together': {('user', 'slot')},
            },
        ),
    ]
