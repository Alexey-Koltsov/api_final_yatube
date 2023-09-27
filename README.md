#Описание проекта

Проект «API для Yatube» предназначен для отправки постов и комментариев к ним аутентифицированным пользователям. Также аутентифицированный пользователль может подписаться на одного либо нескольких авторов. Авторы постов, комментариев и подписчики имеют возможность редактировать и удалять свой контент. Для неаутентифицированных пользователей доступно только чтение постов и комментариев, а данные подписок недоступны.

#Как запустить проект

##Клонировать репозиторий и перейти в него в командной строке

git clone git@github.com:Alexey-Koltsov/api_final_yatube.git

cd api_final_yatube

##Cоздать виртуальное окружение

Windows

python -m venv venv

##Активировать виртуальное окружение

source venv/Scripts/activate

LinuxmacOS

python3 -m venv venv source venvbinactivate

##Обновить PIP

Windows

python -m pip install --upgrade pip

LinuxmacOS

python3 -m pip install --upgrade pip

##Установить зависимости из файла requirements.txt

pip install -r requirements.txt

##Выполнить миграции

Windows

python manage.py makemigrations

python manage.py migrate

LinuxmacOS

python3 manage.py makemigrations

python3 manage.py migrate

##Запустить проект

Windows

python manage.py runserver

LinuxmacOS

python3 manage.py runserver