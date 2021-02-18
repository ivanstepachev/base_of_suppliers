from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from partner.models import Partner, Action, Payment
from django.contrib import messages
from common.decorators import access_paid

from django.views.decorators.csrf import csrf_exempt

from itertools import chain
from operator import attrgetter

from datetime import datetime


@access_paid
@login_required
def partner(request):
    partner = request.user.partner
    if partner.is_partner:
        refs = Partner.objects.filter(mentor=partner, is_partner=True)
        mentor_actions = Action.objects.filter(to_partner=partner)
        grand_mentor_actions = Action.objects.filter(to_grand_partner=partner)
        link = f'http://127.0.0.1:8000/?ref={partner.code}'
        balance = partner.balance
        return render(request, 'partner/partner.html', {'refs': refs, 'mentor_actions': mentor_actions,
                            'grand_mentor_actions': grand_mentor_actions, 'link': link, 'balance': balance})
    else:
        return render(request, 'partner/partner_agreement.html')


@login_required
def partner_accept(request):
    request.user.partner.is_partner = True
    request.user.partner.save()
    return redirect('partner')


# Запрос на выплату
@login_required
def partner_payment(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        if amount >= 500:
            partner = request.user.partner
            payment = Payment(partner=partner, amount=amount)
            payment.save()
            partner.balance = partner.balance - amount
            partner.save()
            messages.success(request, 'Выплата заказана')
            return redirect('partner')
        else:
            messages.info(request, 'Сумма должна быть больше 500Р')
            return redirect('partner')
    return redirect('partner')


# Тут нужно с JS - временный вариант
@csrf_exempt
def confirm_payments(request):
    if request.method == 'POST':
        payment_id = request.POST.get('confirm')
        payment = Payment.objects.filter(id=payment_id).first()
        payment.confirm = True
        payment.save()
        return redirect('confirm_payments')
    payments = Payment.objects.filter(confirm=False)
    context = {'payments': payments}
    return render(request, 'partner/payments.html', context)


@login_required
# Надо разобраться с фильтром точнее
def partner_actions(request):
    partner = request.user.partner
    if request.method == 'POST' and request.POST.get('by_who') is not None:
        by_who = request.POST.get('by_who')
        date = request.POST.get('date')
        if by_who == 'by_me':
            actions = Action.objects.filter(to_partner=partner, date__contains=date)
        elif by_who == 'by_partners':
            actions = Action.objects.filter(to_grand_partner=partner, date__contains=date)

    else:
        partner_actions = Action.objects.filter(to_partner=partner)
        grand_partner_actions = Action.objects.filter(to_grand_partner=partner)
        # Совмещаем все записи первичные и вторичные
        actions = sorted(
            chain(partner_actions, grand_partner_actions),
            key=attrgetter('date'),
            reverse=True
        )
    return render(request, 'partner/actions.html', {'actions': actions})


def partners_list(request):
    search = request.GET.get('search')
    if search:
        partners = Partner.objects.filter(name__contains=search)
    else:
        partners = Partner.objects.all()
    return render(request, 'info/partners.html', {'partners': partners})


# Тестовый по фильтру
def partner_detail(request, code):
    partner = Partner.objects.filter(code=code).first()
    partners = partner.partners.filter(date__month=str(datetime.now().month))
    return render(request, 'partner/partner_detail.html', {'partner': partners})
