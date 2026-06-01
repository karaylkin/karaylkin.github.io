from requests_oauthlib import OAuth2Session
import os
import json

# Для локальной разработки разрешаем HTTP (иначе oauthlib требует HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# 2. Сохраните полученные из регистрационной формы значения:
# Примечание: Для запуска вам нужно установить переменные окружения CLIENT_ID и CLIENT_SECRET
# или временно вставить их прямо сюда (не рекомендуется для продакшена).
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
SCOPE = ["read:user"] # выберите необходимые scopes

if not CLIENT_ID or not CLIENT_SECRET:
    print("Ошибка: Не заданы переменные окружения CLIENT_ID или CLIENT_SECRET.")
    print("Вы можете задать их в терминале перед запуском:")
    print("$env:CLIENT_ID='ваш_id'; $env:CLIENT_SECRET='ваш_secret'; python oauth_client.py")
    exit(1)

# 3. Создайте сессию OAuth и сформируйте URL авторизации:
# Включает response_type=code, client_id, redirect_uri и scope.
# Параметр state используется для предотвращения CSRF.
oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
print("Перейдите по ссылке для авторизации:", authorization_url)

# 4. Запустите скрипт. Откройте полученный URL в браузере...
# 5. После подтверждения провайдер перенаправит браузер на ваш redirect_uri.
redirect_response = input("Вставьте полный URL перенаправления: ")

# Обмен авторизационного кода на access token
# requests-oauthlib автоматически обрабатывает code из URL
token = oauth.fetch_token(
    TOKEN_URL,
    authorization_response=redirect_response,
    client_secret=CLIENT_SECRET
)
print("Токен:", json.dumps(token, indent=2, ensure_ascii=False))

# 6. Используйте полученный token для запроса защищённого ресурса
# В запросе используется заголовок Authorization: Bearer <TOKEN>
r = oauth.get("https://api.github.com/user")
print("Ваши данные:", json.dumps(r.json(), indent=2, ensure_ascii=False))
