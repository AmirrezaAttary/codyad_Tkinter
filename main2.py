import csv

class Task:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority

    def __str__(self):
        return f"{self.name} ({self.priority}) - {self.description}"


class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_name):
        self.tasks = [task for task in self.tasks if task.name != task_name]

    def show_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task}")

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Description", "Priority"])
            for task in self.tasks:
                writer.writerow([task.name, task.description, task.priority])

    def load_from_csv(self, filename):
        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.tasks = [Task(row['Name'], row['Description'], row['Priority']) for row in reader]
        except FileNotFoundError:
            print("CSV file not found. Starting with an empty to-do list.")


def main():
    todo = ToDoList()
    filename = 'todo_list.csv'
    todo.load_from_csv(filename)

    while True:
        print("\nTo-Do List Manager")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Show Tasks")
        print("4. Save and Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Task name: ")
            description = input("Description: ")
            priority = input("Priority (High/Medium/Low): ")
            task = Task(name, description, priority)
            todo.add_task(task)
            print("Task added.")
        elif choice == '2':
            name = input("Enter the task name to remove: ")
            todo.remove_task(name)
            print("Task removed if it existed.")
        elif choice == '3':
            todo.show_tasks()
        elif choice == '4':
            todo.save_to_csv(filename)
            print("List saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
