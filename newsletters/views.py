# Local Apps
from .models import Member
from .serializers import MemberCreateSerializer

# Third Party Packages
from rest_framework.generics import CreateAPIView


class MemberCreateView(CreateAPIView):
    """Create member for newsletters."""
    serializer_class = MemberCreateSerializer
    queryset = Member.objects.all()
