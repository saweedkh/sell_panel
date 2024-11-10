# from django.contrib.auth.backends import BaseBackend
# from .models import User

# class PhoneNumberBackend(BaseBackend):
#     def authenticate(self, request, mobile_number=None, verification_code=None, **kwargs):
#         try:
#             user = User.objects.get(mobile_number=mobile_number,)
#             if user is not None:
#                 return user
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None