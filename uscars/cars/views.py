from django.shortcuts import render
from .scraper import get_html, parse_page

def index(request):
    baseurl = "https://ucars.pro/pl/sales-history/porsche?model=macan%20s"
    context = {'cars_list': []}
    if request.method == 'POST':
        num_pages = int(request.POST.get('num_pages', 1))

        for page in range(1, num_pages + 1):
            html = get_html(baseurl, params={'page': page})
            if html:
                context['cars_list'].extend(parse_page(html))
    else:
        context['num_pages'] = 1
    return render(request, "cars/index.html", context)
