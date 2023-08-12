from django import forms
from .models import News
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
   class Meta:
       model = News
       fields = [
           'name',
           'text',
       ]

       def clean_name(self):
           name = self.cleaned_data["name"]
           if name[0].islower():
               raise ValidationError(
                   "Название должно начинаться с заглавной буквы"
               )
           return name

       def clean(self):
           cleaned_data = super().clean()
           text = cleaned_data.get("text")
           if text is not None and len(text) < 20:
               raise ValidationError({
                   "text": "Текст не может быть менее 20 символов."
               })

           name = cleaned_data.get("name")
           if name == text:
               raise ValidationError(
                   "Текст не должен быть идентичен названию."
               )

           return cleaned_data