
from PyQt6.QtWidgets import QMainWindow ,QApplication,QPushButton
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis
from untitled_ui import Ui_MainWindow

from untitled_ui import Ui_MainWindow

class MyAPP(Ui_MainWindow ,QMainWindow):
    def __init__(self):
        super(MyAPP ,self).__init__()
        self.setupUi(self)
        # button = QPushButton(self.centralwidget ,text='hello')

        #self.pushButton.clicked.connect(self.click_me)
    
#    def click_me(self):
        #print('hello')

        # Create a chart
        chart = QChart()

        # Create a bar series
        series = QBarSeries()

        # Create a set of bars
        set0 = QBarSet('Series 1')
        set0.append([1, 2, 3, 4, 5])  # Sample data

        # Add the set to the series
        series.append(set0)

        # Add the series to the chart
        chart.addSeries(series)

        # Create axes
        axisX = QValueAxis()
        axisY = QValueAxis()

        # Add axes to the chart
        chart.addAxis(axisX, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axisY, QtCore.Qt.AlignmentFlag.AlignLeft)

        # Attach the axes to the series
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        # Create a chart view and set the chart
        chartView = QChartView(chart)
        chartView.setGeometry(QtCore.QRect(120, 70, 511, 371))  # Set the geometry to match the label

        # Add the chart view to the layout
        layout.addWidget(chartView)


if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    myapp = MyAPP()
    myapp.show()
    sys.exit(app.exec())