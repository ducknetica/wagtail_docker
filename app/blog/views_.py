from django.shortcuts import render
from wagtail.search.models import Query
from blog.models import BlogPage

# Create your views here.
def search(request):
    searach_query = request.GET.get('query', None)
    if searach_query:
        # serach_results = BlogPage.objects.live().search(searach_query, fields=["body"])
        serach_results = BlogPage.objects.filter(body=searach_query)

        #запомним запрос
        Query.get(searach_query).add_hit()
    else:
        serach_results = BlogPage.objects.none()

    return render(request, 'search_results.html', {
        'searach_query____': searach_query,
        "serach_results___": serach_results
    })