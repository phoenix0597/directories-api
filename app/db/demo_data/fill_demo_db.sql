-- Заполнение Организаций
-- Создание корневых элементов
INSERT INTO activities (id, name, parent_id, level)
VALUES (1, 'Еда', NULL, 1),
       (2, 'Автомобили', NULL, 1);

-- Создание подкатегорий для "Еда"
INSERT INTO activities (id, name, parent_id, level)
VALUES (3, 'Мясная продукция', 1, 2),
       (4, 'Молочная продукция', 1, 2);

-- Создание подкатегорий для "Автомобили"
INSERT INTO activities (id, name, parent_id, level)
VALUES (5, 'Грузовые', 2, 2),
       (6, 'Легковые', 2, 2);

-- Создание подкатегорий для "Легковые"
INSERT INTO activities (id, name, parent_id, level)
VALUES (7, 'Запчасти', 6, 3),
       (8, 'Аксессуары', 6, 3);


-- Заполнение Зданий
INSERT INTO buildings (address, location)
VALUES ('Москва, Блюхера 23/1', ST_GeographyFromText('SRID=4326;POINT(37.792803 55.953850)')),
       ('Москва, Зеленоград, Ленина 1', ST_GeographyFromText('SRID=4326;POINT(37.173329 55.978468)'));


-- Заполнение Организаций
INSERT INTO organizations (id, name, building_id, phones)
VALUES (1, '''ООО "Промышленная компания"''', 1, '{"2-222-222","3-333-333","8-929-666-13-13"}'),
       (2, '''ООО "Автопром"''', 2, '{"2-222-222","8-999-777-77-77"}'),
       (3, '''ООО "Рога и Копыта"''', 2, '{"8-999-799-99-99"}'),
       (4, '''ООО "4 копыта и 1 седло"''', 1, '{"5-555-666","8-888-111"}');


-- Заполнение промежуточной таблицы
INSERT INTO organizations_activities (organization_id, activity_id)
VALUES (1, 5),
       (2, 3),
       (3, 3),
       (4, 8),
       (3, 7);