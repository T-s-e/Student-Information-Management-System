from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from apps.subjects.models import Subject

from .forms import CreateResults, EditResults
from .models import Result


@login_required
def create_result(request):
    subjects = Subject.objects.all()
    if request.method == "POST":

        # after visiting the second page
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                courses = form.cleaned_data["courses"]
                session = form.cleaned_data["session"]
                term = form.cleaned_data["term"]
                subjects = request.POST["subjects"]
                results = []
                for subject in subjects.split(","):
                    stu = Subject.objects.get(pk=subject)
                    if stu.current_class:
                        for course in courses:
                            check = Result.objects.filter(
                                session=session,
                                term=term,
                                current_class=stu.current_class,
                                course=course,
                                subject=stu,
                            ).first()
                            if not check:
                                results.append(
                                    Result(
                                        session=session,
                                        term=term,
                                        current_class=stu.current_class,
                                        course=course,
                                        subject=stu,
                                    )
                                )

                Result.objects.bulk_create(results)
                return redirect("edit-results")

        # after choosing subjects
        id_list = request.POST.getlist("subjects")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "term": request.current_term,
                }
            )
            subjectlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"subjects": subjectlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didnt select any subject.")
    return render(request, "result/create_result.html", {"subjects": subjects})


@login_required
def edit_results(request):
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        form = EditResults(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})


class ResultListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        bulk = {}

        for result in results:
            test_total = 0
            exam_total = 0
            courses = []
            for course in results:
                if course.subject == result.subject:
                    courses.append(course)
                    test_total += course.test_score
                    exam_total += course.exam_score

            bulk[result.subject.id] = {
                "subject": result.subject,
                "courses": courses,
                "test_total": test_total,
                "exam_total": exam_total,
                "total_total": test_total + exam_total,
            }

        context = {"results": bulk}
        return render(request, "result/all_results.html", context)
