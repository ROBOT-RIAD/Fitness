from django.contrib import admin
from .models import TermsAndConditions, PrivacyPolicy,Email
# Register your models here.



class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent add if one instance already exists
        if self.model.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Allow delete (if needed)
        return True

    def changelist_view(self, request, extra_context=None):
        # Redirect to the edit page if object exists
        obj = self.model.objects.first()
        if obj:
            from django.urls import reverse
            from django.shortcuts import redirect
            return redirect(reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=(obj.id,)))
        return super().changelist_view(request, extra_context)
    

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('short_text',)

    def short_text(self, obj):
        return obj.text[:75] + "..." if len(obj.text) > 75 else obj.text
    short_text.short_description = "Terms & Conditions"


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('short_text',)

    def short_text(self, obj):
        return obj.text[:75] + "..." if len(obj.text) > 75 else obj.text
    short_text.short_description = "Privacy Policy"



@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('user', 'subject', 'sent_at', 'sent_status')

    # Add search functionality for the title and user email
    search_fields = ('user__email', 'subject')

    # Add filters (e.g., filter by sent status)
    list_filter = ('sent_status',)

    # Set the default ordering (order by sent_at in descending order)
    ordering = ('-sent_at',)