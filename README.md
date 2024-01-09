Отправка и обновление товаров в Тильда по протоколу commerceml

Программа отладочная. Ничего не автоматизировано.
Для синхронизации используются 2 xml файла для демонтсрации отправления товара,
третий файл пример того, как можно выгружать фотографии отдельно.

Для проверки нужно указать url, login и password
Шаги расставляются в соответствии с последовательностью запросов

Авторизация:
('get', 'catalog', 'checkauth', '', ''),                   ?type=catalog&mode=checkauth
('get', 'catalog', 'init', '', ''),                        ?type=catalog&mode=init

Загрузка на сервер файлов 3 позиция - какой файл, 4 позиция - передать с каким именем
('post', 'catalog', 'file', '12345.png', '12345.png')      ?type=catalog&mode=file&filename=12345.png
('post', 'catalog', 'file', 'import.xml', 'import.xml'),   ?type=catalog&mode=file&filename=import.xml
('post', 'catalog', 'file', 'offers.xml', 'offers.xml'),   ?type=catalog&mode=file&filename=offers.xml

Команды для обработки файлов
('get', 'catalog', 'import', 'import.xml', ''),            ?type=catalog&mode=import&filename=import.xml
('get', 'catalog', 'import', 'offers.xml', ''),            ?type=catalog&mode=import&filename=offers.xml


Блоки выполнения запросов должны соответствовать шагам
