from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import StudyGroup, GroupMessage
from accounts.views import award_points

class GroupListView(LoginRequiredMixin, ListView):
    model = StudyGroup
    template_name = 'collaboration/group_list.html'
    context_object_name = 'groups'

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = StudyGroup
    fields = ['name', 'description']
    template_name = 'collaboration/group_form.html'
    success_url = reverse_lazy('group_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        award_points(self.request.user, 25, "Community Leader", "You earned 25 points for starting a new study group!")
        return response

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = StudyGroup
    template_name = 'collaboration/group_detail.html'
    context_object_name = 'group'

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        content = request.POST.get('content')
        if content:
            GroupMessage.objects.create(
                group=group,
                sender=request.user,
                content=content
            )
        return redirect('group_detail', pk=group.pk)
