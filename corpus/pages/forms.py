from accounts.models import Faculty
from config.models import SIG
from config.models import Society
from corpus.forms import CorpusModelForm
from django import forms
from newsletter.models import Event


class SIGContentForm(CorpusModelForm):
    class Meta:
        model = SIG
        fields = ["about", "what_we_do", "sig_image"]


class SocietyDashboardForm(CorpusModelForm):
    faculty_advisors = forms.ModelMultipleChoiceField(
        queryset=Faculty.objects.none(),
        required=False,
        help_text="Assign faculty advisors from this SIG.",
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkbox checkbox-primary checkbox-sm"}
        ),
    )

    class Meta:
        model = Society
        fields = ["name", "url", "description", "image", "dark_image"]

    def __init__(self, *args, **kwargs):
        self.sig = kwargs.pop("sig", None)
        super().__init__(*args, **kwargs)
        self.fields["faculty_advisors"].widget.attrs["class"] = "checkbox checkbox-primary checkbox-sm"

        if self.sig is not None:
            advisors_qs = Faculty.objects.filter(sig=self.sig).select_related("user")
            self.fields["faculty_advisors"].queryset = advisors_qs
            self.fields["faculty_advisors"].label_from_instance = (
                lambda obj: (
                    f"{obj.user.first_name} {obj.user.last_name}".strip()
                    or obj.user.email
                )
            )
            if self.instance and self.instance.pk:
                self.fields["faculty_advisors"].initial = advisors_qs.filter(
                    society=self.instance
                )

    def save_faculty_advisors(self, society, sig):
        selected_advisor_ids = list(
            self.cleaned_data.get("faculty_advisors", []).values_list("id", flat=True)
        )

        Faculty.objects.filter(sig=sig, society=society).exclude(
            id__in=selected_advisor_ids
        ).update(society=None)

        if selected_advisor_ids:
            Faculty.objects.filter(sig=sig, id__in=selected_advisor_ids).update(
                society=society
            )
