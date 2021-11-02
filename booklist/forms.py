from django import forms
from .models import Book


class DateInput(forms.DateInput):
    input_type = 'date'


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title', 'language_book', 'published_date',
            'authors_name', 'isbn13_number', 'page_number', 'link_book_cover'
        )
        widgets = {
            'published_date': DateInput(),
        }


class InputForm(forms.ModelForm):
    published_date_from = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
        required=False,
        label='Daty od ',
    )
    published_date_to = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
        required=False,
        label='Daty do ',
    )

    CHOICES = (
        ('ascending', 'rosnąco'),
        ('descending', 'malejąco'),
    )
    order = forms.CharField(
        widget=forms.Select(choices=CHOICES),
        required=False,
    )

    class Meta:
        model = Book
        # fields = ['published_date']
        fields = {
            'title': ['icontains'],
            'authors_name': ['icontains'],
            'language_book': ['icontains'],
            # 'published_date': ['gte', 'lte'],
        }
        # widgets = {
        #     'published_date': DateInput(),
        # }

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['authors_name'].required = False
        self.fields['language_book'].required = False
        self.fields['title'].value = 'dupa'
        # self.fields['email'].label = "New Email Label"




# good example https://www.fullstackpython.com/django-forms-modelform-examples.html
# from django.forms import ModelForm
# from gears.widgets import DropdownSelectSubmit
# from proceedings.models import CameraReady
# EMPTY_VOLUME_LABEL = '(no volume)'
# class UpdateVolumeForm(ModelForm):
#
#     class Meta:
#         model = CameraReady
#         fields = ['volume']
    # widgets = {
    #     'volume': DropdownSelectSubmit(
    #         empty_label=EMPTY_VOLUME_LABEL,
    #         label_class='font-weight-normal dccn-text-small',
    #         empty_label_class='text-warning-18',
    #         nonempty_label_class='text-success-18',
    #     )
    # }
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['volume'].queryset = self.instance.proc_type.volumes.all()
    #     self.fields['volume'].empty_label = EMPTY_VOLUME_LABEL

    # fields = ['ordering']
    # widgets = {'ordering': Select(choices=CHOICES)}
    # from django.forms import ModelForm, Textarea
    # widgets = {'name': Textarea(attrs={'cols': 80, 'rows': 20}),}
    # verbose_name = "E-Mail Address"  - we can use it as parameter in field

    # widgets = {'published_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})}
    # labels = {
    #     'name': _('Writer'),
    # }
    # help_texts = {
    #     'name': _('Some useful help text.'),
    # }
    # , null = True, blank = True


    # published_date_gte = forms.CharField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # published_date_gte = forms.DateField(widget=forms.widgets.DateInput(format='%Y/%m/%d', attrs={'type': 'date'}))
    # DateField has optional argument  input_formats
    # default = '', blank = True

# DATE_INPUT_FORMATS = ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d')
# class MyModelForm(forms.ModelForm):
#     issue_date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS)












