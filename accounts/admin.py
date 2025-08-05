from django.contrib import admin
from .models import User, Profile,PasswordResetOTP,ProfileSpanish
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Info', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(User, UserAdmin)



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'fullname', 'gender', 'date_of_birth',
        'image',
        'weight', 'height', 'abdominal', 'sacroiliac', 'subscapularis', 'triceps',
        'fitness_level', 'trainer',
        'at_home', 'at_gym',
        'martial_arts', 'running', 'other_sports',
        'train_duration', 'interested_workout', 'injuries_discomfort',
        'routine_duration', 'dietary_preferences',
        'allergies', 'food_preference', 'medical_conditions',
        'fitness_goals', 'lifestyle_habits'
    )
    
    search_fields = (
        'user__email', 'user__username', 'fullname'
    )
    
    list_filter = (
        'gender', 'fitness_level', 'trainer', 'routine_duration', 'dietary_preferences', 'lifestyle_habits'
    )




@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'otp', 'created_at', 'is_verified')
    search_fields = ('user__email', 'otp')
    list_filter = ('is_verified', 'created_at')




@admin.register(ProfileSpanish)
class ProfileSpanishAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'fullname', 
        'gender', 
        'date_of_birth', 
        'weight', 
        'height', 
        'fitness_level', 
        'trainer',
        'routine_duration',
        'dietary_preferences',
        'lifestyle_habits'
    ]
    list_filter = ['gender', 'fitness_level', 'trainer', 'dietary_preferences']
    search_fields = ['fullname', 'user__username', 'user__email']
    ordering = ['user']
    readonly_fields = ['user']  # if you want to make the user uneditable

    fieldsets = (
        ("Personal Info", {
            'fields': ('user', 'image', 'fullname', 'gender', 'date_of_birth')
        }),
        ("Body Measurements", {
            'fields': ('weight', 'height', 'abdominal', 'sacroiliac', 'subscapularis', 'triceps')
        }),
        ("Fitness Profile", {
            'fields': ('fitness_level', 'trainer', 'at_home', 'at_gym', 'martial_arts', 'running', 'other_sports')
        }),
        ("Goals & Routine", {
            'fields': ('train_duration', 'interested_workout', 'routine_duration', 'fitness_goals')
        }),
        ("Health & Diet", {
            'fields': ('injuries_discomfort', 'dietary_preferences', 'allergies', 'food_preference', 'medical_conditions', 'lifestyle_habits')
        }),
    )
