from distutils.log import info
from time import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import requests
from bs4 import BeautifulSoup


from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    SiteConfigForm,
    TagForm,
    CourseForm,
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    Tag,
    Course,
)

class Result(object):
    def __init__(self, time, title, link):
        self.time = time
        self.title = title
        self.link = link

def get_data():
    html = requests.get("http://ugs.hust.edu.cn")
    results = []
    if html.status_code == 200:
        html.encoding = 'utf-8'

        soup = BeautifulSoup(html.text, 'html.parser')
        # 复制a标签的selector，并更换为统一格式
        data = soup.select('body > div.main1 > div > div.xwdt.fl > ul > li')
        
        # # 清空test.txt内容
        # f = open(output, 'w')
        # f.truncate()

        for item in data:
            
            title = item.find('a').get_text()
            # print(title)
            time = item.find('span').get_text()
            link = 'http://ugs.hust.edu.cn/' + item.find('a').get('href')
            result = Result(time=time, title=title, link=link)
            # 'ID': re.findall('\d+', item.get('href'))
            results.append(result)
        
            # with open(output, encoding='utf-8', mode='a') as f:
            #     f.write(str(result)+'\n')
    return results

class Template_View(TemplateResponseMixin, ContextMixin, View):
    """
    Render a template. Pass keyword arguments from the URLconf to the context.
    """
    def get(self, request, *args, **kwargs):
        result = get_data()
        # context = self.get_context_data(**kwargs)
        context = {
            'result': result
        }

        return self.render_to_response(context)


class IndexView(LoginRequiredMixin, Template_View):
    template_name = "index.html"




class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context


class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("session-list")
        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    template_name = "corecode/term_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context


class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "New term successfully added"


class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicTerm.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("term")
        return super().form_valid(form)


class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy("terms")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete term as it is set to current")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)


class TagListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Tag
    template_name = "corecode/tag_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TagForm()
        return context


class TagCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("tags")
    success_message = "New tag successfully added"


class TagUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tag
    fields = ["name"]
    success_url = reverse_lazy("tags")
    success_message = "tag successfully updated."
    template_name = "corecode/mgt_form.html"


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy("tags")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The tag {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TagDeleteView, self).delete(request, *args, **kwargs)


class CourseListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Course
    template_name = "corecode/course_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm()
        return context


class CourseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("courses")
    success_message = "New course successfully added"


class CourseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ["name"]
    success_url = reverse_lazy("courses")
    success_message = "Course successfully updated."
    template_name = "corecode/mgt_form.html"


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy("courses")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The course {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(CourseDeleteView, self).delete(request, *args, **kwargs)


class CurrentSessionAndTermView(LoginRequiredMixin, View):
    """Current SEssion and Term"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.filter(current=True),
                "current_term": AcademicTerm.objects.get(current=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicTerm.objects.filter(name=term).update(current=True)
            AcademicTerm.objects.exclude(name=term).update(current=False)


        return render(request, self.template_name, {"form": form})
