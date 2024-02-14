import csv #potrzebne by prawidlowo obrabiac katalog klientow (jezeli np oddzielisz adres od kodu miejscowosci przecinkiem !)
import requests # do obsługi API MF
from datetime import datetime, timedelta # obsługa czasu.
import openpyxl  # Dodajemy obsługę plików Excel
import logging # logowanie bledow openpyxl (naglowek moze powodowac bledy)

class Product:
    def __init__(self, id, name, price):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID produktu musi być dodatnią liczbą całkowitą.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nazwa produktu nie może być pusta.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Cena produktu musi być dodatnią liczbą.")
        self.id = id
        self.name = name
        self.price = price

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Price: {self.price}"

class Catalog:
    def __init__(self):
        self.products = []
        self.file_path = 'katalog.txt'
        self.load_products()

    def add_product(self, name, price):
        new_id = 1
        if self.products:
            new_id = max(product.id for product in self.products) + 1
        new_product = Product(new_id, name, price)
        self.products.append(new_product)
        self.save_products()

    def remove_product(self, id):
        self.products = [product for product in self.products if product.id != id]
        self.save_products()

    def view_products(self):
        for product in self.products:
            print(product)

    def save_products(self):
        with open(self.file_path, 'w') as file:
            for product in self.products:
                file.write(f"{product.id},{product.name},{product.price}\n")

    def load_products(self):
        try:
            with open(self.file_path, 'r', encoding='cp1250') as file:
                for line in file:
                    id, name, price = line.strip().split(',')
                    self.products.append(Product(int(id), name, float(price)))
        except FileNotFoundError:
            pass

    def sort_products(self, criterion='id'):
        if criterion == 'name':
            self.products.sort(key=lambda product: product.name)
        elif criterion == 'price':
            self.products.sort(key=lambda product: product.price)
        else: # default sort by 'id'
            self.products.sort(key=lambda product: product.id)

    def save_sorted_products(self, criterion='id'):
        self.sort_products(criterion)
        with open('posortowane.txt', 'w') as file:
            for product in self.products:
                file.write(f"{product.id},{product.name},{product.price}\n")
        print("Posortowane produkty zostały zapisane do pliku 'posortowane.txt'.")

    def view_sorted_products(self, criterion='id'):
        self.sort_products(criterion)
        self.view_products()

class Client:
    def __init__(self, id, name, address, nip):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID klienta musi być dodatnią liczbą całkowitą.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nazwa klienta nie może być pusta.")
        if not isinstance(address, str) or not address.strip():
            raise ValueError("Adres klienta nie może być pusty.")
        if not isinstance(nip, str) or len(nip) != 10 or not nip.isdigit():
            raise ValueError("Numer NIP klienta musi być ciągiem 10 cyfr.")
        self.id = id
        self.name = name
        self.address = address
        self.nip = nip

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Address: {self.address}, NIP: {self.nip}"

class ClientCatalog:
    def __init__(self):
        self.clients = []
        self.file_path = 'clients.txt'
        self.load_clients()

    def add_client(self, name, address, nip):
        new_id = 1
        if self.clients:
            new_id = max(client.id for client in self.clients) + 1
        new_client = Client(new_id, name, address, nip)
        self.clients.append(new_client)
        self.save_clients()

    def remove_client(self, id):
        self.clients = [client for client in self.clients if client.id != id]
        self.save_clients()

    def view_clients(self):
        for client in self.clients:
            print(client)

    def save_clients(self):
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for client in self.clients:
                writer.writerow([client.id, client.name, client.address, client.nip])

    def load_clients(self):
        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4:
                        id, name, address, nip = row
                        self.clients.append(Client(int(id), name, address, nip))
        except FileNotFoundError:
            pass

    def check_vat_status(self, client_id):
        client = next((client for client in self.clients if client.id == client_id), None)
        if client:
            yesterday = datetime.now() - timedelta(days=1)
            date = yesterday.strftime('%Y-%m-%d')
            nip = client.nip
            url = f'https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={date}'
            headers = {'User-Agent': 'Mozilla/5.0'}
            try:
                response = requests.get(url, headers=headers)
                data = response.json()
                if response.status_code == 200 and 'result' in data:
                    status = data['result']['subject']['statusVat']
                    print(f'Numer NIP {nip} jest czynnym płatnikiem VAT na dzień {date}.' if status == 'Czynny' else f'Numer NIP {nip} nie jest czynnym płatnikiem VAT na dzień {date}.')
                else:
                    print(f'Brak danych dla numeru NIP {nip} na dzień {date}.')
            except requests.exceptions.RequestException as e:
                print('Wystąpił problem z połączeniem:', e)
        else:
            print("Nie znaleziono klienta o podanym ID.")

