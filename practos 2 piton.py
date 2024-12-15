import json
from functools import reduce
from tabulate import tabulate

# Заглушка данных
users_data = {}
services_data = []
purchase_history = {}
favorites_data = {}

# Логин и пароль администратора (можно изменять)
admin_username = "admin"
admin_password = "password"

# Загрузка и сохранение данных
def save_data():
    with open('users.json', 'w') as f:
        json.dump(users_data, f)
    with open('services.json', 'w') as f:
        json.dump(services_data, f)
    with open('purchase_history.json', 'w') as f:
        json.dump(purchase_history, f)
    with open('favorites.json', 'w') as f:
        json.dump(favorites_data, f)

def load_data():
    global users_data, services_data, purchase_history, favorites_data
    try:
        with open('users.json', 'r') as f:
            users_data = json.load(f)
    except FileNotFoundError:
        users_data = {}

    try:
        with open('services.json', 'r') as f:
            services_data = json.load(f)
    except FileNotFoundError:
        services_data = []

    try:
        with open('purchase_history.json', 'r') as f:
            purchase_history = json.load(f)
    except FileNotFoundError:
        purchase_history = {}

    try:
        with open('favorites.json', 'r') as f:
            favorites_data = json.load(f)
    except FileNotFoundError:
        favorites_data = {}

# Авторизация пользователя или администратора
def login(role='user'):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    if role == 'admin':
        if username == admin_username and password == admin_password:
            print(f"Добро пожаловать, администратор {username}!")
            return username
        else:
            print("Неверные учетные данные администратора.")
            return None

    user = users_data.get(username)
    if user and user["password"] == password and user["role"] == role:
        print(f"Добро пожаловать, {username}!")
        return username
    else:
        print("Неверные учетные данные.")
        return None

# Функции для пользователей 

def view_services():
    print("Доступные услуги:")
    if not services_data:
        print("Услуги отсутствуют.")
    else:
        print(tabulate(services_data, headers="keys", tablefmt="grid"))

def purchase_service(username):
    service_name = input("Введите название услуги для покупки: ")
    service = next((s for s in services_data if s['name'] == service_name), None)

    if service:
        try:
            hours = int(input("Введите количество часов: "))
            if username not in purchase_history:
                purchase_history[username] = []
            purchase_history[username].append({"service": service, "hours": hours})
            save_data()
            print(f"Услуга '{service_name}' успешно приобретена на {hours} час(ов)!")
        except ValueError:
            print("Ошибка: введите целое число для количества часов.")
    else:
        print("Услуга не найдена.")

def view_purchase_history(username):
    print(f"История покупок для {username}:")
    history = [{"service": purchase["service"]["name"], "price": purchase["service"]["price"], "hours": purchase["hours"]} 
               for purchase in purchase_history.get(username, [])]
    if history:
        print(tabulate(history, headers="keys", tablefmt="grid"))
    else:
        print("История покупок пуста.")

def add_favorite_game(username):
    game = input("Введите название любимой игры: ")
    if username not in favorites_data:
        favorites_data[username] = {"games": [], "snacks": []}

    if game not in favorites_data[username]["games"]:
        favorites_data[username]["games"].append(game)
        save_data()
        print(f"Игра '{game}' добавлена в любимые.")
    else:
        print("Эта игра уже в вашем списке любимых.")

def remove_favorite_game(username):
    game = input("Введите название игры для удаления: ")
    if username in favorites_data and game in favorites_data[username]["games"]:
        favorites_data[username]["games"].remove(game)
        save_data()
        print(f"Игра '{game}' удалена из любимых.")
    else:
        print("Эта игра не найдена в вашем списке любимых.")

def add_favorite_snack(username):
    snack = input("Введите название любимого снека: ")
    if username not in favorites_data:
        favorites_data[username] = {"games": [], "snacks": []}

    if snack not in favorites_data[username]["snacks"]:
        favorites_data[username]["snacks"].append(snack)
        save_data()
        print(f"Снек '{snack}' добавлен в любимые.")
    else:
        print("Этот снэк уже в вашем списке любимых.")

def remove_favorite_snack(username):
    snack = input("Введите название снека для удаления: ")
    if username in favorites_data and snack in favorites_data[username]["snacks"]:
        favorites_data[username]["snacks"].remove(snack)
        save_data()
        print(f"Снек '{snack}' удален из любимых.")
    else:
        print("Этот снэк не найден в вашем списке любимых.")

def view_favorite_games(username):
    print("Ваши любимые игры:")
    games = favorites_data.get(username, {}).get("games", [])
    if games:
        for game in games:
            print(f"- {game}")
    else:
        print("У вас нет любимых игр.")

def view_favorite_snacks(username):
    print("Ваши любимые снеки:")
    snacks = favorites_data.get(username, {}).get("snacks", [])
    if snacks:
        for snack in snacks:
            print(f"- {snack}")
    else:
        print("У вас нет любимых снеков.")

def update_user_data(username):
    print("Обновление данных пользователя:")
    new_password = input("Введите новый пароль (оставьте пустым для пропуска): ")
    if new_password:
        users_data[username]["password"] = new_password
    # Можно добавить и другие поля, например, имя, телефон и т.д.
    save_data()
    print("Данные пользователя обновлены.")

