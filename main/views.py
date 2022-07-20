from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from .models import Station, Timetable, Course
from datetime import datetime, date


def home(request):
    if request.method == "POST":
        try:
            search_from = Station.objects.get(name__contains=request.POST['search-from'])
            search_to = Station.objects.get(name__contains=request.POST['search-to'])
            search_time = datetime.strptime(request.POST['departing'], '%H:%M').time()

            # Selected courses ids
            selected_courses_from = Timetable.objects.raw('SELECT * from main_timetable '
                                                          'WHERE stations_id = %s AND at_location >= %s '
                                                          'ORDER BY at_location ASC',
                                                          [search_from.id, search_time])
            selected_courses_to = (obj.courses_id for obj in Timetable.objects.filter(stations_id=search_to.id))
            selected_courses_id = [i.courses_id for i in selected_courses_from if i.courses_id in selected_courses_to]

            # Matched courses and its times returned inside lists
            if str(selected_courses_id) != '[]':
                selected_courses = []
                trip_times = {}
                for i in selected_courses_id:
                    selected_courses.append(Course.objects.get(id=i))

                    search_from_time = Timetable.objects.raw('SELECT * from main_timetable '
                                                             'WHERE courses_id = %s AND stations_id = %s',
                                                             [i, search_from.id])
                    search_to_time = Timetable.objects.raw('SELECT * from main_timetable '
                                                           'WHERE courses_id = %s AND stations_id = %s',
                                                           [i, search_to.id])
                    for a, b in zip(search_from_time, search_to_time):
                        trip_times[i] = (datetime.combine(date.today(), b.at_location) -
                                          datetime.combine(date.today(), a.at_location))

                return render(request, 'main/home.html', {'search_from': search_from,
                                                          'search_to': search_to,
                                                          'selected_courses_from': selected_courses_from,
                                                          'selected_courses': selected_courses,
                                                          'trip_times': trip_times})

        except (MultipleObjectsReturned, ValueError, Exception):
            pass

    return render(request, 'main/home.html', {})


def course(request, id):
    single_course = Course.objects.get(id=id)
    return render(request, 'main/course.html', {'single_course': single_course})
