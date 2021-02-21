from django import forms
from notice.models import Board

class WriteForm(forms.ModelForm):
    
    class Meta:
        model = Board

        fields = ['title', 'author', 'content', 'image', 'password']
        labels = {
            'title': "",
            'author': '',
            'content': '',
            'image': '이미지첨부',
            'password': '',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'제목'}),
            'author': forms.TextInput(attrs={'placeholder':'이름'}),
            'content': forms.TextInput(attrs={'placeholder':'내용 최대xx자'}),
            'password': forms.PasswordInput(attrs={'placeholder':'비밀번호'}),
        }          