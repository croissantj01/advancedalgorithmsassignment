import time

class HashSlot:
    def __init__(self, key=None, value=None, is_deleted=False):
        self.key = key
        self.value = value
        self.is_deleted = is_deleted

class PharmacyProduct:
    def __init__(self, product_id, name, category, price, stock_quantity, expiry_date):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
        self.expiry_date = expiry_date

    # To display the results in a table format
    def __str__(self):
        return (f"| {self.product_id:<8} | "
                f"{self._truncate(self.name, 20):<20} | "
                f"{self._truncate(self.category, 18):<18} | "
                f"RM {self.price:>6.2f} | "
                f"{self.stock_quantity:>6} | "
                f"{self.expiry_date:<10} |")

    @staticmethod
    def print_header():
        border = "+" + "-" * 10 + "+" + "-" * 22 + "+" + "-" * 20 + "+" + "-" * 12 + "+" + "-" * 8 + "+" + "-" * 12 + "+"
        print(border)
        print(
            f"| {'ID':<8} | {'Product Name':<20} | {'Category':<18} | {'Price':<10} | {'Stock':<6} | {'Expiry Date':<10} |")
        print(border)

    @staticmethod
    def print_footer():
        border = "+" + "-" * 10 + "+" + "-" * 22 + "+" + "-" * 20 + "+" + "-" * 12 + "+" + "-" * 8 + "+" + "-" * 12 + "+"
        print(border)

    # To shorten the words if it exceeds the character limit set in the print method
    @staticmethod
    def _truncate(text, length):
        return text if len(text) <= length else text[:length-3] + "..."

class HashTableOpenAddressing:
    def __init__(self, capacity=53):
        self.capacity = capacity
        self.size = 0
        self.table = [HashSlot() for _ in range(capacity)]

    def _hash(self, key):
        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.capacity
        return hash_value

    def _probe(self, start_index, key):
        index = start_index
        for _ in range(self.capacity):
            slot = self.table[index]

            if slot.key is None and not slot.is_deleted:
                return index

            # Formula for linear probing
            index = (index + 1) % self.capacity
        return -1

    def insert(self, key, value):
        if self.size >= self.capacity * 0.75:
            self._resize()

        start_index = self._hash(key)
        index = self._probe(start_index, key)

        # To check whether the table is full or not (if full returns -1 from the _probe function)
        if index == -1:
            raise Exception("Hash table is full! Cannot insert any new product!")

        slot = self.table[index]

        # Add 1 to the table size counter
        if slot.key is None:
            self.size += 1

        # Adding the values into the empty index
        slot.key = key
        slot.value = value
        slot.is_deleted = False

    def search(self, key):
        index = self._hash(key)

        original_index = index

        # To find the index in which the value is stored in
        while self.table[index] is not None:
            slot = self.table[index]

            if slot.key is None and not slot.is_deleted:
                return None

            if slot.key == key and not slot.is_deleted:
                return slot.value

            index = (index + 1) % self.capacity

            if index == original_index:
                break

        return None

    def edit(self, key, new_name=None, new_category=None, new_price=None, new_stock=None, new_expiry_date=None):
        product = self.search(key)

        if product is None:
            return False

        if new_name:
            product.name = new_name
        if new_category:
            product.category = new_category
        if new_price:
            product.price = new_price
        if new_stock:
            product.stock = new_stock
        if new_expiry_date:
            product.expiry_date = new_expiry_date
        return True

    def delete(self, key):
        index = self._hash(key)
        original_index = index

        for _ in range(self.capacity):
            slot = self.table[index]

            if slot.key == key and not slot.is_deleted:
                slot.key = None
                slot.value = None
                slot.is_deleted = True
                self.size -= 1
                return True

            index = (index + 1) % self.capacity
            if index == original_index:
                break

        return False

    # This method is called when the table reaches 75% and needs to be expanded
    def _resize(self):
        old_table = self.table

        self.capacity *= 2
        self.size = 0
        self.table = [HashSlot() for _ in range(self.capacity)]

        for slot in old_table:
            if slot.key is not None and not slot.is_deleted:
                self.insert(slot.key, slot.value)

