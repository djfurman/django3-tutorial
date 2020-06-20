from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from .models import Question, Choice


def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]

    context = {"latest_question_list": latest_questions}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selection = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice"},
        )
    else:
        selection.votes += 1
        selection.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
