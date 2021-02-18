from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from info import views as info_views
from partner import views as partner_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', info_views.landing, name='landing'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', info_views.register, name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('cabinet/', info_views.cabinet, name='cabinet'),
    path('first_pay/', info_views.first_pay, name='first_pay'),
    path('base/', info_views.base_of_suppliers, name='base'),
    path('education/', info_views.education, name='education'),
    path('education/<int:article_id>', info_views.article_view, name='article_view'),

    path('partner/', partner_views.partner, name='partner'),
    path('partner/accept', partner_views.partner_accept, name='partner_accept'),
    path('partner/payment', partner_views.partner_payment, name='partner_payment'),
    path('partner/<str:code>', partner_views.partner_detail, name='partner_detail'),

    path('management/', partner_views.confirm_payments, name='confirm_payments'),
    path('management/partners', partner_views.partners_list, name='partners_list'),
    path('partner/actions', partner_views.partner_actions, name='partner_actions'),

    path('education/create', info_views.create_article, name='create_article'),

]
