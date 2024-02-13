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


def main():
    catalog = Catalog()
    while True:
        display_menu()
        choice = input("Wybierz opcję (1-4): ")

        if choice == '1':
            name = input("Podaj nazwę produktu: ")
            price = float(input("Podaj cenę produktu: "))
            catalog.add_product(name, price)
            print("Produkt dodany.")
        elif choice == '2':
            id = int(input("Podaj ID produktu do usunięcia: "))
            catalog.remove_product(id)
            print("Produkt usunięty.")
        elif choice == '3':
            while True:
                display_sort_menu()
                sort_choice = input("Wybierz opcję sortowania (0-3): ")

                if sort_choice == '1':
                    catalog.view_sorted_products('id')
                elif sort_choice == '2':
                    catalog.view_sorted_products('name')
                elif sort_choice == '3':
                    catalog.view_sorted_products('price')
                elif sort_choice == '0':
                    break
                else:
                    print("Nieprawidłowy wybór. Proszę wybrać opcję od 0 do 3.")
        elif choice == '4':
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowy wybór. Proszę wybrać opcję od 1 do 4.")


if __name__ == "__main__":
    main()