from django.shortcuts import render
from visits.models import Visit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def home_page_view(request):
    qs = Visit.objects.filter(path=request.path)
    total_qs = Visit.objects.all()
    try:
        percent = qs.count() * 100 / total_qs.count()
    except ZeroDivisionError:
       pass
    context = {
      'title': 'Home',
      'content': 'GG',
      'qs': qs,
      'total_qs': total_qs,
      'percent': percent
   }


    Visit.objects.create(path=request.path)
    return render(request, 'home/home.html', context=context)

correct_password = '123'

def pw_protected_view(request):
    is_allowed = request.session.get('is_allowed', False)
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == correct_password:
            is_allowed = True
            request.session['is_allowed'] = is_allowed
    if is_allowed:
        return render(request, 'protected/view.html', {})
    return render(request, 'protected/entry.html', {})


@staff_member_required(login_url='/accounts/login/')
def user_only_view(request, *args, **kwargs):
    return render(request, 'protected/user_only.html', {})