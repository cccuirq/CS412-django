from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.

quotes = [
    "Imagination is more important than knowledge.",
    "Life is like riding a bicycle. To keep your balance, you must keep moving.",
    "Try not to become a man of success, but rather try to become a man of value.",
    "In the middle of difficulty lies opportunity.",
    "The important thing is not to stop questioning. Curiosity has its own reason for existing.",
    "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.",
    "I have no special talent. I am only passionately curious.",
    "A person who never made a mistake never tried anything new.",
    "If you can't explain it simply, you don't understand it well enough.",
    "Try not to become a man of success, but rather try to become a man of value.",

]

images = [
    'static/einstein1.jpg',
    'static/einstein2.jpg',
    'static/einstein3.jpg',
    'static/einstein4.jpg',
    'static/einstein5.jpg'
]
def home(request):

    template_name = "quotes/quote.html"


    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'selected_quote' : random.choice(quotes),
        'selected_image' : random.choice(images),
    }

    # delegate response to template
    return render(request, template_name, context)

def quote(request):

    template_name = "quotes/quote.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'selected_quote' : random.choice(quotes),
        'selected_image' : random.choice(images),
    }

    # delegate response to template
    return render(request, template_name, context)

def about(request):

    template_name = "quotes/about.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),

    }

    # delegate response to template
    return render(request, template_name, context)

def show_all(request):

    template_name = "quotes/show_all.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'quotes' : quotes,
        'images' : images,

    }

    # delegate response to template
    return render(request, template_name, context)