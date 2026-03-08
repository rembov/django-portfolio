from django import forms
from .models import Comment
import random

class CommentForm(forms.ModelForm):
    # Поля для капчи
    captcha_answer = forms.IntegerField(label='Сколько будет 2+2?', required=True)

    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'text']

    def clean_captcha_answer(self):
        answer = self.cleaned_data.get('captcha_answer')
        if answer != 4:   # ожидаемый ответ 4
            raise forms.ValidationError('Неправильный ответ на капчу.')
        return answer