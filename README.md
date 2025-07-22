### Hexlet tests and linter status:

[![Actions Status](https://github.com/IvanFoksha/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/IvanFoksha/python-project-83/actions)

# Анализатор страниц

Простое веб-приложение на основе Flask для анализа страниц.

## Деплой

Приложение развернуто на Render.com и доступно по адресу: [https://page-analyzer.onrender.com](https://page-analyzer.onrender.com)

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/IvanFoksha/python-project-83
   ```

2. Установите зависимости

   ```bash
   make install
   ```

3. Запустите в режиме разработки

   ```bash
   make dev
   ```

4. Запустите в режиме продакшена
   ```bash
   make start
   ```

## Переменные окружения

Создайте файл `.env` на освное `.env.example` и установите `SECRET_KEY`.
