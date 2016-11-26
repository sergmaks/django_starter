import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question


def create_question(question_text, days):
    """
    Фабричный метод

    Создает вопрос с заданным `question_text`, публикуемым с заданным
    количеством дней относительно настоящего времени
    (отрицательное значение - для вопросов, опубликованных в прошлом,
    попложительное - для вопросов, которые лоджны быть еще опубликованы)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   pub_date=time)

# Тестрирование представлений
# Наследование от django.test.TestCase
class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        Если вопросов не существует - отображается соотв. сообщение
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Вопросы с pub_date в прошлом должны быть отображены на index-странице
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Вопросы с pub_date, содержащее будущее время, не должны быть отображены на index-странице
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Если существуют вопросы и в прошлом и в будущем,
        отображены должны быть только вопросы из прошлого
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        Главная страница с вопросами может отображать несколько вопросов.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

# Тестирование детального представления вопроса
class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        Детальный вид вопроса с pub_date со значением будущего времени
        должен вернуть 404
        """
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        Детальный вид вопроса с pub_date со значением прошедшего времени
        должен отобразить текст вопроса
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)

# Тестирование модели Question
class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        метод was_published_recently() должен вернуть False для вопроса,
        чей pub_date содержит время в будущем.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        метод was_published_recently() должен вернуть False для вопроса,
        чей pub_date старше одного дня.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        метод was_published_recently() должен вернуть True для вопроса,
        чей pub_date содержит время в рамках последнего дня.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)