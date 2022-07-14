from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from .models import Station, Timetable, Course
from datetime import datetime


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

            # Selected courses returned inside list
            if str(selected_courses_id) != '[]':
                selected_courses = []
                for i in selected_courses_id:
                    selected_courses.append(Course.objects.get(id=i))
                return render(request, 'main/home.html', {'selected_courses': selected_courses})

        except (MultipleObjectsReturned, ValueError, Exception):
            pass

    return render(request, 'main/home.html', {})
