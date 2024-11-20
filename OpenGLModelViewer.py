import sys
import trimesh
import pyglet
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from glooey import Button, Label, Frame

# Create a custom QWidget to hold the trimesh viewer
class TrimeshViewerWidget(QWidget):
    def __init__(self, mesh):
        super().__init__()
        self.mesh = mesh
        self.viewer = mesh.show()

    def closeEvent(self, event):
        # Close the pyglet window when the widget is closed
        pyglet.app.exit()
        event.accept()

# Create the main window for Glooey
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Trimesh Viewer with Glooey')
        
        # Create a layout for the main window
        layout = QVBoxLayout()

        # Load a mesh
        mesh = trimesh.load_mesh('2Body.obj')

        # Create a trimesh viewer widget
        self.trimesh_widget = TrimeshViewerWidget(mesh)

        # Add the trimesh widget to the layout
        layout.addWidget(self.trimesh_widget)

        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize Glooey widgets
        label = Label('Trimesh Viewer')
        button = Button('Close Viewer')

        # Create a frame and add widgets
        frame = Frame()
        frame.add_widget(label)  # Use 'add_widget' instead of 'add_child'
        frame.add_widget(button)

        # Add the frame to the layout
        layout.addWidget(frame)

# Main entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create the main window and show it
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
