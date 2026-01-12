"""Services for the companies app."""

from django.db import transaction

from .models import Company, CompanyRevision


def create_company_revision(company: Company, editor=None, comment: str = "") -> CompanyRevision:
    """
    Create a revision snapshot of a company.

    Args:
        company: The Company instance to snapshot
        editor: The User who made the change (optional)
        comment: Optional comment about the change

    Returns:
        CompanyRevision instance
    """
    snapshot = {
        "name": company.name,
        "slug": company.slug,
        "industry": company.industry.name if company.industry else None,
        "hq_location": company.hq_location,
        "description": company.description,
        "is_stub": company.is_stub,
        "websites": [{"url": w.url, "label": w.label} for w in company.websites.all()],
    }

    return CompanyRevision.objects.create(
        company=company, editor=editor, comment=comment, snapshot=snapshot
    )


def save_company_with_revision(company: Company, editor=None, comment: str = "") -> Company:
    """
    Save a company and create a revision snapshot.

    Args:
        company: The Company instance to save
        editor: The User who made the change (optional)
        comment: Optional comment about the change

    Returns:
        The saved Company instance
    """
    with transaction.atomic():
        company.save()
        create_company_revision(company, editor=editor, comment=comment)
    return company


def restore_company_from_revision(revision: CompanyRevision, editor=None) -> Company:
    """
    Restore a company to a previous revision state.

    Args:
        revision: The CompanyRevision to restore from
        editor: The User performing the restore

    Returns:
        The updated Company instance
    """
    company = revision.company
    snapshot = revision.snapshot

    with transaction.atomic():
        # Update company fields from snapshot
        company.name = snapshot.get("name", company.name)
        company.hq_location = snapshot.get("hq_location", "")
        company.description = snapshot.get("description", "")

        # Handle industry (need to look it up by name)
        industry_name = snapshot.get("industry")
        if industry_name:
            from .models import Industry

            industry, _ = Industry.objects.get_or_create(name=industry_name)
            company.industry = industry
        else:
            company.industry = None

        company.save()

        # Handle websites - delete all and recreate
        company.websites.all().delete()
        websites_data = snapshot.get("websites", [])
        for website_data in websites_data:
            from .models import CompanyWebsite

            CompanyWebsite.objects.create(
                company=company,
                url=website_data.get("url"),
                label=website_data.get("label", ""),
            )

        # Create a new revision for the restore action
        create_company_revision(
            company,
            editor=editor,
            comment=f"Restored from revision {revision.created_at.strftime('%Y-%m-%d %H:%M')}",
        )

    return company
