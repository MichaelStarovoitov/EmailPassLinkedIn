import requests
from bs4 import BeautifulSoup
from data.paths import resultFilePath, screenSot
email = 'nefarionys@gmail.com'
password = '8ce3C161'

login_page_url = 'https://www.linkedin.com/checkpoint/lg/sign-in-another-account?trk=guest_homepage-basic_nav-header-signin'
session = requests.Session()
soup = BeautifulSoup(session.get(login_page_url).text, 'html.parser')
csrf_token = None
for input_tag in soup.find_all('input'):
    if input_tag.get('name') == 'loginCsrfParam':
        csrf_token = input_tag.get('value')
        break

cookies = session.cookies.get_dict()
post_url = 'https://www.linkedin.com/checkpoint/lg/login-submit'
data = {
    'session_key': email, 
    'session_password': password,  
    'loginCsrfParam': csrf_token,
    'authUUID': cookies.get('authUUID', ''),  
    'pageInstance': cookies.get('pageInstance', ''),  
    'trk': cookies.get('trk', ''),
    'parentPageKey': cookies.get('parentPageKey', ''),  
    'fp_data': cookies.get('fp_data', ''), 
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': login_page_url,
}

response = session.post(post_url, data=data, headers=headers , allow_redirects=False)

if response.status_code == 303:
    redirect_url = response.headers.get('Location')
    if redirect_url:
        redirect_url = requests.compat.urljoin(login_page_url, redirect_url)
        redirect_response = session.get(redirect_url)
    else:
        print("No Location header found for redirect.")

# =====================================================================================================================

session_url = "https://www.linkedin.com/checkpoint/challenge/funCaptchaInternal"
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    "Referer": "https://www.linkedin.com",
    # другие заголовки, если необходимо
}
response = requests.get(session_url, headers=headers)

print(response.status_code)
print(response.url)
with open(f'{resultFilePath}\\test.html', 'w', encoding='utf-8') as file:
    file.write(response.text)
# print(response.text)

# # Допустим, что данные sessionToken и gameToken возвращаются в JSON-ответе
# # Хотя на практике они могут быть частью HTML или скрипта, который придется анализировать
# data = response.json()
# session_token = data.get("sessionToken")
# game_token = data.get("gameToken")

# # Шаг 2: Получение изображения капчи
# captcha_url = "https://client-api.arkoselabs.com/rtig/image"
# captcha_params = {
#     "challenge": "0",
#     "sessionToken": session_token,
#     "gameToken": game_token
# }
# captcha_response = requests.get(captcha_url, params=captcha_params)

# # Проверка, успешно ли получено изображение капчи
# if captcha_response.status_code == 200:
#     # Сохранение изображения капчи в файл
#     with open(screenSot, "wb") as file:
#         file.write(captcha_response.content)
#     print("Изображение капчи сохранено как 'captcha_image.png'.")
# else:
#     print("Ошибка при получении изображения капчи:", captcha_response.status_code)