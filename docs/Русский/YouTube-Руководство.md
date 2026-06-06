# Руководство по YouTube

Это руководство помогает новым пользователям настроить приложение `YouTube` с нуля.

## 1. Что показывает приложение

Приложение показывает публичные данные канала:

1. Название канала
2. Аватар
3. Количество подписчиков
4. Общее число просмотров
5. Общее число видео

Приложение использует только публичные данные. Оно не входит в ваш аккаунт YouTube.

## 2. Что нужно подготовить

Нужно подготовить:

1. `Channel Ref`
2. Ключ `YouTube Data API v3`

Также проверьте:

1. Устройство подключено к сети
2. Вы можете открыть `settings.html`

## 3. Что такое Channel Ref

Устройство поддерживает:

1. Channel ID
2. `@handle`
3. username

Примеры:

```text
UCxxxxxxxxxxxxxxxxxxxxxx
@openai
some_channel_name
```

Лучше всего использовать:

1. Channel ID, который начинается с `UC...`
2. `@handle`

## 4. Как получить API Key

В Google Cloud Console:

1. Войдите в аккаунт
2. Создайте или выберите проект
3. Включите `YouTube Data API v3`
4. Создайте API key
5. Скопируйте ключ

Полезные ссылки:

1. Создать API key: <https://console.cloud.google.com/apis/credentials>
2. Официальная инструкция: <https://developers.google.com/youtube/registering_an_application>

## 5. Настройка на странице устройства

На странице `YouTube` заполните:

### Channel Ref

Например:

```text
@yourhandle
```

или

```text
UCxxxxxxxxxxxxxxxxxxxxxx
```

### API Key

Вставьте ваш ключ YouTube Data API v3.

### Refresh Interval

Рекомендуемое значение:

```text
60
```

## 6. Сохранить и проверить

Рекомендуемый порядок:

1. Нажмите `Open This App`
2. Заполните `Channel Ref`
3. Заполните `API Key`
4. Нажмите `Save YouTube`
5. Нажмите `Reload YouTube`

## 7. Как работает кэш

Теперь приложение поддерживает кэш.

Это значит:

1. Если раньше данные уже были успешно загружены
2. Приложение может сначала показать кэш
3. Потом оно обновит данные в фоне

Типичные статусы:

1. `Cached just now`
2. `Cached · updated 25s ago`
3. `Live`
4. `Live · updated 25s ago`

## 8. Частые проблемы

### `Set channel and API key`

Настройка заполнена не полностью.

### `Wi-Fi offline`

Устройство сейчас не в сети.

### `HTTP xxx`

Обычно это значит:

1. Неверный API key
2. API не включен
3. Проблема с квотой проекта
4. Неверный Channel Ref
