from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# Представление для общего списка вопросов
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """возвращает набор данных, содержащий те вопросы,
        у которых pub_date меньше или равна timezone.now."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


# Представление для страницы определенного вопроса
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Исключает вопросы, которые ще не опубликованы.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# Представление отображения результатов голосования
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
Представление для обработки голоса

:param request: объект запроса
:param question_id: id вопроса
:return: объект HttpResponse
"""
def vote(request, question_id):
    # Получаем объект вопроса по первичному ключу или Htttp404
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # Если choice не находится в POST
    except (KeyError, Choice.DoesNotExist):
        # показывает страницу опроса с ошибкой, если не был выбран вариант ответа
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # Мы используем функцию reverse() при создании HttpResponseRedirect.
        # Она принимает название URL-шаблона и необходимые аргументы для создания URL-а.
        # например, reverse() вернет: '/polls/3/results/'
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))