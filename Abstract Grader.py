import sys
import configparser
import os
import random
import pandas as pd

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QLabel, QFrame, QSizePolicy, QDialog, 
                               QLineEdit, QDialogButtonBox, QTextEdit, QFileDialog, QComboBox, QMessageBox, QSpacerItem, QProgressBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Define the path for the .ini file in the same directory as the script
config_path = os.path.join(os.path.dirname(__file__), 'settings.ini')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.csv_data = None  # Initialize csv_data as None
        self.unsaved_changes = False  # Flag to track unsaved changes
        self.save_in_progress = False  # Flag to track if save operation is in progress
        self.initUI()
        self.load_settings()

    def initUI(self):
        # Get screen size
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        max_width = screen_size.width()  # Set maximum width to 80% of screen width

        # Set the window title, size, and maximum width
        self.setWindowTitle("Abstract Grader v0.5")
        self.setGeometry(100, 100, 800, 600)
        self.setMaximumWidth(max_width)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a main vertical layout to hold the top bar and other content
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the top bar
        options_layout = QHBoxLayout()

        # Create buttons for the top bar
        load_button = QPushButton("Load File")
        load_button.clicked.connect(self.load_csv)
        options_button = QPushButton("Options")
        options_button.clicked.connect(self.show_options_window)
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_csv)

        # Add buttons to the horizontal layout
        options_layout.addWidget(load_button)
        options_layout.addWidget(options_button)
        options_layout.addWidget(save_button)

        # Set stretch factors to make buttons fill the width equally
        options_layout.setStretch(0, 1)  # Save File button
        options_layout.setStretch(1, 1)  # Options button
        options_layout.setStretch(2, 1)  # Load File button

        # Add the top bar layout to the main vertical layout
        main_layout.addLayout(options_layout)

        # Create a "Title" label
        title_label = QLabel("Title")
        title_label.setFont(QFont("Arial", weight=QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        # Set QSizePolicy to fixed vertically so it does not stretch
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(title_label)

        # Create label_1 inside a QFrame to allow recolouring
        cont_title_frame = QFrame()
        cont_title_frame.setFrameShape(QFrame.Box)
        cont_title_frame.setStyleSheet("background-color: lightgray;")
        cont_title_layout = QVBoxLayout()
        self.cont_title = QLabel("Initial Text 1")
        self.cont_title.setStyleSheet("color: black;")
        self.cont_title.setWordWrap(True)
        cont_title_layout.addWidget(self.cont_title)
        cont_title_frame.setLayout(cont_title_layout)
        cont_title_frame.setFixedHeight(50)  # Approx. two rows of text
        cont_title_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(cont_title_frame)

        # Create an "Abstract" label
        abstract_label = QLabel("Abstract")
        abstract_label.setFont(QFont("Arial", weight=QFont.Bold))
        abstract_label.setAlignment(Qt.AlignCenter)
        # Set QSizePolicy to fixed vertically so it does not stretch
        abstract_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(abstract_label)

        # Create label_2 inside a QFrame to allow recolouring + stretch
        cont_abstract_frame = QFrame()
        cont_abstract_frame.setFrameShape(QFrame.Box)
        cont_abstract_frame.setStyleSheet("background-color: lightgray;")
        cont_abstract_layout = QVBoxLayout()
        self.cont_abstract = QLabel("Initial Text 2")
        self.cont_abstract.setStyleSheet("color: black;")
        self.cont_abstract.setWordWrap(True)
        cont_abstract_layout.addWidget(self.cont_abstract)
        cont_abstract_frame.setLayout(cont_abstract_layout)
        cont_abstract_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(cont_abstract_frame)

        # Create an "Abstract" label
        rq_label = QLabel("Research Question")
        rq_label.setFont(QFont("Arial", weight=QFont.Bold))
        rq_label.setAlignment(Qt.AlignCenter)
        # Set QSizePolicy to fixed vertically so it does not stretch
        rq_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(rq_label)

        # Create rq_label inside a QFrame to allow recolouring
        cont_rq_frame = QFrame()
        cont_rq_frame.setFrameShape(QFrame.Box)
        cont_rq_frame.setStyleSheet("background-color: lightgray;")
        cont_rq_layout = QVBoxLayout()
        self.cont_rq = QLabel("Placeholder Text")
        self.cont_rq.setStyleSheet("color: black;")
        self.cont_rq.setWordWrap(True)
        cont_rq_layout.addWidget(self.cont_rq)
        cont_rq_frame.setLayout(cont_rq_layout)
        cont_rq_frame.setFixedHeight(75)  # Approx. two rows of text
        cont_rq_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(cont_rq_frame)

        answer_layout = QHBoxLayout()
        # Create a QButtonGroup to enforce exclusivity
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        # Create buttons and add them to the button widget and button group
        self.buttons = []
        for i in range(5):
            button = QPushButton(f"Button {i+1}")
            button.setCheckable(True)
            self.button_group.addButton(button)
            answer_layout.addWidget(button)
            self.buttons.append(button)

            # Connect the button's clicked signal to the slot that handles the color change
            button.clicked.connect(self.mono_choice_select)

        # Add the button widget to the central layout
        main_layout.addLayout(answer_layout)

        self.commit_button = QPushButton("Start")
        self.commit_button.setFixedHeight(self.commit_button.sizeHint().height() * 2)  # adjust height to be bigger
        main_layout.addWidget(self.commit_button)
        self.commit_button.clicked.connect(self.handle_commit)

        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)  # Optional: Show percentage in the progress bar
        main_layout.addWidget(self.progress_bar)

        # Set the main layout to the central widget
        central_widget.setLayout(main_layout)

    def show_options_window(self):
        # Get the current button texts
        button_texts = [button.text() for button in self.buttons]

        # Get the current research question text
        rq_text = self.cont_rq.text()

        # Open the options window, passing current texts
        options_window = OptionsWindow(self, button_texts=button_texts, rq_text=rq_text)
        options_window.exec()

    def load_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")

        if file_path:
            try:
                # Load CSV file using pandas
                self.csv_data = pd.read_csv(file_path)
                self.csv_file_path = file_path

                # Open the combined column selection and output dialog
                combined_dialog = ColumnSelectionDialog(self.csv_data.columns)
                if combined_dialog.exec():
                    title_col, abstract_col, output_col = combined_dialog.get_selected_columns()
                    # Store selected columns as instance variables
                    self.title_col = title_col
                    self.abstract_col = abstract_col
                    self.output_col = output_col

                    if output_col not in self.csv_data.columns:
                        # Add new column to the DataFrame
                        self.csv_data[output_col] = None  # Initialize new column with empty values

                else:
                    QMessageBox.warning(self, "Cancelled", "Column selection cancelled.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV file: {str(e)}")

    def save_csv(self):
        if self.csv_data is not None:
            file_dialog = QFileDialog()
            save_path, _ = file_dialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
            if save_path:
                try:
                    # Save the data to a new CSV file
                    self.csv_data.to_csv(save_path, index=False)
                    QMessageBox.information(self, "File Saved", f"File saved successfully to {save_path}")
                    self.unsaved_changes = False
                    self.save_in_progress = False
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save CSV file: {str(e)}")
        else:
            QMessageBox.warning(self, "No CSV Loaded", "Please load a CSV file before saving.")

    def update_button_texts(self, texts):
        # Remove buttons that don't have corresponding text
        for i, button in enumerate(self.buttons):
            if i < len(texts):  # Update button text if a non-empty text exists
                button.setText(texts[i])
                button.show()  # Make sure the button is visible
            else:
                button.hide()  # Hide the button if there's no corresponding text
    
    def update_rq_text(self, rq_text):
        self.cont_rq.setText(rq_text)

    def mono_choice_select(self):
        # Reset all buttons to default style
        for button in self.buttons:
            button.setStyleSheet("")
        # Set the selected button's style
        selected_button = self.button_group.checkedButton()
        if selected_button:
            selected_button.setStyleSheet("background-color: lightblue; color: black;")

    def handle_commit(self):
        if self.commit_button.text() == "Start":
            self.load_next_row()
        elif self.commit_button.text() == "Submit score":
            self.submit_score()

         # Reset styles and state
        self.button_group.setExclusive(False) # in exclusive mode, one button HAS TO stay checked apparently
        for button in self.buttons:
            button.setChecked(False)
            button.setStyleSheet("")
        self.button_group.setExclusive(True) # re-enable once all are unchecked, which works somehow

    def load_next_row(self):
        # Find rows where output_col is None
        empty_rows = self.csv_data[self.csv_data[self.output_col].isna()]
        if empty_rows.empty:
            QMessageBox.information(self, "No Rows", "No empty Rows left in CSV.")
            return

        # Randomly pick one row
        self.current_row_index = random.choice(empty_rows.index)
        selected_row = self.csv_data.loc[self.current_row_index]

        # Update QLabel texts
        self.cont_title.setText(selected_row[self.title_col])
        self.cont_abstract.setText(selected_row[self.abstract_col])

        # Change button label
        self.commit_button.setText("Submit score")
        # Update progress bar
        self.update_progress_bar()

    def submit_score(self):
        if self.current_row_index is None:
            print("No row selected.")
            return
        
        # Get the text from the selected button
        selected_button = self.button_group.checkedButton()
        if selected_button is None:
            QMessageBox.warning(self, "Selection", "No Score selected!")
            return
        selected_text = selected_button.text()
        # Update the DataFrame
        self.csv_data.at[self.current_row_index, self.output_col] = selected_text
        self.unsaved_changes = True

        # Load the next row
        self.load_next_row()

    def update_progress_bar(self):
        if self.output_col:
            total_rows = len(self.csv_data)
            non_empty_rows = len(self.csv_data[self.csv_data[self.output_col].notna()])
            self.progress_bar.setMaximum(total_rows)
            self.progress_bar.setValue(non_empty_rows)
            self.progress_bar.setFormat(f"{non_empty_rows}/{total_rows} rows completed")

    def load_settings(self):
        # Load button labels and research question from the .ini file if it exists.
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)

            # Load button labels
            if 'ButtonLabels' in config:
                button_texts = [config['ButtonLabels'].get(f'button_{i+1}', '') for i in range(5)]
                self.update_button_texts([text for text in button_texts if text])

            # Load research question
            if 'ResearchQuestion' in config:
                rq_text = config['ResearchQuestion'].get('rq_text', 'Initial Text 3')
                self.update_rq_text(rq_text)

    def closeEvent(self, event):
        if self.unsaved_changes:
            # Show a confirmation dialog to the user
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         'You have unsaved changes. Do you want to save them before exiting?',
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                         QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.save_in_progress = True  # Set flag indicating save is in progress
                self.save_csv()  # Call the save method
                if self.save_in_progress:  # Check if save was interrupted
                    event.ignore()  # Ignore the close event if save was interrupted
                else:
                    event.accept()  # Proceed with closing the application if save was successful
            elif reply == QMessageBox.Cancel:
                event.ignore()  # Ignore the close event if user cancelled
            else:
                event.accept()  # Proceed with closing the application if user chose to discard
        else:
            event.accept()  # Proceed with closing the application if no unsaved changes

