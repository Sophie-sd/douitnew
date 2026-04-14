"""
Management command to populate Russian (_ru) translation fields
for ServicePage, Feature, and FAQ models.

Usage: python manage.py fill_ru_translations
"""
from django.core.management.base import BaseCommand

from apps.services.models import FAQ, Feature, ServicePage

# ---------------------------------------------------------------------------
# Translation data
# ---------------------------------------------------------------------------

PAGES = {
    "internet-mahazyny": {
        "h1_ru": "Разработка интернет-магазинов",
        "hero_subtitle_ru": (
            "Кастомный интернет-магазин — без ежемесячных платежей, "
            "с полным контролем над функционалом и дизайном."
        ),
        "meta_title_ru": "Разработка интернет-магазинов | DOuIT",
        "meta_description_ru": (
            "Кастомный интернет-магазин на Django: без ежемесячных платежей, "
            "с удобной админкой, быстрой загрузкой и интеграцией платёжных систем."
        ),
        "body_intro_ru": (
            "Ваш интернет-магазин — это не шаблон, а полноценная платформа продаж. "
            "Мы создаём магазины, которые работают быстро, конвертируют посетителей "
            "в покупателей и легко масштабируются под рост бизнеса."
        ),
        "process_steps_ru": [
            {
                "title": "Бриф",
                "text": "Анализируем ваш бизнес, конкурентов и целевую аудиторию",
            },
            {
                "title": "Прототип",
                "text": "Создаём структуру сайта и макет ключевых страниц",
            },
            {
                "title": "Разработка",
                "text": "Верстаем и программируем каждую страницу с нуля",
            },
            {
                "title": "Запуск",
                "text": "Тестируем, наполняем контентом и выходим в продакшн",
            },
        ],
    },
    "lendinhy": {
        "h1_ru": "Создание лендингов",
        "hero_subtitle_ru": (
            "Лендинг, заточенный под конверсию — от заголовка до кнопки. "
            "Мгновенная загрузка, UTM-трекинг, готов под рекламу."
        ),
        "meta_title_ru": "Создание лендингов | DOuIT",
        "meta_description_ru": (
            "Кастомные лендинги на Django: мгновенная загрузка, UTM-трекинг, "
            "CRO-оптимизация и высокая конверсия для ваших рекламных кампаний."
        ),
        "body_intro_ru": (
            "Лендинг — это ваш самый эффективный продавец. Мы создаём страницы, "
            "которые загружаются мгновенно, удерживают внимание и превращают клики "
            "из рекламы в реальные заявки."
        ),
        "process_steps_ru": [
            {
                "title": "Бриф",
                "text": "Определяем целевое действие, аудиторию и ключевые преимущества",
            },
            {
                "title": "Копирайт + дизайн",
                "text": "Пишем тексты и создаём визуал под конверсию",
            },
            {
                "title": "Вёрстка",
                "text": "Mobile-first разработка с оптимизацией скорости",
            },
            {
                "title": "Запуск + аналитика",
                "text": "Подключаем трекинг, тестируем и запускаем",
            },
        ],
    },
    "korporatyvni-saity": {
        "h1_ru": "Разработка корпоративных сайтов",
        "hero_subtitle_ru": (
            "Корпоративный сайт, который формирует доверие — быстрый, "
            "современный, с простой админкой на русском языке."
        ),
        "meta_title_ru": "Разработка корпоративных сайтов | DOuIT",
        "meta_description_ru": (
            "Корпоративные сайты на Django: современный дизайн, удобная админка "
            "на русском, SEO из коробки и техническая поддержка после запуска."
        ),
        "body_intro_ru": (
            "Корпоративный сайт — это лицо вашей компании в интернете. "
            "Мы создаём сайты, которые вызывают доверие с первой секунды, "
            "легко обновляются командой и работают на ваш бизнес 24/7."
        ),
        "process_steps_ru": [
            {
                "title": "Анализ",
                "text": "Изучаем компанию, конкурентов и потребности аудитории",
            },
            {
                "title": "Структура",
                "text": "Проектируем архитектуру сайта и навигацию",
            },
            {
                "title": "Разработка",
                "text": "Пишем код с нуля — каждая деталь продумана",
            },
            {
                "title": "Обучение + запуск",
                "text": "Обучаем команду и запускаем",
            },
        ],
    },
}

