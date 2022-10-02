
<!-- ABOUT THE PROJECT -->
## О проекте

Проект на Python для считывания данных с Google Sheets в PostgreSQL. Скрипт постоянно обновляет данные по таблице, а так же курса рубля к доллару по ЦБ РФ.
Так же имеется одностраничное web-приложение на Django, для отрисовки графика.

## Начало работы

Ссылка на Google таблицу - https://docs.google.com/spreadsheets/d/18EfHC-K-r1jj-f-Bxb36CZzpycdulmlVJdk82106eNk/edit#gid=0


### Installation

1. Клонировать данный репозиторий 
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. С активированным вирутальный окружением нужно прописать
   ```sh
   pip install -r requirements.txt
   ```
3. Создать проект в https://console.cloud.google.com/welcome?project=test-gs-363914. Далее подключить два API - Google Drive, Google Sheets. 
4. Для получения json файла с тестовыми учетными данными нужно -> "CREATE CREDENTIALS" -> "OAuth client ID" -> "выбрать тип приложения и название токена" -> "Нажать на    кнопку Скачать". 
5. Пропишите данные в env файл, в данном формате:
   ```sh
   POSTGRES_DB_NAME=your_db
   POSTGRES_HOST=127.0.0.1
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=2105
   POSTGRES_PORT=5432
   JSON_FILE_NAME=json_filename
   GOOGLE_SHEET_NAME=test
   GOOGLE_SHEET_LIST_NAME=Лист1
   ```
 




