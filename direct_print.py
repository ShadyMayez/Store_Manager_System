"""
direct_print.py - طباعة الفواتير مباشرة إلى الطابعة - النسخة المحدثة
"""
import os
from typing import Dict
from datetime import datetime

# استخدام المولد العربي الجديد
from arabic_receipt_generator_new import ArabicReceiptGenerator

from PyQt6.QtWidgets import QMessageBox, QTextEdit, QDialog, QVBoxLayout, QPushButton
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QTextDocument, QFont, QPageSize
from PyQt6.QtCore import Qt, QMarginsF
from PyQt6.QtWidgets import QHBoxLayout


class DirectPrinter:
    """طباعة الفواتير مباشرة إلى الطابعة"""
    
    @staticmethod
    def print_receipt(receipt_data: Dict, parent=None):
        """طباعة الفاتورة مباشرة"""
        try:
            # إنشاء مستند HTML للفاتورة
            html_content = DirectPrinter.create_receipt_html(receipt_data)
            
            # إنشاء طابعة
            printer = QPrinter()
            printer.setPageSize(QPageSize(QPageSize.A4))
            printer.setPageMargins(10, 10, 10, 10, QPrinter.Unit.Millimeter)
            printer.setFullPage(False)
            
            # عرض معاينة الطباعة
            preview_dialog = QPrintPreviewDialog(printer, parent)
            preview_dialog.setWindowTitle("معاينة طباعة الفاتورة")
            preview_dialog.setMinimumSize(800, 600)
            
            def print_preview(printer):
                document = QTextDocument()
                document.setHtml(html_content)
                document.setDefaultFont(QFont("Arial", 10))
                document.print_(printer)
            
            preview_dialog.paintRequested.connect(print_preview)
            
            if preview_dialog.exec():
                QMessageBox.information(parent, "نجاح", "تم إرسال الفاتورة إلى الطابعة")
                return True
            else:
                return False
                
        except Exception as e:
            QMessageBox.critical(parent, "خطأ", f"فشل الطباعة: {str(e)}")
            return False
    
    @staticmethod
    def create_receipt_html(receipt_data: Dict) -> str:
        """إنشاء محتوى HTML للفاتورة باستخدام المولد الجديد"""
        return ArabicReceiptGenerator.create_html_receipt(receipt_data)
    
    @staticmethod
    def download_receipt_image(receipt_data: Dict, parent=None):
        """تحميل الفاتورة كصورة PNG (بديل للفاتورة القديمة)"""
        try:
            receipt_id = receipt_data.get('receipt_id', 'UNKNOWN')
            
            # استخدام المولد العربي الجديد
            output_path = ArabicReceiptGenerator.generate_receipt(receipt_data)
            
            if output_path and os.path.exists(output_path):
                QMessageBox.information(
                    parent,
                    "تم التحميل",
                    f"تم حفظ الفاتورة بنجاح كصورة PNG\n\nالموقع: {output_path}"
                )
                return True
            else:
                QMessageBox.warning(parent, "خطأ", "فشل إنشاء الصورة!")
                return False
                
        except Exception as e:
            QMessageBox.critical(parent, "خطأ", f"حدث خطأ:\n{str(e)}")
            return False
    
    @staticmethod
    def quick_print(receipt_data: Dict, parent=None):
        """طباعة سريعة بدون معاينة"""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setPageSize(QPrinter.PageSize.A4)
            
            # عرض خيارات الطباعة
            print_dialog = QPrintDialog(printer, parent)
            print_dialog.setWindowTitle("طباعة الفاتورة")
            
            if print_dialog.exec():
                html_content = DirectPrinter.create_receipt_html(receipt_data)
                document = QTextDocument()
                document.setHtml(html_content)
                document.setDefaultFont(QFont("Arial", 9))
                document.print_(printer)
                return True
            return False
            
        except Exception as e:
            QMessageBox.critical(parent, "خطأ", f"فشل الطباعة السريعة: {str(e)}")
            return False


class PrintPreviewDialog(QDialog):
    """نافذة معاينة الطباعة - النسخة المحدثة"""
    
    def __init__(self, receipt_data: Dict, parent=None):
        super().__init__(parent)
        self.receipt_data = receipt_data
        self.setWindowTitle("معاينة الفاتورة")
        self.setGeometry(100, 100, 700, 900)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # عرض الفاتورة
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setHtml(DirectPrinter.create_receipt_html(self.receipt_data))
        self.preview_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                font-family: Arial;
            }
        """)
        layout.addWidget(self.preview_text)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        print_btn = QPushButton("🖨️ طباعة")
        print_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        print_btn.clicked.connect(self.print_receipt)
        
        download_btn = QPushButton("📥 حفظ كصورة")
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        download_btn.clicked.connect(self.download_image)
        
        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(print_btn)
        button_layout.addWidget(download_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def print_receipt(self):
        DirectPrinter.print_receipt(self.receipt_data, self)
    
    def download_image(self):
        DirectPrinter.download_receipt_image(self.receipt_data, self)


class ImagePreviewDialog(QDialog):
    """نافذة معاينة الصورة (للتوافق مع الشيفرة القديمة)"""
    
    def __init__(self, receipt_data: Dict, parent=None):
        super().__init__(parent)
        self.receipt_data = receipt_data
        self.setWindowTitle("معاينة الفاتورة")
        self.setGeometry(100, 100, 700, 900)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # عرض HTML للفاتورة
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setHtml(DirectPrinter.create_receipt_html(self.receipt_data))
        self.preview_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                font-family: Arial;
            }
        """)
        layout.addWidget(self.preview_text)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        download_btn = QPushButton("📥 حفظ كصورة")
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        download_btn.clicked.connect(self.download_image)
        
        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(download_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def download_image(self):
        DirectPrinter.download_receipt_image(self.receipt_data, self)


class JPEGReceiptGenerator:
    """فئة توافقية للشيفرة القديمة"""
    
    @staticmethod
    def generate_receipt(receipt_data: Dict, output_path: str = None):
        """دالة توافقية مع الشيفرة القديمة"""
        return ArabicReceiptGenerator.generate_receipt(receipt_data, output_path)