"""Admin configuration for companies app."""

from django.contrib import admin

from .models import Company, CompanyRevision, CompanyUser, CompanyWebsite, Industry


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    """Admin for Industry model."""

    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


class CompanyWebsiteInline(admin.TabularInline):
    """Inline admin for company websites."""

    model = CompanyWebsite
    extra = 1


class CompanyUserInline(admin.TabularInline):
    """Inline admin for company users."""

    model = CompanyUser
    extra = 0
    raw_id_fields = ["user"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin for Company model."""

    list_display = ["name", "slug", "industry", "hq_location", "is_stub", "created_at"]
    list_filter = ["is_stub", "industry", "created_at"]
    search_fields = ["name", "slug", "description"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [CompanyWebsiteInline, CompanyUserInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(CompanyRevision)
class CompanyRevisionAdmin(admin.ModelAdmin):
    """Admin for CompanyRevision model."""

    list_display = ["company", "editor", "created_at", "comment"]
    list_filter = ["created_at"]
    search_fields = ["company__name", "editor__email", "comment"]
    readonly_fields = ["company", "editor", "created_at", "snapshot"]
    raw_id_fields = ["company", "editor"]

    def has_add_permission(self, request):
        """Revisions should only be created automatically."""
        return False
