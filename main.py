import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QComboBox, QPushButton, QTextEdit, QVBoxLayout, 
                             QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt

# --------------------------Core Interference Logic--------------------------
# 1. Multiple groups of invisible interference character pools (anti-background detection)
INVISIBLE_CHAR_POOLS = {
    "Basic Pool": ["\u200B", "\u200C", "\u200D"],
    "Expansion Pool": ["\u00A0", "\u0009", "\u200E"],
    "Spare Pool": ["\u202F", "\u2060", "\uFEFF"]
}

# 2. Interference intensity configuration (corresponding to dropdown options)
INTERFERENCE_LEVELS = {
    "Mild Interference": {"Interval": 5, "Implantation Probability": 0.2, "Character Pool": ["Basic Pool"]},
    "Moderate Interference": {"Interval": 3, "Implantation Probability": 0.5, "Character Pool": ["Basic Pool", "Expansion Pool"]},
    "Severe interference": {"Interval": 2, "Implantation Probability": 0.8, "Character Pool": ["Basic Pool", "Expansion Pool", "Spare Pool"]}
}

# 3. Invalid insertion position filtering (punctuation, spaces, etc.)
INVALID_POS_CHARS = r"""!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ 　\t\n\r"""

def get_random_invisible_char(used_pools):
    """Randomly select invisible characters from the specified character pool."""
    all_chars = []
    for pool_name in used_pools:
        all_chars.extend(INVISIBLE_CHAR_POOLS[pool_name])
    return random.choice(all_chars)

def is_valid_insert_pos(prev_char, next_char):
    """Determine whether it is suitable to insert invisible characters."""
    if prev_char in INVALID_POS_CHARS or next_char in INVALID_POS_CHARS:
        return False
    return True

def insert_adaptive_invisible_traps(text, interference_cfg):
    """Adaptive insertion of invisible characters (core logic)"""
    if not text.strip():
        return ""
    
    interval = interference_cfg["Interval"]
    prob = interference_cfg["Implantation Probability"]
    used_pools = interference_cfg["Character Pool"]
    
    result = list(text)
    char_count = 0
    insert_positions = []
    
    # Mark insertable position
    for i in range(1, len(result)):
        prev_char = result[i-1]
        next_char = result[i]
        if is_valid_insert_pos(prev_char, next_char):
            char_count += 1
            if char_count % interval == 0 and random.random() < prob:
                insert_positions.append(i)
    
    # Reverse order insertion (avoid position offset)
    for pos in reversed(insert_positions):
        result.insert(pos, get_random_invisible_char(used_pools))
    
    # Add a random tag at the end of the sentence.
    end_mark = "".join([get_random_invisible_char(used_pools) for _ in range(2)])
    return "".join(result) + " " + end_mark

# --------------------------GUI Interface--------------------------
class AntiAIToolGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # 1. Basic window settings
        self.setWindowTitle("Antibody: Invisible Anti-AI Training Tool")
        self.resize(1024, 780)
        
        # 2. Layout management (Vertical layout: arranging components from top to bottom)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --------------------------Component 1: Raw Input Area--------------------------
        input_label = QLabel("1. Enter the original content (which may include specific information):")
        input_label.setStyleSheet("font-weight: bold;")
        
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("For example: I want to book a flight from Berlin to Los Angeles at 9 o'clock tomorrow, can you help me check the schedule?")
        self.input_edit.setStyleSheet("padding: 8px; font-size: 14px;")
        
        # Add to the main layout
        main_layout.addWidget(input_label)
        main_layout.addWidget(self.input_edit)
        
        # --------------------------Component 2: Interference Intensity Selection Area--------------------------
        level_layout = QHBoxLayout()  # Horizontal Layout (Labels and Dropdowns Side by Side)
        
        level_label = QLabel("2. Select interference intensity:")
        level_label.setStyleSheet("font-weight: bold;")
        
        self.level_combo = QComboBox()  # Dropdown menu
        # Add interference intensity options (corresponding to the key of INTERFERENCE_LEVELS)
        self.level_combo.addItems(["Mild Interference", "Moderate Interference", "Severe interference"])
        self.level_combo.setStyleSheet("padding: 8px; font-size: 14px;")
        
        # Add components to horizontal layout
        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_combo)
        level_layout.addStretch()
        
        # Add to the main layout
        main_layout.addLayout(level_layout)
        
        # --------------------------Component 3: Result Preview Area--------------------------
        result_label = QLabel("3. Processing results (including invisible interference, can be submitted directly):")
        result_label.setStyleSheet("font-weight: bold;")
        
        self.result_edit = QTextEdit()  # Multi-line text box (convenient for viewing long results)
        self.result_edit.setReadOnly(True)  # Read-only (to avoid unintended modifications)
        self.result_edit.setStyleSheet("padding: 8px; font-size: 14px;")
        self.result_edit.setPlaceholderText("Click 'Processing content' to display the results...")
        
        # Add to the main layout
        main_layout.addWidget(result_label)
        main_layout.addWidget(self.result_edit)
        
        # --------------------------Component 4: Function Button Area--------------------------
        btn_layout = QHBoxLayout()  # Horizontal layout (buttons side by side)
        
        # Processing button
        self.process_btn = QPushButton("Processing content")
        self.process_btn.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 4px; 
            font-size: 14px;
        """)
        self.process_btn.clicked.connect(self.process_input)
        
        # Copy button
        self.copy_btn = QPushButton("Copy result")
        self.copy_btn.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 4px; 
            font-size: 14px;
        """)
        self.copy_btn.clicked.connect(self.copy_result)
        self.copy_btn.setEnabled(False)  # Initially disabled (cannot copy when there are no results)
        
        # Add button to horizontal layout
        btn_layout.addWidget(self.process_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)
        
        # --------------------------Component 5: Information Prompt Area--------------------------
        tip_label = QLabel("Tip: The processed result appears consistent with the original input, you can copy and paste it into the chat box/input box for use.")
        tip_label.setStyleSheet("color: #666; font-size: 12px;")
        tip_label.setAlignment(Qt.AlignCenter)
        
        main_layout.addWidget(tip_label)
        
        self.setLayout(main_layout)
    
    def process_input(self):
        """Process input: Generate results with invisible interference based on the selected intensity."""
        # 1. Get the user's input and the selected intensity.
        raw_input = self.input_edit.text().strip()
        selected_level = self.level_combo.currentText()
        
        # 2. Validate input (prompt if empty)
        if not raw_input:
            QMessageBox.warning(self, "Tip", "Please enter the original content first!", QMessageBox.Ok)
            return
        
        # 3. Call the core logic processing
        interference_cfg = INTERFERENCE_LEVELS[selected_level]
        processed_result = insert_adaptive_invisible_traps(raw_input, interference_cfg)
        
        # 4. Display results and enable the copy button.
        self.result_edit.setText(processed_result)
        self.copy_btn.setEnabled(True)
    
    def copy_result(self):
        """Copy the result to the clipboard"""
        processed_result = self.result_edit.toPlainText().strip()
        if not processed_result:
            QMessageBox.warning(self, "Tip", "No results to copy!", QMessageBox.Ok)
            return
        
        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(processed_result)
        
        # Copy successful
        QMessageBox.information(self, "Tip", "The result has been successfully copied to the clipboard!", QMessageBox.Ok)

# --------------------------Start GUI--------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tool_gui = AntiAIToolGUI()
    tool_gui.show()
    sys.exit(app.exec_())
