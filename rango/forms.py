from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    # password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, label='New category name',
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them.
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        # exclude = ('category',)
        # or specify the fields to include (i.e. not include the category field)
        fields = ('title', 'url',)

    # def clean(self):
    #     # super().clean()  # ensures that any validation logic in parent classes is maintained
    #     cleaned_data = self.cleaned_data
    #     url = cleaned_data.get('url')
    #     # If url is not empty and doesn't start with 'http://',
    #     # then prepend 'http://'.
    #     if url and not url.startswith('http://')\
    #             or not url.startswith('https://'):
    #         url = 'http://' + url
    #         cleaned_data['url'] = url
    #         return cleaned_data
