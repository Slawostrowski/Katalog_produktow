import csv #potrzebne by prawidlowo obrabiac katalog klientow (jezeli np oddzielisz adres od kodu miejscowosci przecinkiem !)
import requests # do obsługi API MF
from datetime import datetime, timedelta # obsługa czasu.

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
            with open(self.file_path, 'r', encoding='iso-8859-2') as file:
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
        print("3. Zakończ")
        choice = input("Wybierz opcję (1-3): ")

        if choice == '1':
            while True:
                display_menu()
                sub_choice = input("Wybierz opcję (0-5): ")
                if sub_choice == '1':
                    name = input("Podaj nazwę produktu: ")
                    price = float(input("Podaj cenę produktu: "))
                    catalog.add_product(name, price)
                    print("Produkt dodany.")
                elif sub_choice == '2':
                    id = int(input("Podaj ID produktu do usunięcia: "))
                    catalog.remove_product(id)
                    print("Produkt usunięty.")
                elif sub_choice == '3':
                    catalog.view_products()
                elif sub_choice == '4':
                    criterion = input("Podaj kryterium sortowania (id, name, price): ")
                    catalog.view_sorted_products(criterion)
                elif sub_choice == '5':
                    catalog.save_products()
                    print("Produkty zostały zapisane.")
                elif sub_choice == '0':
                    break
                else:
                    print("Nieprawidłowy wybór.")
        elif choice == '2':
            while True:
                display_client_menu()
                sub_choice = input("Wybierz opcję (0-4): ")
                if sub_choice == '1':
                    name = input("Podaj nazwę klienta: ")
                    address = input("Podaj adres klienta: ")
                    nip = input("Podaj numer NIP klienta: ")
                    client_catalog.add_client(name, address, nip)
                    print("Klient dodany.")
                elif sub_choice == '2':
                    id = int(input("Podaj ID klienta do usunięcia: "))
                    client_catalog.remove_client(id)
                    print("Klient usunięty.")
                elif sub_choice == '3':
                    client_catalog.view_clients()
                elif sub_choice == '4':
                    client_id = int(input("Podaj ID klienta do sprawdzenia statusu VAT: "))
                    client_catalog.check_vat_status(client_id)
                elif sub_choice == '0':
                    break
                else:
                    print("Nieprawidłowy wybór.")
        elif choice == '3':
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowy wybór.")

if __name__ == "__main__":
    main()