from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Your full name"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Your email"
            }
        )
    )

    content  = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                "placeholder": "Your message" 
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(email)
        if not "gmail.com" in email:
            raise forms.ValidationError("your email must be gmail")
        return email

    # def clean_content(self):
    #     print(self.cleaned_data.get("content"))
    #     raise forms.ValidationError("Content is wrong.")
