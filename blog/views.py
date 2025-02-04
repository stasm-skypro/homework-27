# blog/views.py
import os
import logging
import smtplib

from django.urls import reverse_lazy

from blog.forms import BlogForm
from blog.models import Blog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("blog")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("blog/logs/reports.log", "a", "utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
logger.addHandler(handler)


class BlogListView(ListView):
    """
    Определяет отображение страницы блога.
    """
    model = Blog
    context_object_name = 'blog_list'

    def get_queryset(self):
        return Blog.objects.filter(publicated=True)


class BlogDetailView(DetailView):
    """
    Определяет отображение страницы с содержимым статьи.
    """
    model = Blog

    @staticmethod
    def send_email(login, password, body_text=""):
        """
        Отправляет почту на адрес администратора.
        """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(login, password)
        server.sendmail(login, "stasm226@gmail.com", body_text)
        server.quit()

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1

        # Отправлять уведомление администратору, если количество просмотров превысило 100
        login = os.getenv("SMTP_LOGIN")
        password = os.getenv("SMTP_PASSWORD")
        if self.object.views_counter >= 100:
            self.send_email(
                login=login,
                password=password,
                body_text="Subject: %s\n\n%s"
                          % ("Nobody writes to the colonel",
                             "The number of views increased to %s." % self.object.views_counter),
            )
            logger.info("Количество просмотров превысило %s." % self.object.views_counter)

        self.object.save()

        return self.object


class BlogCreateView(CreateView):
    """
    Определяет отображение страницы добавления статьи.
    """
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        """
        Дополнительная обработка перед сохранением формы.
        """
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Статья '%s' успешно создана." % self.object.title)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обработка в случае неверной формы.
        """
        logger.warning("Ошибка при создании статьи: %s" % form.errors)
        return super().form_invalid(form)


class BlogUpdateView(UpdateView):
    """
    Определяет отображение обновления статьи.
    """
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        """
        Дополнительная обработка перед сохранением формы.
        """
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Статья '%s' успешно обновлена." % self.object.title)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обработка в случае неверной формы.
        """
        logger.warning("Ошибка при обновлении статьи: %s" % form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(DeleteView):
    """
    Определяет отображение удаления статьи.
    """
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def post(self, request, *args, **kwargs):
        """
        Переопределение метода POST для вызова delete.
        """
        logger.info("Удаление статьи через POST-запрос.")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Переопределение метода delete для логирования.
        """
        blog = self.get_object()
        logger.info("Статья '%s' успешно удалена." % blog.title)
        return super().delete(request, *args, **kwargs)
