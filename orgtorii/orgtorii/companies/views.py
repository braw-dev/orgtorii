"""Views for the companies app."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CompanyForm, CompanyWebsiteFormSet
from .models import Company, CompanyRevision
from .services import create_company_revision, restore_company_from_revision


class CompanyListView(ListView):
    """List all companies with search and pagination."""

    model = Company
    template_name = "companies/company_list.html"
    context_object_name = "companies"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related("industry")
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class CompanyDetailView(DetailView):
    """Display a single company profile."""

    model = Company
    template_name = "companies/company_detail.html"
    context_object_name = "company"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return super().get_queryset().select_related("industry").prefetch_related("websites")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_revision"] = self.object.revisions.first()
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """Create a new company profile."""

    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"

    def get_success_url(self):
        return reverse("companies:detail", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        create_company_revision(self.object, editor=self.request.user, comment="Initial creation")
        return response


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing company profile."""

    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["website_formset"] = CompanyWebsiteFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["website_formset"] = CompanyWebsiteFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        website_formset = context["website_formset"]

        with transaction.atomic():
            self.object = form.save()
            if website_formset.is_valid():
                website_formset.instance = self.object
                website_formset.save()
            create_company_revision(
                self.object, editor=self.request.user, comment="Profile updated"
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("companies:detail", kwargs={"slug": self.object.slug})


class CompanyHistoryView(DetailView):
    """Display revision history for a company."""

    model = Company
    template_name = "companies/company_history.html"
    context_object_name = "company"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["revisions"] = self.object.revisions.select_related("editor").all()
        return context


class CompanyRevertView(LoginRequiredMixin, View):
    """Revert a company to a previous revision."""

    def post(self, request, slug, revision_id):
        company = get_object_or_404(Company, slug=slug)
        revision = get_object_or_404(CompanyRevision, id=revision_id, company=company)

        restore_company_from_revision(revision, editor=request.user)
        messages.success(
            request,
            _("Company successfully restored to revision from %(date)s")
            % {"date": revision.created_at.strftime("%Y-%m-%d %H:%M")},
        )

        return redirect("companies:detail", slug=company.slug)
