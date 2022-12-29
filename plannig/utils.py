from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
import calendar
from django.db.models import Q


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    """ formats a day as a td. filter events by day """
    def formatday(self, day, events, year, month, today, listEvents):
        d = ''
        for event in listEvents:
            d += f'<li> {event} </li>'

        if day != 0:
            if f'{year}-{month}-{day}' == today:
                return f"<td bgcolor='#00FF00'><span class='date'>{day}</span><ul> {d} </ul></td>"
            else:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    """ formats a week as a tr  """
    def formatweek(self, theweek, events, year, month, today, listEvents):

        def zero_first(nb):
            if nb <= 9 and nb >= 0:
                return f"0{nb}"
            else:
                return str(nb)

        week = ''
        for d, weekday in theweek:
            id = f'{year}-{zero_first(month)}-{zero_first(d)}'
            if id in listEvents:
                liste = listEvents[id]
            else:
                liste = []
            #print(id)
            week += self.formatday(d, events, year, month, today, liste)
        return f'<tr> {week} </tr>'

    """ formats a month as a table. Filter events by year and month """
    def formatmonth(self, withyear=True):
        """ events = Event.objects.filter(
                    start_time__year=self.year,
                    start_time__month=self.month
                    ) """
        events = Event.objects.filter(end_time__gte=f"{self.year}-{self.month}-01")
        dic = {}

        #print("events: ", events)
        for e in events:
            day_start = e.start_time
            day_end = e.end_time
            print(f"{day_start} {day_end}")
            for date in list(self.daterange(day_start, day_end)):
                if date in dic:
                    dic[date].append(e.title)
                else:
                    dic[date] = [e.title]

        """ for loop in dic:
            print(f"{loop} {dic[loop]}") """

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        today = str(datetime.utcnow()).split(' ')[0]
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, self.year, self.month, today, dic)}\n'
        cal += f'</table>\n'
        return cal

    def daterange(self, start, end):
        DATE_FORMAT = '%Y-%m-%d'

        def convert(date):
                try:
                    date = datetime.strptime(date, DATE_FORMAT)
                    return date.date()
                except TypeError:
                    return date

        def get_date(n):
                return datetime.strftime(convert(start) + timedelta(days=n), DATE_FORMAT)

        days = (convert(end) - convert(start)).days
        print(f"{end} - {start} == {days}")
        if days <= 0:
                raise ValueError('The start date must be before the end date.')
        for n in range(0, days):
                yield get_date(n)
