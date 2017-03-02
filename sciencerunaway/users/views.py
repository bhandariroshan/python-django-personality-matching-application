# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import User

from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import MySignupForm
from .models import UserProfile


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class SignupView(TemplateView):
    """Home page for students."""

    template_name = 'pages/signup.html'
    model = UserProfile

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        form = MySignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MySignupForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            user = User.objects.get(username=username)

            age = form.cleaned_data['age']
            signup_type = form.cleaned_data['signup_type']
            if signup_type == 2:
                user.is_active = False

            name = form.cleaned_data['name']

            user_profile = self.model.objects.create(
                age=age,
                signup_type=signup_type,
                name=name,
                user=user
            )

            user_profile.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            if user_profile.signup_type == 1:
                login(self.request, user)
                return HttpResponseRedirect('/quiz/')
            else:
                return HttpResponseRedirect('/')
        else:
            return render(request, self.template_name, {'form': form})
