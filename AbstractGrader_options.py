import configparser

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QLineEdit, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class OptionsWindow(QDialog):
    def __init__(self, parent=None, button_texts=None, rq_text=None, config_path = None):
        super().__init__(parent)
        self.setWindowTitle("Options")
        self.initUI()
        self.config_path = config_path

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
        self.rqtext_input.setFixedHeight(65)
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
        config['ButtonLabels'] = {f'button_{i+1}': text for i, text in enumerate(btntexts)}
        # Add the research question
        config['ResearchQuestion'] = {'rq_text': rq_text}
        # Write to the settings.ini file
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

        self.accept() # Close the dialog
