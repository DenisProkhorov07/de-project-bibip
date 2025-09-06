import os
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from datetime import datetime
from decimal import Decimal
from typing import Dict
from typing import List


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        # Создаем пути к файлу и сами пустые файлы для models
        self.models_path = os.path.join(root_directory_path, 'models.txt')
        with open(self.models_path, 'w'):
            pass
        self.total_models = 0
        self.models_index_path = os.path.join(
            root_directory_path,
            'models_index.txt')
        with open(self.models_index_path, 'w'):
            pass
        # Создаем пути к файлу и сами пустые файлы для cars
        self.cars_path = os.path.join(root_directory_path, 'cars.txt')
        with open(self.cars_path, 'w'):
            pass
        self.total_cars = 0
        self.cars_index_path = os.path.join(
            root_directory_path,
            'cars_index.txt')
        with open(self.cars_index_path, 'w'):
            pass
        # Создаем пути к файлу и сами пустые файлы для sales
        self.sales_path = os.path.join(root_directory_path, 'sales.txt')
        with open(self.sales_path, 'w'):
            pass
        self.total_sales = 0
        self.sales_index_path = os.path.join(
            root_directory_path,
            'sales_index.txt')
        with open(self.sales_index_path, 'w'):
            pass

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        with open(self.models_path, 'a') as f:
            line = (f'{model.id}, {model.name}, {model.brand}').ljust(500)\
                  + '\n'
            f.seek(self.total_models * (501))
            f.write(line)
            self.total_models += 1
        with open(self.models_index_path, 'a') as f:
            f.write(f'{model.id}, {self.total_models}\n')
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(self.cars_path, 'a') as f:
            line = (f'{car.vin}, {car.model}, {car.price}, {car.date_start},\
                     {car.status}').ljust(500) + '\n'
            f.seek(self.total_cars * (501))
            f.write(line)
            self.total_cars += 1
        with open(self.cars_index_path, 'a') as f:
            f.write(f'{car.vin}, {self.total_cars}\n')
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        # Добавляем строку продаж в файл sales.txt.
        with open(self.sales_path, 'a') as f:
            line = (f'{sale.sales_number}, {sale.car_vin}, {sale.cost}, \
                    {sale.sales_date}').ljust(500) + '\n'
            f.seek(self.total_sales * (501))
            f.write(line)
            self.total_sales += 1
        # Добавляем строку в файл sales_index.txt.
        with open(self.sales_index_path, 'a') as f:
            f.write(f'{sale.sales_number}, {self.total_sales}\n')
        # Считываем индексы и определяем номер строки.
        with open(self.cars_index_path, 'r') as f:
            car_indexes_list = f.readlines()
            line_number = 0
            for car_index in car_indexes_list:
                if str.split(car_index, ', ')[0].strip() == sale.car_vin:
                    line_number = int(str.split(car_index, ', ')[1].strip())
                    break
        # Считываем в объект данные по номеру строки.
        with open(self.cars_path, 'r+') as f:
            f.seek((line_number - 1) * (501))
            val = f.read(500)
            val_list = str.split(val, ', ')
            # Изменяем статус автомобиля в объекте.
            val_list[4] = 'sold'
            val = str.join(', ', val_list).ljust(500) + '\n'
            # Записываем измененные данные в ту же строку.
            f.seek((line_number - 1) * (501))
            f.write(val)
            current_car = Car(
                vin=val_list[0],
                model=int(val_list[1]),
                price=Decimal(val_list[2]),
                date_start=datetime.strptime(
                    val_list[3].strip(), '%Y-%m-%d %H:%M:%S'
                    ),
                status=CarStatus[val_list[4]]
            )
        return current_car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        result: List[Car] = []
        car_val = ''
        with open(self.cars_path, 'r') as f:
            for line in f:
                car_val = line
                if CarStatus[str.split(car_val, ', ')[4].strip()] == status:
                    current_car = Car(
                        vin=str.split(car_val, ', ')[0].strip(),
                        model=int(str.split(car_val, ', ')[1].strip()),
                        price=Decimal(str.split(car_val, ', ')[2].strip()),
                        date_start=datetime.strptime(
                            str.split(car_val, ', ')[3].strip(),
                            '%Y-%m-%d %H:%M:%S'),
                        status=CarStatus[str.split(car_val, ', ')[4].strip()]
                        )
                    list.append(result, current_car)
        return result

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Считываем файл car_index.tx
        with open(self.cars_index_path, 'r') as f:
            car_indexes_list = f.readlines()
            car_line_number = 0
            for car_index in car_indexes_list:
                if str.split(car_index, ', ')[0].strip() == vin:
                    car_line_number = int(
                        str.split(car_index, ', ')[1].strip()
                        )
                    break
            if car_line_number == 0:
                return None
            # Находим строку в файле cars.txt по номеру строки.
        with open(self.cars_path, 'r') as f:
            f.seek((car_line_number - 1) * (501))
            car_val = f.read(500)
        price = Decimal(str.split(car_val, ', ')[2].strip())
        date_start = datetime.strptime(
            str.split(car_val, ', ')[3].strip(), '%Y-%m-%d %H:%M:%S'
            )
        status = str.split(car_val, ', ')[4].strip()
        # Считываем файл model_index.txt
        with open(self.models_index_path, 'r') as f:
            model_indexes_list = f.readlines()
            model_line_number = 0
            for model_index in model_indexes_list:
                if (str.split(model_index, ', ')[0].strip() ==
                        str.split(car_val, ', ')[1].strip()):
                    # Номер строки выбранной модели.
                    model_line_number = int(
                        str.split(model_index, ', ')[1].strip()
                        )
            # Находим строку в файле models.txt по номеру строки.
        with open(self.models_path, 'r') as f:
            f.seek((model_line_number - 1) * (501))
            model_val = f.read(500)
        model_name = str.split(model_val, ', ')[1].strip()
        model_brand = str.split(model_val, ', ')[2].strip()
        # Считываем информацию о продаже.
        if status != 'sold':
            sales_date = None
            sales_cost = None
        else:
            with open(self.sales_path, 'r') as fs:
                sale_val = ' '
                while True:
                    sale_val = fs.readline()
                    if not sale_val:
                        break
                    sale_val = sale_val.strip()
                    if sale_val:
                        sale_values = sale_val.split(', ')
                        if sale_values[1].strip() == vin:
                            sales_date = datetime.strptime(
                                sale_values[3].strip(), '%Y-%m-%d %H:%M:%S'
                                )
                            sales_cost = Decimal(sale_values[2].strip())
                            break
        result = CarFullInfo(
            vin=vin,
            car_model_name=model_name,
            car_model_brand=model_brand,
            price=price,
            date_start=date_start,
            status=CarStatus[status],
            sales_date=sales_date,
            sales_cost=sales_cost
        )
        return result

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:

        # Читаем индексы автомобилей.
        with open(self.cars_index_path, 'r') as f:
            car_indexes_list = f.readlines()
        line_number = 0

        # Находим номер строки.
        for i, car_index in enumerate(car_indexes_list):
            line_list = str.split(car_index, ', ')
            if line_list[0].strip() == vin:
                line_number = int(line_list[1].strip())
                line_list[0] = new_vin
                car_index = str.join(', ', line_list) + '\n'
                car_indexes_list[i] = car_index
                break

        # Читаем строку но найденному номеру.
        with open(self.cars_path, 'r+') as f:
            f.seek((line_number - 1) * (501))
            val = f.read(500)
            val_list = str.split(val, ', ')
            val_list[0] = new_vin
            new_val = str.join(', ', val_list).ljust(500) + '\n'
            # Записываем измененные данные в ту же строку.
            f.seek((line_number - 1) * (501))
            f.write(new_val)

        with open(self.cars_index_path, 'w') as f:
            for car_index in car_indexes_list:
                f.write(car_index)
        result = Car(
            vin=val_list[0].strip(),
            model=int(val_list[1].strip()),
            price=Decimal(val_list[2].strip()),
            date_start=datetime.strptime(
                val_list[3].strip(), '%Y-%m-%d %H:%M:%S'
                ),
            status=CarStatus[val_list[4].strip()]
        )
        return result

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        with open(self.sales_index_path, 'r') as f:
            sale_line_number = 0
            for line in f:
                if sales_number in line:
                    sale_line_number = int(
                        str.split(line.strip(), ', ')[1].strip()
                        )
                    break

        with open(self.sales_path, 'r+') as f:
            f.seek((sale_line_number - 1) * (501))
            sale_val = f.read(500)
            sale_val_list = str.split(sale_val, ', ')
            sale_val_list.append('deleted')
            sale_val = str.join(', ', sale_val_list).ljust(500) + '\n'
            # Записываем измененные данные в ту же строку.
            f.seek((sale_line_number - 1) * (501))
            f.write(sale_val)

        with open(self.cars_index_path, 'r') as f:
            car_line_number = 0
            for line in f:
                if sale_val_list[1] in line:
                    car_line_number = int(
                        str.split(line.strip(), ', ')[1].strip()
                        )
                    break

        with open(self.cars_path, 'r+') as f:
            f.seek((car_line_number - 1) * (501))
            car_val = f.read(500)
            car_val_list = str.split(car_val, ', ')
            # Изменяем статус автомобиля в объекте.
            car_val_list[4] = 'available'
            car_val = str.join(', ', car_val_list).ljust(500) + '\n'
            # Записываем измененные данные в ту же строку.
            f.seek((car_line_number - 1) * (501))
            f.write(car_val)

        result = Car(
            vin=car_val_list[0].strip(),
            model=int(car_val_list[1].strip()),
            price=Decimal(car_val_list[2].strip()),
            date_start=datetime.strptime(
                car_val_list[3].strip(), '%Y-%m-%d %H:%M:%S'
                ),
            status=CarStatus[car_val_list[4].strip()]
        )
        return result

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        # Словарь для хранения количества продаж каждой модели
        sale_dict: Dict[str, int] = {}

        # Читаем индексы автомобилей.
        with open(self.cars_index_path, 'r') as fci:
            car_indexis = fci.readlines()

        # Читаем построчно продажи.
        with open(self.sales_path, 'r') as fs:
            for sale_line in fs:
                # Определяем vin проданного автомобиля.
                sale_vin = sale_line.strip().split(', ')[1].strip()

                # Находим номер строки проданного автомобиля.
                for line in car_indexis:
                    if str.split(line, ', ')[0].strip() == sale_vin:
                        car_line_number = int(str.split(line, ', ')[1].strip())

                # Читаем строку но найденному номеру.
                with open(self.cars_path, 'r') as fc:
                    fc.seek((car_line_number - 1) * (501))
                    car_val = fc.read(500)
                # Находим id модели.
                model_id = str.split(car_val, ', ')[1].strip()
                # Если модель уже есть в словаре, инкреминтируем значение.
                if model_id in sale_dict:
                    sale_dict[model_id] += 1
                # Иначе добавляем модель со значением 1.
                else:
                    sale_dict[model_id] = 1

        # Сортируем словарь по значению.
        sorted_sale_dict = dict(
            sorted(sale_dict.items(), key=lambda item: item[1], reverse=True)
            )
        # Оставляем три первых элемента.
        result_dict = dict(list(sorted_sale_dict.items())[:3])

        # Создаем пустой список для объектов ModelSaleStats.
        top_models_by_sales = []

        with open(self.models_index_path, 'r') as f:
            model_indexes_list = f.readlines()

        # Для каждого ключа словаря.
        for key in result_dict:
            model_line_number = 0
            # Находим номер строки модели.
            for model_index in model_indexes_list:
                if str.split(model_index, ', ')[0].strip() == key:
                    # Номер строки выбранной модели.
                    model_line_number = int(
                        str.split(model_index, ', ')[1].strip()
                        )
            # Читаем найденную строку.
            with open(self.models_path, 'r') as f:
                f.seek((model_line_number - 1) * (501))
                model_val = f.read(500)
            # Cоздаем объект ModelSaleStat.
            model = ModelSaleStats(
                car_model_name=str.split(model_val, ', ')[1].strip(),
                brand=str.split(model_val, ', ')[2].strip(),
                sales_number=result_dict[key]
            )
            # Добавляем объект в список объектов.
            top_models_by_sales.append(model)
        return top_models_by_sales
