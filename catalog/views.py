"""
Контроллеры, определённые внутри приложения catalog.
"""

import logging
import os
import smtplib

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from dotenv import load_dotenv

from catalog.forms import CategoryForm, ProductForm
from catalog.models import Category, Product

load_dotenv()

logger = logging.getLogger("catalog")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("catalog/logs/reports.log", "a", "utf-8")
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
)
logger.addHandler(handler)


# ---- Определяем набор CRUD-операций для модели Category ----
#
class CategoryCreateView(CreateView):
    """
    Определяет отображение добавления категории.
    """

    model = Category
    context_object_name = "category"
    form_class = CategoryForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """
        Дополнительная обработка перед сохранением формы.
        """
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Категория продукта '%s' успешно создана." % self.object.name)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обработка в случае неверной формы.
        """
        logger.warning("Ошибка при создании категории продукта: %s" % form.errors)
        return super().form_invalid(form)


# ---- Определяем набор CRUD-операций для модели Product ----
#
class ProductListView(ListView):
    """
    Определяет отображение страницы со списком продуктов.
    """

    model = Product
    context_object_name = "product_list"


class ProductDetailView(DetailView):
    """
    Определяет отображение детализации (характеристик) продукта.
    """

    model = Product
    context_object_name = "product"

    @staticmethod
    def send_email(login: str | None, password: str | None, body_text: str = ""):
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
                % (
                    "Nobody writes to the colonel",
                    "The number of views increased to %s." % self.object.views_counter,
                ),
            )
            logger.info(
                "Количество просмотров превысило %s." % self.object.views_counter
            )

        self.object.save()

        return self.object


class ProductCreateView(CreateView):
    """
    Определяет отображение добавления продукта.
    """

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """
        Дополнительная обработка перед сохранением формы.
        """
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Продукт '%s' успешно создан." % self.object.product)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обработка в случае неверной формы.
        """
        logger.warning("Ошибка при создании продукта: %s" % form.errors)
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    """
    Определяет отображение обновления продукта.
    """

    model = Product
    # fields = "__all__"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        """
        Дополнительная обработка перед сохранением формы.
        """
        self.object = form.save()  # Сохраняем объект формы в базу
        logger.info("Продукт '%s' успешно обновлён." % self.object.product)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Обработка в случае неверной формы.
        """
        logger.warning("Ошибка при обновлении продукта: %s" % form.errors)
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    """
    Определяет отображение удаления продукта.
    """

    model = Product
    form_class = ProductForm
    context_object_name = "product"
    success_url = reverse_lazy("catalog:product_list")

    def post(self, request, *args, **kwargs):
        """
        Переопределение метода POST для вызова delete.
        """
        logger.info("Удаление продукта через POST-запрос.")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Переопределение метода delete для логирования.
        """
        product = self.get_object()
        logger.info("Продукт '%s' успешно удалён." % product.product)
        return super().delete(request, *args, **kwargs)
