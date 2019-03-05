from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.models import UserProfile, Table, Reservation
import datetime
import calendar


# adding columns titles to django admin page
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'twitter_username')

    def twitter_account(self, object):
        return object.twitter_username


# adding columns titles to django admin page
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'seats', 'available')

    def id(self, object):
        return object.id

    def available(self, object):
        return object.available

    def seats(self, object):
        return object.seats


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'customer', 'date', 'start_time', 'finish_time')
    # change_list_template = '/Users/ishar/Desktop/diso/Diso/diso/website/templates/accounts/change_list.html'

    def id(self, object):
        return object.id

    def table(self, object):
        return object.table

    def customer(self, object):
        return object.customer

    def date(self, object):
        return object.date

    def start_time(self, object):
        return object.start_time

    def finish_time(self, object):
        return object.finish_time

    # def changelist_view(self, request, extra_context=None):
    #     after_day = request.GET.get('day__gte', None)
    #     extra_context = extra_context or {}
    #
    #     if not after_day:
    #         d = datetime.date.today()
    #     else:
    #         try:
    #             split_after_day = after_day.split('-')
    #             d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
    #         except:
    #             d = datetime.date.today()
    #
    #     last_day = calendar.monthrange(d.year, d.month)
    #     next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
    #     next_month = next_month + datetime.timedelta(days=1)  # forward a single day
    #     next_month = datetime.date(year=next_month.year, month=next_month.month, day=1)  # find first day of next month
    #
    #     extra_context['next_month'] = reverse('admin:events_event_changelist') + '?day__gte=' + str(next_month)
    #
    #     cal = calendar.HTMLCalendar()
    #     html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
    #     html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
    #     extra_context['calendar'] = mark_safe(html_calendar)
    #     return super(ReservationAdmin, self).changelist_view(request, extra_context)


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
