from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    """Form for sending a message within an existing conversation."""

    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Type your message...',
            }),
        }


class NewConversationForm(forms.Form):
    """Form for starting a new conversation with a seller."""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Send a message to the seller...',
        }),
    )
