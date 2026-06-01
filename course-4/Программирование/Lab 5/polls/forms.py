from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PollCreateForm(forms.Form):
    title = forms.CharField(
        label="Заголовок вопроса",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    choices = forms.CharField(
        label="Варианты ответа (по одному на строку)",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Вариант 1\nВариант 2\nВариант 3",
            }
        ),
    )

    def clean_choices(self):
        raw = self.cleaned_data["choices"]
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        if len(lines) < 2:
            raise forms.ValidationError(
                "Добавьте как минимум два варианта ответа (каждый на новой строке)."
            )
        return lines


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.widget.attrs.get("class"):
                field.widget.attrs["class"] = "form-control"


