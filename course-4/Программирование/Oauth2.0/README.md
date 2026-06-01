# Лабораторная работа: Практика OAuth 2.0 в Python

## Цели
*   Познакомиться с концепциями OAuth 2.0 (роли, токены, scopes).
*   Реализовать поток **Authorization Code** (на примере GitHub).
*   Реализовать поток **Authorization Code с Refresh Token** (на примере Google).

## Подготовка окружения

Для работы требуется Python 3.11+ и установленные зависимости.

```powershell
# 1. Создание виртуального окружения
python -m venv venv

# 2. Активация (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Установка зависимостей
pip install requests requests-oauthlib
```

---

## Часть 1. GitHub: Authorization Code Flow

В этой части мы реализуем базовый поток получения доступа к данным пользователя GitHub.

### 1. Регистрация приложения
1.  Перейдите в [GitHub Developer Settings -> OAuth Apps](https://github.com/settings/developers).
2.  Нажмите **New OAuth App**.
3.  Заполните форму:
    *   **Application name**: `Python OAuth Lab`
    *   **Homepage URL**: `http://localhost:8000`
    *   **Authorization callback URL**: `http://localhost:8000/callback`
4.  Скопируйте **Client ID**.
5.  Сгенерируйте и скопируйте **Client Secret**.

### 2. Запуск скрипта
Используйте скрипт `oauth_client.py`. Замените значения на свои:

```powershell
$env:CLIENT_ID = "ВАШ_GITHUB_CLIENT_ID"
$env:CLIENT_SECRET = "ВАШ_GITHUB_CLIENT_SECRET"
.\venv\Scripts\python.exe oauth_client.py
```

### 3. Ожидаемый результат
1.  Скрипт выведет ссылку авторизации. Откройте её в браузере.
2.  Разрешите доступ приложению.
3.  Вас перенаправит на `localhost`. Скопируйте **полный URL** из адресной строки (даже если страница не открылась).
4.  Вставьте URL в консоль.
5.  Скрипт выведет:
    *   Ваш **Access Token**.
    *   JSON с данными вашего профиля GitHub.

#### Пример вывода (GitHub):
```json
Токен: {
  "access_token": "(здесь могла быть ваша реклама)",
  "token_type": "bearer",
  "scope": [
    "read:user"
  ]
}
Ваши данные: {
  "login": "Daniyarsick",
  "id": 124454981,
  "avatar_url": "https://avatars.githubusercontent.com/u/124454981?v=4",
  "html_url": "https://github.com/Daniyarsick",
  "type": "User",
  "name": null,
  "plan": {
    "name": "pro",
    "space": 976562499,
    "collaborators": 0,
    "private_repos": 9999
  }
}
```

---

## Часть 2. Google: Refresh Token Flow

В этой части мы реализуем получение `refresh_token` для обновления доступа без участия пользователя.

### 1. Настройка Google Cloud
1.  Создайте проект в [Google Cloud Console](https://console.cloud.google.com/).
2.  **OAuth Consent Screen**:
    *   User Type: **External**.
    *   Scopes: `userinfo.email`, `userinfo.profile`, `openid`.
    *   **Test users**: Обязательно добавьте свой email!
3.  **Credentials**:
    *   Create Credentials -> **OAuth client ID** -> **Web application**.
    *   **Authorized redirect URIs**: `http://localhost:8000/callback`
4.  Скопируйте **Client ID** и **Client Secret**.

### 2. Запуск скрипта
Используйте скрипт `google_oauth_client.py`.

```powershell
$env:GOOGLE_CLIENT_ID = "ВАШ_GOOGLE_CLIENT_ID"
$env:GOOGLE_CLIENT_SECRET = "ВАШ_GOOGLE_CLIENT_SECRET"
.\venv\Scripts\python.exe google_oauth_client.py
```

### 3. Ожидаемый результат
1.  Перейдите по ссылке. Если Google предупреждает о непроверенном приложении, нажмите **Advanced -> Go to ... (unsafe)**.
2.  Разрешите доступ.
3.  Скопируйте URL перенаправления в консоль.
4.  Скрипт покажет:
    *   **Access Token** и **Refresh Token**.
    *   Данные пользователя.
    *   Сообщение об успешном обновлении токена (`refresh_token` flow).
    *   Повторный запрос данных с новым токеном.

#### Пример вывода (Google):
```json
--- ПОЛУЧЕННЫЕ ТОКЕНЫ ---
{
  "access_token": "(здесь могла быть ваша реклама)",
  "expires_in": 3599,
  "refresh_token": "(здесь могла быть ваша реклама)",
  "scope": [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
  ],
  "token_type": "Bearer"
}

--- ЗАПРОС ДАННЫХ ПОЛЬЗОВАТЕЛЯ ---
Данные: {
  "id": "104820385612792685486",
  "email": "dan.annanurov@gmail.com",
  "verified_email": true,
  "name": "Даниил Аннануров",
  "picture": "https://lh3.googleusercontent.com/a/ACg8ocJZgmNgfyqsXtBpjHPoNyOF4uKt549vt58r4BAcnQQr_d0pIWBtEw=s96-c"
}

--- ДЕМОНСТРАЦИЯ ОБНОВЛЕНИЯ ТОКЕНА (REFRESH) ---
Используем refresh_token: 1//09WGuCn...

Токен успешно обновлен!
{
  "access_token": "(здесь могла быть ваша реклама)",
  "expires_in": 3599,
  "scope": [
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile"
  ],
  "token_type": "Bearer"
}
```

---

## Файлы проекта
*   `oauth_client.py` — Клиент для GitHub.
*   `google_oauth_client.py` — Клиент для Google (с поддержкой Refresh Token).
*   `README.md` — Данная инструкция.