def display_shopping_menu():
    print("\nMenu Zakupów:")
    print("1. Dokonaj zakupu")
    print("0. Wróć do poprzedniego menu")
    print("Wybierz opcję (0-1):")

def process_purchase(catalog, client_catalog):
    client_catalog.view_clients()
    client_id = int(input("Podaj ID klienta: "))
    client = next((client for client in client_catalog.clients if client.id == client_id), None)
    if not client:
        print("Nie znaleziono klienta.")
        return

    catalog.view_products()
    selected_products = []
    for i in range(2):  # Prosimy o wybór 2 produktów
        product_id = int(input(f"Podaj ID produktu {i+1}: "))
        product = next((product for product in catalog.products if product.id == product_id), None)
        if product:
            selected_products.append(product)
        else:
            print(f"Nie znaleziono produktu o ID: {product_id}")

    if len(selected_products) == 2:
        save_invoice(client, selected_products)

def save_invoice(client, products):
    logging.getLogger("openpyxl").setLevel(logging.ERROR)
    wb = openpyxl.load_workbook('Faktura.xlsx')
    sheet = wb.active
    sheet['B7'] = f"{client.name}, {client.address}, NIP: {client.nip}"
    for i, product in enumerate(products, start=11):
        sheet[f'B{i}'] = product.name
        sheet[f'C{i}'] = product.price
    wb.save('Faktura.xlsx')
    print("Faktura została zapisana.")

def display_menu():
    print("\nMenu Katalogu Produktów:")
    print("1. Dodaj produkt")
    print("2. Usuń produkt")
    print("3. Przeglądaj produkty")
    print("4. Sortuj i przeglądaj produkty")
    print("5. Zapisz posortowane produkty do pliku")
    print("0. Powrót do menu głównego")
    print("Wybierz opcję (0-5):")

def display_client_menu():
    print("\nMenu Klientów:")
    print("1. Dodaj klienta")
    print("2. Usuń klienta")
    print("3. Przeglądaj klientów")
    print("4. Sprawdź status VAT klienta")
    print("0. Powrót do menu głównego")
    print("Wybierz opcję (0-4):")

def main():
    catalog = Catalog()
    client_catalog = ClientCatalog()
    while True:
        print("\nMenu Główne:")
        print("1. Zarządzaj katalogiem produktów")
        print("2. Zarządzaj katalogiem klientów")
        print("3. Zakupy")
        print("4. Zakończ")
        choice = input("Wybierz opcję (1-4): ")

        if choice == '1':
            # Obsługa katalogu produktów (bez zmian)
            pass
        elif choice == '2':
            # Obsługa katalogu klientów (bez zmian)
            pass
        elif choice == '3':
            while True:
                display_shopping_menu()
                sub_choice = input()
                if sub_choice == '1':
                    process_purchase(catalog, client_catalog)
                elif sub_choice == '0':
                    break
                else:
                    print("Nieprawidłowy wybór.")
        elif choice == '4':
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowy wybór.")

if __name__ == "__main__":
    main()