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



def load_csv():
    locations = [];
    count = 0;
    with open("polls/csv/Locations.csv") as f:
        next(f)
        for line in csv.DictReader(f, fieldnames=('Title', 'Price')):
            locations.append(line['Title'])
            if count == 2:
                break;
            count = count + 1;
    return locations;


from .models import Choice, Question

def get_hotel():
    keywords = ['Queenstown']
    hotels = []
    for keyword in keywords:
        try:
            results = ScrapeBookings.scrape_bookings(keyword)
            for result in results:
                hotels.append(result['Title'] + ' ' + keyword)
        except Exception as e:
            print(e)
        finally:
            time.sleep(10)

    eight_am = int(time.mktime(time.struct_time([2018, 7, 14, 8, 0, 0, 0, 0, 0])))
    params = {
        'mode': 'driving',
        'region': 'sg',
        'alternatives': 'false',
        'departure_time': eight_am,
    }

    totalTravelTime = 0;
    minTravelTime = 100000000;
    bestHotel = '';
    interestedLocations = ScrapePlanet.get_intrested_locations();
    for name in hotels:
        print(name)
        results = GoogleMap.geocode(address= name)
        route = results[0]
        location = route['geometry']['location']
        lat, lng = location['lat'], location['lng']
        source = "%s,%s" % (lat, lng)
        time.sleep(1)

        for location in interestedLocations:
            data = GoogleMap.directions(source, location['Title'], **params)
            if len(data['routes']) > 0:
                timings, dist = GoogleMap.output_routes('driving', data['routes'])
                #print('Timings:')
                #print(timings)
                #print('Distances:')
                #print(dist)
                totalTravelTime += timings['driving-DRIVING'];
        if (totalTravelTime < minTravelTime):
            minTravelTime = totalTravelTime;
            bestHotel = name;
        print('total travel time is ', totalTravelTime)
        totalTravelTime = 0;
    print('best hotel is ', bestHotel);
    return bestHotel, interestedLocations

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
    bestHotel = 'Lakefront Apartments Queenstown'
    interestedLocations = load_csv();
    print(interestedLocations);
    return render(request, 'polls/results.html', {'question': question, "hotel": bestHotel, 'locations': interestedLocations})


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