FEATURES = {
    # ecommerce
    "Каталог товарів": {
        "title_ru": "Каталог товаров",
        "text_ru": "Удобная структура категорий, фильтры, сортировка, поиск.",
    },
    "Кошик та оформлення": {
        "title_ru": "Корзина и оформление",
        "text_ru": "Быстрое оформление заказа без обязательной регистрации.",
    },
    "Оплата онлайн": {
        "title_ru": "Оплата онлайн",
        "text_ru": "LiqPay, Monobank, карты Visa/MasterCard.",
    },
    "Доставка": {
        "title_ru": "Доставка",
        "text_ru": "Интеграция с Новой Почтой, Укрпочтой.",
    },
    "Адмінка українською": {
        "title_ru": "Админка на русском",
        "text_ru": "Добавляйте товары, изменяйте цены — всё на родном языке.",
    },
    "SEO-оптимізація": {
        "title_ru": "SEO-оптимизация",
        "text_ru": "Чистая разметка, мета-теги, Schema.org.",
    },
    # landing
    "CRO-оптимізація": {
        "title_ru": "CRO-оптимизация",
        "text_ru": "Каждый блок продуман с точки зрения конверсии.",
    },
    "Mobile-first": {
        "title_ru": "Mobile-first",
        "text_ru": "Сначала мобильная версия, затем десктоп.",
    },
    "UTM-трекінг": {
        "title_ru": "UTM-трекинг",
        "text_ru": "Автоматическое сохранение UTM-меток.",
    },
    "Форма заявки": {
        "title_ru": "Форма заявки",
        "text_ru": "HTMX-форма без перезагрузки страницы.",
    },
    # corporate
    "Сучасний дизайн": {
        "title_ru": "Современный дизайн",
        "text_ru": "Чистый, профессиональный дизайн под ваш бренд.",
    },
    "Мультисторінковість": {
        "title_ru": "Мультистраничность",
        "text_ru": "Главная, о нас, услуги, команда, контакты.",
    },
    "SEO з коробки": {
        "title_ru": "SEO из коробки",
        "text_ru": "Семантическая разметка, JSON-LD, sitemap.",
    },
    "Безпека": {
        "title_ru": "Безопасность",
        "text_ru": "Наш стек защищает от основных веб-уязвимостей.",
    },
}

FAQS = {
    # ecommerce
    "Скільки часу займає розробка?": {
        "question_ru": "Сколько времени занимает разработка?",
        "answer_ru": (
            "Стандартный интернет-магазин занимает 4–8 недель. "
            "Сроки зависят от количества страниц и требуемого функционала."
        ),
    },
    "Чи можу я сам додавати товари?": {
        "question_ru": "Могу ли я сам добавлять товары?",
        "answer_ru": (
            "Да, для этого предназначена удобная админка на русском языке. "
            "После обучения любой сотрудник сможет самостоятельно управлять каталогом."
        ),
    },
    "Які платіжні системи підтримуєте?": {
        "question_ru": "Какие платёжные системы поддерживаете?",
        "answer_ru": (
            "LiqPay, Monobank, Visa/MasterCard. "
            "Интеграция с другими платёжными системами возможна по запросу."
        ),
    },
    # landing
    "Чим кращий за Tilda, WordPress чи інший конструктор?": {
        "question_ru": "Чем лучше Tilda, WordPress или другого конструктора?",
        "answer_ru": (
            "Кастомный лендинг на Django грузится в 2–5 раз быстрее, "
            "имеет более высокую конверсию, не ограничен шаблоном "
            "и не требует ежемесячных платежей."
        ),
    },
    "Чи підходить для Google Ads?": {
        "question_ru": "Подходит ли для Google Ads?",
        "answer_ru": (
            "Да, все наши лендинги оптимизированы для рекламы: "
            "UTM-трекинг, быстрая загрузка и чистый код повышают Quality Score."
        ),
    },
    "Що входить у вартість від $300?": {
        "question_ru": "Что входит в стоимость от $300?",
        "answer_ru": (
            "Дизайн, вёрстка, форма заявки, UTM-трекинг, адаптивность и базовое SEO. "
            "Точная стоимость зависит от объёма."
        ),
    },
    # corporate
    "Чи можна додати блог?": {
        "question_ru": "Можно ли добавить блог?",
        "answer_ru": (
            "Да, блог можно добавить как отдельный модуль. "
            "Это займёт несколько дней разработки."
        ),
    },
    "Чи буде мобільна версія?": {
        "question_ru": "Будет ли мобильная версия?",
        "answer_ru": (
            "Да, все наши сайты разрабатываются по принципу mobile-first "
            "и отлично выглядят на всех устройствах."
        ),
    },
    "Чи є підтримка після запуску?": {
        "question_ru": "Есть ли поддержка после запуска?",
        "answer_ru": (
            "Да, мы предоставляем техническую поддержку после запуска. "
            "Подробные условия обсуждаются индивидуально."
        ),
    },
}


class Command(BaseCommand):
    help = "Fill Russian translation fields for ServicePage, Feature, and FAQ models"

    def handle(self, *args, **options):
        self._fill_pages()
        self._fill_features()
        self._fill_faqs()
        self.stdout.write(self.style.SUCCESS("Done. All Russian translations applied."))

    def _fill_pages(self):
        for slug, data in PAGES.items():
            try:
                page = ServicePage.objects.get(slug=slug)
            except ServicePage.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"ServicePage slug={slug!r} not found, skipping"))
                continue
            for field, value in data.items():
                setattr(page, field, value)
            page.save()
            self.stdout.write(f"  ServicePage [{slug}]: updated")

    def _fill_features(self):
        updated = 0
        skipped = 0
        for uk_title, data in FEATURES.items():
            qs = Feature.objects.filter(title=uk_title)
            if not qs.exists():
                self.stdout.write(self.style.WARNING(f"  Feature {uk_title!r}: not found"))
                skipped += 1
                continue
            qs.update(**data)
            updated += qs.count()
        self.stdout.write(f"  Features: {updated} updated, {skipped} not found")

    def _fill_faqs(self):
        updated = 0
        skipped = 0
        for uk_question, data in FAQS.items():
            qs = FAQ.objects.filter(question=uk_question)
            if not qs.exists():
                self.stdout.write(self.style.WARNING(f"  FAQ {uk_question!r}: not found"))
                skipped += 1
                continue
            qs.update(**data)
            updated += qs.count()
        self.stdout.write(f"  FAQs: {updated} updated, {skipped} not found")