# Функции для администраторов
def add_service():
    name = input("Введите название услуги: ")
    try:
        price = float(input("Введите цену услуги: "))
        services_data.append({"name": name, "price": price})
        save_data()
        print(f"Услуга '{name}' добавлена.")
    except ValueError:
        print("Ошибка: введите корректную цену.")

def remove_service():
    name = input("Введите название услуги для удаления: ")
    global services_data
    services_data = [s for s in services_data if s["name"] != name]
    save_data()
    print(f"Услуга '{name}' удалена, если она существовала.")

def view_statistics():
    print("Статистика покупок:")
    total_services = sum(len(history) for history in purchase_history.values())
    
    total_hours = reduce(
        lambda acc, x: acc + sum(
            p["hours"] for p in x if isinstance(p["hours"], (int, float))
        ),
        purchase_history.values(), 
        0
    )
    
    print(f"Общее количество покупок: {total_services}")
    print(f"Общее количество часов: {total_hours}")

    if total_services > 0:
        print("\nПодробная статистика покупок по пользователям:")
        for user, history in purchase_history.items():
            user_total_services = len(history)
            user_total_hours = sum(p["hours"] for p in history if isinstance(p["hours"], (int, float)))
            print(f"Пользователь '{user}': {user_total_services} покупок на {user_total_hours} часов.")
    else:
        print("Покупок не совершено ни одним пользователем.")

def add_user():
    username = input("Введите имя нового пользователя: ")
    if username in users_data:
        print("Пользователь с таким именем уже существует.")
    else:
        password = input("Введите пароль: ")
        users_data[username] = {"password": password, "role": "user"}
        purchase_history[username] = []
        favorites_data[username] = {"games": [], "snacks": []}
        save_data()
        print("Пользователь добавлен.")

def remove_user():
    username = input("Введите имя пользователя для удаления: ")
    if username in users_data:
        del users_data[username]
        del purchase_history[username]
        del favorites_data[username]
        save_data()
        print(f"Пользователь '{username}' удален.")
    else:
        print("Пользователь не найден.")

def filter_services_by_price():
    try:
        max_price = float(input("Введите максимальную цену для фильтрации: "))
        filtered_services = list(filter(lambda s: s['price'] <= max_price, services_data))

        print("Фильтрованные услуги:")
        if filtered_services:
            print(tabulate(filtered_services, headers="keys", tablefmt="grid"))
        else:
            print("Нет доступных услуг по указанным критериям.")
    except ValueError:
        print("Ошибка: введите корректное число.")

def filter_services_by_name():
    name_filter = input("Введите часть названия услуги для фильтрации: ")
    filtered_services = list(filter(lambda s: name_filter.lower() in s['name'].lower(), services_data))

    print("Фильтрованные услуги:")
    if filtered_services:
        print(tabulate(filtered_services, headers="keys", tablefmt="grid"))
    else:
        print("Нет доступных услуг по указанным критериям.")

def sort_services():
    sorted_services = sorted(services_data, key=lambda s: s['price'])
    print("Услуги отсортированные по цене:")
    print(tabulate(sorted_services, headers="keys", tablefmt="grid"))



# Главное меню
def main_menu():
    load_data()

    while True:
        print("\n--- Главное меню ---")
        print("1. Вход как пользователь")
        print("2. Вход как администратор")
        print("3. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            username = login(role='user')
            if username:
                user_menu(username)
        elif choice == '2':
            username = login(role='admin')
            if username:
                admin_menu()
        elif choice == '3':
            print("Выход из приложения.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

# меню пользователя 
def user_menu(username):
    while True:
        print("\n--- Пользовательское меню ---")
        print("1. Просмотр услуг")
        print("2. Покупка услуги")
        print("3. История покупок")
        print("4. Добавить любимую игру")
        print("5. Удалить любимую игру")
        print("6. Добавить любимый снэк")
        print("7. Удалить любимый снэк")
        print("8. Просмотр любимых игр")
        print("9. Просмотр любимых снеков")
        print("10. Обновить данные пользователя")
        print("11. Выйти")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            view_services()
        elif choice == "2":
            purchase_service(username)
        elif choice == "3":
            view_purchase_history(username)
        elif choice == "4":
            add_favorite_game(username)
        elif choice == "5":
            remove_favorite_game(username)
        elif choice == "6":
            add_favorite_snack(username)
        elif choice == "7":
            remove_favorite_snack(username)
        elif choice == "8":
            view_favorite_games(username)
        elif choice == "9":
            view_favorite_snacks(username)
        elif choice == "10":
            update_user_data(username)
        elif choice == "11":
            break
        else:
            print("Неверный выбор.")

# меню админа
def admin_menu():
    while True:
        print("\n--- Администраторское меню ---")
        print("1. Добавить услугу")
        print("2. Удалить услугу")
        print("3. Просмотр статистики")
        print("4. Добавить пользователя")
        print("5. Удалить пользователя")
        print("6. Фильтрация услуг по цене")
        print("7. Фильтрация услуг по названию")
        print("8. Сортировка услуг")
        print("9. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            add_service()
        elif choice == "2":
            remove_service()
        elif choice == "3":
            view_statistics()
        elif choice == "4":
            add_user()
        elif choice == "5":
            remove_user()
        elif choice == "6":
            filter_services_by_price()
        elif choice == "7":
            filter_services_by_name()
        elif choice == "8":
            sort_services()
        elif choice == "9":
            break
        else:
            print("Неверный выбор.")

# Запуск приложения
if __name__ == "__main__":
    main_menu()