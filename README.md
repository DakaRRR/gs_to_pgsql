
<!-- ABOUT THE PROJECT -->
## О проекте

Проект на Python для считывания данных с Google Sheets в PostgreSQL. Скрипт постоянно обновляет данные по таблице, а так же курса рубля к доллару по ЦБ РФ.
Так же имеется одностраничное web-приложение на Django, для отрисовки графика.

## Начало работы

Ссылка на Google таблицу - https://docs.google.com/spreadsheets/d/18EfHC-K-r1jj-f-Bxb36CZzpycdulmlVJdk82106eNk/edit#gid=0


### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Клонировать данный репозиторий 
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. С активированным вирутальный окружением нужно прописать
  ```sh
  pip install -r requirements.txt
  ```
3. Создать проект в https://console.cloud.google.com/welcome?project=test-gs-363914. Далее подключить два API - Google Drive, Google Sheets. 
4. Для получения json файла с тестовыми учетными данными нужно -> "CREATE CREDENTIALS" -> "OAuth client ID" -> "выбрать тип приложения и название токена" -> "Нажать на      кнопку Скачать". 
5. Пропишите данные в env файл, в данном формате:
   ![image](https://user-images.githubusercontent.com/82327788/193458051-406c3091-710e-4257-86a6-09e64db9e93d.png)
 




