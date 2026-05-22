from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, BusSlot, Booking


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'role', 'department', 'year_of_study']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department / School'}),
            'year_of_study': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class StudentBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['journey_type', 'reason', 'proof']
        widgets = {
            'journey_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for one-way travel (required for one-way)'}),
            'proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, slot=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.slot = slot
        if slot and not slot.has_return:
            # Only one-way available
            self.fields['journey_type'].choices = [('oneway', 'One Way')]
        elif slot and slot.service_type == 'vacation':
            self.fields['journey_type'].choices = [('oneway', 'One Way')]

    def clean(self):
        cleaned = super().clean()
        jtype = cleaned.get('journey_type')
        reason = cleaned.get('reason')
        proof = cleaned.get('proof')
        slot = self.slot
        if slot and slot.service_type == 'weekend' and jtype == 'oneway':
            if not reason:
                self.add_error('reason', 'Please provide a reason for one-way travel.')
            if not proof:
                self.add_error('proof', 'Please upload proof for one-way travel.')
        return cleaned


class FacultyBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['journey_type', 'reason', 'proof']
        widgets = {
            'journey_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for travel (optional for faculty)'}),
            'proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, slot=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.slot = slot
        if slot and not slot.has_return:
            self.fields['journey_type'].choices = [('oneway', 'One Way')]
        elif slot and slot.service_type == 'vacation':
            self.fields['journey_type'].choices = [('oneway', 'One Way')]


class BusSlotForm(forms.ModelForm):
    class Meta:
        model = BusSlot
        fields = [
            'service_type', 'date', 'departure_time', 'from_location', 'to_location',
            'total_seats', 'description', 'has_return', 'return_time',
            'return_from', 'return_to', 'return_seats'
        ]
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'from_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Lavasa'}),
            'to_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Pune'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short description for this slot'}),
            'has_return': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'hasReturnCheck'}),
            'return_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'return_from': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Pune'}),
            'return_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Lavasa'}),
            'return_seats': forms.NumberInput(attrs={'class': 'form-control'}),
        }
