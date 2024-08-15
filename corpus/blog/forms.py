from django import forms
from .models import Post,Tag
from corpus.forms import CorpusModelForm

class DateTimeInput(forms.DateTimeInput):
    input_type ='datetime-local'

class blog_form(CorpusModelForm):

    class Meta:
        model=Post
        fields = ['blog_tag','layout','title','description','author_github','text','published_date']
        widgets = {
            'published_date':DateTimeInput(),
        }
    
    blog_tag = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.all()
    )