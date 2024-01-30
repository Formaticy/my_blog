from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    """
    Класс для того, чтобы sitemap включал все ссылки до каждого нашего поста
    """
    changefreq = 'weekly'  # Вероятная частота изменения страницы постов (для сканера поисковой системы это как подсказка, а не как команда)
    priority = 0.9  # Релевантность URL на сайте относительно других URL на сайте (макс = 1)

    def items(self):
        """
        Возвращает набор запросов QuerySet объектов, подлежащих включению в эту карту сайта.
        По умолчанию джанго вызвает get_absolute_url() по каждому объекту, чтобы получить его URL адрес
        """
        return Post.published.all()

    def lastmod(self, obj):
        """
        Дата datetime последнего изменения файла (определение по документации).
        Получает каждый возвращаемый items объект и возвращает время последнего изменение объекта
        """
        return obj.updated
