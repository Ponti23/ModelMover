from PyQt5.QtWidgets import QListWidgetItem, QApplication, QMainWindow, QListWidget, QMenu, QAction, QVBoxLayout, QWidget, QLabel, QMessageBox

class ListWidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QListWidget with Group Change")
        self.setGeometry(100, 100, 400, 300)

        # Create the QListWidget
        self.list_widget = QListWidget(self)

        # Add items with groups (simulating initial group assignment)
        self.items = []
        self.items.append(self.add_item("Item 1", "Group A"))
        self.items.append(self.add_item("Item 2", "Group B"))
        self.items.append(self.add_item("Item 3", "Group A"))

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_widget)

        # Set the central widget
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_item(self, text, group):
        item = QListWidgetItem(text)
        item.setData(1, group)  # Store the group as custom data
        self.list_widget.addItem(item)
        return item

    def contextMenuEvent(self, event):
        # Get the list item that was right-clicked
        item = self.list_widget.itemAt(event.pos())
        if item:
            self.show_context_menu(item)

    def show_context_menu(self, item):
        context_menu = QMenu(self)
        
        # Add actions for changing the group
        change_group_action = QAction("Change Group", self)
        change_group_action.triggered.connect(lambda: self.change_group(item))
        context_menu.addAction(change_group_action)
        
        # Show the context menu
        context_menu.exec_(self.mapToGlobal(item.pos()))

    def change_group(self, item):
        # Show a message box to simulate group change
        current_group = item.data(1)  # Get the current group from the custom data
        new_group, ok = self.get_new_group(current_group)
        
        if ok:
            item.setData(1, new_group)  # Update the group data
            print(f"Item group changed to: {new_group}")
            item.setText(f"{item.text()} (Group: {new_group})")

    def get_new_group(self, current_group):
        # Simulate getting a new group from the user (you could use an input dialog)
        groups = ["Group A", "Group B", "Group C"]
        new_group, ok = QMessageBox.getItem(self, "Select New Group", 
                                            "Choose a new group:", 
                                            groups, 
                                            current=groups.index(current_group), 
                                            editable=False)
        return new_group, ok


if __name__ == "__main__":
    app = QApplication([])
    window = ListWidgetExample()
    window.show()
    app.exec_()
