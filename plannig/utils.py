from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    """ formats a day as a td. filter events by day """
    def formatday(self, day, events, year, month, today):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event.title} </li>'

        if day != 0:
            if f'{year}-{month}-{day}' == today:
                return f"<td bgcolor='#00FF00'><span class='date'>{day}: today</span><ul> {d} </ul></td>"
            else:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    """ formats a week as a tr  """
    def formatweek(self, theweek, events, year, month, today):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, year, month, today)
        return f'<tr> {week} </tr>'

    """ formats a month as a table. Filter events by year and month """
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(
                    start_time__year=self.year,
                    start_time__month=self.month
                    )
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        today = str(datetime.utcnow()).split(' ')[0]
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, self.year, self.month, today)}\n'
        cal += f'</table>\n'
        return cal
