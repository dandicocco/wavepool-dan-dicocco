from django.template import loader
from django.http import HttpResponse

from wavepool.models import NewsPost
from wavepool.code_exercise_defs import code_exercise_defs, code_review_defs, code_design_defs
from django.conf import settings


def front_page(request):
    """ View for the site's front page
        Returns all available newsposts, formatted like:
            cover_story: the newsposts with is_cover_story = True
            top_stories: the 3 most recent newsposts that are not cover story
            archive: the rest of the newsposts, sorted by most recent
    """
    template = loader.get_template('wavepool/frontpage.html')
    cover_story = NewsPost.objects.all().order_by('-is_cover_story').first() #sort by is_cover_story = true and take 1st
    top_stories = NewsPost.objects.all().order_by('-publish_date').exclude(is_cover_story=True)[:3] #order by publish_date most recent, exclude cover story
    other_stories = NewsPost.objects.all().order_by('-publish_date').exclude(title__in=[story.title for story in top_stories]).exclude(title=cover_story.title)
    #exclude cover story & top story titles, order by most recent first

    context = {
        'cover_story': cover_story,
        'top_stories': top_stories,
        'archive': other_stories,
    }

    return HttpResponse(template.render(context, request))


def newspost_detail(request, newspost_id=None):
    template = loader.get_template('wavepool/newspost.html')
    newspost = NewsPost.objects.order_by('?').first()
    context = {
        'newspost': newspost
    }

    return HttpResponse(template.render(context, request))


def instructions(request):
    template = loader.get_template('wavepool/instructions.html')

    context = {
        'code_exercise_defs': code_exercise_defs,
        'code_design_defs': code_design_defs,
        'code_review_defs': code_review_defs,
        'show_senior_exercises': settings.SENIOR_USER,
    }
    return HttpResponse(template.render(context, request))
