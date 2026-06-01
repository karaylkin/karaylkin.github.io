from requests_oauthlib import OAuth2Session
import os
import json

# Разрешаем HTTP для локального тестирования
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Данные приложения
# Вы должны установить эти переменные окружения перед запуском
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"

# Google Endpoints
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

# Scope: запрашиваем email и профиль
SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

if not CLIENT_ID or not CLIENT_SECRET:
    print("Ошибка: Не заданы переменные окружения GOOGLE_CLIENT_ID или GOOGLE_CLIENT_SECRET.")
    exit(1)

# 1. Создание сессии
# ВАЖНО: access_type="offline" и prompt="consent" обязательны для получения refresh_token
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
authorization_url, state = oauth.authorization_url(
    AUTHORIZATION_BASE_URL,
    access_type="offline",
    prompt="consent"
)

print("1. Перейдите по ссылке для авторизации:", authorization_url)

# 2. Получение кода от пользователя
redirect_response = input("2. Вставьте полный URL перенаправления: ")

# 3. Обмен кода на токены
try:
    token = oauth.fetch_token(
        TOKEN_URL,
        authorization_response=redirect_response,
        client_secret=CLIENT_SECRET
    )
except Exception as e:
    print(f"Ошибка при получении токена: {e}")
    exit(1)

print("\n--- ПОЛУЧЕННЫЕ ТОКЕНЫ ---")
print(json.dumps(token, indent=2))

# 4. Проверка доступа к ресурсу
print("\n--- ЗАПРОС ДАННЫХ ПОЛЬЗОВАТЕЛЯ ---")
try:
    r = oauth.get("https://www.googleapis.com/oauth2/v1/userinfo")
    print("Данные:", json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Ошибка запроса: {e}")

# 5. Демонстрация обновления токена (Refresh Token Flow)
if 'refresh_token' in token:
    print("\n--- ДЕМОНСТРАЦИЯ ОБНОВЛЕНИЯ ТОКЕНА (REFRESH) ---")
    print(f"Используем refresh_token: {token['refresh_token'][:10]}...")
    
    # Для обновления токена нам снова нужны client_id и client_secret
    extra = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    try:
        # refresh_token() автоматически обновляет access_token в сессии
        new_token = oauth.refresh_token(TOKEN_URL, refresh_token=token['refresh_token'], **extra)
        
        print("\nТокен успешно обновлен!")
        print(json.dumps(new_token, indent=2))
        
        # Проверяем, что новый токен работает
        print("\n--- ПОВТОРНЫЙ ЗАПРОС ДАННЫХ (С НОВЫМ ТОКЕНОМ) ---")
        r = oauth.get("https://www.googleapis.com/oauth2/v1/userinfo")
        print("Данные:", json.dumps(r.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Ошибка при обновлении токена: {e}")
else:
    print("\nВнимание: refresh_token не получен. Убедитесь, что вы используете access_type='offline' и prompt='consent'.")
