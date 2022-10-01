# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# import sys

# # QT application
# # QT Main window
# # event loop
# # add widgets

# class MyDialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(MyDialog, self).__init__(*args, **kwargs)
#         self.setWindowTitle("Dialog")

#         QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
#         self.buttonBox = QDialogButtonBox(QBtn)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)

#         layout = QVBoxLayout()
#         layout.addWidget(self.buttonBox)
#         self.setLayout(layout)


# class MainWindow(QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)

#         self.setWindowTitle("AZlyrics")
#         toolbar = QToolBar("Menu")
#         self.setIconSize(QSize(16,16))
#         self.addToolBar(toolbar)

#         # QAction
#         button_action = QAction(QIcon("bug.png"),"CLICK", self)
#         button_action.setStatusTip("This is a button")
#         button_action.triggered.connect(self.when_toolbar_btn_clicked)
#         button_action.setCheckable(True)
#         self.setStatusBar(QStatusBar(self))

#         # add qaction to toolbar
#         toolbar.addAction(button_action)
#         toolbar.addWidget(QLabel('Hello'))
#         toolbar.addWidget(QCheckBox())

#         # file menu
#         menu = self.menuBar()
#         file_menu = menu.addMenu(u'&File')
#         file_menu.addAction(button_action)
#         file_menu.addSeparator()
#         submenu = file_menu.addMenu("Submenu")

#         # QAction
#         button_action2 = QAction(QIcon("bug.png"),"CLICK", self)
#         button_action2.setStatusTip("This is a button")
#         button_action2.triggered.connect(self.when_toolbar_btn_clicked)
#         button_action2.setCheckable(True)
#         self.setStatusBar(QStatusBar(self))
#         submenu.addAction(button_action2)

#     def when_toolbar_btn_clicked(self, s):
#         print("Button clicked", s)
#         dlg = MyDialog(self)
#         if dlg.exec_():
#             print("Success")
#         else:
#             print("Fail")

# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec_()

# import dearpygui.dearpygui as dpg

# dpg.create_context()
# dpg.create_viewport(title='Operating system viewport', width=640, height=480)

# def print_input():
#     print(dpg.get_value("userinpt"))

# with dpg.font_registry():
#     default_font = dpg.add_font("myfont.otf", 20)
#     fallback_font = dpg.add_font("myfont.otf",10)

# with dpg.window(label="Mywindow",width=640, height=480):
#     dpg.add_text("Name",)
#     dpg.add_input_text(default_value='Spider1', tag='userinpt',indent=50, width=100)
#     dpg.add_button(label="show",callback=print_input)

#     dpg.bind_font(default_font)


# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()
