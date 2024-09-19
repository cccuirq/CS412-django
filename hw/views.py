## hw/views.py
## description: the logix to handle URL requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.

# def home(request):

#     '''A function to respond to the /hw URL
#     '''

#     #create some text
#     #f 就是可以加import的东西
#     response_tex = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>
#     This is our first django we page!
#     </p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     '''

#     #return a response to the client
#     return HttpResponse(response_tex)

def home(request):
    '''A function to respond to the /hw URL
    '''

    template_name = "hw/home.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'letter1' : chr(random.randint(65,90)), #a letter
        'letter2' : chr(random.randint(65,90)),
        'number' : random.randint(1,10), #a number

    }

    # delegate response to template
    return render(request, template_name, context)

def about(request):
    '''A function to respond to the /hw/about URL
    '''

    template_name = "hw/about.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),

    }

    # delegate response to template
    return render(request, template_name, context)