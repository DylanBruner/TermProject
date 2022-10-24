import os

class Search(object):
    def __init__(self, items: list):
        self.items = items
        self.results = []

    def search(self) -> str:
        os.system('cls' if os.name == 'nt' else 'clear')
        query = input("Search: ")
        self.results = [item for item in self.items if query.lower() in item.lower()][:25]

        for result in self.results:
            print(f"{self.results.index(result)+1}. {result}")
        
        print('\nLeave blank to search again')
        selection = input("Select: ")
        if selection == "":
            self.search()
        else:
            if selection.isdigit():
                if int(selection) <= len(self.results):
                    return self.results[int(selection)-1]
                else:
                    print("Invalid selection")
                    self.search()
            else:
                print("Invalid selection")
                self.search()