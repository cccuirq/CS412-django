from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . models import *
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .forms import AddWaterLogForm, CreatProfileForm
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.db.models.functions import TruncDate
from django.db.models import Sum
from datetime import datetime
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
        now = timezone.localtime()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        today_logs = self.get_object().get_water_log().filter(
            timestamp__gte=start_of_day,
            timestamp__lt=end_of_day
        )
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

            print(f'self.request.POST={self.request.POST}')
            form = UserCreationForm(self.request.POST)
            if not form.is_valid():
                print(f'form_erroes={form.errors}')
                return super().dispatch(*args, **kwargs)
            
            user = form.save()
            print(f"RegistrationView.dispatch: created user {user}")
            login(self.request, user)
            print(f'RegistrationView.dispatch, user {user} is logged in.')

            return redirect(reverse('create_profile'))

        return super().dispatch(request, *args, **kwargs)
    
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

        now = timezone.localtime()
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
