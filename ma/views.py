from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Result
import plotly
import plotly.graph_objs as go
# Create your views here.

class ResultsListView(ListView):
    '''Views to display list of marathon results'''

    template_name = 'ma/results.html'
    model = Result
    context_object_name = "results"
    paginate_by = 50

    def get_queryset(self):
        
        # start with entire queryset
        qs = super().get_queryset().order_by('place_overall')
        # filter results by these field(s):
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if city:
                qs = Result.objects.filter(city__icontains=city)
                
        return qs
    
class ResultDetailView(DetailView):
    '''show results for one request'''

    template_name ='ma/result_detail.html'
    model = Result
    context_object_name = 'r'

    def get_context_data(self, **kwargs):
        '''Add some data to the context object, including graph'''
        context = super().get_context_data(**kwargs)
        r = context['r']#our runner
        #build the graph
        x = [f'Runners Passsed by {r.first_name}',
             f'Runners who Passed {r.first_name}']
        
        y = [r.get_runners_passed(), r.get_runners_passed_by()]

        # print(f'x={x}')
        # print(f'y={y}')
        fig = go.Bar(x=x, y=y)
        graph_div = plotly.offline.plot({"data": [fig], 
                                         }, 
                                         auto_open=False, 
                                         output_type="div")

        #and the graph to the context
        context['graph_div'] = graph_div
       
        x = ['first half', 'second half']
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        y = [first_half_seconds , second_half_seconds]
        
        # generate the Pie chart
        fig = go.Pie(labels=x, values=y) 
        title_text = f"Half Marathon Splits"

        graph_div_splits = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        
        context['graph_div_splits'] = graph_div_splits
        return context