import random

from django.core.exceptions import MultipleObjectsReturned
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

import stripe

from .models import Station, Timetable, Course, Carriage, Seating, Reservation
from .forms import ReservationForm
from datetime import datetime, date

stripe.api_key = settings.SECRET_KEY


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
            selected_courses_to = [obj.courses_id for obj in Timetable.objects.filter(stations_id=search_to.id)]
            selected_courses_id = [i.courses_id for i in selected_courses_from if i.courses_id in selected_courses_to]

            # Matched courses and its times returned inside lists
            if str(selected_courses_id) != '[]':
                selected_courses = []
                trip_times = {}
                random_car_id = {}
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

                    random_car_id[i] = random.choice([obj.id for obj in Carriage.objects.filter(courses_id=i)])

                return render(request, 'main/home.html', {'search_from': search_from,
                                                          'search_to': search_to,
                                                          'selected_courses_from': selected_courses_from,
                                                          'selected_courses': selected_courses,
                                                          'trip_times': trip_times,
                                                          'random_car_id': random_car_id})

        except (MultipleObjectsReturned, ValueError, Exception):
            pass

    return render(request, 'main/home.html', {})


def course(request, id_cour, id_from, id_to, id_car):
    course_name = Course.objects.get(id=id_cour)
    search_from = Station.objects.get(id=id_from)
    search_to = Station.objects.get(id=id_to)
    course_timetable = Timetable.objects.filter(courses_id=id_cour)
    carriages = Carriage.objects.filter(courses_id=id_cour)
    seats = Seating.objects.raw('SELECT * from main_seating '
                                'WHERE carriages_id = %s '
                                'ORDER BY id ASC', [id_car])
    row_list = [i for i in range(250) if i % 4 == 0]

    # Selected reserved seats
    seats_id_list = [seat.id for seat in seats]
    search_from_time = [p.at_location for p in Timetable.objects.raw('SELECT * from main_timetable '
                                                                     'WHERE courses_id = %s AND stations_id = %s',
                                                                     [id_cour, id_from])][0]
    search_to_time = [p.at_location for p in Timetable.objects.raw('SELECT * from main_timetable '
                                                                   'WHERE courses_id = %s AND stations_id = %s',
                                                                   [id_cour, id_to])][0]
    reservations = [p.seats for p in
                    Reservation.objects.raw('SELECT * from main_reservation '
                                            'WHERE (seats_id = ANY(%s) AND reservation_start_time < %s '
                                            'AND reservation_end_time > %s) '
                                            'OR (seats_id = ANY(%s) AND reservation_start_time >= %s '
                                            'AND reservation_end_time <= %s) '
                                            'OR (seats_id = ANY(%s) AND reservation_start_time < %s '
                                            'AND reservation_end_time > %s)',
                                            [seats_id_list, search_from_time, search_from_time,
                                             seats_id_list, search_from_time, search_to_time,
                                             seats_id_list, search_to_time, search_to_time])]

    if request.method == "POST":
        chose_id = Seating.objects.get(id=request.POST['chose'])

        # div with personal data
        form = ReservationForm(request.POST)
        if form.is_valid() and request.POST['first-name'] and request.POST['last-name'] \
                and request.POST['year-of-birth'] and request.POST['kod_znizki']:
            reservation = form.save(commit=False)
            reservation.reservation_start_time = datetime.strptime(request.POST['reservation_start_time'], '%H:%M').time()
            reservation.reservation_end_time = datetime.strptime(request.POST['reservation_end_time'], '%H:%M').time()
            reservation.personality = f"{request.POST['first-name']} {request.POST['last-name']} " \
                                      f"{request.POST['year-of-birth']}"
            reservation.discount = int(request.POST['kod_znizki'])/100
            reservation.save()
            return render(request, 'main/create_checkout_session.html', {})

        return render(request, 'main/course.html', {'course_name': course_name,
                                                    'search_from': search_from,
                                                    'search_to': search_to,
                                                    'course_timetable': course_timetable,
                                                    'carriages': carriages,
                                                    'id_car': id_car,
                                                    'seats': seats,
                                                    'row_list': row_list,
                                                    'reservations': reservations,
                                                    'chose_id': chose_id})

    return render(request, 'main/course.html', {'course_name': course_name,
                                                'search_from': search_from,
                                                'search_to': search_to,
                                                'course_timetable': course_timetable,
                                                'carriages': carriages,
                                                'id_car': id_car,
                                                'seats': seats,
                                                'row_list': row_list,
                                                'reservations': reservations})


def create_checkout_session(request):
    try:
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
    except Exception as e:
        return str(e)

    return JsonResponse({
        'id': checkout_session.id
    })