def performance_experiment():
    # Benchmark testing
    test_size = 10000
    hash_table_bench = HashTableOpenAddressing(capacity=2000)
    array_bench = []

    for i in range(test_size):
        testing_product_id = f"MED{i:04d}"
        testing_product = PharmacyProduct(testing_product_id, f"Drug", "General Drug", 5, 100, "2030/02/10")
        hash_table_bench.insert(testing_product_id, testing_product)

        array_bench.append((testing_product_id, testing_product))

    # Finding worst-case scenario
    target_key = f"MED0999"

    start_time = time.perf_counter()
    for _ in range(10000):
        hash_table_bench.search(target_key)
    hash_duration = time.perf_counter() - start_time

    start_time = time.perf_counter()
    for _ in range(10000):
        for key, val in array_bench:
            if key == target_key:
                break
    array_duration = time.perf_counter() - start_time

    print(f"\nHash Table Search Time for 10000 lookups: {hash_duration:.6f} seconds")
    print(f"1D Array Search Time for 10000 lookups: {array_duration:.6f} seconds")
    if hash_duration > 0:
        multiplier = array_duration / hash_duration
        print(f"Hash Table is {multiplier:.1f}x faster than the 1D Array!")

def main():
    pharmacydb = HashTableOpenAddressing()

    initial_products = [
        PharmacyProduct("MED001", "Prednisolone", "Glucocorticoid", 4.80, 10, "2027/10/21"),
        PharmacyProduct("MED002", "Colchicine", "Anti-gout Agent", 12.50, 30, "2028/9/30"),
        PharmacyProduct("MED003", "Amlodipine", "Calcium Channel Blockers", 5.50, 40, "2027/4/12"),
        PharmacyProduct("MED004", "Fenofibrate", "Fibric Acid Derivative", 18.90, 10, "2029/2/25"),
        PharmacyProduct("MED005", "Simvastatin", "HMG-CoA Reductase Inhibitor", 7.20, 50, "2030/7/6")
    ]

    for product in initial_products:
        pharmacydb.insert(product.product_id, product)

    print("Pharmacy Inventory System Initialised!")
    print(f"Loaded {len(initial_products)} pre-defined records into the Hash Table. \n")

    while True:
        print("\n---Inventory Menu---")
        print("1 - Search Product by ID")
        print("2 - Insert New Product")
        print("3 - Edit Product Details")
        print("4 - Delete Product")
        print("5 - Exit")
        print("6 - Performance Experiment for testing the worst-case (EXTRA)")

        try:
            option = int(input("Please choose a number (1-6): "))
        except ValueError:
            print("Invalid input! Please enter a number 1 - 6!")
            continue

        if option == 1:
            product_id = input("Enter Product ID to search (e.g. MED001): ").strip().upper()
            result = pharmacydb.search(product_id)
            if result:
                print(f"Product with the id {product_id} is found: ")
                PharmacyProduct.print_header()
                print(result)
                PharmacyProduct.print_footer()
            else:
                print(f"No product with the id {product_id} is found!")

        elif option == 2:
            print("Enter the details for the new products: ")
            new_product_id = input("Product ID (e.g. MED001): ").strip().upper()
            if pharmacydb.search(new_product_id) is None:
                name = input("Product Name: ").strip()
                category = input("Category: ").strip()
                try:
                    price = float(input("Price (RM): "))
                    stock = int(input("Stock Quantity: "))
                except ValueError:
                    print("Price must be a number and stock must be an integer!")
                    continue
                expiry_date = input("Expiry Date (YYYY/MM/DD): ").strip()
                new_product = PharmacyProduct(new_product_id, name, category, price, stock, expiry_date)

                try:
                    pharmacydb.insert(new_product_id, new_product)
                    print(f"Product with the id {new_product_id} is inserted successfully!")
                except Exception as e:
                    print("Error occurred!")
            else:
                print("The product_id already exists in the table! Unable to add!")

        elif option == 3:
            product_id = input("Enter the product ID to edit details (e.g. MED001): ").strip().upper()
            result = pharmacydb.search(product_id)
            if result:
                print("Enter the new details of the product: ")
                print("Leave the blank to keep the current value!")
                new_name = input("Product Name: ")
                new_category = input("Category: ")
                try:
                    new_price = float(input("Price (RM): "))
                    new_stock = int(input("Stock Quantity: "))
                except ValueError:
                    print("Price must be a number and stock must be an integer!")
                    continue
                new_expiry_date = input("Expiry Date (YYYY/MM/DD): ").strip()

                if new_name: result.name = new_name
                if new_category: result.category = new_category
                if new_price: result.price = new_price
                if new_stock: result.stock = new_stock
                if new_expiry_date: result.expiry_date = new_expiry_date

                print(f"Product with id {product_id} successfully edited the product details!")
            else:
                print(f"No product with id {product_id} is found!")

        elif option == 4:
            product_id = input("Enter Product ID to delete (e.g. MED001): ").strip().upper()
            result = pharmacydb.delete(product_id)
            if result:
                print(f"Product with id {product_id} has been successfully deleted!")
            else:
                print(f"No product with id {product_id} is found!")

        elif option == 5:
            print("Exiting the system...")
            print("Exited!")
            break

        elif option == 6:
            performance_experiment()

if __name__ == "__main__":
    main()