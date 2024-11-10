from django.contrib.auth.decorators import user_passes_test


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = '/'
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url,
        redirect_field_name=None
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
