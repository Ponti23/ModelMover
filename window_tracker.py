import sys
from PyQt5.QtWidgets import (
    QVBoxLayout, QMenu, QMessageBox, QInputDialog, QWidget, QListWidget,
    QOpenGLWidget, QMainWindow, QListWidgetItem, QApplication, QLabel,
    QFileDialog, QPushButton, QSizePolicy, QDialog, QCheckBox, QScrollArea
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

import multiprocessing
import trimesh

# Function to display the viewer using Pyglet
def run_pyglet_viewer(file_path):
    try:
        print("SHOWING PYGLET")
        mesh = trimesh.load(file_path)
        mesh.show()  # Display using Pyglet
    except Exception as e:
        print(f"Error: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)  # Load UI
        self.show()

        # Find and connect buttons
        self.import_button = self.findChild(QPushButton, "import_button")
        self.import_button.clicked.connect(self.import_file)

        # Dictionary to track active viewer processes
        self.viewer_processes = {}

    def import_file(self):
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Wavefront OBJ Files (*.obj)")
        if file_path:
            # Check if there's an existing process for this file
            if file_path in self.viewer_processes:
                existing_process = self.viewer_processes[file_path]
                if existing_process.is_alive():
                    print(f"Terminating existing viewer for {file_path}.")
                    existing_process.terminate()
                    existing_process.join()

            # Start a new viewer process for the file
            new_process = multiprocessing.Process(target=run_pyglet_viewer, args=(file_path,))
            new_process.start()
            self.viewer_processes[file_path] = new_process

            print(self.viewer_processes)

    def close_all_viewers(self):
        """Terminate all active viewer processes."""
        for file_path, process in self.viewer_processes.items():
            if process.is_alive():
                print(f"Terminating viewer for {file_path}.")
                process.terminate()
                process.join()
        self.viewer_processes.clear()

    def closeEvent(self, event):
        """Ensure cleanup of processes when the main window closes."""
        self.close_all_viewers()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
