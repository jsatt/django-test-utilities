from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.template import RequestContext

def get_test(request):
    messages.success(request, 'test success')
    messages.error(request, 'test error')
    c = RequestContext(request)
    return render_to_response('test_page.html', context_instance=c)

def post_test(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    else:
        form = UserCreationForm()
    c = RequestContext(request, {'form': form})
    return render_to_response('test_page.html', context_instance=c)


