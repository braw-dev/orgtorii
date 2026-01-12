"""Models for the companies app."""

import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Industry(models.Model):
    """Normalized industry category."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    name = models.CharField(_("Name"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), unique=True, max_length=100)

    class Meta:
        verbose_name = _("Industry")
        verbose_name_plural = _("Industries")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Company(models.Model):
    """Public company profile."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, max_length=255, db_index=True)
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
        verbose_name=_("Industry"),
    )
    hq_location = models.CharField(_("HQ Location"), max_length=255, blank=True)
    description = models.TextField(_("Description"), blank=True)
    is_stub = models.BooleanField(_("Is Stub"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Company.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Update is_stub based on content
        self.is_stub = not (self.description or self.hq_location or self.industry_id)

        super().save(*args, **kwargs)


class CompanyWebsite(models.Model):
    """Official website URL for a company."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="websites",
        verbose_name=_("Company"),
    )
    url = models.URLField(_("URL"), max_length=500)
    label = models.CharField(
        _("Label"), max_length=50, blank=True, help_text=_('e.g. "Homepage", "Careers", "Blog"')
    )

    class Meta:
        verbose_name = _("Company Website")
        verbose_name_plural = _("Company Websites")
        ordering = ["id"]

    def __str__(self):
        return f"{self.company.name} - {self.label or self.url}"


class CompanyUser(models.Model):
    """Official user associated with a company."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        EDITOR = "EDITOR", _("Editor")
        READ_ONLY = "READ_ONLY", _("Read Only")

    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_users",
        verbose_name=_("Company"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_memberships",
        verbose_name=_("User"),
    )
    role = models.CharField(_("Role"), max_length=20, choices=Role.choices, default=Role.READ_ONLY)

    class Meta:
        verbose_name = _("Company User")
        verbose_name_plural = _("Company Users")
        constraints = [
            models.UniqueConstraint(fields=["company", "user"], name="unique_company_user"),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.company.name} ({self.get_role_display()})"


class CompanyRevision(models.Model):
    """Snapshot of a company's state at a specific point in time."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="revisions",
        verbose_name=_("Company"),
    )
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_edits",
        verbose_name=_("Editor"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(_("Comment"), max_length=255, blank=True)
    snapshot = models.JSONField(
        _("Snapshot"), help_text=_("Full copy of Company fields at this time")
    )

    class Meta:
        verbose_name = _("Company Revision")
        verbose_name_plural = _("Company Revisions")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.company.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
