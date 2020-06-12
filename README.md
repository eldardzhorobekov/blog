# blog
Реализация блога с подписками на Django



## Как запустить проект

Установить docker, docker-compose
Скачать репозиторий
В корне репозитория ввести команды:
  sudo docker build
  sudo docker-compose up



### Чтобы работала отправка сообщений

Остановить проект

В файле docker-compose.yml изменить следующие поля на свою почту:
  EMAIL_HOST_USER
  EMAIL_HOST_PASSWORD

Перезапустить проект