**Vinyl Tracker**  
Веб-приложение для учета, анализа и оценки вашей коллекции виниловых пластинок. Позволяет отслеживать стоимость, жанровое распределение и получать подробную статистику по коллекции. 

**Ссылка на рабочий проект**: https://vinyl-tracker-keai.onrender.com (юзер с тестовыми данными:demo_user, пароль: parol123)  

**Стек технологий**
* Backend: Python 3.11, Django 4.2
* Database: SQLite (Dev), PostgreSQL (Prod)
* Analytics: Django ORM (расчет и фильтрация), Pandas (подготовка данных для графиков), Plotly (отрисовка графиков)
* Frontend: HTML5, CSS  

**Интерфейс**  
Папка со всеми скриншотами: https://drive.google.com/drive/folders/1HyYkjlNo6eWaEUcTBd95FpQFtPbpuKxy?usp=sharing
1. Список коллекции  
   Здесь можно увидеть все элементы коллекции  
   https://drive.google.com/file/d/1-6anyLxVo1wdZMa7aGim2opOs-axWBdY/view?usp=sharing
2. Статистика  
   Распределение пластинок и их средняя стоимость по жанрам и форматам  
   https://drive.google.com/file/d/1ccN5ypgnkhGO085rESao__uoV9c4IqyA/view?usp=sharing  
   https://drive.google.com/file/d/1IO0097Dt0AbfzpQiiVgoMCOyD5KflwZS/view?usp=sharing  
3. 
**Как запустить проект локально**  
1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ваш-юзернейм/ваш-репо.git](https://github.com/ваш-юзернейм/ваш-репо.git)
   ```
2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows
   ```
3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Выполните миграции:**
   ```bash
   python manage.py migrate
   ```
5. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```
6. **Откройте проект в браузере:**
   Перейдите по ссылке: http://127.0.0.1:8000/