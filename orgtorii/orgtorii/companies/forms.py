"""Forms for the companies app."""

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import Company, CompanyWebsite, Industry


class CompanyForm(forms.ModelForm):
    """Form for creating and updating Company profiles."""

    class Meta:
        model = Company
        fields = ["name", "industry", "hq_location", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "industry": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "hq_location": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "description": forms.Textarea(
                attrs={"class": "textarea textarea-bordered w-full", "rows": 5}
            ),
        }
        help_texts = {
            "name": _("The legal or common name of the company"),
            "industry": _("Select the primary industry this company operates in"),
            "hq_location": _("City and country of the company headquarters"),
            "description": _("A brief description of what this company does"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["industry"].queryset = Industry.objects.all().order_by("name")
        self.fields["industry"].empty_label = _("Select an industry...")


class CompanyWebsiteForm(forms.ModelForm):
    """Form for company website entries."""

    class Meta:
        model = CompanyWebsite
        fields = ["url", "label"]
        widgets = {
            "url": forms.URLInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "https://"}
            ),
            "label": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": _("e.g. Homepage, Careers"),
                }
            ),
        }


CompanyWebsiteFormSet = inlineformset_factory(
    Company,
    CompanyWebsite,
    form=CompanyWebsiteForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)
