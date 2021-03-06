from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from polls import ScrapeBookings
from polls import GoogleMap
from polls import ScrapePlanet
import time
import csv
import os

def load_location_coords():
    lats = [];
    lngs = []
    count = 0;
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__));
    # The first row is the hotel name and price
    my_file = os.path.join(THIS_FOLDER, 'Coords.csv')
    print(THIS_FOLDER)
    with open(my_file) as f:
        next(f)
        for idx, line in enumerate(csv.DictReader(f, fieldnames=('lat', 'lng'))):
            if (idx == 0):
                continue;
            count = count + 1;
            lats.append(line['lat']);
            lngs.append(line['lng']);
    return lats, lngs;


def lood_hotels():
    count = 0;
    hotels = [];
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__));
    # The first row is the hotel name and price
    my_file = os.path.join(THIS_FOLDER, 'Hotels.csv')
    print(THIS_FOLDER)
    with open(my_file) as f:
        next(f)
        for idx, line in enumerate(csv.DictReader(f, fieldnames=('Title', 'Price', 'Traveltime'))):
            hotels.append(line['Title'])
            count = count + 1;
    print(hotels);
    return hotels;


def load_location_string():
    count = 0;
    locations = [];
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__));
    # The first row is the hotel name and price
    my_file = os.path.join(THIS_FOLDER, 'Locations.csv')
    print(THIS_FOLDER)
    with open(my_file) as f:
        next(f)
        for idx, line in enumerate(csv.DictReader(f, fieldnames=('Title', 'Price'))):
            locations.append(line['Title'])
            count = count + 1;
    return locations;


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    cityNames = ['Auckland', 'Wellington']


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    interestedLocations = load_location_string();
    print(interestedLocations);
    return render(request, 'polls/results.html', {'question': question, "hotel": bestHotel, 'locations': interestedLocations})

def travel(request):
    lats, lngs = load_location_coords();
    hotels = lood_hotels();
    interestedLocations = load_location_string();
    print(interestedLocations);
    print(hotels);
    return render(request, 'polls/travel.html', {"myhotels": hotels, 'locations': interestedLocations, 'lats': lats,'lngs': lngs, 'bestHotel':hotels[0]})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
