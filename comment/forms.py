# Django Built-in modules
from django import forms
from django.utils.translation import gettext_lazy as _


class AnonymousBaseCommentForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control validate-name',
                'placeholder': _('نام'),
            }
        ),
        label=_('نام')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control validate-email',
                'placeholder': _('ایمیل'),
            }
        ),
        label=_('ایمیل')
    )
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control validate-review',
                'placeholder': _('نظر'),
            }
        ), label=_('نظر')
    )


class AuthenticatedBaseCommentForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control validate-review',
                'placeholder': _('نظر'),
            }
        ), label=_('نظر')
    )


class AnonymousBaseReplyForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control validate-name',
                'placeholder': _('نام'),
            }
        ),
        label=_('نام')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control validate-email',
                'placeholder': _('ایمیل'),
            }
        ),
        label=_('ایمیل')
    )
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control validate-review',
                'placeholder': _('نظر'),
            }
        ), label=_('نظر')
    )
    parent = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    comment_type = forms.IntegerField(
        widget=forms.HiddenInput()
    )


class AuthenticatedBaseReplyForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control validate-review',
                'placeholder': _('نظر'),
            }
        ), label=_('نظر')
    )
    parent = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    comment_type = forms.IntegerField(
        widget=forms.HiddenInput()
    )
