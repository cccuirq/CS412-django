from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . models import *
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .forms import AddWaterLogForm, CreatProfileForm, NotificationReadForm
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.db.models.functions import TruncDate, TruncMonth
from django.db.models import Sum, Avg, Max, F, Count, FloatField
from datetime import datetime,timezone
from django.http import HttpResponseRedirect
from django.utils.timezone import localtime
import plotly
import plotly.graph_objs as go
# Create your views here.
class ShowTodayWaterView(LoginRequiredMixin, DetailView):
    model = WProfile
    template_name = 'waterlog/show_today_log.html'
    context_object_name = 'profileMe'

    def get_object(self):
        return get_object_or_404(WProfile, waterUser=self.request.user)

    def get_login_url(self) -> str:
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get today's date in the correct format
        now = localtime()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        today_logs = self.get_object().get_water_log().filter(
            timestamp__gte=start_of_day,
            timestamp__lt=end_of_day
        )
        # print(today_logs[0].timestamp)
        context['today_water_logs'] = today_logs

        total_ml = 0
        unit_conversion = {
            'ml': 1,
            'L': 1000,
            'Cup': 250,
            'Bottle': 500,
            'Can': 330,
        }

        for log in today_logs:
            unit = log.water_type
            amount = log.amount_consumed
            total_ml += amount * unit_conversion.get(unit, 1)
        
        still = self.get_object().Goal - total_ml
        context['total_ml'] = total_ml
        context['goal_met'] = total_ml >= self.get_object().Goal
        context['still_need'] = still
        return context


def home(request):

    template_name = "waterlog/home.html"

    return render(request, template_name)

class AddWaterLogView(LoginRequiredMixin, CreateView):
    model = WaterLog
    form_class = AddWaterLogForm
    template_name = 'waterlog/add_water_log.html'
    success_url = reverse_lazy('show_today_log')

    def form_valid(self, form):
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)
        form.instance.wprofile = user_profile
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wprofile'] = get_object_or_404(WProfile, waterUser=self.request.user)
        return context
    
class DeleteWaterLogView(LoginRequiredMixin, DeleteView):
    model = WaterLog
    template_name = "waterlog/delete_water_log.html"
    context_object_name = 'waterlog'

    def get_success_url(self):
        return reverse("show_today_log")

    
class UpdateWaterLogView(LoginRequiredMixin, UpdateView):
    model = WaterLog
    template_name = "waterlog/update_water_log.html"
    form_class = AddWaterLogForm
    context_object_name = 'waterlog'

    def form_valid(self, form):
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)
        form.instance.wprofile = user_profile
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wprofile'] = get_object_or_404(WProfile, waterUser=self.request.user)
        return context
    
    def get_success_url(self):
        return reverse("show_today_log")
    
class RegistrationView(CreateView):
    '''Display and process the UserCreationForm for account registration'''

    template_name = 'waterlog/register.html'
    form_class = UserCreationForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.POST:

            form = UserCreationForm(self.request.POST)
            if not form.is_valid():
                return super().dispatch(*args, **kwargs)
            
            user = form.save()
            login(self.request, user)

            return redirect(reverse('create_profile'))

        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        # Optional: Log errors or display a message in debug mode
        print(f'Form errors: {form.errors}')
        return super().form_invalid(form)
    
class ShowMyProfileView(LoginRequiredMixin , DetailView):
    model = WProfile
    template_name = 'waterlog/show_my_profile.html'
    context_object_name = 'profileMe'

    def get_object(self):
        return get_object_or_404(WProfile, waterUser=self.request.user)

    def get_login_url(self) -> str:
        return reverse('login')

class CreateProfileView(LoginRequiredMixin, CreateView):
    model = WProfile
    template_name = 'waterlog/create_profile.html'
    form_class = CreatProfileForm

    def form_valid(self, form):
        form.instance.waterUser = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_today_log')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = WProfile
    template_name = "waterlog/update_profile.html"
    form_class = CreatProfileForm

    def get_object(self):
        return get_object_or_404(WProfile, waterUser=self.request.user)
    
    def get_success_url(self):
        return reverse("my_profile")
    
