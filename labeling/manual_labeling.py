import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt

FILE = 'edible_test_set'

class LabelingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manual Labeling")
        self.resize(500, 300)

        # Counter at the top
        self.counter = QLabel("1")
        self.counter.setAlignment(Qt.AlignCenter)
        self.counter.setStyleSheet("font-size: 18px;")

        # Text in the center
        self.text_label = QLabel("Example product name")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 24px;")

        # Buttons
        self.true_button = QPushButton("True")
        self.false_button = QPushButton("False")

        self.false_button.clicked.connect(self.on_false_clicked)
        self.true_button.clicked.connect(self.on_true_clicked)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.true_button)
        button_layout.addWidget(self.false_button)

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(self.counter)
        main_layout.addSpacing(30)
        main_layout.addWidget(self.text_label)
        main_layout.addSpacing(30)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        ### load the csv file
        df = pd.read_csv('../data/german_foods.csv', sep=",")

        ### only keep those where edible has been selected as False
        ### then sample 100 items
        df = df[df["edible"]==False]
        self.df = df.sample(100).reset_index(drop=True)

        ### create a new column for the manual label
        self.df["manual_label"] = None
        self.current_idx = 0
        self.len = len(self.df)

        ### update the text
        self.update_text(self.df.loc[0, "product_name"])

    def get_next_item(self):
        next_item = self.df.loc[self.current_idx, "product_name"]
        return next_item
    
    def update_counter(self):
        self.counter.setText(str(self.current_idx + 1))
    
    def update_text(self, text):
        self.text_label.setText(text)

    def set_label(self, label):
        self.df.loc[self.current_idx, "manual_label"] = label

    def on_click(self, label):
        self.set_label(label)
        self.current_idx += 1

        if self.current_idx >= self.len:
            columns =[col for col in list(self.df) if 'unnamed' in col.lower()] + ["categories", "countries", "german_name", "edible"]
            self.df = self.df.drop(columns=columns)
            self.df.to_csv(
                f"../data/{FILE}.csv"
            )
            self.update_text("Done")

        else:

            next_item = self.get_next_item()
            self.update_text(next_item)
            self.update_counter()

    def on_false_clicked(self):
        self.on_click(False)

    def on_true_clicked(self):
        self.on_click(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LabelingWindow()
    window.show()

    sys.exit(app.exec_())