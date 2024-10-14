from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from visits.models import Visit
from django.contrib.auth.models import User




@login_required
def profile_list(request):
    context = {
        'object_list': User.objects.filter(is_active=True)
    }
    return render(request, 'profiles/profile_list.html', context=context)


@login_required
def detail_view(request, username, *args, **kwargs):
    user = request.user
    object = get_object_or_404(User, username=username)
    context = {
            'object': object
        }
    user_groups = user.groups.all()
    if user_groups.filter(name__icontains='basic').exists():
        return HttpResponse('Congrats!')
    return render(request, 'profiles/profile_detail.html', context)