class DailyWaterLogListView(LoginRequiredMixin, ListView):
    model = WaterLog
    template_name = 'waterlog/daily_water_logs.html'
    context_object_name = 'daily_logs'

    def get_queryset(self):
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)

        unit_conversion = {
            'ml': 1,
            'L': 1000,
            'Cup': 250,
            'Bottle': 500,
            'Can': 330,
        }

        raw_daily_logs = (
            WaterLog.objects.filter(wprofile=user_profile)
            .annotate(date=TruncDate('timestamp'))
            .values('date', 'water_type', 'amount_consumed')
            .order_by('-date')
        )

        daily_logs = {}
        for log in raw_daily_logs:
            date = log['date']
            water_type = log['water_type']
            amount = log['amount_consumed']

            converted_amount = amount * unit_conversion.get(water_type, 1)

            if date not in daily_logs:
                daily_logs[date] = 0
            daily_logs[date] += converted_amount

        daily_logs_list = [
            {'date': date, 'total_consumed': total_ml}
            for date, total_ml in sorted(daily_logs.items(), reverse=True)
        ]

        return daily_logs_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user) 
        context['goal'] = user_profile.Goal
        return context
    
class ShowDayLogView(LoginRequiredMixin, ListView):
    model = WaterLog
    template_name = 'waterlog/day_log.html'
    context_object_name = 'day_logs'

    def get_queryset(self):
        date = self.kwargs.get('date')
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)

        return WaterLog.objects.filter(
            wprofile=user_profile,
            timestamp__date=date
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.kwargs.get('date')

        context['selected_date'] = datetime.strptime(self.kwargs['date'], "%Y-%m-%d")
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)

        today_logs = WaterLog.objects.filter(
            wprofile=user_profile,
            timestamp__date=date
        )
        
        total_ml = 0
        unit_conversion = {
            'ml': 1,
            'L': 1000,
            'Cup': 250,
            'Bottle': 500,
            'Can': 330,
        }

        for log in today_logs:
            unit = log.water_type
            amount = log.amount_consumed
            total_ml += amount * unit_conversion.get(unit, 1)
        
        context['total_ml'] = total_ml
        context['goal_met'] = total_ml >= user_profile.Goal
        return context

class ShowFriendsLogView(LoginRequiredMixin, DetailView):
    model = WProfile
    template_name = 'waterlog/show_friends_log.html'
    context_object_name = 'wprofile'

    def get_object(self):
        return get_object_or_404(WProfile, waterUser=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        now = localtime()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        friends_logs = []
        for friend in user_profile.get_friends():
            today_logs = (
                friend.get_water_log()
                .filter(timestamp__gte=start_of_day, timestamp__lt=end_of_day)
            )
            
            total_ml = 0
            unit_conversion = {
                'ml': 1,
                'L': 1000,
                'Cup': 250,
                'Bottle': 500,
                'Can': 330,
            }

            for log in today_logs:
                total_ml += log.amount_consumed * unit_conversion.get(log.water_type, 1)
            
            progress = (total_ml / friend.Goal) * 100 if friend.Goal else 0
            friends_logs.append({
                'id': friend.id,
                'name': friend.user_name,
                'total_ml': total_ml,
                'goal': friend.Goal,
                'progress': min(progress, 100),
            })

        context['friends_logs'] = friends_logs
        return context

class AddFriendsView(LoginRequiredMixin, TemplateView):
    template_name = 'waterlog/add_friends.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)

        if search_query:
            potential_friends = WProfile.objects.filter(
                models.Q(user_name__icontains=search_query),
            ).exclude(
                id__in=user_profile.get_friends().values_list('id', flat=True)
            ).exclude(id=user_profile.id)

            context['potential_friends'] = potential_friends
        else:
            context['potential_friends'] = None

        context['search_query'] = search_query
        return context

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)
        friend_id = request.POST.get('friend_id')

        if friend_id:
            friend_profile = get_object_or_404(WProfile, id=friend_id)

            friend.objects.create(wprofile1=user_profile, wprofile2=friend_profile)
        return redirect('add_friends')  # Redirect to the same page

class MonthlyStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'waterlog/statistics.html'
    model = WaterLog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)
        
        if not user_profile:
            context['error'] = "User profile not found."
            return context
        
        current_date = localtime()

        year = self.kwargs.get('year', current_date.year)
        month = self.kwargs.get('month', current_date.month)

        start_of_month = datetime(year, month, 1, tzinfo=timezone.utc)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1)

        monthly_logs = WaterLog.objects.filter(
            wprofile=user_profile,
            timestamp__gte=start_of_month,
            timestamp__lt=end_of_month
        )

        unit_conversion = {
            'ml': 1,
            'L': 1000,
            'Cup': 250,
            'Bottle': 500,
            'Can': 330,
        }

        daily_totals = {}
        for log in monthly_logs:
            log_local_time = localtime(log.timestamp)
            log_date = log_local_time.date()
            log_amount_ml = log.amount_consumed * unit_conversion.get(log.water_type, 1)
            if log_date in daily_totals:
                daily_totals[log_date] += log_amount_ml
            else:
                daily_totals[log_date] = log_amount_ml

        sorted_dates = sorted(daily_totals.keys())
        sorted_totals = [daily_totals[date] for date in sorted_dates]

        #####################################################################
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=sorted_dates,
                y=sorted_totals,
                mode="lines+markers",
                name="Water Log (ml)",
                line=dict(color="blue"),
                marker=dict(size=8),
            )
        )
        fig.update_layout(
            title="Current Month's Daily Water Log (ml)",
            xaxis_title="Date",
            yaxis_title="Total Water Intake (ml)",
            xaxis=dict(
                tickformat="%d %b",
                title="Days in Month",
            ),
            yaxis=dict(
                title="Water Intake (ml)",
                tickformat=",.0f",
            ),
            template="plotly_white",
        )

        graph_div_b = plotly.offline.plot(
            fig,
            auto_open=False,
            output_type="div"
        )

        context['graph_div_b'] = graph_div_b
        ###########################################################
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=sorted_dates,
                y=sorted_totals,
                mode="markers",
                name="Actual Intake (ml)",
                marker=dict(size=10, color="blue", symbol="circle"),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=sorted_dates,
                y=[user_profile.Goal] * len(sorted_dates),
                mode="lines",
                name="Daily Goal (ml)",
                line=dict(color="red", dash="dash"),
            )
        )

        fig.update_layout(
            title="Goal vs. Actual Daily Water Intake",
            xaxis_title="Date",
            yaxis_title="Water Intake (ml)",
            xaxis=dict(
                tickformat="%d %b",
                title="Days in Month",
            ),
            yaxis=dict(
                title="Water Intake (ml)",
                tickformat=",.0f",
            ),
            template="plotly_white",
            legend=dict(
                x=0.5, y=-0.2,
                xanchor='center',
                orientation="h"
            ),
        )
        graph_div_scatter = plotly.offline.plot(
            fig,
            auto_open=False,
            output_type="div"
        )

        context['graph_div_scatter'] = graph_div_scatter

        ########################################################################
        months_with_logs = (
            WaterLog.objects.filter(wprofile=user_profile)
            .annotate(month=TruncMonth('timestamp'))
            .values('month')
            .annotate(log_count=Count('id'))
            .order_by('-month')
        )
        past_months = [(entry['month'].year, entry['month'].month) for entry in months_with_logs]
        context['past_months'] = past_months

        total_intake_ml = sum(sorted_totals)
        average_daily_intake = total_intake_ml / len(sorted_totals) if sorted_totals else 0
        max_daily_intake = max(sorted_totals, default=0)
        goal_met_days = sum(1 for total in sorted_totals if total >= user_profile.Goal)
        
        context['user_name'] = user_profile.user_name
        context.update({
            'year': year,
            'month': month,
            'total_intake_ml': total_intake_ml,
            'average_daily_intake': average_daily_intake,
            'max_daily_intake': max_daily_intake,
            'goal_met_days': goal_met_days,
        })

        return context

class CreateNotificationView(LoginRequiredMixin, CreateView):
    model = Notification
    fields = ['message']
    template_name = 'waterlog/create_notification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_id = self.kwargs.get('friend_id')
        friend_profile = get_object_or_404(WProfile, id=friend_id)
        context['object'] = friend_profile  # Provide the friend's profile
        return context

    def form_valid(self, form):
        friend_id = self.kwargs.get('friend_id')
        friend_profile = get_object_or_404(WProfile, id=friend_id)
        sender_profile = get_object_or_404(WProfile, waterUser=self.request.user)

        form.instance.wprofile = friend_profile
        form.instance.sender = sender_profile  # Set the sender
        form.instance.timestamp = localtime()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the friends log after sending the notification
        return reverse('friends_log')

    
class ShowUnreadNotificationsView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'waterlog/unread_notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)
        return Notification.objects.filter(wprofile=user_profile, read=False).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)

        notifications = Notification.objects.filter(
            wprofile=user_profile, read=False
        ).select_related('sender').order_by('-timestamp')

        context['notifications'] = notifications
        return context

class MarkNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(WProfile, waterUser=request.user)
        form = NotificationReadForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            notifications = form.cleaned_data['notification_ids']
            # Mark the selected notifications as read
            notifications.update(read=True)
        return HttpResponseRedirect(reverse('unread_notifications'))

class ShowAllNotificationsView(LoginRequiredMixin, TemplateView):
    template_name = "waterlog/show_all_notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(WProfile, waterUser=self.request.user)

        # Fetch all notifications for the logged-in user
        all_notifications = Notification.objects.filter(wprofile=user_profile).order_by('-timestamp')

        context['all_notifications'] = all_notifications
        return context
