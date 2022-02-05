from cProfile import label
from curses import panel
from dataclasses import Field
from re import search
from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from wagtail.search import index

from modelcluster.fields import ParentalKey

from wagtail.images.edit_handlers import ImageChooserPanel

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=200)
    body = RichTextField(blank=True)


    #indexing
    search_fields = Page.search_fields + [
        #поля для поиска
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery_images"),
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=200)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]




