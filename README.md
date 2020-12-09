#1)Скачуємо  alembic library своїм віртуальним середовищем, у моєму випадку: poetry install alembic

#2)Робимо в своїй рут директорії ініціалізацію: alembic init alembic(отримаємо папку з alembic файлами
)
#3)У файлі alembic.ini, а саме у строці sqlalchemy.url, прописуємо шлях до нашої бд(приклад: postgresql://username:password@localhost:5432/name_of_db)

#Якщо все зроблено правильно, то ми законектились до нашої бд

#4)Створюємо файл models.py і там прописуємо наші models

#5)Потім в згенерованому файлі env.py робимо імпорт Base з цього файлу
#sys.path = ['', '..'] + sys.path[1:]
#from Base import Base
#target_metadata = Base.metadata
#(Замінили target_metadata=None на target_metadata = Base.metadata )

#6)Ранимо наш скрипт alembic revision --autogenerate, згенерується файл з апгрейд і даунгрейд функцією

#7)Після всіх виконаних пунктів, отримуємо наші сутності в бд


#Щоб відкотити дб на 1 крок назад ранимо: alembic downgrade -1
#Щоб апгрейднути усі зміни, ранимо alembic upgrade head
