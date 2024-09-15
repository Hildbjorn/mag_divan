from django.http import JsonResponse

from catalog.models import Color


def get_all_colors(request):
    colors = Color.objects.all().values('id', 'name', 'hex_code')
    return JsonResponse({'colors': list(colors)})


def get_colors(request, model_id):
    colors = Color.objects.filter(
        furniture_models=model_id).values('id', 'name', 'hex_code')
    return JsonResponse({'colors': list(colors)})
