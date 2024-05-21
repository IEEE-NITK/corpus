from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from farewell.forms import SeniorForm
from farewell.models import Senior

# Create your views here
def index(request, pk=None):
    if pk is None:
        return redirect('https://http.cat/404')
    try:
        form = SeniorForm(instance=Senior.objects.get(url_id=pk))
    except:
        return redirect('https://http.cat/404')
    
    if request.method == "POST":
        form = SeniorForm(request.POST, instance=Senior.objects.get(url_id=pk))
        try:
            senior = Senior.objects.get(url_id=pk)
            form = SeniorForm(request.POST, instance=senior)
        except:
            senior = None
            form.name = "Senior"
            form.url_id = pk
            
        if form.is_valid():
            form.save()
            if form.cleaned_data["coming_farewell"]:
                messages.success(request, "Yayy! Here's to a great farewell! 🍻")
            else:
                messages.success(request, "Oh no! We'll miss you! 😢")
                
            # save the senior info with the form
            senior = form.save(commit=False)
            senior.save()

            redirect_url = f"/farewell/{pk}"
            return HttpResponseRedirect(redirect_url)
            
        else:
            print(form.errors)
            return HttpResponseRedirect(request.path)
            
            
    try:        
        name = Senior.objects.get(url_id=pk).name
    except:
        name = "Senior"
        
    
    args={
        'name':name,
        'form':form
    }
    
    
    
    return render(request, "farewell/farewell.html", args)
