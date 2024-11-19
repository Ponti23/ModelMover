import sys
from PyQt5.QtWidgets import (
    QVBoxLayout, QMenu, QMessageBox, QInputDialog, QWidget, QListWidget, 
    QOpenGLWidget, QMainWindow, QListWidgetItem, QApplication, QLabel, 
    QFileDialog, QPushButton, QSizePolicy, QDialog, QCheckBox, QScrollArea
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from functions import *


import multiprocessing
import trimesh
def run_pyglet_viewer(mesh, my_list):
    try:
        print("SHOWING PYGLET")
        # If you want to display the mesh using Pyglet:
        combined_mesh = combine_mesh(mesh, my_list)  # Make sure this function is defined correctly
        combined_mesh.show()  # This uses Pyglet for rendering
    except Exception as e:
        print(f"Error: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the main UI from the 'main.ui'
        loadUi("main.ui", self)

        # Create the OpenGL widget (model_viewer)
        self.model_viewer = self.findChild(QOpenGLWidget, "model_viewer")
        self.model_viewer.setStyleSheet("background-color: gray;")

        # Create the property window on top of OpenGL
        self.create_property_window()

        # Show the main window
        self.show()

        self.import_button = self.findChild(QPushButton, "import_button")
        self.import_button.clicked.connect(self.import_file)

        self.export_button = self.findChild(QPushButton, "export_button")
        self.export_button.clicked.connect(self.export_file)

        self.object_list = self.findChild(QListWidget, "object_list")
        
        self.group_list = self.findChild(QListWidget, "group_list")
        #self.add_group_item = QListWidgetItem("Add Group")
        #self.group_list.addItem(self.add_group_item)
        
        # Create a dictionary to store the selected objects for each group
        self.group_objects = {}

        # Track all selected objects across groups
        self.selected_objects_all_groups = set()

        # Connect single-click to handle the "Add Group" item
        self.group_list.itemClicked.connect(self.on_group_item_clicked)
        
        # Enable custom context menu on the list widget
        self.group_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.group_list.customContextMenuRequested.connect(self.show_context_menu)
        
        self.object_list_label = self.findChild(QLabel, "object_list_label")
        self.group_list_label = self.findChild(QLabel, "group_list_label")

    def show_context_menu(self, position):
        # Get the item at the clicked position
        selected_item = self.group_list.itemAt(position)
        
        # Only show the context menu if an item (not "Add Group") is right-clicked
        if selected_item and selected_item != self.add_group_item:
            context_menu = QMenu(self)
            
            # Add "Remove" action to the context menu
            remove_action = context_menu.addAction("Remove")
            add_objects_action = context_menu.addAction("Add Objects")
            rename_action = context_menu.addAction("Rename")
            preview_action = context_menu.addAction("Preview")
            
            # Execute the context menu at the cursor position
            action = context_menu.exec_(self.group_list.mapToGlobal(position))
            
            # Handle the "Remove" action
            if action == remove_action:
                reply = QMessageBox.question(
                    self, "Remove Group", f"Are you sure you want to remove '{selected_item.text()}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    group_name = selected_item.text()
                    # Remove the selected item
                    self.group_list.takeItem(self.group_list.row(selected_item))
                    # Also remove the group from the dictionary
                    objects_in_group = self.group_objects.pop(group_name, [])
                    
                    # Add objects from the removed group back to the available objects
                    for obj in objects_in_group:
                        self.selected_objects_all_groups.discard(obj)  # Remove from selected objects list
                    print(f"Group '{group_name}' has been removed, and its objects are now available for selection.")

            # Handle the "Add Objects" action
            elif action == add_objects_action:
                self.show_add_objects_dialog(selected_item)

            # Handle the "Rename" action
            elif action == rename_action:
                new_name, ok = QInputDialog.getText(self, "Rename Group", "Enter new name for the group:", text=selected_item.text())
                if ok and new_name:
                    selected_item.setText(new_name)
                    # Update the group_objects dictionary to reflect the renamed group
                    if selected_item.text() in self.group_objects:
                        self.group_objects[new_name] = self.group_objects.pop(selected_item.text())
                elif not new_name:
                    QMessageBox.warning(self, "Warning", "Group name cannot be empty.")

            elif action == preview_action:
                print("PREVIEWING THE GROUP")
                group_objects = self.group_objects.get(group_name, [])
                if group_objects != []:
                    int_list = [int(item) for item in group_objects]
                    new_mesh = combine_mesh(self.loaded_mesh, int_list)
                    viewer_process = multiprocessing.Process(target=run_pyglet_viewer, args=(self.loaded_mesh, int_list))
                    viewer_process.start()
                    # Ensure new_mesh is a top-level window and movable
                    #ew_mesh.setWindowFlags(Qt.Window)  # Make it a top-level window
                    #new_mesh.show()
                else:
                    print("group empty")

    def show_add_objects_dialog(self, selected_item):
        # Get the group name
        group_name = selected_item.text()

        # Get all the objects already added to the group
        selected_objects_in_group = set(self.group_objects.get(group_name, []))

        # Create a dialog to select multiple objects from the object_list
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Objects to Add")

        layout = QVBoxLayout(dialog)

        # Create a scrollable area for checkboxes
        scroll_area = QScrollArea(dialog)
        scroll_area.setWidgetResizable(True)
        checkbox_widget = QWidget(scroll_area)
        scroll_area.setWidget(checkbox_widget)
        checkbox_layout = QVBoxLayout(checkbox_widget)

        # Store checkboxes for selected objects
        checkboxes = {}

        # Create checkboxes for each object in the object list, but only for unselected ones across all groups
        for row in range(self.object_list.count()):
            object_item = self.object_list.item(row)
            object_text = object_item.text()

            # If the object is not already selected across any groups, show it, otherwise, don't show it
            if object_text not in self.selected_objects_all_groups or object_text in selected_objects_in_group:
                checkbox = QCheckBox(object_text, checkbox_widget)
                # If the object is already selected for the group, pre-check the box
                checkbox.setChecked(object_text in selected_objects_in_group)
                checkbox_layout.addWidget(checkbox)
                checkboxes[checkbox] = object_text

        layout.addWidget(scroll_area)

        # Add a button to confirm the selection
        confirm_button = QPushButton("Confirm", dialog)
        confirm_button.clicked.connect(lambda: self.add_selected_objects(group_name, checkboxes))
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def add_selected_objects(self, group_name, checkboxes):
        # Get the selected objects (those that are checked)
        selected_objects = [obj for checkbox, obj in checkboxes.items() if checkbox.isChecked()]
        
        # If no objects are selected (i.e., all checkboxes are unchecked)
        if not selected_objects:
            # If we uncheck everything, clear the group (empty list)
            self.group_objects[group_name] = []
            print(f"Group '{group_name}' now has no objects.")
        else:
            # If there are selected objects, update the group with them
            self.group_objects[group_name] = selected_objects

        # Update the global list of selected objects to reflect the changes
        self.selected_objects_all_groups = set()  # Clear the global list

        # Rebuild the global list of selected objects (this list should now reflect all selected objects in the groups)
        for group in self.group_objects.values():
            self.selected_objects_all_groups.update(group)

        # Optionally, print the updated objects in the group
        print(f"Objects added/removed in '{group_name}': {selected_objects}")

        ########## CHECKING
        available_objects = []

        # Iterate through the object list and check if the object is not selected in any group
        for i in range(self.object_list.count()):
            object_name = self.object_list.item(i).text()
            if object_name not in self.selected_objects_all_groups:
                available_objects.append(object_name)

        # Print the available (unassigned) objects
        print(f"Available (unassigned) objects: {available_objects}")

        print(f"available: ")
        print(f"selected objects: {self.selected_objects_all_groups}")
        print(f"groups: {self.group_objects}")


    def on_group_item_clicked(self, item):
        # Only handle the "Add Group" item for adding new groups
        if item == self.add_group_item:
            new_group_name, ok = QInputDialog.getText(self, "Add Group", "Enter new group name:")
            if ok and new_group_name:
                # Check if the group already exists in the list
                group_names = [self.group_list.item(i).text() for i in range(self.group_list.count())]
                if new_group_name in group_names:
                    QMessageBox.warning(self, "Duplicate Group", "A group with this name already exists.")
                else:
                    # Add the new group as an item in the list
                    self.group_list.addItem(new_group_name)
                    self.group_objects[new_group_name] = []  # Initialize an empty list for this group
            elif not new_group_name:
                QMessageBox.warning(self, "Warning", "Group name cannot be empty.")
        
        if item != self.add_group_item:
            group_name = item.text()  # Get the name of the selected group
            
            # Get the objects associated with this group from the dictionary
            group_objects = self.group_objects.get(group_name, [])
            print(f"Group '{group_name}' contains the following objects: {group_objects}")
            self.preview_group(group_objects)

    def preview_group(self, group_objects):
        print("PREVIEWING THE GROUP")

        if group_objects != []:
            int_list = [int(item) for item in group_objects]
            new_mesh = combine_mesh(self.loaded_mesh, int_list)
            viewer_process = multiprocessing.Process(target=run_pyglet_viewer, args=(self.loaded_mesh, int_list))
            viewer_process.start()
            # Ensure new_mesh is a top-level window and movable
            #ew_mesh.setWindowFlags(Qt.Window)  # Make it a top-level window
            #new_mesh.show()
        else:
            print("group empty")




    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Wavefront OBJ Files (*.obj)")
        self.loaded_mesh = load_mesh(file_path)
        self.loaded_groups = generate_list(self.loaded_mesh)
        self.object_list.clear()  # Removes all items from the object_list
        for current in self.loaded_groups:
            self.object_list.addItem(str(current))
        
        if self.selected_objects_all_groups != None:
            print(self.selected_objects_all_groups)
            print("SAVE FIRST")
            self.selected_objects_all_groups.clear()
            self.group_list.clear()
            
            self.add_group_item = QListWidgetItem("Add Group")
            self.group_list.addItem(self.add_group_item)
        
        


    def export_file(self):
        view_mesh(self.loaded_mesh, [0, 19])

    def create_property_window(self):
        """Create the floating property window on the top-right corner."""
        self.property_window = QWidget(self)
        loadUi("property_window.ui", self.property_window)
        opengl_geometry = self.model_viewer.geometry()
        property_window_width, property_window_height = 409, 139
        x_position = opengl_geometry.right() - property_window_width
        y_position = opengl_geometry.top()
        self.property_window.setGeometry(x_position+240, y_position+25, property_window_width, property_window_height)
        self.property_window.setStyleSheet("background-color: rgba(255, 255, 255, 230);")
        self.property_window.raise_()
        self.property_window.show()

    def set_openGL_info(self, object_num, group_num):
        """Function to update the property window information."""
        object_label = self.property_window.findChild(QLabel, "object_number")
        group_label = self.property_window.findChild(QLabel, "group_number")
        if object_label and group_label:
            object_label.setText(str(object_num))
            group_label.setText(str(group_num))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.set_openGL_info(1, 2)
    sys.exit(app.exec_())
