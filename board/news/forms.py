from django import forms
from django.core.exceptions import ValidationError
from .models import Post, User, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'postCategory',
            'upload',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title[0].islower():
            raise ValidationError(
                {"Заголовок должен начинаться с заглавной буквы"}
            )

        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичен названию."
            )

        return cleaned_data


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'resp_text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('resp_text')

        return cleaned_data
