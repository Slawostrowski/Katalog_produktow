import csv #potrzebne by prawidlowo obrabiac katalog klientow (jezeli np oddzielisz adres od kodu miejscowosci przecinkiem !)
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
        self.file_path = 'katalog.txt'  # Dodanie ścieżki do pliku
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
            with open(self.file_path, 'r') as file:
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
        elif criterion == 'id':
            self.products.sort(key=lambda product: product.id)

    def view_sorted_products(self, criterion='id'):
        self.sort_products(criterion)
        self.view_products()

    def save_sorted_products(self):
        with open('posortowane.txt', 'w') as file:
            for product in self.products:
                file.write(f"{product.id},{product.name},{product.price}\n")
        print("Posortowane produkty zostały zapisane do pliku 'posortowane.txt'.")


def display_menu():
    print("\nMenu Katalogu Produktów:")
    print("1. Dodaj produkt")
    print("2. Usuń produkt")
    print("3. Przeglądaj produkty")
    print("4. Zakończ")
    print("Wybierz opcję (1-4):")


def display_sort_menu():
    print("\nOpcje sortowania produktów:")
    print("1. Sortuj według ID")
    print("2. Sortuj według nazwy")
    print("3. Sortuj według ceny")
    print("0. Powrót do menu głównego")
    print("Wybierz opcję sortowania (0-3):")

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
                    if len(row) == 4:  # Sprawdzamy, czy mamy 4 pola
                        id, name, address, nip = row
                        self.clients.append(Client(int(id), name, address, nip))
                    else:
                        print("Nieprawidłowy format danych dla klienta. Pomijanie linii.")
        except FileNotFoundError:
            pass

def display_client_menu():
    print("\nMenu Klientów:")
    print("1. Dodaj klienta")
    print("2. Usuń klienta")
    print("3. Przeglądaj klientów")
    print("0. Powrót do menu głównego")
    print("Wybierz opcję (0-3):")

def main():
    catalog = Catalog()
    client_catalog = ClientCatalog()
    while True:
        print("\nMenu Główne:")
        print("1. Katalog produktów")
        print("2. Klienci")
        print("3. Zakończ")
        choice = input("Wybierz opcję (1-3): ")

        if choice == '1':
            while True:
                display_menu()
                sub_choice = input("Wybierz opcję (1-4): ")
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
                    while True:
                        display_sort_menu()
                        sort_choice = input("Wybierz opcję sortowania (0-3): ")
                        if sort_choice in ['1', '2', '3']:
                            criterion = 'id' if sort_choice == '1' else ('name' if sort_choice == '2' else 'price')
                            catalog.view_sorted_products(criterion)
                            print("Czy chcesz zapisać posortowane produkty do pliku 'posortowane.txt'? (tak/nie)")
                            save_decision = input()
                            if save_decision.lower() in ('tak', 'yes', 'y', 't'):
                                catalog.save_sorted_products()
                        elif sort_choice == '0':
                            break
                        else:
                            print("Nieprawidłowy wybór. Proszę wybrać opcję od 0 do 3.")
                elif sub_choice == '4':
                    break
                else:
                    print("Nieprawidłowy wybór. Proszę wybrać opcję od 1 do 4.")
        elif choice == '2':
            while True:
                display_client_menu()
                sub_choice = input("Wybierz opcję (0-3): ")
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
                elif sub_choice == '0':
                    break
                else:
                    print("Nieprawidłowy wybór. Proszę wybrać opcję od 0 do 3.")
        elif choice == '3':
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowy wybór. Proszę wybrać opcję od 1 do 3.")

if __name__ == "__main__":
    main()