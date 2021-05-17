from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import ModelScrapes
from django.http import HttpResponseRedirect


# Create your views here.

def scrapeView(request):
    if request.method == 'POST':
        url = request.POST.get('weblink', '')
        source = requests.get(url)
        scrape = BeautifulSoup(source.text, 'html.parser')
        links_search = scrape.find_all('a')

        for link in links_search:
            links = (link.get('href'))
            links_text = link.string
            ModelScrapes.objects.create(link=links, name=links_text)
        return HttpResponseRedirect('/')
    else:
        data = ModelScrapes.objects.all()
    context = {
        'data': data
    }
    return render(request, 'scraper/scrape.html', context)


def delete(request):
    ModelScrapes.objects.all().delete()
    return render(request, 'scraper/scrape.html')
