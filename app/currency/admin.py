from currency.models import ContactUs, Rate, Source

from django.contrib import admin

from rangefilter.filters import DateRangeFilter


class RateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'source',
        'buy',
        'sale',
        'base_type',
        'type',
        'created',
    )
    readonly_fields = (
        'type',
        'base_type',
    )
    list_filter = (
        'type',
        'base_type',
        ('created', DateRangeFilter),
    )

    def has_delete_permission(self, request, obj=None):
        return False


class SourceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = (
        'id',
        'name',
        'code_name',
        'source_url',
    )
    list_filter = (
        'code_name',
    )


class ContactUsAdmin(admin.ModelAdmin):
    search_fields = ['email_from', 'reply_to']
    list_display = (
        'id',
        'email_from',
        'reply_to',
        'subject',
        'message',
        'created',
    )
    list_filter = (
        ('created', DateRangeFilter),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Rate, RateAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
