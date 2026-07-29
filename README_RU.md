# 🛒 Фреймворк для автоматизации тестирования PrestaShop (`prestashop-qa`)

[ [English](README.md) ] | [ Русский ] 

[![Статус CI](https://github.com/ruvild/prestashop-qa/actions/workflows/prestashop.yaml/badge.svg)](https://github.com/ruvild/prestashop-qa/actions/workflows/prestashop.yaml)

Контейнеризированный фреймворк для автоматизации тестирования **PrestaShop** (с использованием дополнительного модуля **Binshops** для расширенных возможностей API), объединяющий **UI-, API- и сквозное (E2E) тестирование**. Решение создано с использованием Python, Pytest, Playwright и Docker Compose; оно поддерживает как локальную разработку, так и кросс-браузерное выполнение тестов в пайплайнах CI/CD на базе GitHub Actions. Среда тестирования разворачивается автоматически, что позволяет использовать единый сценарий настройки как при локальном запуске, так и в GitHub Actions.

---

## 💻 Технологический стек

- Python
- Pytest
- Playwright
- Requests
- Pydantic
- Docker и Docker Compose
- GitHub Actions
- PrestaShop 9
---

## 🚧 Статус проекта

- 🟩 **Процесс создания учетной записи** — *Готово (UI и API)*
- 🟩 **Аутентификация / Вход в систему** — *Готово (Гибрид UI/API)*
- 🚧 **Навигация по главной странице** — *В процессе / Запланировано*
- 🚧 **Просмотр товаров и поиск** — *В процессе / Запланировано*
- 🚧 **Полный процесс оформления заказа (Checkout)** — *В процессе / Запланировано*

---

## 🏗️ Архитектура и ключевые особенности

* **Изолированная контейнерная среда:** Автоматический запуск локальных контейнеров PrestaShop и MySQL с помощью `compose.yaml`.
* **Гибридная стратегия тестирования:** Сочетание быстрой проверки подготовки и очистки данных через API (с использованием моделей/схем Pydantic) и глубокой автоматизации UI с применением паттерна Page Object Model (POM).
* **Параллельное и кросс-браузерное выполнение:** Поддержка одновременного запуска тестов в браузерах Chromium, Firefox и WebKit с помощью `pytest-xdist`.
* **Автоматизированный CI/CD:** Пайплайн GitHub Actions использует кэширование зависимостей Playwright и автоматический сбор артефактов (скриншоты при сбоях, логи сервера и HTML-отчеты). Набор тестов запускается автоматически при каждом push-событии или создании pull-запроса с помощью GitHub Actions.

![Запуск конвейера GitHub Actions](docs/assets/ci_pipeline_steps.png)

*Рисунок 1: Автоматизированный запуск тестов в различных браузерах и сбор артефактов в GitHub Actions.*

---

## 📂 Структура репозитория

```text
prestashop-qa/
├── .github/workflows/
│   └── prestashop.yaml         # Определение конвейера CI/CD для GitHub Actions
├── clients/                    # API-клиенты и обертки для HTTP-сессий
├── config/                     # Вспомогательные утилиты, константы и матрицы прав доступа к API
├── docs/assets/                # Изображения для README
├── factories/                  # Генераторы тестовых данных
├── models/                     # Модели данных для полей форм UI
├── pages/                      # Реализация паттерна Page Object Model (POM)
├── schemas/                    # Схемы Pydantic для валидации ответов API
├── scripts/                    # Скрипты подготовки окружения и инициализации API-клиентов
├── tests/                      # Модули UI- и API-тестов, тестовые данные и фикстуры
├── .gitignore                  # Правила отслеживания файлов в Git
├── compose.yaml                # Конфигурация контейнеров PrestaShop и MySQL
├── conftest.py                 # Глобальные фикстуры Pytest, автонастройка для CI и OAuth-токены
├── pytest.ini                  # Флаги Pytest, настройки отчетов HTML и правила запуска
└── requirements.txt            # Зависимости Python
```
# 🛠️ Предварительные требования и настройка

## Требования

- Python **3.14** (или **3.11+**)
- Docker Engine **29.0+**
- Docker Compose **v5.0+**

## 1. Установка

Клонируйте репозиторий и установите зависимости:

```bash
git clone https://github.com/ruvild/prestashop-qa.git
cd prestashop-qa

pip install -r requirements.txt
```

## 2. Подготовка окружения

Фреймворк включает скрипт автоматической настройки, который:

- Запускает контейнеры Docker.
- Ожидает завершения инициализации PrestaShop.
- Автоматически отключает обязательную проверку HTTPS/TLS для Admin API в режиме отладки. Для подготовки окружения локально создайте небольшой вспомогательный скрипт:

```python
from scripts.setup_environment import ensure_environment

if __name__ == "__main__":
    ensure_environment()
```

Сохраните его под именем `local_env_setup.py`, а затем выполните команду:

```bash
python local_env_setup.py
```

> **Примечание:** В средах CI файл `conftest.py` автоматически обнаруживает переменную `CI=true` и запускает `ensure_environment()` во время выполнения `pytest_configure()`, поэтому ручная настройка не требуется.

---

# 🧪 Запуск тестов

После подготовки окружения запустите набор тестов, используя стандартные команды `pytest`.

## Стандартный локальный запуск

```bash
pytest
```

## Параллельный запуск

```bash
pytest -n auto
```

## Запуск тестов в конкретном браузере

```bash
pytest --browser chromium
```

## HTML-отчеты о тестировании

HTML-отчеты генерируются автоматически по следующему пути:

```text
reports/report.html
```

согласно настройкам в файле `pytest.ini`.

![HTML-отчет Pytest](docs/assets/html_report_preview.png)

*Рисунок 2: Автономный HTML-отчет о выполнении, отображающий статистику успешных/неудачных тестов и время их выполнения.*

---

# 🐛 Обнаруженные и зарегистрированные дефекты

В процессе разработки был выявлен ряд дефектов, которые были отправлены в официальные репозитории [PrestaShop](https://github.com/PrestaShop/PrestaShop) и [Binshops Plugin](https://github.com/binshops/prestashop-rest). Соответствующие тесты сохранены в данном проекте как регрессионные тесты с использованием `pytest.mark.xfail` там, где это уместно.

* 🐛 [#42129](https://github.com/PrestaShop/PrestaShop/issues/42129) — Различия в правилах для паролей между UI и API
* 🐛 [#42130](https://github.com/PrestaShop/PrestaShop/issues/42130) — Возможность создания клиента с привязкой к несуществующей группе
* 🐛 [#42131](https://github.com/PrestaShop/PrestaShop/issues/42131) — Несогласованность регистра ключей в различных JSON-ответах
* 🐛 [#42132](https://github.com/PrestaShop/PrestaShop/issues/42132) — Несогласованная обработка пробельных символов
* 🐛 [#42133](https://github.com/PrestaShop/PrestaShop/issues/42133) — В описании именных полей на странице регистрации дефис не указан как допустимый символ
* 🐛 [#55](https://github.com/binshops/prestashop-rest/issues/55) — Сбой эндпоинта входа в PrestaShop 9.2.0

> 🔗 **Посмотреть все отправленные отчеты:** [Трекер задач PrestaShop](https://github.com/PrestaShop/PrestaShop/issues?q=is%3Aissue+author%3Aruvild)