class OptionsWindow(QDialog):
    def __init__(self, parent=None, button_texts=None, rq_text=None):
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.initUI()

        # Pre-fill the inputs with current button labels and research question text
        for i, text in enumerate(button_texts):
            self.btntext_inputs[i].setText(text)  # Fill button texts
        self.rqtext_input.setPlainText(rq_text)  # Fill research question


    def initUI(self):
        # Use a QVBoxLayout to arrange the label, input fields, and button vertically
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Research Question Chunk
        rq_label = QLabel("Research Question:")
        rq_label.setFont(QFont("Arial", weight=QFont.Bold))
        rq_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(rq_label)
        self.rqtext_input = QTextEdit()  # Store as an instance variable
        self.rqtext_input.setFixedHeight(100)
        main_layout.addWidget(self.rqtext_input)

        # Button Text Chunk
        btn_label = QLabel("Category labels:")
        btn_label.setFont(QFont("Arial", weight=QFont.Bold))
        btn_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(btn_label)

        # Create a QHBoxLayout for the text input fields
        btn_layout = QHBoxLayout()
        self.btntext_inputs = []

        for _ in range(5):
            btntext_input = QLineEdit()
            self.btntext_inputs.append(btntext_input)
            btn_layout.addWidget(btntext_input)

        # Add the input layout to the main layout
        main_layout.addLayout(btn_layout)

        # Add the "Confirm" button below the input fields
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.apply_options)
        confirm_button.setFixedHeight(50)
        main_layout.addWidget(confirm_button)

    def apply_options(self):
        rq_text = self.rqtext_input.toPlainText()
        self.parent().update_rq_text(rq_text)

        btntexts = [btntext_input.text() for btntext_input in self.btntext_inputs]
        # Filter out empty inputs
        btntexts_nonempty = [text for text in btntexts if text]
        self.parent().update_button_texts(btntexts_nonempty)

        # Save to the .ini file
        config = configparser.ConfigParser()
        # Create a section for button labels
        config['ButtonLabels'] = {f'button_{i+1}': text for i, text in enumerate(btntexts_nonempty)}
        # Add the research question
        config['ResearchQuestion'] = {'rq_text': rq_text}
        # Write to the settings.ini file
        with open(config_path, 'w') as configfile:
            config.write(configfile)

        self.accept() # Close the dialog

