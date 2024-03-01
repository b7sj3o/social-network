from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import BaseMessage, Friends, User
from django.contrib.auth.decorators import login_required

# @login_required
def home(request):
    form = MessageForm()
    messages = BaseMessage.objects.all().order_by('-id')
    friends = Friends.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # current_user = request.user
            # form.cleaned_data['sender'] = User.objects.get(pk=current_user.pk)
            form.sender = 'hello'
            print(form.data)
            form.save()
            # TODO #1: connect to ws and send message
        

    context = {
        'forms': form,
        'messages': messages,
        'friends': friends 
    }
        
    return render(request, 'index.html', context=context)       

        