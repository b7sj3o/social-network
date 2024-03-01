from .models import BaseMessage
from django.forms import ModelForm


class MessageForm(ModelForm):
    class Meta:
        model = BaseMessage
        exclude = ['sender', 'created']
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control w-100'
