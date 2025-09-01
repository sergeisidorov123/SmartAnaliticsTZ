**Здравствуйте!**

Чтобы запустить проект, нужно воспользоваться х-сервером, т.к. докер не может открыть gui на рабочем экране.
Я пользовался :  https://github.com/marchaesen/vcxsrv

Если что, проект запускался на 15 версии постгреса(чтобы не было конфликта версий, если есть нужда запустить проект без докера )

Ответы на задания по SQL:
1.Какие поля вы бы выбрали для задания первичного ключа в нижеприведённой таблице? Объясните выбор.	

<img width="527" height="196" alt="image" src="https://github.com/user-attachments/assets/e35c8ca6-e8e9-4d33-9301-5a86597eeeb6" />

В качестве первичного ключа резонно использовать только **CityID**, т.к. во-первых оно не null, во-вторых айди города как раз таки должен быть уникальным. Все остальные поля,
кроме location - не могут быть уникальны, а поле location - может быть null, поэтому тоже не подходит.
Поле cityname - не всегда уникально, т.к. существует множество городов с одинаковым названием
Поля CountryID и StateProvinceID - так же не подходят, т.к. страны и регионы имеют в своем составе много городов
Поле LatestRecordedPopulation - так же не может быть, т.к. есть вероятность совпадение этого числа в нескольких городах. 

Ответ: **CityID**

2. Таблица Orders содержит список заказов, в котором SalespersonPersonID – продавец, CustomerID – покупатель, а OrderDate – дата заказа.	
Напишите запрос, который вернёт список продавцов, оформивших заказы в 2013 году и количество заказов, оформленных каждым продавцом. Формат результата запроса: SalespersonPersonID, OrderCount.

<img width="481" height="358" alt="image" src="https://github.com/user-attachments/assets/fba2a0b4-e706-4933-9409-5c9686293252" />

SELECT SalespersonPersonID, COUNT(*) AS OrderCount FROM Sales.Orders 
WHERE YEAR(OrderDate) = 2013
GROUP BY SalespersonPersonID

3. Таблица OrderLines содержит список товаров каждого заказа, где UnitPrice – цена единицы товара, а Quantity – их количество. OrderLines связана с Orders по OrderID.	
Напишите запрос, который вернёт список заказов, покупателя, а также полную стоимость заказа. 
Результат должен содержать только заказы с полной стоимостью более 25000 и быть упорядоченным по убыванию этой величины. Формат результата: OrderID, CustomerID, TotalCost.	

<img width="442" height="153" alt="image" src="https://github.com/user-attachments/assets/66146612-cb59-4a0c-a915-15eadad72ecf" />

SELECT o.OrderID, o.CustomerID, SUM(ol.UnitPrice * ol.Quantity) AS TotalCost FROM Sales.Orders o
JOIN Sales.OrderLines ol ON o.OrderID = ol.OrderID
GROUP BY o.OrderID, o.CustomerID
HAVING SUM(ol.UnitPrice * ol.Quantity) > 25000
ORDER BY TotalCost DESC

Так же мой sql-academy(задачки по sql, которые я решал, если интересно посмотреть): https://sql-academy.org/ru/profile/6873f592f84ed9002956ea68
