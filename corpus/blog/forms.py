from accounts.models import ExecutiveMember
from blog.models import Post
from blog.models import Tag
from django import forms
from django.db.models import Value
from django.db.models.functions import Concat

from corpus.forms import CorpusForm
from corpus.forms import CorpusModelForm


class BlogFilterForm(CorpusForm):
    author = forms.ChoiceField(choices=[])
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(BlogFilterForm, self).__init__(*args, **kwargs)

        # Fetch unique authors from Post model
        author_choices = [(0, "All Authors")] + list(
            ExecutiveMember.objects.annotate(
                full_name=Concat("user__first_name", Value(" "), "user__last_name")
            )
            .values_list("user_id", "full_name")
            .distinct()
        )

        # Fetch SIG (blog_tag) choices from Tag model
        # sig_choices = list(Tag.objects.values_list("id", "tag_name"))
        self.fields["tag"].queryset = Tag.objects.all()

        # Assign choices to fields
        self.fields["author"].choices = author_choices
        # self.fields["sig"].choices = sig_choices


class BlogForm(CorpusModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "author_github", "text", "blog_tag", "slug"]
        widgets = {
            "blog_tag": forms.CheckboxSelectMultiple(),
        }


class AdminBlogForm(CorpusModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "blog_tag",
            "text",
            "ready_for_approval",
            "approver",
            "approved",
            "published_date",
            "slug",
        ]
        widgets = {
            "blog_tag": forms.CheckboxSelectMultiple(),
        }
