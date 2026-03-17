from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
#from django.template import loader
from .models import Question, Choice
from django.views import generic
from django.utils import timezone
# Create your views here.

class IndexView(generic.ListView):
    #lastest_question_list = Question.objects.order_by("-pub_date")[:5]
    #output=", ".join([q.question_text for q in lastest_question_list])
    #template=loader.get_template("polls/index.html")
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    #try:
    #    question=Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    model = Question
    template_name= "polls/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    #respose = "You are looking the result of question %s"
    model = Question
    template_name= "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.hmtl",
            {
                "question": question,
                "error_message": "No choice selected",
            }
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))