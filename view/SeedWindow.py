# Form implementation generated from reading ui file 'view/ui/SeedWindow.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(456, 328)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/assets/icons/AVEGA-Favicon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(parent=Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 411, 251))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 30, 391, 211))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.radio_continue_using_seed = QtWidgets.QRadioButton(parent=self.gridLayoutWidget)
        self.radio_continue_using_seed.setObjectName("radio_continue_using_seed")
        self.gridLayout.addWidget(self.radio_continue_using_seed, 3, 0, 1, 1)
        self.radio_old_seed = QtWidgets.QRadioButton(parent=self.gridLayoutWidget)
        self.radio_old_seed.setObjectName("radio_old_seed")
        self.gridLayout.addWidget(self.radio_old_seed, 2, 0, 1, 1)
        self.radio_new_seed = QtWidgets.QRadioButton(parent=self.gridLayoutWidget)
        self.radio_new_seed.setObjectName("radio_new_seed")
        self.gridLayout.addWidget(self.radio_new_seed, 1, 0, 1, 1)
        self.radio_gen_new_seed = QtWidgets.QRadioButton(parent=self.gridLayoutWidget)
        self.radio_gen_new_seed.setChecked(True)
        self.radio_gen_new_seed.setObjectName("radio_gen_new_seed")
        self.gridLayout.addWidget(self.radio_gen_new_seed, 0, 0, 1, 1)
        self.seed_input = QtWidgets.QSpinBox(parent=self.gridLayoutWidget)
        self.seed_input.setObjectName("seed_input")
        self.gridLayout.addWidget(self.seed_input, 1, 1, 1, 1)
        self.old_seed_regenerate = QtWidgets.QSpinBox(parent=self.gridLayoutWidget)
        self.old_seed_regenerate.setObjectName("old_seed_regenerate")
        self.gridLayout.addWidget(self.old_seed_regenerate, 2, 1, 1, 1)
        self.old_seed_continue = QtWidgets.QSpinBox(parent=self.gridLayoutWidget)
        self.old_seed_continue.setObjectName("old_seed_continue")
        self.gridLayout.addWidget(self.old_seed_continue, 3, 1, 1, 1)
        self.line = QtWidgets.QFrame(parent=Form)
        self.line.setGeometry(QtCore.QRect(20, 270, 411, 16))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Form)
        self.buttonBox.setGeometry(QtCore.QRect(270, 290, 161, 24))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "AVEGA Random"))
        self.groupBox.setTitle(_translate("Form", "Enter or select the seed for the pseudorandom number generation"))
        self.radio_continue_using_seed.setText(_translate("Form", "Continue generating a series using a continuation seed"))
        self.radio_old_seed.setText(_translate("Form", "Regenerate a series using an old seed"))
        self.radio_new_seed.setText(_translate("Form", "Enter a new seed"))
        self.radio_gen_new_seed.setText(_translate("Form", "New seed generated by the application"))
