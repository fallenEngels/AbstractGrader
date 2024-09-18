from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QDialog, QLineEdit, QDialogButtonBox, QComboBox, QSpacerItem)

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
