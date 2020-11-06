# new_pp_lab4
#Інструкція
#Для запуску проекту потрібно виконати кілька кроків
#Встановити версію python 3.8 через термінал
#Створили віртуальне середовище poetry в папці сховища за допомогою python3 -m poetry та активуйте його за допомогою source poetry/bin/activate
#Встановити  залежності за допомогою наступної команди: pip3 freeze > requirements.txt
Вміст requirements.txt:
click==7.1.2
Flask==1.1.2
gunicorn==20.0.4
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
Werkzeug==1.0.1

#Після цього створюємо Procfile із вмістом:
web: gunicorn app:app

#Перше app - ім'я python-файлу, який запускає додаток, або ім'я модуля, в якому воно знаходиться. Друге app - назва програми, тобто app.py. Цей Procfile працює з gunicorn і Heroku, щоб обслуговувати додаток віддалено.



