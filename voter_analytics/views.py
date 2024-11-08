from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Votes
import plotly
from datetime import datetime
import plotly.graph_objs as go
from django.db.models import Count
from collections import Counter

# Create your views here.
class VotesListView(ListView):
    template_name = 'voter_analytics/votes.html'
    model = Votes
    context_object_name = 'votes'
    paginate_by = 100

    def get_queryset(self):
        
        # start with entire queryset
        qs = super().get_queryset().order_by('voter_score')
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        if party_affiliation:
            qs = qs.filter(party_affiliation__iexact=party_affiliation.strip())

        if min_dob:
            qs = qs.filter(DOB__gte=f"{min_dob}-01-01")

        if max_dob:
            qs = qs.filter(DOB__lte=f"{max_dob}-12-31")

        if voter_score:
            qs = qs.filter(voter_score=int(voter_score))

        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field) == 'True':
                qs = qs.filter(**{field: True})
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        context['years'] = range(1900, current_year + 1)
        context['scores'] = range(0, 6)
        return context
    
class VotesDetailView(DetailView):
    template_name = 'voter_analytics/votes_detail.html'
    model = Votes
    context_object_name = 'v'

class GraphsListView(ListView):
    template_name = 'voter_analytics/graphs.html'
    model = Votes
    context_object_name = 'graphs'

    def get_queryset(self):
        qs = super().get_queryset().order_by('voter_score')
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        if party_affiliation:
            qs = qs.filter(party_affiliation__iexact=party_affiliation.strip())

        if min_dob:
            qs = qs.filter(DOB__gte=f"{min_dob}-01-01")

        if max_dob:
            qs = qs.filter(DOB__lte=f"{max_dob}-12-31")

        if voter_score:
            qs = qs.filter(voter_score=int(voter_score))

        for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
            if self.request.GET.get(field) == 'True':
                qs = qs.filter(**{field: True})
        return qs

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_queryset = self.get_queryset()

        birth_years = filtered_queryset.values_list('DOB', flat=True)
        birth_years = [dob.year for dob in birth_years if dob]

        birth_year_counts = Counter(birth_years)

        
        sorted_years = sorted(birth_year_counts.keys())
        counts = [birth_year_counts[year] for year in sorted_years]

        fig = go.Bar(
            x=sorted_years,
            y=counts,
            marker_color='lightskyblue'
        )

        title_text = "Distribution of Voters by Year of Birth"
        graph_div = plotly.offline.plot(
            {
                "data": [fig],
                "layout": {
                    "title": title_text,
                    "xaxis_title": "Year of Birth",
                    "yaxis_title": "Number of Voters",
                    "template": "plotly_white"
                }
            },
            auto_open=False,
            output_type="div"
        )

        context['graph_div'] = graph_div

        ###############################

        party_distribution = filtered_queryset.values('party_affiliation').annotate(count=Count('party_affiliation')).order_by('-count')

        
        threshold = 0.01 * sum(entry['count'] for entry in party_distribution)
        main_labels = []
        main_values = []
        other_count = 0

        for entry in party_distribution:
            if entry['count'] >= threshold:
                main_labels.append(entry['party_affiliation'])
                main_values.append(entry['count'])
            else:
                other_count += entry['count']

        if other_count > 0:
            main_labels.append('Other')
            main_values.append(other_count)

        
        fig = go.Figure(
            data=[go.Pie(
                labels=main_labels,
                values=main_values,
                hole=0.3,  
                textinfo='label+percent',
                insidetextorientation='auto',
            )]
        )

        
        fig.update_layout(
            title=f"Voter Distribution by Party Affiliation (n={sum(main_values)})",
            showlegend=True,
            legend=dict(
                orientation="v",
                x=1.1,
                y=1
            )
        )

        graph_div_a = plotly.offline.plot(
            fig,
            auto_open=False,
            output_type="div"
        )

        
        context['graph_div_a'] = graph_div_a


        ###############################
        elections = {
            '2020 State': filtered_queryset.filter(v20state=True).count(),
            '2021 Town': filtered_queryset.filter(v21town=True).count(),
            '2021 Primary': filtered_queryset.filter(v21primary=True).count(),
            '2022 General': filtered_queryset.filter(v22general=True).count(),
            '2023 Town': filtered_queryset.filter(v23town=True).count(),
        }

        labels = list(elections.keys())
        values = list(elections.values())

        fig = go.Figure(
            data=[go.Bar(
                x=labels,
                y=values,
                marker_color='lightskyblue'
            )]
        )

    
        fig.update_layout(
            title=f"Vote Count by Election (n={sum(values)})",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
        )

        graph_div_b = plotly.offline.plot(
            fig,
            auto_open=False,
            output_type="div"
        )


        context['graph_div_b'] = graph_div_b
        current_year = datetime.now().year
        context['years'] = range(1900, current_year + 1)
        context['scores'] = range(0, 6)
        return context