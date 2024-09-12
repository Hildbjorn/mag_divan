import os
from pathlib import Path
from django.http import FileResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from django.conf import settings


__all__ = (
    'page_not_found_view',
    'IndexPageView',
    'serve_documents',
)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


class IndexPageView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        # Получаем полный путь к директории проекта
        project_path = Path(__file__).resolve().parent
        # Извлекаем только название директории
        project_name = str(project_path.name)
        context = super().get_context_data(**kwargs)
        context['project_name'] = project_name
        return context


def serve_documents(request, filename):
    """
    Функция, которая принимает имя файла в качестве аргумента и возвращает файл.
    """
    filepath = os.path.join(settings.MEDIA_ROOT, 'documents', filename)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
