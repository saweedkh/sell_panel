from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone, datetime_safe

# Local Apps
from gateways.models.banks import Bank
from utils.datetime import check_and_make_aware
from .models import  MobilePhoneVerify, User, UserAddress
from seo.serializers import BaseDateTimeModelSerializer
from .encode import encode_dict, decode_dict, SECRET_KEY
from rest_framework_simplejwt.tokens import RefreshToken



# Third Party Packages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from drf_spectacular.utils import extend_schema_field


class CustomTokenObtainPairSerializer(serializers.Serializer):
    token_class = RefreshToken

    mobile_number = PhoneNumberField()
    otp = serializers.IntegerField(write_only=True)



    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number')
        active_otp = attrs.get('otp')

        # try:
        record = MobilePhoneVerify.objects.get(mobile_number=mobile_number)
        # except:
        #     raise serializers.ValidationError(_("شماره موبایل وجود ندارد."))
        
        
        if record.code == active_otp:
            
            if record.status == MobilePhoneVerify.USELESS:
                raise serializers.ValidationError(_("این کد استفاده شده است."))
        
            record.status = MobilePhoneVerify.USELESS
            if (check_and_make_aware(datetime.now()) - record.updated).seconds > 5 * 60:
                record.save()
                raise serializers.ValidationError(_("این کد تایید منقضی شده است. لطفا یک کد دیگر درخواست دهید."))
            record.save()

            
            try:
                user = User.objects.get(mobile_number=mobile_number)
            except User.DoesNotExist:
                raise serializers.ValidationError(_("کاربر با این شماره موبایل وجود ندارد."))

            refresh = self.get_token(user)


            return { 
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        
        else:
            raise serializers.ValidationError( _('کد تایید اشتباه است.'))
            

    
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class OtpSendSerializer(serializers.Serializer):
    """
     Register user.
    """
    mobile_number = PhoneNumberField()
    class Meta:
        
        fields = ('mobile_number',)
        

class VerifySerializer(serializers.ModelSerializer):
    """
     Register user.
    """
    
    mobile_number = PhoneNumberField()
    
    code = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            'mobile_number', 
            'code',
            'created',
            'updated',
            )
        optional_fields = ('mobile_number', 'code',)
        read_only_fields = ('created', 'updated')
        
class RegisterComplateSerializer(serializers.ModelSerializer):
    """
    Complate Register user.
    """
    
    token = serializers.CharField()
    
    class Meta:
        model = User
        fields = (
            'token',
            'full_name', 
            'email', 
            'password', 
            'created',
            'updated',
            )
        optional_fields = ('email',)
        read_only_fields = ('created', 'updated')
        write_only_fields  = ('token', 'password')
        
        

            

    

        
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Change user password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password',)
        
        
    

class ProfileSerializer(serializers.ModelSerializer):
    """
    Get user profile.
    """
    
    profile_completion = serializers.SerializerMethodField()
    

    class Meta:
        model = User
        fields = (
            'pk',
            'confirm_profile', 
            'username', 
            'full_name', 
            'birthday',
            'mobile_number', 
            'email', 
            'avatar', 
            'profile_completion',
            'created',
            'updated',
            
        )
        read_only_fields = ('pk', 'created', 'updated', 'mobile_number', )
        
            
    def get_profile_completion(self, obj):
        return obj.get_profile_completion_percentage()

        

class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Update user profile.
    """
        
    class Meta:
        model = User
        fields = (
            'full_name', 
            'username', 
            'birthday',
            'email', 
            'avatar',
            'created',
            'updated',
        )
        optional_fields = ('full_name', 
            'username', 
            'birthday',
            'email', 
            'avatar',
            )
        read_only_fields = ('created', 'updated')
    

    def update(self, instance, validated_data):

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        return instance

    

class ForgotPasswordSerializer(serializers.Serializer):
    
    
    token = serializers.CharField()
    new_password = serializers.CharField(
        max_length=128
    )
    
    
    
class TransactionSerializer(BaseDateTimeModelSerializer):
    """Get transaction details."""

    class Meta:
        model = Bank
        fields = (
            'id',
            'user',
            'amount',
            'tracking_code',
            'status',
            *BaseDateTimeModelSerializer.Meta.fields
        
        )

class UserAddressListSerializer(BaseDateTimeModelSerializer):
    """Get user addresses."""

    class Meta:
        model = UserAddress
        fields = (
            'id',
            'author',
            'name',
            'address',
            'mobile_number',
            'postal_code',
            'is_default',
            *BaseDateTimeModelSerializer.Meta.fields
        )
        
        read_only_fields = ('author',)
        
        
    def create(self, validated_data):
        """Ensure only one address can be set as default."""
        request = self.context.get('request')
        author = request.user
        is_default = validated_data.get('is_default', False)
        
        if is_default:
            UserAddress.objects.filter(author=author, is_default=True).update(is_default=False)

        validated_data['author'] = author
        return super().create(validated_data)


class UserAddressUpdateSerializer(BaseDateTimeModelSerializer):
    """Update user address."""

    class Meta:
        model = UserAddress
        fields = (
            'name',
            'address',
            'mobile_number',
            'postal_code',
            'is_default',
        )
        
    def update(self, instance, validated_data):
        """Ensure only one address can be set as default."""
        user = self.context['request'].user
        is_default = validated_data.get('is_default', instance.is_default)
        
        if is_default:
            # Set other addresses to not default
            UserAddress.objects.filter(author=user, is_default=True).exclude(pk=instance.pk).update(is_default=False)
        
        return super().update(instance, validated_data)


