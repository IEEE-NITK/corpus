from django import forms


# Not exactly DRY, but I don't know of any cleaner way to do it.


class CorpusForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CorpusForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = """
                mt-1 block w-full rounded-md border-base-800
                text-black shadow-sm focus:border-primary
                focus:ring focus:ring-primary-200 focus:ring-opacity-50
            """


class CorpusModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CorpusModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = """
                mt-1 block w-full rounded-md border-base-800
                text-black shadow-sm focus:border-primary
                focus:ring focus:ring-primary-200 focus:ring-opacity-50
            """
