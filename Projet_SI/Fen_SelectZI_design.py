# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fen_SelectZI_design.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Fen_SelectZI_Dialog(object):
    def setupUi(self, Fen_SelectZI_Dialog):
        Fen_SelectZI_Dialog.setObjectName("Fen_SelectZI_Dialog")
        Fen_SelectZI_Dialog.resize(554, 498)
        self.buttonBox = QtWidgets.QDialogButtonBox(Fen_SelectZI_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 450, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtWidgets.QFrame(Fen_SelectZI_Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 20, 511, 411))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(1, 4, 511, 401))
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(Fen_SelectZI_Dialog)
        self.buttonBox.accepted.connect(Fen_SelectZI_Dialog.accept)
        self.buttonBox.rejected.connect(Fen_SelectZI_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Fen_SelectZI_Dialog)

    def retranslateUi(self, Fen_SelectZI_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Fen_SelectZI_Dialog.setWindowTitle(_translate("Fen_SelectZI_Dialog", "Selectionner une zone d\'interet"))

