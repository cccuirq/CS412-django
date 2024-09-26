from django.shortcuts import render, HttpResponse, redirect
import time
import random

potbase = [
    "Seafood Broth $20",
    "Coconut Chicken Broth $20",
    "Bone Broth $20",
    "Pickled Cabbage & Fish Broth $18",
    "Curry Broth $18",
]
# Create your views here.
def main(request):
    template_name = "restaurant/main.html"

    context = {
        'current_time': time.ctime(),
    }

    return render(request, template_name, context)

def order(request):
    template_name = "restaurant/order.html"
    
    context = {
        'current_time': time.ctime(),
        'random_potbase': random.choice(potbase),
    }
    return render(request, template_name, context)

def confirmation(request):
    template_name = "restaurant/confirmation.html"

    if request.POST:
        
        pot_base_data = request.POST.getlist('potbase')
        vegetables_data = request.POST.getlist('vegetables')
        beaf_data = request.POST.getlist('beef')

        daily = request.POST.get('daily', None)

        special = request.POST.get('special', None)
        name = request.POST.get('name', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        
        pot_base = []
        vegetables = []
        meat = []
        total = 0
        for veg_data in vegetables_data:
            veg_name, veg_price = veg_data.split(':')
            vegetables.append(veg_name)
            total += float(veg_price)

        for base_data in pot_base_data:
            base_name, base_price = base_data.split(':')
            pot_base.append(base_name)
            total += float(base_price)

        for meat_data in beaf_data:
            meat_name, meat_price = meat_data.split(':')
            meat.append(meat_name)
            total += float(meat_price)
        
        if daily:
            daily_name, daily_price = daily.split('$')
            total += float(daily_price)
        else:
            daily_name = None
        
        random_minutes = random.choice(range(30, 61))
        random_sec = random_minutes * 60
        current = time.time()
        finisht = current + random_sec
        finish_time_str = time.ctime(finisht)
        context = {
            'name': name,
            'pot_base': pot_base,
            'vegetables': vegetables,
            'meat': meat,
            'daily_name': daily_name,
            'total': total,
            'special': special,
            'phone': phone,
            'email': email,
            'current_time': time.ctime(),
            'finish_time': finish_time_str,
        }
        
        return render(request, template_name, context)

    return redirect("order")



