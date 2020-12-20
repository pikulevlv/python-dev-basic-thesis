import time
import os
from django.shortcuts import render, redirect
from .models import AdvUser, Order, Tool, ToolType
from .tasks import save_orders, send_mail_task, tool_1_task
from celery import current_app, result, Celery
from django.views.generic import ListView, DetailView, UpdateView, \
    CreateView, FormView, DeleteView
from .forms import ContactForm, OrderForm, RegistrationForm, LoginForm
from eoscan_app.settings import BYTES_TO_MB_COEF, BASE_DIR

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from django.urls import reverse_lazy
from captcha.fields import CaptchaField
from django.http import FileResponse
from django.core.paginator import Paginator
import random
# from osgeo import gdal
# import cv2
# import numpy as np
# from scipy import ndimage
# import glob
# from matplotlib import pyplot as plt


# PERMISSIONS ________________________________________________


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        # просто сформулировать условие выдачи прав
        # return self.request.user.email.endswith('@example.com')
        return self.request.user.is_superuser


class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# CONTACTS ________________________________________________


class ContactFormView(LoginRequiredMixin, FormView):
    template_name = "recognition/contact.html"
    form_class = ContactForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Contact'
        return context

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        text = form.cleaned_data['message']
        email = form.cleaned_data['email']
        send_mail_task.delay(subject, text, email)
        return super().form_valid(form)


# ABOUT ________________________________________________

def about_view(request):
    text = """eoScan is the collection of tools for recognizing 
    images in agriculture and other industries."""
    context = {'text': text, 'active_page': 'About'}
    return render(request, 'recognition/about.html', context)


# USER ________________________________________________


class UserCreateView(CreateView):
    model = AdvUser
    form_class = RegistrationForm
    success_url = '/'
    template_name = 'recognition/register.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Register'
        return context


class LoginUserView(LoginView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'recognition/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Login'
        return context


class LogoutUserView(LogoutView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Logout'
        return context


# TOOLS ________________________________________________


class ToolListView(ListView):
    model = Tool
    template_name = "recognition/tool_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Tools'
        return context


class ToolDetailView(DetailView):
    model = Tool
    template_name = "recognition/tool_info.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Tools'
        return context

# TOOLTYPE ________________________________________________


class ToolTypeListView(ListView):
    model = ToolType
    template_name = "recognition/tooltype_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Tool types'
        return context

# ORDER ________________________________________________


# class OrderListView(LoginRequiredMixin, ListView):
#     model = Order
#     template_name = "recognition/order_list.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#
#         context['active_page'] = 'Orders'
#         return context

@login_required
def order_list_view(request):
    context = {}
    object_list = Order.objects.order_by('-created').\
        select_related('tool', 'tool__tool_type').\
        filter(user__pk=request.user.id)
    context['active_page'] = 'Orders'

    paginator = Paginator(object_list, 10)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context['page'] = page
    context['object_list'] = page.object_list

    user_id = request.user.id
    if request.method == 'POST':
        task = save_orders.delay(user_id=user_id)
        context['task_id'] = task.id

        while current_app.AsyncResult(task.id).status != 'SUCCESS':
            print(current_app.AsyncResult(task.id).status)
            time.sleep(1)
            continue

        filename = f'media/reports/orders_user_{user_id}.txt'
        file = FileResponse(open(filename, 'rb'), as_attachment=True)
        return file

    return render(request, 'recognition/order_list.html', context)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "recognition/order_detail.html"

    # def get_object(self):
    #     return get_object_or_404(User, id=self.request.user.first_name)
    # user = get_object()
    # extra_context = {'user': user}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Orders'

        return context

    def post(self, request, *args, **kwargs):

        req = self.request.__dict__['META']['HTTP_REFERER']
        req = int(req.split('order_list/')[-1].split('/')[0])
        task = tool_1_task.delay(order_id=req)
        order = Order.objects.get(pk=req)
        order.task_id = str(task.id)
        print('TASK ID! ', task.id)
        order.save()

        return redirect('recognition:order_detail', req)

# def download_view(request, order_id):
#     context = {}
#     context['order_id'] = order_id
#     if request.method == 'POST':
#         filename = os.path.join(BASE_DIR, 'media', str(Order.objects.get(pk=req).img))
#         file = FileResponse(open(filename, 'rb'), as_attachment=True)
#         return file


class OrderDownloadView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "recognition/order_download.html"
    # success_url = '/order_list/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Orders'
        return context

    def post(self, request, *args, **kwargs):

        req = self.request.__dict__['META']['HTTP_REFERER']
        req = int(req.split('order_list/')[-1].split('/')[0])
        order = Order.objects.get(pk=req)
        try:
            filename = order.result_path
            file = FileResponse(open(filename, 'rb'), as_attachment=True)
        except:
            user_id = self.request.user.id
            result_folder_path = order.result_folder_path
            extension = order.extension
            filenames = [i.name for i in os.scandir(result_folder_path) if
                         i.is_file() and f'{req}.{user_id}.{extension}'
                         in i.name]
            filename = os.path.join(
                result_folder_path, random.choice(filenames)
            )
            file = FileResponse(open(filename, 'rb'), as_attachment=True)
            order.result_path = filename
            order.save()

        return file


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = "recognition/order_create.html"
    form_class = OrderForm
    success_url = "/order_list/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active_page'] = 'Orders'
        return context

    def form_valid(self, form):
        user_id = self.request.user.id
        user = AdvUser.objects.get(id=user_id)
        form.instance.user = user
        order = form.save(commit=False)
        order.save()
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'recognition/order_create.html'

    form_class = OrderForm

    def form_valid(self, form):
        try:
            req = self.request.__dict__['META']['HTTP_REFERER']
            req = int(req.split('order_list/')[-1].split('/')[0])
            self.success_url = f'/order_list/{req}/'
        except:
            self.success_url = '/order_list/'
        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'recognition/order_delete.html'
    success_url = '/'

# INDEX ________________________________________________


def index_view(request):
    context = {}
    context['text'] = "You can start!"
    return render(request, 'recognition/index.html', context)


@login_required
def reports_view(request):
    user_id = request.user.id
    context = {"active_page": "Reports"}
    if request.method == 'POST':
        task = save_orders.delay(user_id=user_id)
        context['task_id'] = task.id
    return render(request, 'recognition/reports.html', context)


@login_required
def personal_view(request):
    orders = Order.objects.select_related('tool', 'tool__tool_type').\
        filter(user__pk=request.user.id)
    feature = request.user.id
    context = {
        "orders": orders,
        "feature": feature,
        "active_page": "Personal",
    }

    if request.method == 'POST':
        task = send_mail_task.delay(subject='scelery_sub',
                                    text_message='scelery_text',
                                    email_to='scelery@scelery.com')
        context['task_id'] = task.id

    return render(request, 'recognition/personal.html', context)


@login_required
def task_status_view(request):
    if request.method == 'GET':
        task_id = request.GET['task_id']
        task = current_app.AsyncResult(task_id)
        task_status = task.status

        context = {}
        context['status'] = task_status
        context['task_id'] = task_id
        return render(request, 'recognition/task_status.html', context)
