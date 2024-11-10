# Django Built-in modules
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

# Local apps
from .models import User, UserAddress


# Start Admin Panel Forms #

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور'),
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
            'username',
            'email',
            'avatar',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if not cd['password1'] or not cd['password2']:
            raise forms.ValidationError(_('این فیلد الزامی است.'))
        elif cd['password1'] != cd['password2']:
            raise forms.ValidationError(_('رمز عبور و تکرار آن مطابقت ندارد.'))
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('رمز عبور'),
        help_text=_(
            "رمزهای عبور خام ذخیره نمی شوند، بنابراین راهی برای دیدن رمز عبور این کاربر وجود ندارد، اما می توانید رمز عبور را با استفاده از <a href=\"../password/\">این فرم</a> تغییر دهید."
        ),
    )

    class Meta:
        model = User
        fields = (
            'mobile_number',
            'full_name',
            'username',
            'email',
            'avatar',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def clean_password(self):
        return self.initial['password']
    
    
    # def clean(self):
    #     cleaned_data = super().clean()

    #     # Validate that only one address is set as default
    #     user = self.instance
    #     if user:
    #         default_addresses = UserAddress.objects.filter(author=user, is_default=True)
    #         if default_addresses.count() > 1:
    #             self.add_error(None, _('فقط یک آدرس مجاز به پر کردن فیلد دیفالت است.'))

    #     return cleaned_data


    

# End Admin Panel Forms #
