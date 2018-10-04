from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login
from django.views.generic import TemplateView, UpdateView, CreateView, ListView

from .models import User
from .froms import FreelancerSignUpForm, OwnerSignUpForm


class SigUpView(TemplateView):
    """
    提供注册选择页面
    """
    template_name = 'users/sigup.html'


class UserDetailView(TemplateView):
    """
    展示个人信息
    """
    model = User
    template_name = 'users/user_profile.html'

    def get_context_data(self, **kwargs):
        """
        此方法获取url中的参数,再根据参数返回一个
        整个模板可以使用的context字典

        具体步骤如下:
        1. 获取URL 127.0.0.1:8000/user/<str:username>中的username的值.
        2. 根据username的值调用指定的用户对象实例.
        3. 定义了context['profile'].
        4. 在模板中可以直接使用profile调用该关键字.

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['profile'] = User.objects.get(username=username)
        return context


class UpdateProfileView(UpdateView):
    """
    修改个人性息的视图
    """

    model = User
    # fields字段指定页面表单将出现的字段
    fields = ['profile_photo', 'first_name', 'last_name', 'profile', 'skills']
    template_name = 'users/user_profile_update.html'

    def form_valid(self, form):
        """
        Checks valid form and add/save many to many tags field in user object.
        :param form:
        :return:
        """
        # 将表单置commit置为False是为了
        # 不让表单立即改变数据库,在保存之前
        # 我们还能对数值有其他自定的操作
        user = form.save(commit=False)
        user.save()

        # 保存了其他关联数据库更改信息
        form.save_m2m()
        messages.success(self.request, 'Your profile is updated successfully.')
        return redirect('users:user_profile', self.object.username)

    def get_success_url(self):
        """
        Prepares success url for successful form submission.
        :return:
        """
        return reverse('users:user_profile', kwargs={'username': self.object.username})


class ListFreelancersView(ListView):
    """
    显示所有自由职业者
    """

    model = User
    context_object_name = 'freelancers'
    template_name = 'users/freelancer_list.html'

    def get_queryset(self):
        """
        Prepare all freelancers on is_freelancer col
        in user model
        :return:
        """
        return User.objects.filter(is_freelancer=True)


class FreelancerSignUpView(CreateView):
    """
    Register a freelancer
    """

    model = User
    form_class = FreelancerSignUpView
    template_name = 'users/sigup_form.html'

    def get_context_data(self, **kwargs):
        """
        Updates context value 'user_type' in
        current context
        :param kwargs:
        :return:
        """

        kwargs['user_type'] = 'freelancer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class OwnerSignUpView():
    pass
