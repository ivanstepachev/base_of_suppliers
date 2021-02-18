from django.shortcuts import redirect


# Декоратор для проверки статуса оплаты
def access_paid(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_paid:
            return redirect('cabinet')
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
