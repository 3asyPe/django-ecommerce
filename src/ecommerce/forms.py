from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField()
    content = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(email)
        if not "gmail.com" in email:
            raise forms.ValidationError("your email must be by gmail")
        return email
