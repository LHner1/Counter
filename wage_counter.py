import sys
import time
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTimeEdit
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtGui import QColor

class WageCounter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.is_running = False
        self.total_earnings = 0.0
        self.hourly_wage = 0.0
        self.elapsed_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)
        self.timer.setInterval(1000)  # Update every second
        
    def initUI(self):
        self.setWindowTitle('Wage Counter')
        self.setGeometry(300, 300, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        

        wage_layout = QHBoxLayout()
        wage_label = QLabel('Stundenlohn (€):')
        self.wage_input = QLineEdit()
        self.wage_input.setPlaceholderText('z.B. 15.50')
        wage_layout.addWidget(wage_label)
        wage_layout.addWidget(self.wage_input)
        main_layout.addLayout(wage_layout)
        

        start_time_layout = QHBoxLayout()
        start_time_label = QLabel('Startzeit:')
        self.start_time_input = QTimeEdit()
        self.start_time_input.setDisplayFormat("HH:mm")
        self.start_time_input.setTime(QTime.currentTime())
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(self.start_time_input)
        main_layout.addLayout(start_time_layout)
        

        button_layout = QHBoxLayout()
        self.start_button = QPushButton('Start')
        self.stop_button = QPushButton('Stop')
        self.reset_button = QPushButton('Reset')
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(True)
        
        self.start_button.clicked.connect(self.start_counting)
        self.stop_button.clicked.connect(self.stop_counting)
        self.reset_button.clicked.connect(self.reset_counter)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        main_layout.addLayout(button_layout)
        
        # Earings display
        earnings_layout = QVBoxLayout()
        self.earnings_label = QLabel('+0.00 €')
        self.earnings_label.setAlignment(Qt.AlignCenter)
        self.earnings_label.setStyleSheet('font-size: 24px; font-weight: bold; margin-top: 20px; color: green;')
        earnings_layout.addWidget(self.earnings_label)
        
        # Timer display
        self.timer_label = QLabel('Zeit: 00:00:00')
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet('font-size: 18px; margin-top: 10px;')
        earnings_layout.addWidget(self.timer_label)
        
        main_layout.addLayout(earnings_layout)
        
    def start_counting(self):
        # Get wage from input
        try:
            self.hourly_wage = float(self.wage_input.text().replace(',', '.'))
            if self.hourly_wage <= 0:
                raise ValueError("Stundenlohn muss größer als 0 sein")
        except ValueError:
            self.earnings_label.setText("Bitte gültigen Stundenlohn eingeben!")
            return
        
        # Get start time from input
        start_time = self.start_time_input.time()
        current_time = QTime.currentTime()
        
        # Calculate seconds elapsed since start time if start time is earlier today
        if start_time < current_time:
            start_seconds = start_time.hour() * 3600 + start_time.minute() * 60 + start_time.second()
            current_seconds = current_time.hour() * 3600 + current_time.minute() * 60 + current_time.second()
            self.elapsed_seconds = current_seconds - start_seconds
            
            # Calculate initial earnings
            earnings_per_second = self.hourly_wage / 3600
            self.total_earnings = self.elapsed_seconds * earnings_per_second
            

            self.earnings_label.setText(f'+{self.total_earnings:.2f} €')
            hours = self.elapsed_seconds // 3600
            minutes = (self.elapsed_seconds % 3600) // 60
            seconds = self.elapsed_seconds % 60
            self.timer_label.setText(f'Zeit: {hours:02d}:{minutes:02d}:{seconds:02d}')
        
        self.is_running = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.wage_input.setEnabled(False)
        self.start_time_input.setEnabled(False)
        
        self.timer.start()
        
    def stop_counting(self):
        self.timer.stop()
        self.is_running = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.wage_input.setEnabled(True)
        self.start_time_input.setEnabled(True)
        
    def reset_counter(self):
        self.total_earnings = 0.0
        self.elapsed_seconds = 0
        
        self.earnings_label.setText(f'+0.00 €')
        self.timer_label.setText('Zeit: 00:00:00')
        
        self.start_time_input.setTime(QTime.currentTime())
        
    def update_counter(self):
        self.elapsed_seconds += 1
        
        # Calculate earnings per second (hourly wage / 3600)
        earnings_per_second = self.hourly_wage / 3600
        self.total_earnings += earnings_per_second
        
        self.earnings_label.setText(f'+{self.total_earnings:.2f} €')
        
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        self.timer_label.setText(f'Zeit: {hours:02d}:{minutes:02d}:{seconds:02d}')
        
def main():
    app = QApplication(sys.argv)
    window = WageCounter()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
