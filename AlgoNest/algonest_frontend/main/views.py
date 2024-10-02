# from django.shortcuts import render, get_object_or_404
# from .models import Bot
# import random

# def landing_page(request):
#     return render(request, 'landing_page.html')

# def bots_list(request):
#     bots = Bot.objects.all()
#     return render(request, 'bots_list.html', {'bots': bots})

# def bot_detail(request, bot_id):
#     bot = get_object_or_404(Bot, pk=bot_id)
#     return render(request, 'bot_detail.html', {'bot': bot})

# def user_dashboard(request):
#     # Sample investment data
#     investment_data = {
#         'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
#         'values': [random.randint(1000, 5000) for _ in range(6)],
#     }
#     return render(request, 'user_dashboard.html', {'investment_data': investment_data})

# def about(request):
#     return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')

from django.shortcuts import render, get_object_or_404
from .models import Bot
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def profile(request):
    return render(request, 'profile.html')

def landing_page(request):
    return render(request, 'landing_page.html')

def bots_list(request):
    bots = Bot.objects.all()
    return render(request, 'bots_list.html', {'bots': bots})

def bot_detail(request, bot_id):
    bot = get_object_or_404(Bot, pk=bot_id)
    return render(request, 'bot_detail.html', {'bot': bot})

@login_required
def user_dashboard(request):
    # Simulate user's investments in bots
    # In a real application, retrieve this data from the database based on the logged-in user
    user_investments = [
        {
            'bot': Bot.objects.get(name='Aggressive Alpha'),
            'amount_invested': 5000,
            'current_value': 6200,
            'performance_data': [
                ['2024-09-01', 5000],
                ['2024-09-08', 5400],
                ['2024-09-15', 5800],
                ['2024-09-22', 6000],
                ['2024-09-29', 6200],
            ],
        },
        {
            'bot': Bot.objects.get(name='Balanced Beta'),
            'amount_invested': 3000,
            'current_value': 3300,
            'performance_data': [
                ['2024-09-01', 3000],
                ['2024-09-08', 3100],
                ['2024-09-15', 3200],
                ['2024-09-22', 3250],
                ['2024-09-29', 3300],
            ],
        },
    ]

    # Check if the user has investments
    if user_investments:
        # Calculate totals
        total_invested = sum(inv['amount_invested'] for inv in user_investments)
        total_current_value = sum(inv['current_value'] for inv in user_investments)
        total_profit_loss = total_current_value - total_invested

        # Prepare data for the overall performance chart
        performance_dates = [data[0] for data in user_investments[0]['performance_data']]
        performance_values = [
            sum(inv['performance_data'][i][1] for inv in user_investments)
            for i in range(len(performance_dates))
        ]
    else:
        # Default values when no investments
        total_invested = 0
        total_current_value = 0
        total_profit_loss = 0
        performance_dates = []
        performance_values = []

    context = {
        'user_investments': user_investments,
        'total_invested': total_invested,
        'total_current_value': total_current_value,
        'total_profit_loss': total_profit_loss,
        'performance_dates': performance_dates,
        'performance_values': performance_values,
    }

    return render(request, 'user_dashboard.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
