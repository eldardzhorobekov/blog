# Blog
Реализация блога с подписками на Django




## Как запустить проект

  
  Установить docker, docker-compose
  
  
  Скачать репозиторий


  В корне репозитория ввести команды:
      
      
    sudo docker build
    sudo docker-compose up

  


## Чтобы работала отправка сообщений


В файле docker-compose.yml изменить следующие поля на свою почту:
  
  
    EMAIL_HOST_USER=<ваша почта>
    EMAIL_HOST_PASSWORD=<ваш пароль>
    
    
    
##### Сайт в онлайн доступе по [ссылке](https://eldar.pythonanywhere.com)
Чтобы войти: 
        
    Username: test
    Password: test!querty