class ColumnSelectionDialog(QDialog):
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Columns and Output Column")
        self.columns = columns
        self.setGeometry(100, 100, 400, 200)

        # Layouts
        layout = QVBoxLayout()

        # Title ComboBox
        self.title_combo = QComboBox()
        self.title_combo.addItems(self.columns)
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Select Title Column:"))
        title_layout.addWidget(self.title_combo)

        # Abstract ComboBox
        self.abstract_combo = QComboBox()
        self.abstract_combo.addItems(self.columns)
        abstract_layout = QHBoxLayout()
        abstract_layout.addWidget(QLabel("Select Abstract Column:"))
        abstract_layout.addWidget(self.abstract_combo)        

        # Existing Column ComboBox
        self.existing_combo = QComboBox()
        self.existing_combo.addItems(self.columns)
        existing_layout = QHBoxLayout()
        existing_layout.addWidget(QLabel("Select Existing Output Column:"))
        existing_layout.addWidget(self.existing_combo)

        # New Column Name Input
        self.new_column_input = QLineEdit()
        new_layout = QHBoxLayout()
        new_layout.addWidget(QLabel("Or Enter New Column Name:"))
        new_layout.addWidget(self.new_column_input)

        # OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Adding widgets to layout
        layout.addLayout(title_layout)
        layout.addLayout(abstract_layout)
        verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(verticalSpacer)
        layout.addLayout(existing_layout)
        layout.addLayout(new_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_selected_columns(self):
        if self.new_column_input.text().strip():
            output = self.new_column_input.text()
        else:
            output = self.existing_combo.currentText()
        return (self.title_combo.currentText(), 
                self.abstract_combo.currentText(), 
                output)


# run app
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
