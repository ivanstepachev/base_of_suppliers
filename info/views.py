from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, CreateArticleForm
from partner.models import Partner, Action
from info.models import Article
from user.models import CustomUser
from partner import utils

from common.decorators import access_paid

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def landing(request):
    code = request.GET.get('ref')
    if code:
        # Проверка на корректность реферальной ссылки, если неверно, то зачисление на админа
        partner = Partner.objects.filter(code=code).first()
        if partner:
            if request.session.get('code') is None:
                #utils.action_alert('Уникальный переход по ссылке', to_partner=partner)
                admin = Partner.objects.get(id=1)
                Action.objects.create(verb='Eyb', status='following', to_partner=partner, to_grand_partner=admin)
            request.session['code'] = code
        else:
            request.session['code'] = 'admin'
        return render(request, 'info/landing.html', {'id': id})
    # тут ошибка возникает без реф ссылки
    # c = request.session['code']
    return render(request, 'info/landing.html')



@login_required
def cabinet(request):
    return render(request, 'info/cabinet.html')


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # Проверка сессии и кукис
            if request.session.get('code'):
                code = request.session['code']
                mentor = Partner.objects.filter(code=code).first()
            else:
                mentor = Partner.objects.get(id=1)
            Partner.objects.create(user=new_user, mentor=mentor)
            new_user = authenticate(email=user_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return redirect('cabinet')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'info/register.html', {'user_form': user_form})


@login_required
def first_pay(request):
    request.user.is_paid = True
    request.user.save()

    # Временная логика платежа
    mentor = Partner.objects.get(user=request.user).mentor
    mentor.balance += 500
    mentor.save()

    grand_mentor = mentor.mentor
    grand_mentor.balance += 100
    grand_mentor.save()

    admin = Partner.objects.get(id=1)
    admin.balance += 300
    admin.save()
    utils.action_alert(verb=f'Оплата от {request.user.email}', to_partner=mentor, to_grand_partner=grand_mentor)

    return redirect('cabinet')


@login_required
def base_of_suppliers(request):
    return render(request, 'info/base.html')


@access_paid
@login_required
def education(request):
    articles = Article.objects.all()
    return render(request, 'info/education.html', {'articles': articles})


@login_required
def article_view(request, article_id):
    article = Article.objects.filter(id=article_id).first()
    return render(request, 'info/article.html', {'article': article})


@staff_member_required
def create_article(request):
    if request.method == 'POST':
        article_form = CreateArticleForm(data=request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('landing')
    else:
        article_form = CreateArticleForm(data=request.GET)
    return render(request, 'info/create_article.html', {'article_form': article_form})
