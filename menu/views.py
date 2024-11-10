# Django Built-in Module
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.urls import reverse


@staff_member_required
def gfk_lookup(request):
    if request.method == 'POST':
        content_type_id = request.POST.get('content_type_id')
        content_type = ContentType.objects.get(id=content_type_id)
        url = reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist')
        return JsonResponse({'status': 200, 'object_url': url})
    return JsonResponse({'status': 400})
