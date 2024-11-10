from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

from utils.models import AbstractDateTimeModel



TYPE_CHOICES = (
    
)



SEND_SMS_IP_LIMIT = '1/2m'
WAIT_LIMIT_LIFTED = 15 * 60
RESEND_LIMIT = 2 * 60


class Notification(AbstractDateTimeModel):
    # type = models.CharField(
    #     _("تایپ"), 
    #     max_length=50,
    #     choices=TYPE_CHOICES,
    # )
    text = models.TextField(
        _("متن پیام"),
    )
    subject = models.CharField(
        _("عنوان"), 
        max_length=255,
        default='Subject'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("کاربر"), 
        on_delete=models.CASCADE,
    )
    is_read = models.BooleanField(
        _("خوانده شده"),
        default=False,
    )
    
    class Meta:
        verbose_name = _('نوتیفیکیشن')
        verbose_name_plural = _('نوتیفیکیشن ها')
        
    def __str__(self) -> str:
        return f'{self.type} | {self.user.username}'
    

    
    @classmethod
    def create(cls, user, text, subject='Subject'):
        n = cls.objects.create(user=user, text=text, subject=subject)
        mobile_number = user.mobile_number
        # try:
        #     SendSMSWithPattern(
        #             str(mobile_number.national_number),
        #             text,
        #         ).send()
        # except : 
        #     print('Sms not Send')
        
    #     n.send_notification_email([user.email], text, subject)
        
        
    # def send_notification_email(self, email, text, subject=None):
    #     try:
    #         subject = subject
    #         message = text
    #         from_email = 'ohana@saweed.fun'
    #         recipient_list = email
    #     except NameError:
    #         print("Error: 'email' is not defined")

    #     try:
    #         send_mail(subject, message, from_email, recipient_list)
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #     return HttpResponse('Email sent successfully.')

