[ТОЛЬКО README ИЗМЕНЕН ПОСЛЕ ДЕДЛАЙНА]
Версия в соответствии с дедлайном: https://github.com/dingaidarbek/incubator/tree/a419fda2dd8e38c5fc8b30645cbccb08df500691


# **Репозиторий для 8 задания**

Ссылка на сайт: https://dingaidarbek.vercel.app/


# **Документация**

## **Процесс проектирования**

Будучи знакомым с HTML, CSS, JavaScript и Python по отдельности, но не имея полноценного опыта разработки вебсайтов, я решил просмотреть Интернет для поиска подходящего мне стека. Я остановился на двух фреймворках: Flask и Django. 
Как было описано, Flask является очень хорошим инструментом для подобных маленьких проектов, который я создавал. И я это очень сильно почувствовал на практике, сравнивая его с Django.
Попробовав оба и взвесив все плюсы и минусы, о которых писали в Интернете, я решил что буду работать над приложением с использованием Flask.

Начал я с исследования двух гигантов: Spotify и Apple Music.

У них была похожая структура сайта: боковое меню слева и основное справа:
![image](https://github.com/dingaidarbek/incubator/assets/143844447/c179125e-429f-455b-b2aa-8bb2200bb24a)
![image](https://github.com/dingaidarbek/incubator/assets/143844447/b40f00be-0d8d-4490-86e1-e2d14316c8bf)

Поэтому, я решил создать похожий дизайн.

## **Процесс разработки**
Так как это мой первый опыт, в процессе я столкнулся со некоторыми проблемами, которые мне приходилось решать по ходу обучения. Главной из них было подключение Spotify API к проекту.
В процессе устранения проблем в работе с API напрямую, я наткнулся на библиотеку, которая позволяет работать со Spotify API намного легче. Поэтому, было решено возложить работу с API именно на эту библиотеку (spotipy).

После подключения данной библиотеки, работа пошла намного быстрее.

В целом, разработка шла поэтапно: сначала я создал HTML темплейты для всех страниц, а уже затем создавал функционал. С частью, которая была мне уже знакома, существенных проблем не возникало.

## **Дизайн сайта**
Я решил оставить минималистический дизайн, так как front часть индивидуальна для каждого - кому то нравится что-то одно, а другим это совершенно не по вкусу. Поэтому, имея минималистический дизайна, это подойдет большинству людей.


## **Найденные ошибки**

Как я уже говорил, я учился всему в процессе разработки и деплой на Vercel также входит туда. Во время разработки я создал JSON файл для хранения там данных пользователей (логин и пароль) и комментариев к альбому. Однако, уже только после завершения работы я обнаружил, что Vercel запрещает изменение любых файлов и что следовало использовать базу данных для таких целей. Поэтому, на Vercel недоступна функция оставления комментариев и регистрации.

Однако, при клонировании репозитория и запуске его на локальном сервере, все работает исправно.

Я не стал модифицировать вебсайт после дедлайна, так как это нечестно по отношению к другим участникам, поэтому оставил всё как есть. Для полной оценки моей работы прошу запускать репозиторий с компьютера.

# **Заключение**
Данный опыт дал мне очень сильный толчок в направлении full-stack web-разработки. Во время работы я заработал себе "шишки", которые помогут мне не совершать те же самые ошибки, которые я совершал, только начав разработку вебсайта. Смотря на результат своей работы, я думаю что это очень хорошее начало для разработки веб приложения, которое было создано с параллельным обучением и путем проб и ошибок. 

Надеюсь, что данная работа, проделанная с нуля и в кратчайшие сроки, будет достойной для дальнейшего развиватия в этой сфере во время Инкубатора.


# **Как запустить приложение на ПК**
1) Установить следующие зависимости (если они не установлены):
pip install Flask;
pip install requests;
pip install datetime;
pip install spotipy;
pip install http.client;
pip install datetime
2) Клонировать репозиторий в папку (git clone)
3) Запустить файл "app.py" (python app.py)
4) Перейти на сайт, который появился в терминале (по умолчанию 127.0.0.1:5000)

**Спасибо**
