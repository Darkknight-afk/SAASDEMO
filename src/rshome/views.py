from django.shortcuts import render
from visits.models import Visit

def home_page_view(request):
   qs = Visit.objects.filter(path=request.path)
   total_qs = Visit.objects.all()
   context = {
      'title': 'Home',
      'content': 'GG',
      'qs': qs,
      'total_qs': total_qs,
      'percent': qs.count() * 100 / total_qs.count()
   }
   Visit.objects.create(path=request.path)
   return render(request, 'home/home.html', context=context)