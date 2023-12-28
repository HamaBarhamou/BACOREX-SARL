from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from datetime import datetime, date, timedelta
from .models import *
from django.utils.safestring import mark_safe
from calendar import monthrange
from .utils import Calendar


def prev_month(d):
    first = d.replace(day=1)
    return first - timedelta(days=1)


def next_month(d):
    days_in_month = monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    return next_month


# Create your views here.
@login_required(login_url="/user/")
def calendar(request, date=None, cmd=None, calendarType=None):
    if date is None:
        d = datetime.today()
    if cmd == "next":
        d = next_month(datetime.strptime(date, "%Y-%m-%d"))
    elif cmd == "prev":
        d = prev_month(datetime.strptime(date, "%Y-%m-%d"))

    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(withyear=True)

    context = {"calendar": mark_safe(html_cal), "date": str(d).split(" ")[0]}
    template = loader.get_template("plannig/calendar.html")
    return HttpResponse(template.render(context, request))
