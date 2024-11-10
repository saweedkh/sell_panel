# Local Apps
from .models import MenuObject


def menu(request):
    return {'menu_objects': MenuObject.objects.all()}
