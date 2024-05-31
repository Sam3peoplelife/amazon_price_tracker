from django.shortcuts import render
from .forms import AddLinkForm
from .models import Link
from django.views.generic import DeleteView
from django.urls import reverse_lazy

def home_view(request):
    no_discounted = 0
    error = None

    form = AddLinkForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "An error occurred while receiving data"
        except:
            error = "Something went wrong"

    form = AddLinkForm()

    qs = Link.objects.all()
    items_no = qs.count()
    
    if items_no > 0:
        discount_list = []
        for item in qs:
            if item.price_difference < 0:
                discount_list.append(item)
        no_discounted = len(discount_list)
    
    context = {
        'qs':qs,
        'items_no': items_no,
        'no_discounted': no_discounted,
        'form' : form,
        'error' : error,
    }

    return render(request, 'links/main.html', context)

class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'links/confirm_delete.html'
    success_url = reverse_lazy('home')
