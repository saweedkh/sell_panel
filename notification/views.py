from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from notification.models import Notification
from notification.serializers import ListNotificationSerializers


# Create your views here.


class NotificationListView(ListAPIView):
    
    serializer_class = ListNotificationSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ('is_read',)
    queryset = Notification.objects.none()
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        notif = Notification.objects.filter(user=request.user)
        if notif:
            serializer = self.serializer_class(notif, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response({'message': 'اعلانی یافت نشد'}, status=status.HTTP_404_NOT_FOUND) 
        
    
    
class DetailNotificationView(APIView):
    
    """ Notification Detail """
    
    serializer_class = ListNotificationSerializers
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, pk, *args, **kwargs):
        notif = Notification.objects.filter(pk=pk).first()
        if notif:
            if notif.user == request.user:
                serializer = self.serializer_class(notif)
                return Response(serializer.data, status=status.HTTP_200_OK)                
            return Response({'message': 'شما به این اعلان دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'اعلان مورد نظر یافت نشد!'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class ReadNotificationView(APIView):
    
    """ Read Notification """
    
    serializer_class = ListNotificationSerializers
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, pk, *args, **kwargs):
        notif = Notification.objects.filter(pk=pk, ).first()
        if notif:
            if notif.user == request.user:
                notif.is_read = True
                notif.save()
                serializer = self.serializer_class(notif)
                return Response(serializer.data, status=status.HTTP_200_OK)                
            return Response({'message': 'شما به این اعلان دسترسی ندارید'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'اعلان مورد نظر یافت نشد!'}, status=status.HTTP_400_BAD_REQUEST)