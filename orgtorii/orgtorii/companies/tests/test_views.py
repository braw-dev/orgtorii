"""Tests for companies views."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from orgtorii.companies.models import Company

User = get_user_model()


@pytest.mark.django_db
class TestCompanyCreateView:
    """Tests for company creation."""

    def test_create_company_requires_login(self, client):
        """Test that creating a company requires authentication."""
        url = reverse("companies:create")
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_create_company_with_valid_data(self, client, django_user_model):
        """Test creating a company with valid data."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        client.force_login(user)

        url = reverse("companies:create")
        response = client.post(
            url,
            {
                "name": "Acme Corp",
                "description": "A test company",
                "hq_location": "San Francisco, USA",
            },
        )

        assert response.status_code == 302
        company = Company.objects.get(name="Acme Corp")
        assert company.slug == "acme-corp"
        assert company.is_stub is False
        assert response.url == reverse("companies:detail", kwargs={"slug": company.slug})

    def test_create_company_minimal_data(self, client, django_user_model):
        """Test creating a company with only name (stub)."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        client.force_login(user)

        url = reverse("companies:create")
        response = client.post(url, {"name": "Minimal Corp"})

        assert response.status_code == 302
        company = Company.objects.get(name="Minimal Corp")
        assert company.is_stub is True

    def test_slug_collision_handling(self, client, django_user_model):
        """Test that slug collisions are handled with numeric suffix."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        client.force_login(user)

        # Create first company
        Company.objects.create(name="Acme Corp", slug="acme-corp")

        # Create second company with same name
        url = reverse("companies:create")
        response = client.post(url, {"name": "Acme Corp"})

        assert response.status_code == 302
        company = Company.objects.get(slug="acme-corp-1")
        assert company.name == "Acme Corp"


@pytest.mark.django_db
class TestCompanyListView:
    """Tests for company list view."""

    def test_list_companies(self, client):
        """Test listing companies."""
        Company.objects.create(name="Company A", description="Test A")
        Company.objects.create(name="Company B", description="Test B")

        url = reverse("companies:list")
        response = client.get(url)

        assert response.status_code == 200
        assert b"Company A" in response.content
        assert b"Company B" in response.content

    def test_search_companies(self, client):
        """Test searching companies by name."""
        Company.objects.create(name="Acme Corp", description="Test")
        Company.objects.create(name="Beta Inc", description="Test")

        url = reverse("companies:list")
        response = client.get(url, {"q": "Acme"})

        assert response.status_code == 200
        assert b"Acme Corp" in response.content
        assert b"Beta Inc" not in response.content


@pytest.mark.django_db
class TestCompanyDetailView:
    """Tests for company detail view."""

    def test_view_company_detail(self, client):
        """Test viewing a company detail page."""
        company = Company.objects.create(
            name="Test Company",
            slug="test-company",
            description="A test company",
            hq_location="San Francisco, USA",
        )

        url = reverse("companies:detail", kwargs={"slug": company.slug})
        response = client.get(url)

        assert response.status_code == 200
        assert b"Test Company" in response.content
        assert b"San Francisco, USA" in response.content


@pytest.mark.django_db
class TestCompanyUpdateView:
    """Tests for company update view."""

    def test_update_company_requires_login(self, client):
        """Test that updating a company requires authentication."""
        company = Company.objects.create(name="Test Company", slug="test-company")
        url = reverse("companies:edit", kwargs={"slug": company.slug})
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_update_company_data(self, client, django_user_model):
        """Test updating company data creates a revision."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        client.force_login(user)

        company = Company.objects.create(name="Old Name", slug="old-name")

        url = reverse("companies:edit", kwargs={"slug": company.slug})
        response = client.post(
            url,
            {
                "name": "New Name",
                "description": "Updated description",
                "form-TOTAL_FORMS": "0",
                "form-INITIAL_FORMS": "0",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
            },
        )

        assert response.status_code == 302
        company.refresh_from_db()
        assert company.name == "New Name"
        assert company.description == "Updated description"
        assert company.revisions.count() >= 1


@pytest.mark.django_db
class TestCompanyHistoryView:
    """Tests for company history view."""

    def test_view_company_history(self, client, django_user_model):
        """Test viewing company revision history."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        company = Company.objects.create(name="Test Company", slug="test-company")

        from orgtorii.companies.services import create_company_revision

        create_company_revision(company, editor=user, comment="First edit")
        create_company_revision(company, editor=user, comment="Second edit")

        url = reverse("companies:history", kwargs={"slug": company.slug})
        response = client.get(url)

        assert response.status_code == 200
        assert b"First edit" in response.content
        assert b"Second edit" in response.content


@pytest.mark.django_db
class TestCompanyRevertView:
    """Tests for company revert view."""

    def test_revert_company_requires_login(self, client):
        """Test that reverting a company requires authentication."""
        company = Company.objects.create(name="Test Company", slug="test-company")

        from orgtorii.companies.services import create_company_revision

        revision = create_company_revision(company, comment="Test")

        url = reverse("companies:revert", kwargs={"slug": company.slug, "revision_id": revision.id})
        response = client.post(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_revert_company_to_previous_state(self, client, django_user_model):
        """Test reverting a company to a previous revision."""
        user = django_user_model.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        client.force_login(user)

        company = Company.objects.create(
            name="Original Name", slug="original-name", description="Original"
        )

        from orgtorii.companies.services import create_company_revision

        old_revision = create_company_revision(company, editor=user, comment="First version")

        # Update company
        company.name = "New Name"
        company.description = "New description"
        company.save()
        create_company_revision(company, editor=user, comment="Updated")

        # Revert to old revision
        url = reverse(
            "companies:revert", kwargs={"slug": company.slug, "revision_id": old_revision.id}
        )
        response = client.post(url)

        assert response.status_code == 302
        company.refresh_from_db()
        assert company.name == "Original Name"
        assert company.description == "Original"
