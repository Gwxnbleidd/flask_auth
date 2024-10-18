## Задание 2
1. Вам необходимо вывести/вернуть список всех заказчиков (id, локальное имя, тип, актуального руководителя) отсортировав результаты по возрастанию по полям:
   - типу лица;
   - в алфавитном порядке по локальным именам;
   - только рабочих заказчиков.

```sql

select  id, internal_name, person, heads 
from counterparties.counterparties
where active = True
order by person, internal_name

```

2. Необходимо вывести/вернуть список банков определенного заказчика (по его уникальному полю)

Вернем заказчика с id = 4 (тот, у которого два банка): <br>

``` sql

select t.key as banks  
from jsonb_each (
(select c.banks as banks  
 FROM counterparties.counterparties AS c
 where id = '4')) as t

```
