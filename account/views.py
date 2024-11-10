import random
from datetime import datetime
from django.forms import ValidationError
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.exceptions import (
    InvalidToken, TokenError
)
from .serializers import CustomTokenObtainPairSerializer, UserAddressListSerializer, UserAddressUpdateSerializer

# Local Apps
from account.permissions import IsOwnerOrReadOnly
from gateways.models.banks import Bank
from utils.datetime import check_and_make_aware
from .utils import send_verification_code
from .models import MobilePhoneVerify, User, UserAddress
from .serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    RegisterComplateSerializer,
    OtpSendSerializer,
    ProfileSerializer,
    TransactionSerializer,
    VerifySerializer,
    UpdateProfileSerializer,
)
from .encode import encode_dict, decode_dict, SECRET_KEY

# Third Party Packages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, BlacklistedToken

from rest_framework.throttling import UserRateThrottle


class CustomTokenObtainView(TokenObtainPairView, UserRateThrottle):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    


class SendOtpView(APIView, UserRateThrottle):
    """
    Send Otp
    """
    
    serializer_class = OtpSendSerializer
    permission_classes = [AllowAny, ]
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            srz_data = serializer.data
            mobile_number = srz_data.get('mobile_number')
                
            result = send_verification_code(request, mobile_number)
            return Response(result.get('message'), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
 
                
class OtpVerifyView(APIView):
    """
    Verify Otp 
    """
    
    serializer_class = VerifySerializer
    permission_classes = [AllowAny, ]
    model = User
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            srz_data = serializer.data
            mobile_number = srz_data.get('mobile_number')
            code = srz_data.get('code')
            
            try:
                record = MobilePhoneVerify.objects.get(mobile_number=mobile_number)
            except:
                return Response({"message": _('شماره تلفن یافت نشد!')}, status=status.HTTP_400_BAD_REQUEST)
            
            if record.status == MobilePhoneVerify.USELESS:
                return Response( {"message": 'این کد استفاده شده است!'}, status=status.HTTP_400_BAD_REQUEST)
            
            if record.code == code:
                record.status = MobilePhoneVerify.USELESS
                if (check_and_make_aware(datetime.now()) - record.updated).seconds > 5 * 60:
                    record.save()
                    return Response({"message": _('این کد تایید منقضی شده است. لطفا یک کد دیگر درخواست دهید.')}, status=status.HTTP_400_BAD_REQUEST)
                record.save()
                current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

                session_data = {
                    'active_otp_code' : current_time,
                    'mobile_number' : mobile_number
                }
                
                
               
                # Encoding
                encoded_data = encode_dict(SECRET_KEY, session_data )
                # print("Encoded data:", encoded_data)

                
                
                
                return Response({"message": 'کد تایید شد', 'token' : encoded_data}, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"message": _('کد تایید اشتباه است.')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class RegisterView(APIView):
    """
    Register user
    """
    
    serializer_class = RegisterComplateSerializer
    permission_classes = [AllowAny, ]
    model = User
    
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            srz_data = serializer.data
            verify = srz_data.get('token')
            print(verify)
            # # Decoding
            decoded_data = decode_dict(SECRET_KEY, verify)
            
            active_otp = decoded_data.get('active_otp_code')
            mobile_number = decoded_data.get('mobile_number')
            
            if not active_otp or not mobile_number:
                return Response('شما به این بخش دسترسی ندارید', status=status.HTTP_403_FORBIDDEN)
 
            active_otp= datetime.strptime(active_otp, '%Y-%m-%d %H:%M:%S')
            time_now = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            time_now =  datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
            if (time_now - active_otp).seconds > 5 * 60:
                return Response(_('لطفا مجدد شماره تلفن خود را تایید کنید'), status=status.HTTP_400_BAD_REQUEST)
            
                
            full_name=srz_data.get('full_name')
            password=srz_data.get('password')
            email = srz_data.get('email')

            try:
                user = User.objects.create_user(
                        username=mobile_number,
                        full_name=full_name,
                        mobile_number=mobile_number,
                        password=password,
                        email=email,
                    )
                        
            except IntegrityError as e: 
                if 'unique constraint' in str(e.args).lower():
                    return Response(f'کاربر {mobile_number} موجود است', status=status.HTTP_409_CONFLICT)
                
            
            return Response(_(f'حساب کاربری شما با نام کاربری  {mobile_number} ساخته شد.'), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    """
    Get user profile.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(instance=user).data
        return Response(serializer, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    Change user password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        self.current_user = self.request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.current_user.check_password(serializer.data.get("old_password")):
                return Response({"message": "Wrong password."}, status=status.HTTP_200_OK)
            self.current_user.set_password(serializer.data.get("new_password"))
            self.current_user.save()
            return Response({"message": 'رمزعبور با موفقیت تغییر کرد!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(APIView):
    """
    Update user profile.
    """
    serializer_class = UpdateProfileSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request: HttpRequest, *args, **kwargs):
        current_user = request.user
        serializer = self.serializer_class(instance=current_user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            profile = ProfileSerializer(instance=current_user)
            return Response(profile.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    """
    Forgot password 
    """
    
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny, ]
    model = User
    
    def post(self, request, *args, **kwargs):
            
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            srz_data = serializer.data
            
            
            
            
            verify = srz_data.get('token')
            
            # # Decoding
            decoded_data = decode_dict(SECRET_KEY, verify)
            
            
            
            active_otp = decoded_data.get('active_otp_code')
            mobile_number = decoded_data.get('mobile_number')
            
            if not active_otp or not mobile_number:
                return Response({"message": "شما به این بخش دسترسی ندارید."}, status=status.HTTP_403_FORBIDDEN)
            
            
            active_otp= datetime.strptime(active_otp, '%Y-%m-%d %H:%M:%S')
            time_now = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            time_now =  datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
            if (time_now - active_otp).seconds > 5 * 60:
                return Response({"message": _('لطفا مجدد شماره تلفن خود را تایید کنید')}, status=status.HTTP_400_BAD_REQUEST)
            
            
            
            
            
            new_password = srz_data.get('new_password')
            

            
            user = User.objects.filter(mobile_number=mobile_number).first()
            
            if not user :
                return Response( {"message": _('کاربر مورد نطر یافت نشد')}, status=status.HTTP_400_BAD_REQUEST)

            
            user.set_password(new_password)
            user.save()
            return Response({"message": 'رمزعبور شما تغییر کرد.'}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(ListAPIView):
    
    permission_classes = [IsAdminUser]
    

class TransactionView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user).all()
    
        




class UserAddressListView(ListCreateAPIView):
    serializer_class = UserAddressListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserAddress.objects.filter(author=self.request.user).all()


class UserAddressRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressUpdateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = UserAddress.objects.all()
    
    
    