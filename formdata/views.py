from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def show_form(request):
    # Show the html form to the client.

    # use this template to produce the response
    template_name = "formdata/form.html"
    return render(request, template_name)

def submit(request):
    # handle form submmission, Read out the from data, Generate a response.

    template_name = "formdata/confirmation.html"

    # check if the request is a POST (vs GET)
    if request.POST:
        
        # Read the form data into python variables:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        #package the data up to be used in response
        context = {
            'name': name,
            'favorite_color': favorite_color,
        }
        
        return render(request, template_name, context)
    
    # GET lands down there: no return statments!
    
    #this is a OK sultion: a graceful failure
    # return HttpResponse('Nope.')

    # this is a "better solution", but shows the wrong URL
    # template_name = "formdata/form.html"
    # return render(request, template_name)

    return redirect("show_form")



