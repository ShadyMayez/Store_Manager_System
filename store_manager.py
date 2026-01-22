"""
store_manager.py
نظام إدارة المتجر - النسخة المحسّنة
Store Management System - Enhanced Arabic Version
"""
import sys
import os
import traceback
import csv
import json
from datetime import datetime
# في terminal، نفّذ هذا الأمر:
from arabic_receipt_generator_new import ArabicReceiptGenerator, create_arabic_receipt
from direct_print import DirectPrinter, PrintPreviewDialog, ImagePreviewDialog, JPEGReceiptGenerator
import sys
import os
import csv
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QPixmap
import os
import time
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QComboBox, QTableWidget, QTableWidgetItem, QPushButton, 
                            QDialog, QTextEdit, QMessageBox)
from PyQt6.QtGui import QColor
try:
    from arabic_font_receipt import ArabicReceiptGenerator, create_arabic_receipt
    ARABIC_RECEIPT_AVAILABLE = True
except ImportError as e:
    ARABIC_RECEIPT_AVAILABLE = False
    print(f" Arabic receipt generator not available: {e}")

try:
    from direct_print import DirectPrinter, ImagePreviewDialog, JPEGReceiptGenerator
    DIRECT_PRINT_AVAILABLE = True
except ImportError as e:
    DIRECT_PRINT_AVAILABLE = False
    print(f" Direct print module not available: {e}")

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import arabic_reshaper
from bidi.algorithm import get_display
from PyQt6.QtGui import QPixmap
import os
import tempfile
import csv
import json
import random
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from PyQt6.QtWidgets import QMessageBox
import os
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
import subprocess
import os
from datetime import datetime  # تأكد من وجود هذا
import json  # تأكد من وجود هذا

class CSVDatabase:
    """معالج ملفات CSV متكامل لإدارة المخزون والمبيعات"""
    
    def __init__(self):
        self.items_file = "items.csv"
        self.history_file = "history.csv"
        self.imports_file = "imports.csv"
        self.suppliers_file = "suppliers.csv"
        
        print("=" * 60)
        print("🚀 بدء تحميل قاعدة البيانات")
        print("=" * 60)
        
        # تهيئة الملفات
        self.initialize_files()
        
        # التحقق من سلامة البيانات
        self.verify_database_integrity()
        
        print("✅ تم تهيئة قاعدة البيانات بنجاح")
        print("=" * 60)
    
    def initialize_files(self):
        """إنشاء ملفات CSV إذا لم تكن موجودة"""
        print(f"🔧 بدء تهيئة الملفات...")
        
        # ملف المنتجات
        if not os.path.exists(self.items_file):
            print(f"📁 إنشاء ملف جديد: {self.items_file}")
            sample_items = [
            # --- الفاتورة المطبوعة (Image 11282a.jpg) ---
            {"item_id": "1001", "name": "برنكس (تايلاندي)", "unit": "عدد", "size": "14/65/185", "buying_price": 1500.00, "selling_price": 1600.00, "quantity": 12},
            {"item_id": "1002", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "14/65/185", "buying_price": 1525.00, "selling_price": 1600.00, "quantity": 12},
            {"item_id": "1003", "name": "لوفن (كوري)", "unit": "عدد", "size": "14/65/185", "buying_price": 1825.00, "selling_price": 1950.00, "quantity": 4},
            {"item_id": "1004", "name": "اطلس (تايلاندي)", "unit": "عدد", "size": "14/195/R14", "buying_price": 2725.00, "selling_price": 2800.00, "quantity": 6},
            {"item_id": "1005", "name": "بريدجستون (تركي)", "unit": "عدد", "size": "14/195/R14", "buying_price": 3850.00, "selling_price": 3950.00, "quantity": 2},
            {"item_id": "1006", "name": "هاي فلاي (صيني)", "unit": "عدد", "size": "14/195/R14", "buying_price": 1675.00, "selling_price": 1800.00, "quantity": 6},
            {"item_id": "1007", "name": "جي تي خط ابيض (اندونيسي)", "unit": "عدد", "size": "14/75/205", "buying_price": 2650.00, "selling_price": 2750.00, "quantity": 4},
            {"item_id": "1008", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "15/50/195", "buying_price": 1725.00, "selling_price": 1800.00, "quantity": 2},
            {"item_id": "1009", "name": "اريفو (صيني)", "unit": "عدد", "size": "15/55/195", "buying_price": 1425.00, "selling_price": 1500.00, "quantity": 6},
            {"item_id": "1010", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "15/55/195", "buying_price": 1700.00, "selling_price": 1750.00, "quantity": 12},
            {"item_id": "1011", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "15/65/195", "buying_price": 1700.00, "selling_price": 1750.00, "quantity": 9},
            {"item_id": "1012", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "15/65/205", "buying_price": 2075.00, "selling_price": 2150.00, "quantity": 4},
            {"item_id": "1013", "name": "ترك (صيني)", "unit": "عدد", "size": "15/70/215", "buying_price": 2125.00, "selling_price": 2250.00, "quantity": 4},
            {"item_id": "1014", "name": "جودرايد خط ابيض (تايلاندي)", "unit": "عدد", "size": "15/70/215", "buying_price": 2800.00, "selling_price": 2900.00, "quantity": 4},
            {"item_id": "1015", "name": "كيندا (تايواني)", "unit": "عدد", "size": "16/45/205", "buying_price": 2250.00, "selling_price": 2300.00, "quantity": 4},
            {"item_id": "1016", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "16/50/205", "buying_price": 2150.00, "selling_price": 2200.00, "quantity": 4},
            {"item_id": "1017", "name": "لوفن (كوري)", "unit": "عدد", "size": "16/55/205", "buying_price": 2300.00, "selling_price": 2400.00, "quantity": 5},
            {"item_id": "1018", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "16/55/205", "buying_price": 1950.00, "selling_price": 2100.00, "quantity": 12},
            {"item_id": "1019", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "16/65/215", "buying_price": 2675.00, "selling_price": 2750.00, "quantity": 2},

            # --- الصورة المكتوبة بخط اليد 1 (Image 112860) ---
            {"item_id": "2001", "name": "جي تي (اندونيسي)", "unit": "عدد", "size": "13/70/175", "buying_price": 1000.00, "selling_price": 1050.00, "quantity": 6},
            {"item_id": "2002", "name": "جي تي (صيني)", "unit": "عدد", "size": "13/70/175", "buying_price": 1000.00, "selling_price": 1025.00, "quantity": 10},
            {"item_id": "2003", "name": "جي تي راديال (تايلاندي)", "unit": "عدد", "size": "13/70/175", "buying_price": 1275.00, "selling_price": 1300.00, "quantity": 8},
            {"item_id": "2004", "name": "جراند (صيني)", "unit": "عدد", "size": "13/70/175", "buying_price": 1000.00, "selling_price": 1050.00, "quantity": 38},
            {"item_id": "2005", "name": "لينج لونج (تايلاندي)", "unit": "عدد", "size": "13/70/175", "buying_price": 1200.00, "selling_price": 1250.00, "quantity": 15},
            {"item_id": "2006", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "13/70/175", "buying_price": 1275.00, "selling_price": 1300.00, "quantity": 15},
            {"item_id": "2007", "name": "لاسا (تركي)", "unit": "عدد", "size": "13/70/175", "buying_price": 1400.00, "selling_price": 1450.00, "quantity": 2},
            {"item_id": "2008", "name": "دبل ستار (صيني)", "unit": "عدد", "size": "13/70/175", "buying_price": 1050.00, "selling_price": 1100.00, "quantity": 6},
            {"item_id": "2009", "name": "مايلز (صيني)", "unit": "عدد", "size": "13/70/175", "buying_price": 1225.00, "selling_price": 1250.00, "quantity": 7},
            {"item_id": "2010", "name": "ستار بلس (صيني)", "unit": "عدد", "size": "13/70/175", "buying_price": 1200.00, "selling_price": 1250.00, "quantity": 2},
            {"item_id": "2011", "name": "هانكوك (كوري)", "unit": "عدد", "size": "13/70/175", "buying_price": 2075.00, "selling_price": 2125.00, "quantity": 4},
            {"item_id": "2012", "name": "ناونج (تايلاندي)", "unit": "عدد", "size": "13/80/165", "buying_price": 1650.00, "selling_price": 1700.00, "quantity": 2},
            {"item_id": "2013", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "14/60/185", "buying_price": 1700.00, "selling_price": 1750.00, "quantity": 4},
            {"item_id": "2014", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "14/60/185", "buying_price": 1700.00, "selling_price": 1750.00, "quantity": 4},
            {"item_id": "2015", "name": "سنفور (صيني)", "unit": "عدد", "size": "14/60/185", "buying_price": 1200.00, "selling_price": 1250.00, "quantity": 6},
            {"item_id": "2016", "name": "أوتاني (تايلاندي)", "unit": "عدد", "size": "14/65/185", "buying_price": 1750.00, "selling_price": 1800.00, "quantity": 4},
            {"item_id": "2017", "name": "سنفور (صيني)", "unit": "عدد", "size": "14/65/185", "buying_price": 1200.00, "selling_price": 1250.00, "quantity": 5},
            {"item_id": "2018", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "14/65/185", "buying_price": 1575.00, "selling_price": 1600.00, "quantity": 1},
            {"item_id": "2019", "name": "أفالون (صيني)", "unit": "عدد", "size": "14/65/185", "buying_price": 1200.00, "selling_price": 1250.00, "quantity": 11},
            {"item_id": "2020", "name": "هانكوك (كوري)", "unit": "عدد", "size": "14/65/185", "buying_price": 2350.00, "selling_price": 2450.00, "quantity": 6},
            {"item_id": "2021", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "14/70/195", "buying_price": 1875.00, "selling_price": 1900.00, "quantity": 8},
            {"item_id": "2022", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "14/70/185", "buying_price": 1650.00, "selling_price": 1700.00, "quantity": 6},
            {"item_id": "2023", "name": "مارشال (فيتنامي)", "unit": "عدد", "size": "14/70/205", "buying_price": 2100.00, "selling_price": 2200.00, "quantity": 4},
            {"item_id": "2024", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "14/70/195", "buying_price": 2400.00, "selling_price": 2450.00, "quantity": 21},
            {"item_id": "2025", "name": "دبل ستار (صيني)", "unit": "عدد", "size": "14/70/195", "buying_price": 1900.00, "selling_price": 1950.00, "quantity": 8},
            {"item_id": "2026", "name": "أطلس (تايلاندي)", "unit": "عدد", "size": "14/70/195", "buying_price": 2775.00, "selling_price": 2825.00, "quantity": 4},

            # --- الصورة المكتوبة بخط اليد 2 (Image 112865) ---
            {"item_id": "2027", "name": "دايموند (صيني)", "unit": "عدد", "size": "14/195", "buying_price": 1790.00, "selling_price": 1850.00, "quantity": 4},
            {"item_id": "2028", "name": "بريدجستون (تركي)", "unit": "عدد", "size": "14/195", "buying_price": 2900.00, "selling_price": 3000.00, "quantity": 4},
            {"item_id": "2029", "name": "دنلوب (تايلاندي)", "unit": "عدد", "size": "14/195", "buying_price": 2000.00, "selling_price": 2200.00, "quantity": 10},
            {"item_id": "2030", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "14/195", "buying_price": 2475.00, "selling_price": 2525.00, "quantity": 6},
            {"item_id": "2031", "name": "لونج لونج (تايلاندي)", "unit": "عدد", "size": "14/195", "buying_price": 2800.00, "selling_price": 2900.00, "quantity": 2},
            {"item_id": "2032", "name": "جي تي (اندونيسي)", "unit": "عدد", "size": "14/75/205", "buying_price": 2750.00, "selling_price": 2850.00, "quantity": 4},
            {"item_id": "2033", "name": "فالكن (تايلاندي)", "unit": "عدد", "size": "14/75/205", "buying_price": 4950.00, "selling_price": 5000.00, "quantity": 4},
            {"item_id": "2034", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "14/80/205", "buying_price": 2100.00, "selling_price": 2150.00, "quantity": 4},
            {"item_id": "2035", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "15/50/195", "buying_price": 1750.00, "selling_price": 1800.00, "quantity": 4},
            {"item_id": "2036", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "15/50/195", "buying_price": 1800.00, "selling_price": 1900.00, "quantity": 2},
            {"item_id": "2037", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "15/55/195", "buying_price": 1725.00, "selling_price": 1750.00, "quantity": 4},
            {"item_id": "2038", "name": "لوفن (كوري)", "unit": "عدد", "size": "15/55/195", "buying_price": 2225.00, "selling_price": 2300.00, "quantity": 4},
            {"item_id": "2039", "name": "اندونيسي (اندونيسي)", "unit": "عدد", "size": "15/55/195", "buying_price": 2150.00, "selling_price": 2200.00, "quantity": 4},
            {"item_id": "2040", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "15/55/195", "buying_price": 1750.00, "selling_price": 1800.00, "quantity": 4},
            {"item_id": "2041", "name": "بريدجستون (تايلاندي)", "unit": "عدد", "size": "15/55/195", "buying_price": 1750.00, "selling_price": 1800.00, "quantity": 8},
            {"item_id": "2042", "name": "اريفو (صيني)", "unit": "عدد", "size": "15/55/195", "buying_price": 1425.00, "selling_price": 1500.00, "quantity": 4},
            {"item_id": "2043", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "15/60/195", "buying_price": 1750.00, "selling_price": 1800.00, "quantity": 8},
            {"item_id": "2044", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "15/60/195", "buying_price": 1825.00, "selling_price": 1850.00, "quantity": 12},
            {"item_id": "2045", "name": "نكسن (تايلاندي)", "unit": "عدد", "size": "15/60/195", "buying_price": 1710.00, "selling_price": 1750.00, "quantity": 8},
            {"item_id": "2046", "name": "أوتاني (تايلاندي)", "unit": "عدد", "size": "15/60/195", "buying_price": 1400.00, "selling_price": 1500.00, "quantity": 8},
            {"item_id": "2047", "name": "جي تي (اندونيسي)", "unit": "عدد", "size": "15/60/195", "buying_price": 2275.00, "selling_price": 2350.00, "quantity": 2},
            {"item_id": "2048", "name": "اطلس (تايلاندي)", "unit": "عدد", "size": "15/60/195", "buying_price": 1750.00, "selling_price": 1800.00, "quantity": 5},
            {"item_id": "2049", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "15/65/195", "buying_price": 1700.00, "selling_price": 1750.00, "quantity": 2},
            {"item_id": "2050", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "15/65/195", "buying_price": 1800.00, "selling_price": 1900.00, "quantity": 2},
            {"item_id": "2051", "name": "أفالون (صيني)", "unit": "عدد", "size": "15/65/195", "buying_price": 1400.00, "selling_price": 1500.00, "quantity": 5},
            {"item_id": "2052", "name": "هانكوك (كوري)", "unit": "عدد", "size": "15/65/195", "buying_price": 2800.00, "selling_price": 2900.00, "quantity": 4},
            {"item_id": "2053", "name": "رافين (أندونيسي)", "unit": "عدد", "size": "15/65/195", "buying_price": 2125.00, "selling_price": 2200.00, "quantity": 4},
            {"item_id": "2054", "name": "برنكس (تايلاندي)", "unit": "عدد", "size": "15/65/195", "buying_price": 1750.00, "selling_price": 1800.00, "quantity": 6},
            {"item_id": "2055", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "15/65/195", "buying_price": 1825.00, "selling_price": 1900.00, "quantity": 12},
            {"item_id": "2056", "name": "دايتون (صيني)", "unit": "عدد", "size": "15/70/225", "buying_price": 2700.00, "selling_price": 2800.00, "quantity": 4},
            {"item_id": "2057", "name": "سنفور (صيني)", "unit": "عدد", "size": "15/70/225", "buying_price": 2450.00, "selling_price": 2500.00, "quantity": 2},
            {"item_id": "2058", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "15/65/185", "buying_price": 1800.00, "selling_price": 1900.00, "quantity": 8},

            # --- الصورة المكتوبة بخط اليد 3 (Image 112880) ---
            {"item_id": "2059", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "15/70/205", "buying_price": 1975.00, "selling_price": 2050.00, "quantity": 3},
            {"item_id": "2060", "name": "هانكوك (كوري)", "unit": "عدد", "size": "15/70/205", "buying_price": 2190.00, "selling_price": 2250.00, "quantity": 5},
            {"item_id": "2061", "name": "لاسـا (تركي)", "unit": "عدد", "size": "15/70/205", "buying_price": 2150.00, "selling_price": 2250.00, "quantity": 1},
            {"item_id": "2062", "name": "زينا (اندونيسي)", "unit": "عدد", "size": "15/70/205", "buying_price": 2000.00, "selling_price": 2100.00, "quantity": 4},
            {"item_id": "2063", "name": "لوفن (كوري)", "unit": "عدد", "size": "16/60/205", "buying_price": 2125.00, "selling_price": 2200.00, "quantity": 4},
            {"item_id": "2064", "name": "هانكوك (كوري)", "unit": "عدد", "size": "16/60/205", "buying_price": 2350.00, "selling_price": 2400.00, "quantity": 2},
            {"item_id": "2065", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "16/60/215", "buying_price": 2175.00, "selling_price": 2250.00, "quantity": 11},
            {"item_id": "2066", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "16/60/215", "buying_price": 2700.00, "selling_price": 2800.00, "quantity": 4},
            {"item_id": "2067", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "16/60/225", "buying_price": 2950.00, "selling_price": 3000.00, "quantity": 6},
            {"item_id": "2068", "name": "لاسـا (تركي)", "unit": "عدد", "size": "16/60/225", "buying_price": 4600.00, "selling_price": 4700.00, "quantity": 6},
            {"item_id": "2069", "name": "دبل كوين (صيني)", "unit": "عدد", "size": "16/70/215", "buying_price": 4200.00, "selling_price": 4700.00, "quantity": 2},
            {"item_id": "2070", "name": "دبل كوين (صيني)", "unit": "عدد", "size": "16/70/225", "buying_price": 4500.00, "selling_price": 4600.00, "quantity": 2},

            # --- الصورة المكتوبة بخط اليد 4 (Image 112884) ---
            {"item_id": "2071", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "17/40/205", "buying_price": 2500.00, "selling_price": 2600.00, "quantity": 4},
            {"item_id": "2072", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "17/45/215", "buying_price": 2500.00, "selling_price": 2600.00, "quantity": 5},
            {"item_id": "2073", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "17/45/215", "buying_price": 2475.00, "selling_price": 2550.00, "quantity": 8},
            {"item_id": "2074", "name": "ستارلي (تايلاندي)", "unit": "عدد", "size": "17/45/215", "buying_price": 2450.00, "selling_price": 2500.00, "quantity": 4},
            {"item_id": "2075", "name": "فالكن (تايلاندي)", "unit": "عدد", "size": "17/45/225", "buying_price": 2560.00, "selling_price": 2650.00, "quantity": 11},
            {"item_id": "2076", "name": "لافين (اندونيسي)", "unit": "عدد", "size": "17/45/225", "buying_price": 2250.00, "selling_price": 2300.00, "quantity": 4},
            {"item_id": "2077", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "17/50/215", "buying_price": 2250.00, "selling_price": 2350.00, "quantity": 10},
            {"item_id": "2078", "name": "ماكسيس (تايلاندي)", "unit": "عدد", "size": "17/50/225", "buying_price": 2725.00, "selling_price": 2850.00, "quantity": 12},
            {"item_id": "2079", "name": "مارشال (فيتنامي)", "unit": "عدد", "size": "17/55/225", "buying_price": 2900.00, "selling_price": 3000.00, "quantity": 2},
            {"item_id": "2080", "name": "نكسن (كوري)", "unit": "عدد", "size": "17/55/215", "buying_price": 2700.00, "selling_price": 2800.00, "quantity": 2},
            {"item_id": "2081", "name": "نكسن (كوري)", "unit": "عدد", "size": "17/65/225", "buying_price": 2300.00, "selling_price": 2400.00, "quantity": 4},
            {"item_id": "2082", "name": "هانكوك (كوري)", "unit": "عدد", "size": "17/65/265", "buying_price": 4950.00, "selling_price": 5050.00, "quantity": 4},
            {"item_id": "2083", "name": "ماتريكس (تايلاندي)", "unit": "عدد", "size": "18/55/225", "buying_price": 2200.00, "selling_price": 2450.00, "quantity": 4},
            {"item_id": "2084", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "18/55/225", "buying_price": 2225.00, "selling_price": 2350.00, "quantity": 4},
            {"item_id": "2085", "name": "جودرايد (تايلاندي)", "unit": "عدد", "size": "18/45/245", "buying_price": 2325.00, "selling_price": 2500.00, "quantity": 4}
        ]
            self.save_items(sample_items)
        else:
            print(f"📁 الملف موجود: {self.items_file} (الحجم: {os.path.getsize(self.items_file)} بايت)")
        
        # ملف السجل
        if not os.path.exists(self.history_file):
            print(f"📁 إنشاء ملف جديد: {self.history_file}")
            self.save_history([])
        else:
            print(f"📁 الملف موجود: {self.history_file} (الحجم: {os.path.getsize(self.history_file)} بايت)")
        
        # ملف الاستيراد
        if not os.path.exists(self.imports_file):
            print(f"📁 إنشاء ملف جديد: {self.imports_file}")
            self.save_imports([])
        else:
            print(f"📁 الملف موجود: {self.imports_file} (الحجم: {os.path.getsize(self.imports_file)} بايت)")
        
        # ملف الموردين
        if not os.path.exists(self.suppliers_file):
            print(f"📁 إنشاء ملف جديد: {self.suppliers_file}")
            sample_suppliers = [
                {"supplier_id": "S001", "name": "شركة الأزياء الرئيسية", "phone": "0123456789", "address": "القاهرة", "email": "info@fashion-supplier.com"},
            ]
            self.save_suppliers(sample_suppliers)
        else:
            print(f"📁 الملف موجود: {self.suppliers_file} (الحجم: {os.path.getsize(self.suppliers_file)} بايت)")
    
    def verify_database_integrity(self):
        """التحقق من سلامة قاعدة البيانات"""
        print("\n🔍 التحقق من سلامة البيانات...")
        
        # التحقق من items.csv
        items = self.load_items()
        print(f"📦 عدد المنتجات: {len(items)}")
        
        if items:
            print("🔢 عينة من item_id:")
            for i, item in enumerate(items[:5]):
                item_id = item.get('item_id', 'MISSING')
                name = item.get('name', 'غير معروف')
                print(f"  {i+1}. ID: '{item_id}' ({type(item_id).__name__}), Name: '{name[:20]}...'")
            
            # التحقق من وجود item_id
            missing_ids = [item for item in items if not item.get('item_id') or str(item['item_id']).strip() == '']
            if missing_ids:
                print(f"⚠ تحذير: {len(missing_ids)} عنصر بدون item_id")
                self.fix_missing_item_ids()
        
        # التحقق من history.csv
        history = self.load_history()
        print(f"📋 عدد سجلات المبيعات: {len(history)}")
        
        # التحقق من imports.csv
        imports = self.load_imports()
        print(f"📤 عدد سجلات الاستيراد: {len(imports)}")
        
        # التحقق من suppliers.csv
        suppliers = self.load_suppliers()
        print(f"🏢 عدد الموردين: {len(suppliers)}")
        
        return len(items) > 0
    
    def fix_missing_item_ids(self):
        """إصلاح العناصر التي تفتقد item_id"""
        items = self.load_items()
        fixed = False
        
        for i, item in enumerate(items):
            if not item.get('item_id') or str(item['item_id']).strip() == '':
                # إنشاء ID جديد
                new_id = f"FIXED_{i+1000}"
                item['item_id'] = new_id
                fixed = True
                print(f"🔧 إصلاح item_id للعنصر {i}: تعيين '{new_id}'")
        
        if fixed:
            self.save_items(items)
            print("✅ تم إصلاح العناصر بدون item_id")
    
    def safe_arabic_text(self, text):
        """معالجة وحفظ النص العربي"""
        if not text or not isinstance(text, str):
            return str(text) if text else ""
        
        # تنظيف النص
        cleaned_text = text.strip()
        
        # استخدام Unicode normalization
        try:
            import unicodedata
            normalized_text = unicodedata.normalize('NFC', cleaned_text)
            return normalized_text
        except:
            return cleaned_text
    
    # ========== إدارة المنتجات ==========
    
    def load_items(self) -> List[Dict]:
        """تحميل جميع المنتجات"""
        items = []
        try:
            if not os.path.exists(self.items_file):
                print(f"⚠ الملف {self.items_file} غير موجود")
                return []
            
            with open(self.items_file, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                if not reader.fieldnames:
                    print("⚠ الملف فارغ أو تالف")
                    return []
                
                print(f"📊 حقول الملف: {reader.fieldnames}")
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # تأكد من أن item_id هو string
                        if 'item_id' in row:
                            row['item_id'] = str(row['item_id']).strip()
                        
                        # تحويل الحقول الرقمية
                        if 'buying_price' in row:
                            try:
                                row['buying_price'] = float(row['buying_price'])
                            except (ValueError, TypeError):
                                row['buying_price'] = 0.0
                        
                        if 'selling_price' in row:
                            try:
                                row['selling_price'] = float(row['selling_price'])
                            except (ValueError, TypeError):
                                row['selling_price'] = 0.0
                        
                        if 'quantity' in row:
                            try:
                                row['quantity'] = int(float(row['quantity']))
                            except (ValueError, TypeError):
                                row['quantity'] = 0
                        
                        # إذا لم يكن حقل 'unit' موجوداً، أضفه
                        if 'unit' not in row:
                            row['unit'] = 'عدد'
                        
                        items.append(row)
                        
                    except Exception as e:
                        print(f"⚠ خطأ في معالجة السطر {row_num}: {e}")
                        continue
                
                print(f"✅ تم تحميل {len(items)} عنصر من {self.items_file}")
                
        except FileNotFoundError:
            print(f"❌ الملف {self.items_file} غير موجود")
            self.initialize_files()
            return self.load_items()
        except Exception as e:
            print(f"❌ خطأ في تحميل المنتجات: {e}")
            import traceback
            traceback.print_exc()
        
        return items
    
    def save_items(self, items: List[Dict]):
        """حفظ المنتجات"""
        try:
            print(f"💾 محاولة حفظ {len(items)} عنصر...")
            
            if not items:
                print("⚠ لا توجد عناصر للحفظ")
                return
            
            # التحقق من البيانات قبل الحفظ
            for i, item in enumerate(items):
                if not item.get('item_id') or str(item['item_id']).strip() == '':
                    print(f"⚠ تحذير: العنصر {i} بدون item_id: {item.get('name', 'غير معروف')}")
                    item['item_id'] = f"AUTO_{i+1000}_{random.randint(100, 999)}"
            
            with open(self.items_file, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = ['item_id', 'name', 'unit', 'size', 'buying_price', 'selling_price', 'quantity']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for i, item in enumerate(items):
                    # تنظيف البيانات
                    row = {}
                    for field in fieldnames:
                        if field in item:
                            value = item[field]
                            
                            # تنظيف النصوص العربية
                            if isinstance(value, str):
                                value = self.safe_arabic_text(value)
                            
                            # تأكد من أن item_id هو string
                            if field == 'item_id':
                                value = str(value).strip()
                                if not value:
                                    value = f"ROW_{i+1000}"
                            
                            row[field] = value
                        else:
                            # القيم الافتراضية للحقول المفقودة
                            if field == 'item_id':
                                row[field] = f"MISSING_{i+1000}"
                            elif field in ['buying_price', 'selling_price']:
                                row[field] = 0.0
                            elif field == 'quantity':
                                row[field] = 0
                            elif field == 'unit':
                                row[field] = 'عدد'
                            else:
                                row[field] = ''
                    
                    writer.writerow(row)
            
            print(f"✅ تم حفظ {len(items)} عنصر في {self.items_file}")
            
            # التحقق من الحفظ
            self.verify_save(items)
            
        except Exception as e:
            print(f"❌ خطأ في حفظ المنتجات: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(None, "خطأ في الحفظ", 
                               f"حدث خطأ في حفظ البيانات:\n\n{str(e)}\n\n"
                               f"تأكد أن الملف {self.items_file} غير مفتوح في برنامج آخر.")
    
    def verify_save(self, original_items):
        """التحقق من أن البيانات حفظت بشكل صحيح"""
        try:
            loaded_items = self.load_items()
            
            if len(loaded_items) != len(original_items):
                print(f"⚠ تحذير: تم تحميل {len(loaded_items)} عنصر لكن كان يجب تحميل {len(original_items)}")
            
            # مقارنة أول 3 عناصر
            print("🔍 مقارنة البيانات المحفوظة مع الأصلية:")
            for i in range(min(3, len(original_items), len(loaded_items))):
                orig = original_items[i]
                loaded = loaded_items[i]
                
                print(f"  العنصر {i+1}:")
                print(f"    الأصل - ID: '{orig.get('item_id')}', Name: '{orig.get('name')}'")
                print(f"    المحمل - ID: '{loaded.get('item_id')}', Name: '{loaded.get('name')}'")
                
                if str(orig.get('item_id', '')).strip() != str(loaded.get('item_id', '')).strip():
                    print(f"    ⚡ اختلاف في item_id!")
        
        except Exception as e:
            print(f"⚠ خطأ في التحقق: {e}")
    
    def add_item(self, item_data: Dict):
        """إضافة منتج جديد"""
        try:
            items = self.load_items()
            
            # التحقق من عدم تكرار item_id
            item_id = str(item_data.get('item_id', '')).strip()
            if not item_id:
                # إنشاء ID تلقائي
                existing_ids = [int(i['item_id']) for i in items if i['item_id'].isdigit()]
                new_id = max(existing_ids) + 1 if existing_ids else 1001
                item_data['item_id'] = str(new_id)
            
            # التحقق من أن جميع الحقول موجودة
            required_fields = ['name', 'unit', 'size', 'buying_price', 'selling_price', 'quantity']
            for field in required_fields:
                if field not in item_data:
                    if field in ['buying_price', 'selling_price']:
                        item_data[field] = 0.0
                    elif field == 'quantity':
                        item_data[field] = 0
                    else:
                        item_data[field] = ''
            
            items.append(item_data)
            self.save_items(items)
            
            print(f"✅ تم إضافة المنتج: {item_data['item_id']} - {item_data['name']}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إضافة المنتج: {e}")
            return False
    
    def update_item(self, item_id: str, updated_data: Dict):
        """تحديث بيانات منتج"""
        try:
            items = self.load_items()
            updated = False
            
            for i, item in enumerate(items):
                if str(item.get('item_id', '')).strip() == str(item_id).strip():
                    items[i].update(updated_data)
                    updated = True
                    break
            
            if updated:
                self.save_items(items)
                print(f"✅ تم تحديث المنتج: {item_id}")
                return True
            else:
                print(f"⚠ لم يتم العثور على المنتج: {item_id}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في تحديث المنتج: {e}")
            return False
    
    def delete_item(self, item_id: str):
        """حذف منتج"""
        try:
            items = self.load_items()
            new_items = [item for item in items if str(item.get('item_id', '')).strip() != str(item_id).strip()]
            
            if len(new_items) < len(items):
                self.save_items(new_items)
                print(f"✅ تم حذف المنتج: {item_id}")
                return True
            else:
                print(f"⚠ لم يتم العثور على المنتج: {item_id}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في حذف المنتج: {e}")
            return False
    
    def update_item_quantity(self, item_id: str, quantity_change: int):
        """تحديث كمية المنتج"""
        items = self.load_items()
        for item in items:
            if str(item.get('item_id', '')).strip() == str(item_id).strip():
                new_quantity = item['quantity'] + quantity_change
                if new_quantity < 0:
                    raise ValueError("المخزون غير كافي")
                item['quantity'] = new_quantity
                break
        self.save_items(items)
    
    def find_item_by_id(self, item_id: str) -> Optional[Dict]:
        """البحث عن منتج برقمه"""
        items = self.load_items()
        for item in items:
            if str(item.get('item_id', '')).strip() == str(item_id).strip():
                return item
        return None
    
    # ========== إدارة سجلات المبيعات ==========
    
    def load_history(self) -> List[Dict]:
        """تحميل سجل المبيعات"""
        history = []
        
        if not os.path.exists(self.history_file):
            return history
        
        try:
            with open(self.history_file, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                if not reader.fieldnames:
                    return []
                
                for row in reader:
                    try:
                        # تحويل الحقول الرقمية
                        numeric_fields = ['total', 'profit', 'previous_balance', 
                                        'total_cumulative', 'amount_paid', 'remaining']
                        
                        for field in numeric_fields:
                            if field in row and row[field]:
                                try:
                                    row[field] = float(row[field])
                                except (ValueError, TypeError):
                                    row[field] = 0.0
                        
                        # تحويل حقل items من JSON
                        if 'items' in row and row['items']:
                            try:
                                row['items'] = json.loads(row['items'])
                            except json.JSONDecodeError:
                                row['items'] = []
                        else:
                            row['items'] = []
                        
                        # إضافة الحقول الإضافية
                        default_fields = {
                            'customer_code': '',
                            'receipt_code': '',
                            'representative_code': '',
                            'representative_name': '',
                            'customer_address': '',
                            'due_date': '',
                            'customer_notes': '',
                            'payment_status': 'غير مدفوع',
                            'notes': ''
                        }
                        
                        for field, default in default_fields.items():
                            if field not in row:
                                row[field] = default
                        
                        history.append(row)
                        
                    except Exception as e:
                        print(f"⚠ خطأ في معالجة سطر: {e}")
                        continue
                        
        except Exception as e:
            print(f"❌ خطأ في تحميل السجل: {e}")
        
        return history
    
    def save_history(self, history: List[Dict]):
        """حفظ سجل المبيعات"""
        if not history:
            # حفظ ملف فارغ
            with open(self.history_file, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = ['receipt_id', 'customer_id', 'customer_name',
                            'date', 'items', 'total', 'profit', 'payment_method',
                            'notes', 'previous_balance', 'total_cumulative',
                            'amount_paid', 'remaining', 'payment_status']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        # تحديد جميع الحقول
        all_fields = set()
        for record in history:
            all_fields.update(record.keys())
        
        # الحقول الأساسية
        base_fields = ['receipt_id', 'customer_id', 'customer_name',
                      'date', 'items', 'total', 'profit', 'payment_method',
                      'notes', 'previous_balance', 'total_cumulative',
                      'amount_paid', 'remaining', 'payment_status']
        
        # إضافة الحقول الإضافية
        additional_fields = [field for field in all_fields if field not in base_fields]
        fieldnames = base_fields + sorted(additional_fields)
        
        try:
            with open(self.history_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in history:
                    row_copy = row.copy()
                    
                    # معالجة الحقول الخاصة
                    if 'items' in row_copy and isinstance(row_copy['items'], (list, dict)):
                        row_copy['items'] = json.dumps(row_copy['items'], ensure_ascii=False)
                    
                    writer.writerow(row_copy)
            
            print(f"✅ تم حفظ {len(history)} سجل مبيعات")
            
        except Exception as e:
            print(f"❌ خطأ في حفظ السجل: {e}")
            raise
    
    def add_history_record(self, receipt_data: Dict):
        """إضافة سجل مبيعات جديد"""
        try:
            # إنشاء رقم فاتورة فريد
            if 'receipt_id' not in receipt_data or not receipt_data['receipt_id']:
                receipt_data['receipt_id'] = f"INV{random.randint(10000, 99999)}"
            
            # تحميل التاريخ الحالي
            history = self.load_history()
            
            # التحقق من عدم التكرار
            receipt_ids = [r.get('receipt_id', '') for r in history]
            if receipt_data['receipt_id'] in receipt_ids:
                receipt_data['receipt_id'] = f"INV{random.randint(10000, 99999)}"
            
            # إضافة السجل
            history.append(receipt_data)
            self.save_history(history)
            
            print(f"✅ تم إضافة فاتورة: {receipt_data['receipt_id']}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في إضافة الفاتورة: {e}")
            return False
    
    def delete_history_record(self, receipt_id: str) -> bool:
        """حذف سجل مبيعات"""
        history = self.load_history()
        new_history = [record for record in history if record.get('receipt_id') != receipt_id]
        
        if len(new_history) < len(history):
            self.save_history(new_history)
            print(f"✅ تم حذف الفاتورة: {receipt_id}")
            return True
        
        print(f"⚠ لم يتم العثور على الفاتورة: {receipt_id}")
        return False
    
    def update_receipt(self, receipt_id: str, updated_data: Dict) -> bool:
        """تحديث بيانات الفاتورة"""
        try:
            history = self.load_history()
            updated = False
            
            for i, record in enumerate(history):
                if record.get('receipt_id') == receipt_id:
                    history[i].update(updated_data)
                    updated = True
                    break
            
            if updated:
                self.save_history(history)
                print(f"✅ تم تحديث الفاتورة: {receipt_id}")
                return True
            else:
                print(f"⚠ لم يتم العثور على الفاتورة: {receipt_id}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في تحديث الفاتورة: {e}")
            return False
    
    # اسم بديل لحذف الفاتورة
    def delete_receipt(self, receipt_id: str) -> bool:
        """حذف فاتورة"""
        return self.delete_history_record(receipt_id)
    
    # ========== إدارة سجلات الاستيراد ==========
    
    def load_imports(self) -> List[Dict]:
        """تحميل سجلات الاستيراد"""
        imports = []
        try:
            if not os.path.exists(self.imports_file):
                return []
            
            with open(self.imports_file, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # تحويل الحقول الرقمية
                    numeric_fields = ['price', 'quantity', 'paid', 'remaining', 'total']
                    for field in numeric_fields:
                        if field in row and row[field]:
                            try:
                                if field == 'quantity':
                                    row[field] = int(row[field])
                                else:
                                    row[field] = float(row[field])
                            except (ValueError, TypeError):
                                row[field] = 0
                    
                    imports.append(row)
        except Exception as e:
            print(f"❌ خطأ في تحميل سجلات الاستيراد: {e}")
        
        return imports
    
    def save_imports(self, imports: List[Dict]):
        """حفظ سجلات الاستيراد"""
        # تحديد الحقول
        base_fields = ['import_id', 'supplier_name', 'item_name', 'size', 'price', 
                      'quantity', 'date', 'paid', 'remaining', 'notes',
                      'total', 'settlement_date', 'payment_status']
        
        with open(self.imports_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=base_fields)
            writer.writeheader()
            
            for row in imports:
                # تأكد من وجود جميع الحقول
                row_copy = {}
                for field in base_fields:
                    if field in row:
                        row_copy[field] = row[field]
                    else:
                        # قيم افتراضية
                        if field in ['price', 'paid', 'remaining', 'total']:
                            row_copy[field] = 0.0
                        elif field == 'quantity':
                            row_copy[field] = 0
                        else:
                            row_copy[field] = ''
                
                writer.writerow(row_copy)
        
        print(f"✅ تم حفظ {len(imports)} سجل استيراد")
    
    def add_import_record(self, record: Dict):
        """إضافة سجل استيراد"""
        imports = self.load_imports()
        
        # إنشاء ID إذا لم يكن موجوداً
        if 'import_id' not in record or not record['import_id']:
            record['import_id'] = f"IMP{random.randint(1000, 9999)}"
        
        imports.append(record)
        self.save_imports(imports)
        
        print(f"✅ تم إضافة سجل استيراد: {record['import_id']}")
    
    def delete_import_record(self, import_id: str) -> bool:
        """حذف سجل استيراد"""
        imports = self.load_imports()
        new_imports = [rec for rec in imports if rec.get('import_id') != import_id]
        
        if len(new_imports) < len(imports):
            self.save_imports(new_imports)
            print(f"✅ تم حذف سجل الاستيراد: {import_id}")
            return True
        
        print(f"⚠ لم يتم العثور على سجل الاستيراد: {import_id}")
        return False
    
    def update_import_record(self, import_id: str, updated_record: Dict) -> bool:
        """تحديث سجل استيراد"""
        try:
            imports = self.load_imports()
            updated = False
            
            for i, rec in enumerate(imports):
                if rec.get('import_id') == import_id:
                    imports[i] = updated_record
                    updated = True
                    break
            
            if updated:
                self.save_imports(imports)
                print(f"✅ تم تحديث سجل الاستيراد: {import_id}")
                return True
            else:
                print(f"⚠ لم يتم العثور على سجل الاستيراد: {import_id}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في تحديث سجل الاستيراد: {e}")
            return False
    
    # ========== إدارة الموردين ==========
    
    def load_suppliers(self) -> List[Dict]:
        """تحميل الموردين"""
        suppliers = []
        try:
            with open(self.suppliers_file, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    suppliers.append(row)
        except FileNotFoundError:
            self.initialize_files()
            return self.load_suppliers()
        except Exception as e:
            print(f"❌ خطأ في تحميل الموردين: {e}")
        
        return suppliers
    
    def save_suppliers(self, suppliers: List[Dict]):
        """حفظ الموردين"""
        with open(self.suppliers_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['supplier_id', 'name', 'phone', 'address', 'email']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(suppliers)
        
        print(f"✅ تم حفظ {len(suppliers)} مورد")
    
    # ========== إدارة العملاء ==========
    
    def find_customer_id(self, customer_name: str) -> Optional[str]:
        """البحث عن معرف العميل"""
        history = self.load_history()
        for record in history:
            if record.get('customer_name', '').strip().lower() == customer_name.strip().lower():
                return record.get('customer_id', '')
        return None
    
    def get_customer_balance(self, customer_id: str) -> float:
        """حساب رصيد العميل"""
        try:
            history = self.load_history()
            customer_records = [record for record in history if record.get('customer_id') == customer_id]
            
            if not customer_records:
                return 0.0
            
            total_owed = sum(record.get('remaining', 0) for record in customer_records)
            return total_owed
            
        except Exception as e:
            print(f"⚠ خطأ في حساب رصيد العميل: {e}")
            return 0.0
    
    # ========== أدوات مساعدة ==========
    
    def backup_database(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"backups/backup_{timestamp}"
            
            os.makedirs(backup_dir, exist_ok=True)
            
            files_to_backup = [self.items_file, self.history_file, 
                              self.imports_file, self.suppliers_file]
            
            for file in files_to_backup:
                if os.path.exists(file):
                    shutil.copy2(file, os.path.join(backup_dir, os.path.basename(file)))
            
            print(f"✅ تم إنشاء نسخة احتياطية في: {backup_dir}")
            return backup_dir
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return None
    
    def export_to_excel(self):
        """تصدير البيانات إلى Excel"""
        try:
            import pandas as pd
            
            # تحميل البيانات
            items = self.load_items()
            history = self.load_history()
            imports = self.load_imports()
            suppliers = self.load_suppliers()
            
            # تصدير إلى Excel
            with pd.ExcelWriter('database_export.xlsx', engine='openpyxl') as writer:
                if items:
                    pd.DataFrame(items).to_excel(writer, sheet_name='المنتجات', index=False)
                if history:
                    pd.DataFrame(history).to_excel(writer, sheet_name='المبيعات', index=False)
                if imports:
                    pd.DataFrame(imports).to_excel(writer, sheet_name='الاستيراد', index=False)
                if suppliers:
                    pd.DataFrame(suppliers).to_excel(writer, sheet_name='الموردين', index=False)
            
            print("✅ تم تصدير البيانات إلى database_export.xlsx")
            return True
            
        except ImportError:
            print("❌ تحتاج إلى تثبيت pandas و openpyxl: pip install pandas openpyxl")
            return False
        except Exception as e:
            print(f"❌ خطأ في التصدير: {e}")
            return False
    
    def get_database_stats(self) -> Dict:
        """الحصول على إحصائيات قاعدة البيانات"""
        return {
            "المنتجات": len(self.load_items()),
            "سجلات المبيعات": len(self.load_history()),
            "سجلات الاستيراد": len(self.load_imports()),
            "الموردين": len(self.load_suppliers()),
            "ملف المنتجات": f"{os.path.getsize(self.items_file)} بايت",
            "ملف المبيعات": f"{os.path.getsize(self.history_file)} بايت"
        }
    
    def rebuild_database(self):
        """إعادة بناء قاعدة البيانات (استخدم بحذر)"""
        confirm = input("⚠ هل أنت متأكد من إعادة بناء قاعدة البيانات؟ سيتم حذف جميع البيانات! (نعم/لا): ")
        
        if confirm.lower() == 'نعم':
            try:
                # حذف الملفات
                for file in [self.items_file, self.history_file, self.imports_file, self.suppliers_file]:
                    if os.path.exists(file):
                        os.remove(file)
                        print(f"🗑️ تم حذف {file}")
                
                # إعادة الإنشاء
                self.initialize_files()
                print("✅ تم إعادة بناء قاعدة البيانات بنجاح")
                
            except Exception as e:
                print(f"❌ خطأ في إعادة البناء: {e}")
        else:
            print("❌ تم إلغاء العملية")
class ReceiptGenerator:
    """مولد فواتير بتنسيق شركة مكة المكرمة مع حفظ كصورة"""
    
    @staticmethod
    def generate_receipt(receipt_data: Dict, output_path: str = None):
        """إنشاء فاتورة كصورة"""
        if output_path is None:
            # حفظ في نفس مجلد البرنامج
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      f"فاتورة_{receipt_data['receipt_id']}.png")
        
        try:
            # إعادة تشكيل النص العربي
            def format_arabic_text(text):
                reshaped_text = arabic_reshaper.reshape(text)
                return get_display(reshaped_text)
            
            # إنشاء صورة الفاتورة
            img_width = 800
            line_height = 30
            margin = 40
            
            # حساب ارتفاع الصورة
            num_lines = 15 + len(receipt_data['items']) * 2  # السطور الأساسية + المنتجات
            img_height = margin * 2 + num_lines * line_height
            
            # إنشاء صورة جديدة
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # محاولة تحميل خط عربي، أو استخدام الخط الافتراضي
            try:
                font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'arial.ttf')
                font = ImageFont.truetype(font_path, 14)
                font_bold = ImageFont.truetype(font_path, 16)
                font_large = ImageFont.truetype(font_path, 18)
            except:
                font = ImageFont.load_default()
                font_bold = ImageFont.load_default()
                font_large = ImageFont.load_default()
            
            # البدء في الرسم
            y_position = margin
            
            # =======================================
            # عنوان الشركة
            company_title = format_arabic_text("شركة مكة المكرمة")
            title_width = draw.textlength(company_title, font=font_large)
            draw.text(((img_width - title_width) // 2, y_position), 
                     company_title, fill='black', font=font_large)
            y_position += line_height
            
            # العنوان الفرعي
            subtitle = format_arabic_text("الاستيراد والتجارة والتوزيع")
            subtitle_width = draw.textlength(subtitle, font=font_bold)
            draw.text(((img_width - subtitle_width) // 2, y_position), 
                     subtitle, fill='black', font=font_bold)
            y_position += line_height
            
            # المالك
            owner = format_arabic_text("أشرف حافظ")
            owner_width = draw.textlength(owner, font=font)
            draw.text(((img_width - owner_width) // 2, y_position), 
                     owner, fill='black', font=font)
            y_position += line_height * 2
            
            # =======================================
            # معلومات الفاتورة
            info_lines = [
                f"رقم الفاتورة: {receipt_data['receipt_id']}",
                f"التاريخ: {receipt_data['date']}",
                f"العميل: {receipt_data['customer_name']}",
                f"معرف العميل: {receipt_data['customer_id']}"
            ]
            
            for line in info_lines:
                formatted_line = format_arabic_text(line)
                draw.text((margin, y_position), formatted_line, fill='black', font=font)
                y_position += line_height
            
            y_position += line_height // 2
            
            # =======================================
            # جدول المنتجات
            products_title = format_arabic_text("المنتجات")
            draw.text((margin, y_position), products_title, fill='black', font=font_bold)
            y_position += line_height
            
            # عنوان الجدول
            table_header = format_arabic_text("اسم المنتج | الكمية | السعر | الإجمالي")
            draw.text((margin, y_position), table_header, fill='black', font=font)
            y_position += line_height
            
            # المنتجات
            for item in receipt_data['items']:
                subtotal = item['quantity'] * item['selling_price']
                item_name = item['name']
                if len(item_name) > 20:
                    item_name = item_name[:17] + "..."
                
                # تنسيق السطر
                full_name = f"{item_name} ({item.get('size', '')})"
                formatted_name = format_arabic_text(full_name.ljust(24))
                
                # كتابة المنتج في سطرين
                product_line = format_arabic_text(f"{formatted_name} | {item['quantity']:^6} | {item['selling_price']:>6.2f} | {subtotal:>8.2f}")
                draw.text((margin, y_position), product_line, fill='black', font=font)
                y_position += line_height
            
            y_position += line_height // 2
            
            # =======================================
            # الإجماليات
            totals_title = format_arabic_text("الإجماليات")
            draw.text((margin, y_position), totals_title, fill='black', font=font_bold)
            y_position += line_height
            
            # حساب الإجماليات من البيانات
            current_total = receipt_data.get('total', 0)
            previous_balance = receipt_data.get('previous_balance', 0)
            total_cumulative = receipt_data.get('total_cumulative', current_total)
            amount_paid = receipt_data.get('amount_paid', 0)
            remaining = receipt_data.get('remaining', 0)
            
            # تحديد حالة الدفع
            if remaining == 0:
                payment_status = "مدفوع بالكامل"
            elif amount_paid == 0:
                payment_status = "غير مدفوع"
            else:
                payment_status = "مدفوع جزئيًا"
            
            # إنشاء أسطر الإجماليات
            totals_lines = [
                f"الإجمالي الحالي: {current_total:>10.2f} ج.م",
                f"الرصيد السابق: {previous_balance:>10.2f} ج.م",
                f"الإجمالي الكلي: {total_cumulative:>10.2f} ج.م",
                "",
                f"المدفوع الآن: {amount_paid:>10.2f} ج.م",
                f"المبلغ المتبقي: {remaining:>10.2f} ج.م",
                "",
                f"طريقة الدفع: {receipt_data.get('payment_method', 'نقدي')}",
                f"حالة الدفع: {payment_status}"
            ]
            
            for line in totals_lines:
                if line:  # إذا لم يكن السطر فارغاً
                    formatted_line = format_arabic_text(line)
                    draw.text((margin, y_position), formatted_line, fill='black', font=font)
                y_position += line_height
            
            # الملاحظات
            if receipt_data.get('notes'):
                notes = receipt_data['notes']
                notes_text = format_arabic_text(f"ملاحظات: {notes}")
                draw.text((margin, y_position), notes_text, fill='black', font=font)
                y_position += line_height
            
            # الربح
            profit = receipt_data.get('profit', 0)
            profit_line = format_arabic_text(f"الربح الصافي: {profit:>10.2f} ج.م")
            draw.text((margin, y_position), profit_line, fill='black', font=font)
            y_position += line_height
            
            # كود الفاتورة
            code_line = format_arabic_text(f"كود الفاتورة: INV{receipt_data['receipt_id']}")
            draw.text((margin, y_position), code_line, fill='black', font=font)
            y_position += line_height * 2
            
            # =======================================
            # التذييل
            footer = format_arabic_text("شكراً لتعاملكم مع شركة مكة المكرمة")
            footer_width = draw.textlength(footer, font=font_bold)
            draw.text(((img_width - footer_width) // 2, y_position), 
                     footer, fill='black', font=font_bold)
            
            # حفظ الصورة
            img.save(output_path, 'PNG')
            print(f" تم حفظ الفاتورة كصورة: {output_path}")
            
            # أيضًا إنشاء نص الفاتورة وحفظه كملف نصي
            txt_output = output_path.replace('.png', '.txt')
            text_receipt = ReceiptGenerator.create_text_receipt(receipt_data)
            with open(txt_output, 'w', encoding='utf-8') as f:
                f.write(text_receipt)
            
            return output_path
            
        except Exception as e:
            print(f" خطأ في إنشاء صورة الفاتورة: {e}")
            # العودة إلى الطريقة القديمة في حالة الخطأ
            return ReceiptGenerator.create_text_file_receipt(receipt_data)
    
    @staticmethod
    def create_text_receipt(receipt_data: Dict):
        """إنشاء فاتورة كنص (بديل)"""
        try:
            # معلومات الفاتورة
            receipt_id = receipt_data['receipt_id']
            customer_name = receipt_data['customer_name']
            customer_id = receipt_data['customer_id']
            date_str = receipt_data['date']
            
            # حساب الإجماليات
            current_total = receipt_data.get('total', 0)
            previous_balance = receipt_data.get('previous_balance', 0)
            total_cumulative = receipt_data.get('total_cumulative', current_total)
            amount_paid = receipt_data.get('amount_paid', 0)
            remaining = receipt_data.get('remaining', 0)
            profit = receipt_data.get('profit', 0)
            payment_method = receipt_data.get('payment_method', 'نقدي')
            
            # تحديد حالة الدفع
            if remaining == 0:
                payment_status = "مدفوع بالكامل"
            elif amount_paid == 0:
                payment_status = "غير مدفوع"
            else:
                payment_status = "مدفوع جزئيًا"
            
            # بناء الفاتورة كنص
            receipt = f"""
            =======================================
                        شركة مكة المكرمة           
                الاستيراد والتجارة والتوزيع      
                        أشرف حافظ                
            =======================================
            رقم الفاتورة: {receipt_id}
            التاريخ: {date_str}
            العميل: {customer_name}
            معرف العميل: {customer_id}
            =======================================
                    المنتجات                   
            ----------------------------------------
            اسم المنتج | الكمية | السعر  | الإجمالي
            ----------------------------------------
            """
            
            # إضافة المنتجات
            for item in receipt_data['items']:
                subtotal = item['quantity'] * item['selling_price']
                item_name = item['name']
                if len(item_name) > 20:
                    item_name = item_name[:17] + "..."
                full_name = f"{item_name} ({item.get('size', '')})"
                receipt += f"{full_name:<24} | {item['quantity']:^6} | {item['selling_price']:>6.2f} | {subtotal:>8.2f}\n"
            
            receipt += f"""---------------------------------------------------------
            الإجمالي الحالي:          {current_total:>10.2f} ج.م
            الرصيد السابق:            {previous_balance:>10.2f} ج.م
            الإجمالي الكلي:           {total_cumulative:>10.2f} ج.م

            المدفوع الآن:             {amount_paid:>10.2f} ج.م
            المبلغ المتبقي:           {remaining:>10.2f} ج.م

            طريقة الدفع: {payment_method}
            حالة الدفع: {payment_status}
            """
            
            # الملاحظات
            if receipt_data.get('notes'):
                receipt += f"""
            ملاحظات: {receipt_data['notes']}
            """
            
            receipt += f"""
            الربح الصافي:             {profit:>10.2f} ج.م

            كود الفاتورة: INV{receipt_id}
            =======================================
            شكراً لتعاملكم مع شركة مكة المكرمة   
            =======================================
            """
            
            return receipt
            
        except Exception as e:
            return f"خطأ في إنشاء الفاتورة: {str(e)}"
    
    @staticmethod
    def create_text_file_receipt(receipt_data: Dict):
        """إنشاء ملف نصي للفاتورة (بديل)"""
        try:
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      f"فاتورة_{receipt_data['receipt_id']}.txt")
            
            text_receipt = ReceiptGenerator.create_text_receipt(receipt_data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_receipt)
            
            print(f" تم حفظ الفاتورة كنص: {output_path}")
            return output_path
            
        except Exception as e:
            print(f" خطأ في إنشاء ملف نصي: {e}")
            return None
    
    @staticmethod
    def generate_receipt_from_text(text: str, output_path: str = None):
        """إنشاء صورة من نص الفاتورة مباشرة"""
        if output_path is None:
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      "فاتورة_مؤقتة.png")
        
        try:
            # إعادة تشكيل النص العربي
            def format_arabic_text(text):
                reshaped_text = arabic_reshaper.reshape(text)
                return get_display(reshaped_text)
            
            # حساب أبعاد الصورة
            lines = text.split('\n')
            img_width = 800
            line_height = 25
            margin = 40
            
            img_height = margin * 2 + len(lines) * line_height
            
            # إنشاء الصورة
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # محاولة تحميل خط
            try:
                font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'arial.ttf')
                font = ImageFont.truetype(font_path, 12)
            except:
                font = ImageFont.load_default()
            
            # كتابة النص
            y_position = margin
            for line in lines:
                if line.strip():
                    formatted_line = format_arabic_text(line)
                    draw.text((margin, y_position), formatted_line, fill='black', font=font)
                y_position += line_height
            
            # حفظ الصورة
            img.save(output_path, 'PNG')
            print(f" تم حفظ الصورة من النص: {output_path}")
            return output_path
            
        except Exception as e:
            print(f" خطأ في إنشاء الصورة من النص: {e}")
            return None

class AddItemDialog(QDialog):
    """نافذة إضافة منتج جديد مع حقل الوحدة"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("إضافة منتج جديد")
        self.setFixedSize(400, 350)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # رقم المنتج (تلقائي)
        self.id_input = QLineEdit()
        self.id_input.setText(str(random.randint(1000, 9999)))
        self.id_input.setReadOnly(True)
        form_layout.addRow("رقم المنتج:", self.id_input)
        
        # اسم المنتج (الصنف)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("أدخل اسم المنتج")
        form_layout.addRow("اسم المنتج (الصنف):", self.name_input)
        
        # الوحدة
        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("عدد، كيلو، لتر، متر، ...")
        self.unit_input.setText("عدد")  # القيمة الافتراضية
        form_layout.addRow("الوحدة:", self.unit_input)
        
        # المقاس
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("وسط، كبير، 100 مل، ...")
        form_layout.addRow("المقاس:", self.size_input)
        
        # سعر الشراء
        self.buying_price_input = QDoubleSpinBox()
        self.buying_price_input.setDecimals(2)
        self.buying_price_input.setMinimum(0.0)
        self.buying_price_input.setMaximum(999999.99)
        self.buying_price_input.setPrefix("ج.م ")
        form_layout.addRow("سعر الشراء:", self.buying_price_input)
        
        # سعر البيع
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setDecimals(2)
        self.selling_price_input.setMinimum(0.0)
        self.selling_price_input.setMaximum(999999.99)
        self.selling_price_input.setPrefix("ج.م ")
        form_layout.addRow("سعر البيع:", self.selling_price_input)
        
        # الكمية
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(99999)
        form_layout.addRow("الكمية:", self.quantity_input)
        
        layout.addLayout(form_layout)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("إضافة")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        add_btn.clicked.connect(self.accept)
        button_layout.addWidget(add_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_item(self):
        """الحصول على بيانات المنتج المدخلة"""
        return {
            'item_id': self.id_input.text().strip(),
            'name': self.name_input.text().strip(),
            'unit': self.unit_input.text().strip() or "عدد",
            'size': self.size_input.text().strip(),
            'buying_price': self.buying_price_input.value(),
            'selling_price': self.selling_price_input.value(),
            'quantity': self.quantity_input.value()
        }

class MainWindow(QMainWindow):
    """النافذة الرئيسية المحسّنة"""
   
    def __init__(self):
        super().__init__()
        self.db = CSVDatabase()
        self.init_ui()
   
    def init_ui(self):
        self.setWindowTitle('نظام إدارة المتجر - شركة مكة المكرمة')
        self.setGeometry(100, 100, 1000, 600)  # جعلها أصغر قليلاً
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
       
        # خلفية غامقة كما كانت في السابق
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1f2327;
            }
            QLabel {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
        """)
       
        # الويدجت المركزية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
       
        # عنوان لوحة التحكم (بدون أي صناديق أو خطوط)
        header = QLabel("لوحة التحكم الرئيسية")
        header.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #3498db;
                padding: 10px;
                background-color: transparent;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # عنوان الشركة أسفل لوحة التحكم
        company_title = QLabel("شركة مكة المكرمة")
        company_title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                color: #3498db;
                padding: 5px;
                background-color: transparent;
            }
        """)
        company_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(company_title)
        
        # وصف الشركة
        company_desc = QLabel("الاستيراد والتجارة والتوزيع")
        company_desc.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #7f8c8d;
                padding: 5px;
                background-color: transparent;
            }
        """)
        company_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(company_desc)
        
        # فاصل بسيط
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #34495e; margin: 10px 50px;")
        main_layout.addWidget(separator)
       
        # الأزرار الرئيسية (5 أزرار فقط، بدون إدارة العملاء)
        buttons_widget = QWidget()
        button_layout = QGridLayout(buttons_widget)
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(20, 20, 20, 20)
       
        # فقط 5 أزرار كما كانت في السابق
        main_buttons = [
            ("📦", "إدارة المخزون", self.open_items_management, "#3498db", "#2980b9"),
            ("🧾", "إنشاء فاتورة", self.open_create_receipt, "#2ecc71", "#27ae60"),
            ("📤", "الاستيراد", self.open_imports, "#e67e22", "#d35400"),
            ("📜", "سجل المبيعات", self.open_history, "#9b59b6", "#8e44ad"),
            ("📊", "تحليل الأرباح", self.open_profit_analysis, "#27ae60", "#229954"),
        ]
       
        for i, (icon, text, slot, color, hover_color) in enumerate(main_buttons):
            btn = self.create_simple_button(icon, text, color, hover_color)
            btn.clicked.connect(slot)
            button_layout.addWidget(btn, i // 2, i % 2)
       
        main_layout.addWidget(buttons_widget)
        main_layout.addStretch()
       
       # معلومات الشركة في الأسفل (بدون أي صندوق أو خط)
        company_info = QLabel("ENG/Shady_Mayez")
        company_info.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #3498db;
                padding: 10px;
                background-color: transparent;
            }
        """)

        company_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(company_info)
       
        # زر الخروج فقط في الزاوية اليسرى السفلية
        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        
        # زر الخروج فقط (بدون إعدادات أو مساعدة)
        exit_btn = QPushButton(" خروج")
        exit_btn.setFixedSize(100, 35)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_btn.clicked.connect(self.close)
        exit_layout.addWidget(exit_btn)
        
        main_layout.addLayout(exit_layout)
       
        # شريط الحالة
        self.statusBar().showMessage("مرحباً بك في نظام إدارة المتجر - جاهز للعمل")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #2c3e50;
                color: white;
                font-size: 12px;
                padding: 5px;
            }
        """)
    
    def create_simple_button(self, icon, text, color, hover_color):
        """إنشاء زر بسيط بدون صناديق داخلية"""
        btn = QPushButton(f"{icon}\n{text}")
        btn.setMinimumSize(200, 120)
        btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                background-color: {color};
                color: white;
                border: 2px solid {color};
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 2px solid {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {color};
                border: 2px solid white;
            }}
        """)
        return btn
   
    def open_items_management(self):
        self.items_window = ItemsManagementWindow(self.db)
        self.items_window.show()
   
    def open_create_receipt(self):
        self.receipt_window = CreateReceiptWindow(self.db)
        self.receipt_window.show()
   
    def open_imports(self):
        self.imports_window = ImportsWindow(self.db)
        self.imports_window.show()
   
    def open_history(self):
        self.history_window = HistoryWindow(self.db)
        self.history_window.show()
   
    def open_profit_analysis(self):
        self.profit_window = ProfitAnalysisWindow(self.db)
        self.profit_window.show()

import time
import threading
from datetime import datetime


class ItemsManagementWindow(QWidget):
    """إدارة المخزون المحسّنة مع تمكين التعديل الكامل"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db  # استخدام CSVDatabase مباشرة (ليس SmartCSVManager)
        self.edit_mode = False
        self.original_items = []  # تخزين العناصر الأصلية للبحث
        self.init_ui()
        self.load_items()
    
    def init_ui(self):
        self.setWindowTitle('إدارة المخزون')
        self.setGeometry(150, 150, 1100, 600)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout()
        
        # الرأس
        header_layout = QHBoxLayout()
        title = QLabel("إدارة المخزون")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        
        # زر التبديل
        self.mode_btn = QPushButton("وضع التعديل")
        self.mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.mode_btn.clicked.connect(self.toggle_mode)
        header_layout.addWidget(self.mode_btn)
        
        # زر إضافة
        self.add_btn = QPushButton("+ إضافة منتج")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.add_btn.clicked.connect(self.add_item)
        self.add_btn.setVisible(False)
        header_layout.addWidget(self.add_btn)
        
        # زر حذف الصف المحدد
        self.delete_btn = QPushButton("- حذف المحدد")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected_item)
        self.delete_btn.setVisible(False)  # يظهر فقط في وضع التعديل
        header_layout.addWidget(self.delete_btn)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # شريط البحث
        search_layout = QHBoxLayout()
        
        # البحث بالاسم
        name_search_layout = QVBoxLayout()
        name_search_layout.addWidget(QLabel("البحث بالاسم:"))
        
        self.name_search_input = QLineEdit()
        self.name_search_input.setPlaceholderText("أدخل جزء من اسم المنتج...")
        self.name_search_input.textChanged.connect(self.filter_items)
        name_search_layout.addWidget(self.name_search_input)
        
        search_layout.addLayout(name_search_layout)
        
        # البحث بالمقاس
        size_search_layout = QVBoxLayout()
        size_search_layout.addWidget(QLabel("البحث بالمقاس:"))
        
        self.size_search_combo = QComboBox()
        self.size_search_combo.setEditable(True)
        self.size_search_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.size_search_combo.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.size_search_combo.lineEdit().setPlaceholderText("اختر أو اكتب المقاس...")
        self.size_search_combo.lineEdit().textChanged.connect(self.filter_items)
        self.size_search_combo.setMinimumWidth(300)
        size_search_layout.addWidget(self.size_search_combo)
        
        search_layout.addLayout(size_search_layout)
        
        # الإحصائيات
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        
        # مجموع الكمية
        total_qty_layout = QVBoxLayout()
        total_qty_layout.addWidget(QLabel("مجموع الكمية:"))
        
        self.total_qty_label = QLabel("0")
        self.total_qty_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                min-width: 80px;
                text-align: center;
            }
        """)
        self.total_qty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_qty_layout.addWidget(self.total_qty_label)
        
        stats_layout.addLayout(total_qty_layout)
        
        # رأس المالي
        total_capital_layout = QVBoxLayout()
        total_capital_layout.addWidget(QLabel("رأس المالي:"))
        
        self.total_capital_label = QLabel("0.00 ج.م")
        self.total_capital_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #27ae60;
                padding: 5px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                min-width: 120px;
                text-align: center;
            }
        """)
        self.total_capital_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_capital_layout.addWidget(self.total_capital_label)
        
        stats_layout.addLayout(total_capital_layout)
        
        search_layout.addLayout(stats_layout)
        
        # زر إعادة تعيين البحث
        reset_btn = QPushButton("إعادة تعيين")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        reset_btn.clicked.connect(self.reset_search)
        search_layout.addWidget(reset_btn)
        
        search_layout.addStretch()
        layout.addLayout(search_layout)
        
        # الجدول - تم تحديث الأعمدة
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["الرقم", "الصنف", "الوحدة", "المقاس", "سعر الشراء", "سعر البيع", "الكمية"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        
        # تنسيق موحد لجميع الجداول
        self.table.setStyleSheet(self.get_table_style())
        
        # تمكين التحرير عند النقر المزدوج
        self.table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.SelectedClicked)
        
        layout.addWidget(self.table)
        
        # الأزرار
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("حفظ التغييرات")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        save_btn.clicked.connect(self.save_changes)
        save_btn.setVisible(False)
        self.save_btn = save_btn
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.cancel_edit)
        cancel_btn.setVisible(False)
        self.cancel_btn = cancel_btn
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("إغلاق")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_table_style(self):
        """إرجاع تنسيق موحد لجميع الجداول"""
        return """
            QTableWidget {
                background-color: #1f2327;
                alternate-background-color: #272a2d;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """
    
    def closeEvent(self, event):
        """❌ إغلاق مباشر بدون أسئلة أو حفظ تلقائي"""
        event.accept()
    
    def get_virtual_table(self):
        """
        إرجاع نسخة افتراضية من جدول المخزون
        تستخدم في نافذة إنشاء الفواتير
        """
        return self.create_virtual_copy()
    
    def create_virtual_copy(self):
        """إنشاء نسخة عميقة من العناصر الحالية"""
        import copy
        return copy.deepcopy(self.original_items)
    
    def commit_virtual_changes(self, virtual_table):
        """
        تطبيق التغييرات من الجدول الافتراضي على الجدول الحقيقي
        يتم استدعاؤها من نافذة إنشاء الفواتير بعد تأكيد الدفع
        """
        try:
            # تحديث العناصر الأصلية بالبيانات من الجدول الافتراضي
            for virtual_item in virtual_table:
                item_id = virtual_item.get('item_id')
                
                # البحث عن العنصر المطابق في القائمة الأصلية
                for i, original_item in enumerate(self.original_items):
                    if original_item.get('item_id') == item_id:
                        # تحديث الكمية فقط (الحفاظ على باقي البيانات)
                        if 'quantity' in virtual_item:
                            self.original_items[i]['quantity'] = virtual_item['quantity']
                        break
            
            # حفظ التغييرات في قاعدة البيانات
            self.db.save_items(self.original_items)
            
            # تحديث واجهة المستخدم
            self.filter_items()
            self.calculate_totals()
            
            return True
        except Exception as e:
            print(f"خطأ في تطبيق التغييرات الافتراضية: {e}")
            return False
    
    def update_item_quantity(self, item_id, quantity_change):
        """
        تحديث كمية عنصر في المخزون الحقيقي
        quantity_change: التغيير في الكمية (سالب للخصم، موجب للإضافة)
        """
        try:
            # البحث عن العنصر وتحديث الكمية
            for item in self.original_items:
                if str(item.get('item_id', '')) == str(item_id):
                    current_qty = item.get('quantity', 0)
                    new_qty = current_qty + quantity_change
                    
                    # التأكد من أن الكمية لا تكون سالبة
                    if new_qty < 0:
                        new_qty = 0
                        print(f"تحذير: الكمية أصبحت سالبة للعنصر {item_id}، تم ضبطها لـ 0")
                    
                    item['quantity'] = new_qty
                    print(f"تم تحديث العنصر {item_id}: {current_qty} → {new_qty} (تغيير: {quantity_change})")
                    
                    # حفظ التغييرات في قاعدة البيانات
                    self.db.save_items(self.original_items)
                    
                    # تحديث العرض
                    self.filter_items()
                    self.calculate_totals()
                    
                    return True
            
            print(f"خطأ: العنصر {item_id} غير موجود في المخزون")
            return False
            
        except Exception as e:
            print(f"خطأ في تحديث كمية العنصر: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_items(self):
        """تحميل العناصر من قاعدة البيانات"""
        self.original_items = self.db.load_items()  # تحميل مباشر من CSVDatabase
        self.populate_size_combo()
        self.filter_items()
        self.calculate_totals()  # حساب الإحصائيات عند تحميل العناصر
    
    def populate_size_combo(self):
        """تعبئة خانة البحث بالمقاسات الفريدة"""
        try:
            # مسح المحتوى الحالي مع الاحتفاظ على العناصر الأساسية
            self.size_search_combo.clear()
            
            # استخراج المقاسات الفريدة من العناصر الأصلية
            unique_sizes = set()
            for item in self.original_items:
                size = str(item.get('size', '')).strip()
                if size:
                    unique_sizes.add(size)
            
            # إضافة خيار "جميع المقاسات" أولاً
            self.size_search_combo.addItem("جميع المقاسات")
            
            # إضافة المقاسات مرتبة
            for size in sorted(unique_sizes):
                self.size_search_combo.addItem(size)
            
            # إعداد الـ completer
            completer = QCompleter([self.size_search_combo.itemText(i) for i in range(self.size_search_combo.count())])
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.size_search_combo.setCompleter(completer)
            
            # اختيار العنصر الأول افتراضياً
            self.size_search_combo.setCurrentIndex(0)
            
        except Exception as e:
            print(f"خطأ في تحميل المقاسات: {e}")
    
    def filter_items(self):
        """فلترة العناصر بناءً على البحث بالاسم والمقاس"""
        try:
            # الحصول على قيم البحث
            name_filter = self.name_search_input.text().strip()
            size_filter = self.size_search_combo.currentText().strip()
            
            # إذا كان البحث بالمقاس هو "جميع المقاسات"، تجاهل الفلترة بالمقاس
            apply_size_filter = (size_filter and size_filter != "جميع المقاسات")
            
            # فلترة العناصر
            filtered_items = []
            for item in self.original_items:
                # فلترة بالاسم (بحث جزئي)
                name_match = True
                if name_filter:
                    item_name = str(item.get('name', '')).lower()
                    if name_filter.lower() not in item_name:
                        name_match = False
                
                # فلترة بالمقاس
                size_match = True
                if apply_size_filter:
                    item_size = str(item.get('size', '')).strip()
                    if size_filter.lower() != item_size.lower():
                        size_match = False
                
                # إذا تطابق كلا الشرطين (أو أحدهما إذا الآخر فارغ)
                if name_match and size_match:
                    filtered_items.append(item)
            
            # عرض العناصر المفلترة في الجدول
            self.display_filtered_items(filtered_items)
            
            # حساب الإحصائيات للعناصر المفلترة
            self.calculate_totals(filtered_items)
            
        except Exception as e:
            print(f"خطأ في فلترة العناصر: {e}")
            QMessageBox.warning(self, "خطأ", f"حدث خطأ في الفلترة: {str(e)}")
    
    def display_filtered_items(self, items):
        """عرض العناصر المفلترة في الجدول"""
        self.table.setRowCount(len(items))
        
        for i, item in enumerate(items):
            self.add_item_to_row(i, item)
        
        # ضبط عرض الأعمدة
        self.table.setColumnWidth(0, 80)   # الرقم
        self.table.setColumnWidth(1, 200)  # الصنف (تم التوسيع)
        self.table.setColumnWidth(2, 100)  # الوحدة
        self.table.setColumnWidth(3, 100)  # المقاس
        self.table.setColumnWidth(4, 120)  # سعر الشراء
        self.table.setColumnWidth(5, 120)  # سعر البيع
        self.table.setColumnWidth(6, 80)   # الكمية
        
        # عرض عدد النتائج
        if hasattr(self, 'result_label'):
            self.result_label.setText(f"عدد النتائج: {len(items)}")
    
    def calculate_totals(self, items=None):
        """حساب مجموع الكمية ورأس المالي"""
        try:
            if items is None:
                items = self.original_items
            
            total_quantity = 0
            total_capital = 0.0
            
            for item in items:
                # حساب مجموع الكمية
                quantity = item.get('quantity', 0)
                if isinstance(quantity, (int, float)):
                    total_quantity += int(quantity)
                
                # حساب رأس المالي (سعر الشراء × الكمية)
                buying_price = item.get('buying_price', 0.0)
                if isinstance(buying_price, (int, float)):
                    total_capital += float(buying_price) * quantity
            
            # تحديث التسميات
            self.total_qty_label.setText(str(total_quantity))
            self.total_capital_label.setText(f"{total_capital:,.2f} ج.م")
            
        except Exception as e:
            print(f"خطأ في حساب الإحصائيات: {e}")
            self.total_qty_label.setText("0")
            self.total_capital_label.setText("0.00 ج.م")
    
    def add_item_to_row(self, row_index, item_data):
        """إضافة عنصر إلى صف محدد مع تمكين التحرير"""
        # الرقم (الرقم التسلسلي) - لا يمكن تحريره
        item_id = str(item_data.get('item_id', ''))
        item_id_widget = QTableWidgetItem(item_id)
        item_id_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item_id_widget.setFlags(item_id_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)  # غير قابل للتحرير
        self.table.setItem(row_index, 0, item_id_widget)
        
        # الصنف - يمكن تحريره (نص أو أرقام)
        name = str(item_data.get('name', ''))
        name_widget = QTableWidgetItem(name)
        name_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.edit_mode:
            name_widget.setFlags(name_widget.flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            name_widget.setFlags(name_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 1, name_widget)
        
        # الوحدة - يمكن تحريره (نص أو أرقام)
        unit = str(item_data.get('unit', 'عدد'))  # Default: "عدد"
        unit_widget = QTableWidgetItem(unit)
        unit_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.edit_mode:
            unit_widget.setFlags(unit_widget.flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            unit_widget.setFlags(unit_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 2, unit_widget)
        
        # المقاس - يمكن تحريره (نص أو أرقام)
        size = str(item_data.get('size', ''))
        size_widget = QTableWidgetItem(size)
        size_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.edit_mode:
            size_widget.setFlags(size_widget.flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            size_widget.setFlags(size_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 3, size_widget)
        
        # سعر الشراء - يمكن تحريره (أرقام فقط)
        buying_price = item_data.get('buying_price', 0.0)
        buying_price_widget = QTableWidgetItem(f"{buying_price}")
        buying_price_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.edit_mode:
            buying_price_widget.setFlags(buying_price_widget.flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            buying_price_widget.setFlags(buying_price_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 4, buying_price_widget)
        
        # سعر البيع - يمكن تحريره (أرقام فقط)
        selling_price = item_data.get('selling_price', 0.0)
        selling_price_widget = QTableWidgetItem(f"{selling_price}")
        selling_price_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.edit_mode:
            selling_price_widget.setFlags(selling_price_widget.flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            selling_price_widget.setFlags(selling_price_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 5, selling_price_widget)
        
        # الكمية - يمكن تحريره (أرقام فقط)
        quantity = item_data.get('quantity', 0)
        quantity_widget = QTableWidgetItem(str(quantity))
        quantity_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.edit_mode:
            quantity_widget.setFlags(quantity_widget.flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            quantity_widget.setFlags(quantity_widget.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 6, quantity_widget)
    
    def toggle_mode(self):
        self.edit_mode = not self.edit_mode
        
        if self.edit_mode:
            self.mode_btn.setText("وضع العرض")
            self.add_btn.setVisible(True)
            self.delete_btn.setVisible(True)
            self.save_btn.setVisible(True)
            self.cancel_btn.setVisible(True)
            self.enable_all_editing()
        else:
            self.mode_btn.setText("وضع التعديل")
            self.add_btn.setVisible(False)
            self.delete_btn.setVisible(False)
            self.save_btn.setVisible(False)
            self.cancel_btn.setVisible(False)
            self.disable_all_editing()
        
        self.load_items()
    
    def enable_all_editing(self):
        """تمكين تحرير جميع الخلايا"""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                if col != 0:  # تخطي عمود الرقم (غير قابل للتحرير)
                    item = self.table.item(row, col)
                    if item:
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
    
    def disable_all_editing(self):
        """تعطيل تحرير جميع الخلايا"""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    
    def add_item(self):
        dialog = AddItemDialog(self)
        if dialog.exec():
            new_item = dialog.get_item()
            items = self.db.load_items()
            
            # توليد رقم تسلسلي جديد
            existing_ids = []
            for item in items:
                try:
                    # حاول تحويل ID إلى رقم
                    item_id = int(item.get('item_id', '0'))
                    existing_ids.append(item_id)
                except ValueError:
                    # إذا لم يكن رقماً، تجاهله
                    pass
            
            new_id = str(max(existing_ids, default=999) + 1)
            
            # إنشاء العنصر مع حقل 'unit'
            item_to_save = {
                'item_id': new_id,
                'name': new_item.get('name', ''),
                'size': new_item.get('size', ''),
                'buying_price': new_item.get('buying_price', 0.0),
                'selling_price': new_item.get('selling_price', 0.0),
                'quantity': new_item.get('quantity', 0),
                'unit': new_item.get('unit', 'عدد')
            }
            
            items.append(item_to_save)
            
            # حفظ العناصر في قاعدة البيانات
            try:
                self.db.save_items(items)
                QMessageBox.information(self, "نجاح", f"تمت إضافة المنتج '{new_item['name']}' بنجاح!")
                self.load_items()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل حفظ المنتج:\n{str(e)}")
    
    def save_changes(self):
        """حفظ جميع التغييرات في جدول إدارة المخزون"""
        try:
            # تحميل العناصر الحالية من قاعدة البيانات
            current_items = self.db.load_items()
            
            # إنشاء قاموس للبحث السريع عن العناصر
            items_dict = {item['item_id']: item for item in current_items}
            
            # تحديث العناصر المعدلة من الجدول
            for i in range(self.table.rowCount()):
                item_id = self.table.item(i, 0).text()
                
                # إذا كان العنصر موجوداً، قم بتحديثه
                if item_id in items_dict:
                    item = items_dict[item_id]
                    
                    # تحديث الاسم
                    name_item = self.table.item(i, 1)
                    if name_item:
                        item['name'] = name_item.text().strip()
                    
                    # تحديث الوحدة
                    unit_item = self.table.item(i, 2)
                    if unit_item:
                        item['unit'] = unit_item.text().strip()
                    
                    # تحديث المقاس
                    size_item = self.table.item(i, 3)
                    if size_item:
                        item['size'] = size_item.text().strip()
                    
                    # تحديث سعر الشراء
                    buying_price_item = self.table.item(i, 4)
                    if buying_price_item:
                        buying_price_text = buying_price_item.text().replace('ج.م', '').strip()
                        try:
                            item['buying_price'] = float(buying_price_text)
                        except ValueError:
                            QMessageBox.warning(self, "تحذير", f"سعر الشراء غير صحيح للعنصر {item_id}")
                            continue
                    
                    # تحديث سعر البيع
                    selling_price_item = self.table.item(i, 5)
                    if selling_price_item:
                        selling_price_text = selling_price_item.text().replace('ج.م', '').strip()
                        try:
                            item['selling_price'] = float(selling_price_text)
                        except ValueError:
                            QMessageBox.warning(self, "تحذير", f"سعر البيع غير صحيح للعنصر {item_id}")
                            continue
                    
                    # تحديث الكمية
                    quantity_item = self.table.item(i, 6)
                    if quantity_item:
                        try:
                            item['quantity'] = int(quantity_item.text().strip())
                        except ValueError:
                            QMessageBox.warning(self, "تحذير", f"الكمية غير صحيحة للعنصر {item_id}")
                            continue
                else:
                    # عنصر جديد (إذا كان المستخدم أضافه مباشرة في الجدول)
                    try:
                        name_item = self.table.item(i, 1)
                        unit_item = self.table.item(i, 2)
                        size_item = self.table.item(i, 3)
                        buying_price_item = self.table.item(i, 4)
                        selling_price_item = self.table.item(i, 5)
                        quantity_item = self.table.item(i, 6)
                        
                        if not all([name_item, unit_item, size_item, buying_price_item, selling_price_item, quantity_item]):
                            QMessageBox.warning(self, "تحذير", f"بيانات غير كاملة للصف {i+1}")
                            continue
                        
                        new_item = {
                            'item_id': item_id,
                            'name': name_item.text().strip(),
                            'unit': unit_item.text().strip(),
                            'size': size_item.text().strip(),
                            'buying_price': float(buying_price_item.text().replace('ج.م', '').strip()),
                            'selling_price': float(selling_price_item.text().replace('ج.م', '').strip()),
                            'quantity': int(quantity_item.text().strip())
                        }
                        
                        current_items.append(new_item)
                        
                    except Exception as e:
                        QMessageBox.warning(self, "تحذير", f"خطأ في معالجة العنصر الجديد: {str(e)}")
                        continue
            
            # حفظ جميع العناصر - حفظ مباشر في ملف واحد
            self.db.save_items(current_items)
            
            # تحديث عرض الجدول والإحصائيات
            self.load_items()
            
            QMessageBox.information(self, "نجاح", "تم حفظ جميع التغييرات بنجاح!")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ:\n{str(e)}")
    
    def cancel_edit(self):
        self.toggle_mode()
        self.load_items()  # إعادة تحميل البيانات الأصلية
    
    def update_or_add_item_from_import(self, import_data):
        """
        تحديث أو إضافة منتج من بيانات الاستيراد
        يتم استدعاؤها من نافذة الاستيراد
        """
        items = self.db.load_items()
        
        # البحث عن منتج موجود بنفس الاسم والمقاس وسعر الشراء
        existing_item = None
        for item in items:
            if (item['name'] == import_data['item_name'] and 
                item['size'] == import_data['size'] and 
                abs(item['buying_price'] - import_data['price']) < 0.01):
                existing_item = item
                break
        
        if existing_item:
            # تحديث الكمية فقط
            existing_item['quantity'] += import_data['quantity']
            QMessageBox.information(self, "تحديث", f"تم تحديث كمية المنتج '{existing_item['name']}' بإضافة {import_data['quantity']} وحدة")
        else:
            # إضافة منتج جديد
            new_item_id = str(random.randint(1000, 9999))
            new_item = {
                'item_id': new_item_id,
                'name': import_data['item_name'],
                'unit': import_data.get('unit', 'عدد'),  # إضافة الوحدة
                'size': import_data['size'],
                'buying_price': import_data['price'],
                'selling_price': 0.0,
                'quantity': import_data['quantity']
            }
            items.append(new_item)
            QMessageBox.information(self, "إضافة", f"تم إضافة منتج جديد '{import_data['item_name']}' إلى المخزون")
        
        self.db.save_items(items)
        self.load_items()
    
    def delete_selected_item(self):
        """حذف الصف المحدد من الجدول"""
        selected_row = self.table.currentRow()
        
        if selected_row >= 0:
            # الحصول على بيانات الصف المحدد
            item_id = self.table.item(selected_row, 0).text()
            item_name = self.table.item(selected_row, 1).text()
            item_size = self.table.item(selected_row, 3).text()
            
            reply = QMessageBox.question(
                self, 
                "تأكيد الحذف",
                f"هل أنت متأكد من حذف المنتج:\n\n"
                f"الاسم: {item_name}\n"
                f"المقاس: {item_size}\n"
                f"الرقم: {item_id}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    # تحميل العناصر من قاعدة البيانات
                    items = self.db.load_items()
                    
                    # البحث عن العنصر وحذفه
                    items_to_keep = []
                    for item in items:
                        if str(item.get('item_id', '')) != item_id:
                            items_to_keep.append(item)
                    
                    # حفظ العناصر المتبقية
                    self.db.save_items(items_to_keep)
                    
                    # إعادة تحميل الجدول والإحصائيات
                    self.load_items()
                    
                    QMessageBox.information(
                        self, 
                        "تم الحذف",
                        f"تم حذف المنتج '{item_name}' بنجاح!"
                    )
                    
                except Exception as e:
                    QMessageBox.critical(
                        self, 
                        "خطأ", 
                        f"فشل حذف المنتج:\n{str(e)}"
                    )
        else:
            QMessageBox.warning(
                self, 
                "تحذير", 
                "الرجاء تحديد صف لحذفه!"
            )
    
    def reset_search(self):
        """إعادة تعيين البحث"""
        self.name_search_input.clear()
        self.size_search_combo.setCurrentIndex(0)
        self.filter_items()

class AddItemDialog(QDialog):
    """نافذة إضافة منتج جديد مع حقل الوحدة"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("إضافة منتج جديد")
        self.setFixedSize(400, 350)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # رقم المنتج (تلقائي)
        self.id_input = QLineEdit()
        self.id_input.setText(str(random.randint(1000, 9999)))
        self.id_input.setReadOnly(True)
        form_layout.addRow("رقم المنتج:", self.id_input)
        
        # اسم المنتج (الصنف)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("أدخل اسم المنتج")
        form_layout.addRow("اسم المنتج (الصنف):", self.name_input)
        
        # الوحدة
        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("عدد، كيلو، لتر، متر، ...")
        self.unit_input.setText("عدد")  # القيمة الافتراضية
        form_layout.addRow("الوحدة:", self.unit_input)
        
        # المقاس
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("وسط، كبير، 100 مل، ...")
        form_layout.addRow("المقاس:", self.size_input)
        
        # سعر الشراء
        self.buying_price_input = QDoubleSpinBox()
        self.buying_price_input.setDecimals(2)
        self.buying_price_input.setMinimum(0.0)
        self.buying_price_input.setMaximum(999999.99)
        self.buying_price_input.setPrefix("ج.م ")
        form_layout.addRow("سعر الشراء:", self.buying_price_input)
        
        # سعر البيع
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setDecimals(2)
        self.selling_price_input.setMinimum(0.0)
        self.selling_price_input.setMaximum(999999.99)
        self.selling_price_input.setPrefix("ج.م ")
        form_layout.addRow("سعر البيع:", self.selling_price_input)
        
        # الكمية
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(0)
        self.quantity_input.setMaximum(99999)
        form_layout.addRow("الكمية:", self.quantity_input)
        
        layout.addLayout(form_layout)
        
        # أزرار
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("إضافة")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        add_btn.clicked.connect(self.accept)
        button_layout.addWidget(add_btn)
        
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_item(self):
        """الحصول على بيانات المنتج المدخلة"""
        return {
            'item_id': self.id_input.text().strip(),
            'name': self.name_input.text().strip(),
            'unit': self.unit_input.text().strip() or "عدد",
            'size': self.size_input.text().strip(),
            'buying_price': self.buying_price_input.value(),
            'selling_price': self.selling_price_input.value(),
            'quantity': self.quantity_input.value()
        }

class ImportsWindow(QWidget):
    """نافذة الاستيراد المحسنة مع نظام فواتير الاستيراد"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_step = 1
        self.cart_items = []
        self.current_supplier_id = None
        self.current_supplier_name = None
        self.supplier_address = ""
        self.due_date = ""
        self.supplier_notes = ""
        self.supplier_previous_balance = 0
        self.current_total = 0
        self.total_paid_now = 0
        self.total_cumulative = 0
        self.total_remaining = 0
        self.current_balance = 0
        self.preview_receipt_data = None
        
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة مع الخيارين الرئيسيين"""
        self.setWindowTitle('نظام الاستيراد')
        self.setGeometry(150, 150, 1000, 600)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # العنوان
        title = QLabel("نظام الاستيراد")
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background-color: #ecf0f1;
                border-radius: 10px;
                text-align: center;
            }
        """)
        main_layout.addWidget(title)
        
        # الوصف
        description = QLabel("اختر الخدمة المطلوبة:")
        description.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #7f8c8d;
                text-align: center;
                padding: 10px;
            }
        """)
        main_layout.addWidget(description)
        
        # أزرار الخيارات الرئيسية
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(40)
        buttons_layout.setContentsMargins(50, 50, 50, 50)
        
        # زر إنشاء فاتورة استيراد
        create_btn = self.create_main_button("📋", "إنشاء فاتورة استيراد", "#3498db", self.open_create_import)
        buttons_layout.addWidget(create_btn)
        
        # زر سجل الاستيراد
        history_btn = self.create_main_button("📊", "سجل الاستيراد", "#2ecc71", self.open_imports_history)
        buttons_layout.addWidget(history_btn)
        
        main_layout.addWidget(buttons_widget)
        main_layout.addStretch()
        
        # زر إغلاق
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        close_btn = QPushButton("إغلاق")
        close_btn.setFixedSize(100, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        close_btn.clicked.connect(self.close)
        close_layout.addWidget(close_btn)
        
        main_layout.addLayout(close_layout)
        self.setLayout(main_layout)
    
    def create_main_button(self, icon, text, color, callback):
        """إنشاء زر رئيسي"""
        btn = QPushButton(f"{icon}\n{text}")
        btn.setMinimumSize(300, 200)
        btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 20px;
                font-weight: bold;
                border-radius: 15px;
                background-color: {color};
                color: white;
                border: 3px solid {color};
                padding: 20px;
            }}
            QPushButton:hover {{
                background-color: #2c3e50;
                border: 3px solid #2c3e50;
                transform: scale(1.05);
            }}
        """)
        btn.clicked.connect(callback)
        return btn
    
    def open_create_import(self):
        """فتح نافذة إنشاء فاتورة استيراد"""
        self.create_window = CreateImportWindow(self.db)
        self.create_window.show()
        self.close()
    
    def open_imports_history(self):
        """فتح نافذة سجل الاستيراد"""
        self.history_window = ImportsHistoryWindow(self.db)
        self.history_window.show()
        self.close()

class CreateImportWindow(QWidget):
    """نافذة إنشاء فاتورة استيراد مع الخطوات الثلاث ونظام Virtual Table"""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_step = 1
        self.cart_items = []
        self.current_supplier_id = None
        self.current_supplier_name = None
        self.supplier_address = ""
        self.due_date = ""
        self.supplier_notes = ""
        self.current_total = 0
        self.total_paid_now = 0
        self.total_cumulative = 0
        self.total_remaining = 0
        self.current_balance = 0
        self.existing_supplier = False

        # ✅ نظام الجدول الافتراضي
        self.virtual_table = None  # النسخة الافتراضية من المخزون
        self.virtual_table_changes = {}  # تعقب التغييرات في الجدول الافتراضي

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('إنشاء فاتورة استيراد')
        self.setMinimumSize(900, 650)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.layout = QVBoxLayout()

        # مؤشر الخطوة
        self.step_label = QLabel("الخطوة 1: معلومات البائع")
        self.step_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db; padding: 10px;")
        self.layout.addWidget(self.step_label)

        # الخطوات
        self.stacked_widget = QStackedWidget()

        self.step1_widget = self.create_step1()
        self.stacked_widget.addWidget(self.step1_widget)

        self.step2_widget = self.create_step2()
        self.stacked_widget.addWidget(self.step2_widget)

        self.step3_widget = self.create_step3()
        self.stacked_widget.addWidget(self.step3_widget)

        self.layout.addWidget(self.stacked_widget)

        # أزرار التنقل
        nav_layout = QHBoxLayout()

        self.prev_btn = QPushButton("→ السابق")
        self.prev_btn.clicked.connect(self.prev_step)
        self.prev_btn.setEnabled(False)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        nav_layout.addWidget(self.prev_btn)

        nav_layout.addStretch()

        self.next_btn = QPushButton("التالي ←")
        self.next_btn.clicked.connect(self.next_step)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        nav_layout.addWidget(self.next_btn)

        self.layout.addLayout(nav_layout)
        self.setLayout(self.layout)

    def create_step1(self):
        """الخطوة 1: معلومات البائع"""
        widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # كود البائع
        supplier_code_layout = QHBoxLayout()
        supplier_code_layout.addWidget(QLabel("كود البائع:"))

        self.supplier_code_input = QLineEdit()
        self.supplier_code_input.setPlaceholderText("كود البائع")
        self.supplier_code_input.setFixedWidth(100)
        supplier_code_layout.addWidget(self.supplier_code_input)

        supplier_code_layout.addStretch()
        form_layout.addRow(supplier_code_layout)

        # اسم البائع
        supplier_name_layout = QHBoxLayout()
        supplier_name_layout.addWidget(QLabel("اسم البائع:"))

        self.supplier_name_input = QLineEdit()
        self.supplier_name_input.setPlaceholderText("اسم البائع")
        self.supplier_name_input.textChanged.connect(self.check_supplier_existence)
        supplier_name_layout.addWidget(self.supplier_name_input)

        # زر البحث في البائعين
        search_btn = QPushButton("🔍")
        search_btn.setToolTip("البحث عن البائع في السجلات")
        search_btn.setFixedWidth(40)
        search_btn.clicked.connect(self.search_supplier_in_history)
        supplier_name_layout.addWidget(search_btn)

        supplier_name_layout.addStretch()
        form_layout.addRow(supplier_name_layout)

        # هاتف البائع
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("هاتف البائع")
        form_layout.addRow("هاتف البائع:", self.phone_input)

        # عنوان البائع
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("عنوان البائع")
        form_layout.addRow("عنوان البائع:", self.address_input)

        # تاريخ الاستحقاق
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate().addDays(30))
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("تاريخ الاستحقاق:", self.due_date_input)

        # ملاحظات
        self.notes_input_step1 = QTextEdit()
        self.notes_input_step1.setMaximumHeight(80)
        self.notes_input_step1.setPlaceholderText("ملاحظات إضافية...")
        form_layout.addRow("ملاحظات:", self.notes_input_step1)

        # التاريخ
        date_layout = QHBoxLayout()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.date_input)

        now_btn = QPushButton("الآن")
        now_btn.clicked.connect(lambda: self.date_input.setDate(QDate.currentDate()))
        now_btn.setFixedWidth(60)
        date_layout.addWidget(now_btn)
        date_layout.addStretch()
        form_layout.addRow("التاريخ:", date_layout)

        # نتيجة البحث عن البائع
        self.supplier_info_label = QLabel("")
        self.supplier_info_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        form_layout.addRow("", self.supplier_info_label)

        layout.addLayout(form_layout)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def create_step2(self):
        """الخطوة 2: اختيار المنتجات مع سعر الشراء والبيع"""
        widget = QWidget()
        layout = QVBoxLayout()

        # خانة لإضافة منتج جديد
        new_product_frame = QGroupBox("إضافة منتج جديد")
        new_product_frame.setStyleSheet("QGroupBox { font-weight: bold; color: #3498db; }")
        new_product_layout = QFormLayout()

        # اسم المنتج الجديد
        self.new_product_name = QLineEdit()
        self.new_product_name.setPlaceholderText("اسم المنتج الجديد")
        new_product_layout.addRow("اسم المنتج:", self.new_product_name)

        # المقاس الجديد
        size_layout = QHBoxLayout()
        self.new_product_size = QLineEdit()
        self.new_product_size.setPlaceholderText("المقاس")
        size_layout.addWidget(self.new_product_size)

        add_new_product_btn = QPushButton("➕ إضافة للمخزن")
        add_new_product_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        add_new_product_btn.clicked.connect(self.add_new_product_to_inventory)
        size_layout.addWidget(add_new_product_btn)
        new_product_layout.addRow("المقاس:", size_layout)

        new_product_frame.setLayout(new_product_layout)
        layout.addWidget(new_product_frame)

        # اختيار المنتج مع فلترة المقاس
        form_layout = QFormLayout()

        # إضافة خانة اختيار/بحث المقاس
        size_search_layout = QHBoxLayout()
        size_search_layout.addWidget(QLabel("اختر/ابحث بالمقاس:"))

        self.size_filter_combo = QComboBox()
        self.size_filter_combo.setEditable(True)
        self.size_filter_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.load_sizes_combo()
        self.size_filter_combo.currentTextChanged.connect(self.filter_items_by_size)
        self.size_filter_combo.lineEdit().setPlaceholderText("اكتب للبحث أو اختر من القائمة")
        size_search_layout.addWidget(self.size_filter_combo)

        size_search_btn = QPushButton("🔍")
        size_search_btn.setToolTip("بحث في المقاسات")
        size_search_btn.setMaximumWidth(30)
        size_search_btn.clicked.connect(lambda: self.search_in_combo(self.size_filter_combo))
        size_search_layout.addWidget(size_search_btn)
        form_layout.addRow(size_search_layout)

        # إضافة خانة اختيار/بحث المنتج
        item_search_layout = QHBoxLayout()
        item_search_layout.addWidget(QLabel("اختر/ابحث بالمنتج:"))

        self.item_combo = QComboBox()
        self.item_combo.setEditable(True)
        self.item_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.load_items_combo()
        self.item_combo.lineEdit().setPlaceholderText("اكتب للبحث أو اختر من القائمة")
        self.item_combo.lineEdit().textEdited.connect(self.filter_items_combo)
        item_search_layout.addWidget(self.item_combo)

        item_search_btn = QPushButton("🔍")
        item_search_btn.setToolTip("بحث في المنتجات")
        item_search_btn.setMaximumWidth(30)
        item_search_btn.clicked.connect(lambda: self.search_in_combo(self.item_combo))
        item_search_layout.addWidget(item_search_btn)
        form_layout.addRow(item_search_layout)

        # الكمية
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(999)
        form_layout.addRow("الكمية:", self.quantity_spin)

        # سعر الشراء
        self.buying_price_input = QDoubleSpinBox()
        self.buying_price_input.setDecimals(2)
        self.buying_price_input.setMinimum(0.0)
        self.buying_price_input.setMaximum(999999.99)
        self.buying_price_input.setPrefix("ج.م ")
        form_layout.addRow("سعر الشراء:", self.buying_price_input)

        # سعر البيع
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setDecimals(2)
        self.selling_price_input.setMinimum(0.0)
        self.selling_price_input.setMaximum(999999.99)
        self.selling_price_input.setPrefix("ج.م ")
        form_layout.addRow("سعر البيع:", self.selling_price_input)

        add_btn = QPushButton("إضافة للسلة")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        add_btn.clicked.connect(self.add_to_cart)
        form_layout.addRow("", add_btn)

        layout.addLayout(form_layout)

        # عرض السلة
        layout.addWidget(QLabel("المنتجات في السلة:"))
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(8)
        self.cart_table.setHorizontalHeaderLabels(["الرقم", "الصنف", "المقاس", "الكمية", "سعر الشراء", "سعر البيع", "الإجمالي شراء", "الإجمالي بيع"])
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.setStyleSheet(self.get_table_style())
        layout.addWidget(self.cart_table)

        # إجمالي السلة (على أساس سعر الشراء)
        self.cart_total_label = QLabel("إجمالي السلة (شراء):")
        self.cart_total_label.setStyleSheet("font-weight: bold; color: white; font-size: 16px; background-color: #2c3e50; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.cart_total_label)

        # إجمالي البيع
        self.cart_selling_total_label = QLabel("إجمالي السلة (بيع):")
        self.cart_selling_total_label.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 14px;")
        layout.addWidget(self.cart_selling_total_label)

        # زر الحذف
        remove_btn = QPushButton("حذف المحدد")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        remove_btn.clicked.connect(self.remove_from_cart)
        layout.addWidget(remove_btn)

        widget.setLayout(layout)
        return widget

    def create_step3(self):
        """الخطوة 3: الدفع والإجماليات مع Scroll Area"""
        # إنشاء Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #f5f5f5;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #3498db;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #2980b9;
            }
        """)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # عنوان الخطوة
        title = QLabel("الدفع والإجماليات")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; text-align: center; padding: 10px;")
        layout.addWidget(title)

        # معلومات البائع
        supplier_frame = QGroupBox("معلومات البائع")
        supplier_frame.setStyleSheet("QGroupBox { font-weight: bold; }")
        supplier_layout = QVBoxLayout()

        self.supplier_summary_label = QLabel("")
        self.supplier_summary_label.setStyleSheet("font-size: 12px; color: #34495e;")
        supplier_layout.addWidget(self.supplier_summary_label)

        supplier_frame.setLayout(supplier_layout)
        layout.addWidget(supplier_frame)

        # الإجماليات
        totals_frame = QGroupBox("الإجماليات")
        totals_frame.setStyleSheet("QGroupBox { font-weight: bold; }")
        totals_layout = QFormLayout()

        # الإجمالي الحالي (سعر الشراء)
        self.current_total_label = QLabel("")
        self.current_total_label.setStyleSheet("font-size: 14px; color: #2c3e50; font-weight: bold;")
        totals_layout.addRow("الإجمالي الحالي (شراء):", self.current_total_label)

        # الإجمالي البيع
        self.current_selling_total_label = QLabel("")
        self.current_selling_total_label.setStyleSheet("font-size: 14px; color: #27ae60; font-weight: bold;")
        totals_layout.addRow("الإجمالي الحالي (بيع):", self.current_selling_total_label)

        # الإجمالي الكلي
        self.cumulative_total_label = QLabel("0.00 ج.م")
        self.cumulative_total_label.setStyleSheet("font-size: 16px; color: #c0392b; font-weight: bold;")
        totals_layout.addRow("الإجمالي الكلي:", self.cumulative_total_label)

        totals_frame.setLayout(totals_layout)
        layout.addWidget(totals_frame)

        # الدفع الحالي
        payment_frame = QGroupBox("الدفع الحالي")
        payment_frame.setStyleSheet("QGroupBox { font-weight: bold; }")
        payment_layout = QVBoxLayout()

        # مدى الدفع المسموح
        self.range_label = QLabel("المبلغ المسموح دفعه: 0.00 - 0.00 ج.م")
        self.range_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        payment_layout.addWidget(self.range_label)

        # إدخال المبلغ المدفوع
        paid_layout = QHBoxLayout()
        paid_layout.addWidget(QLabel("المبلغ المدفوع الآن:"))

        self.amount_paid_input = QDoubleSpinBox()
        self.amount_paid_input.setDecimals(2)
        self.amount_paid_input.setMinimum(0.0)
        self.amount_paid_input.setMaximum(0.0)
        self.amount_paid_input.setPrefix("ج.م ")
        self.amount_paid_input.valueChanged.connect(self.update_payment_summary)
        paid_layout.addWidget(self.amount_paid_input)

        payment_layout.addLayout(paid_layout)

        # المبلغ المتبقي للفاتورة
        remaining_invoice_layout = QHBoxLayout()
        remaining_invoice_layout.addWidget(QLabel("متبقي الفاتورة:"))

        self.remaining_invoice_label = QLabel("0.00 ج.م")
        self.remaining_invoice_label.setStyleSheet("font-size: 14px; color: #e74c3c; font-weight: bold;")
        remaining_invoice_layout.addWidget(self.remaining_invoice_label)
        remaining_invoice_layout.addStretch()
        payment_layout.addLayout(remaining_invoice_layout)

        # المبلغ المتبقي الكلي
        remaining_total_layout = QHBoxLayout()
        remaining_total_layout.addWidget(QLabel("المتبقي الكلي:"))

        self.remaining_total_label = QLabel("0.00 ج.م")
        self.remaining_total_label.setStyleSheet("font-size: 16px; color: #e74c3c; font-weight: bold;")
        remaining_total_layout.addWidget(self.remaining_total_label)
        remaining_total_layout.addStretch()
        payment_layout.addLayout(remaining_total_layout)

        payment_frame.setLayout(payment_layout)
        layout.addWidget(payment_frame)

        # حالة الدفع
        payment_status_frame = QGroupBox("حالة الدفع")
        payment_status_frame.setStyleSheet("QGroupBox { font-weight: bold; }")
        payment_status_layout = QVBoxLayout()

        self.payment_status_label = QLabel("غير مدفوع")
        self.payment_status_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #e74c3c;
            padding: 10px;
            text-align: center;
            border: 2px solid #e74c3c;
            border-radius: 5px;
            background-color: #fff;
        """)
        payment_status_layout.addWidget(self.payment_status_label)

        payment_status_frame.setLayout(payment_status_layout)
        layout.addWidget(payment_status_frame)

        # ملاحظات إضافية
        notes_frame = QGroupBox("ملاحظات إضافية")
        notes_frame.setStyleSheet("QGroupBox { font-weight: bold; }")
        notes_layout = QVBoxLayout()

        self.notes_input_step3 = QTextEdit()
        self.notes_input_step3.setMaximumHeight(60)
        self.notes_input_step3.setPlaceholderText("أدخل ملاحظات إضافية هنا...")
        notes_layout.addWidget(self.notes_input_step3)

        notes_frame.setLayout(notes_layout)
        layout.addWidget(notes_frame)

        # أزرار الإجراءات
        actions_layout = QHBoxLayout()

        # زر حفظ الفاتورة
        self.save_invoice_btn = QPushButton("💾 حفظ الفاتورة")
        self.save_invoice_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.save_invoice_btn.clicked.connect(self.save_import_invoice)
        actions_layout.addWidget(self.save_invoice_btn)

        # زر حفظ في المخزن
        self.save_inventory_btn = QPushButton("📦 حفظ في المخزن")
        self.save_inventory_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.save_inventory_btn.clicked.connect(self.update_inventory)
        self.save_inventory_btn.setEnabled(False)
        actions_layout.addWidget(self.save_inventory_btn)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        widget.setLayout(layout)
        scroll_area.setWidget(widget)

        return scroll_area

    def get_table_style(self):
        return """
            QTableWidget {
                background-color: #1f2327;
                alternate-background-color: #272a2d;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """

    # ✅ دالة جديدة: إنشاء الجدول الافتراضي
    def create_virtual_table(self):
        """إنشاء نسخة افتراضية من جدول المخزون"""
        try:
            # استلام نسخة من جدول المخزون الحقيقي
            self.virtual_table = self.db.load_items()
            self.virtual_table_changes = {}
            print(f"✅ تم إنشاء الجدول الافتراضي مع {len(self.virtual_table)} عنصر")
            return True
        except Exception as e:
            print(f"خطأ في إنشاء الجدول الافتراضي: {e}")
            return False

    # ✅ دالة جديدة: إضافة منتج جديد إلى المخزن والجدول الافتراضي
    def add_new_product_to_inventory(self):
        """إضافة منتج جديد إلى المخزن والجدول الافتراضي"""
        product_name = self.new_product_name.text().strip()
        product_size = self.new_product_size.text().strip()

        if not product_name:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال اسم المنتج!")
            return

        if not product_size:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال مقاس المنتج!")
            return

        try:
            # ✅ إذا كان الجدول الافتراضي غير موجود، إنشاؤه
            if not self.virtual_table:
                self.create_virtual_table()

            # التحقق من عدم تكرار المنتج في الجدول الافتراضي
            for item in self.virtual_table:
                if item['name'] == product_name and item['size'] == product_size:
                    QMessageBox.warning(self, "تحذير", "هذا المنتج موجود بالفعل في المخزن!")
                    return

            # إضافة المنتج الجديد إلى الجدول الافتراضي فقط
            new_item = {
                'item_id': str(random.randint(1000, 9999)),
                'name': product_name,
                'size': product_size,
                'unit': 'عدد',
                'buying_price': 0.0,  # سعر شراء صفر
                'selling_price': 0.0,  # سعر بيع صفر
                'quantity': 0  # كمية صفر
            }

            self.virtual_table.append(new_item)

            # تحديث قائمة المنتجات
            self.load_items_combo()
            self.load_sizes_combo()

            # تفريغ الحقول
            self.new_product_name.clear()
            self.new_product_size.clear()

            QMessageBox.information(self, "نجاح", f"تم إضافة المنتج '{product_name}' للجدول الافتراضي!")

        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء إضافة المنتج:\n{str(e)}")

    # ✅ دالة جديدة: تحميل المنتجات في الكومبو من الجدول الافتراضي
    def load_items_combo(self):
        """تحميل المنتجات في الكومبو مع الكميات من الجدول الافتراضي"""
        try:
            items = self.virtual_table if self.virtual_table else self.db.load_items()
            self.item_combo.clear()

            if not items:
                self.item_combo.addItem("لا توجد منتجات في المخزون", None)
                return

            for item in items:
                name = item.get('name', 'غير معروف')
                size = item.get('size', '')
                buying_price = item.get('buying_price', 0.0)
                selling_price = item.get('selling_price', 0.0)
                quantity = item.get('quantity', 0)

                display_text = f"{name} ({size}) - شراء: {buying_price} ج.م - بيع: {selling_price} ج.م - كميه: {quantity}"
                self.item_combo.addItem(display_text, item)

            if self.item_combo.count() > 0:
                self.item_combo.setCurrentIndex(0)

        except Exception as e:
            print(f"خطأ في تحميل المنتجات: {e}")

    # ✅ دالة جديدة: فلترة المنتجات حسب المقاس من الجدول الافتراضي
    def filter_items_by_size(self, selected_size):
        """فلترة المنتجات حسب المقاس من الجدول الافتراضي"""
        try:
            items = self.virtual_table if self.virtual_table else self.db.load_items()
            self.item_combo.clear()

            if selected_size == "جميع المقاسات" or not selected_size:
                # عرض جميع المنتجات
                for item in items:
                    name = item.get('name', 'غير معروف')
                    size = item.get('size', '')
                    buying_price = item.get('buying_price', 0.0)
                    selling_price = item.get('selling_price', 0.0)
                    quantity = item.get('quantity', 0)

                    display_text = f"{name} ({size}) - شراء: {buying_price} ج.م - بيع: {selling_price} ج.م - كميه: {quantity}"
                    self.item_combo.addItem(display_text, item)
                return

            # فلترة حسب المقاس المحدد
            filtered_items = []
            for item in items:
                if item.get('size', '') == selected_size:
                    filtered_items.append(item)

            if not filtered_items:
                self.item_combo.addItem(f"لا توجد منتجات بالمقاس: {selected_size}", None)
                return

            for item in filtered_items:
                name = item.get('name', 'غير معروف')
                size = item.get('size', '')
                buying_price = item.get('buying_price', 0.0)
                selling_price = item.get('selling_price', 0.0)
                quantity = item.get('quantity', 0)

                display_text = f"{name} ({size}) - شراء: {buying_price} ج.م - بيع: {selling_price} ج.م - كميه: {quantity}"
                self.item_combo.addItem(display_text, item)

            self.item_combo.setCurrentIndex(0)

        except Exception as e:
            print(f"خطأ في فلترة المنتجات: {e}")

    # ✅ دالة جديدة: البحث عن منتج مطابق في الجدول الافتراضي
    def find_matching_item_in_virtual_table(self, item_name, item_size, buying_price, selling_price):
        """البحث عن منتج مطابق تماماً في الجدول الافتراضي"""
        try:
            if not self.virtual_table:
                return None
            
            for item in self.virtual_table:
                # مطابقة الاسم والمقاس والأسعار
                if (item['name'] == item_name and 
                    item['size'] == item_size and
                    abs(item['buying_price'] - buying_price) < 0.01 and  # نفس سعر الشراء
                    abs(item['selling_price'] - selling_price) < 0.01):  # نفس سعر البيع
                    return item
            return None
        except Exception as e:
            print(f"خطأ في البحث عن منتج مطابق: {e}")
            return None

    # ✅ دالة جديدة: تحديث كمية المنتج في الجدول الافتراضي
    def update_item_quantity_in_virtual_table(self, item_id, quantity_to_add):
        """تحديث كمية المنتج في الجدول الافتراضي"""
        try:
            if not self.virtual_table:
                return False
            
            for item in self.virtual_table:
                if item['item_id'] == item_id:
                    current_qty = item.get('quantity', 0)
                    item['quantity'] = current_qty + quantity_to_add
                    
                    # تسجيل التغيير
                    key = f"{item['name']}_{item['size']}"
                    if key in self.virtual_table_changes:
                        self.virtual_table_changes[key] += quantity_to_add
                    else:
                        self.virtual_table_changes[key] = quantity_to_add
                    
                    print(f"تم تحديث الكمية للعنصر {item_id}: {current_qty} → {item['quantity']}")
                    return True
            return False
        except Exception as e:
            print(f"خطأ في تحديث كمية المنتج: {e}")
            return False

    # ✅ دالة معدلة: إضافة منتج للسلة مع تطبيق النظام المطلوب
    def add_to_cart(self):
        """إضافة منتج للسلة مع تطبيق النظام المطلوب"""
        item_data = self.item_combo.currentData()

        if item_data is None:
            QMessageBox.warning(self, "خطأ", "لا توجد منتجات متاحة!")
            return

        quantity = self.quantity_spin.value()
        buying_price = self.buying_price_input.value()
        selling_price = self.selling_price_input.value()

        if buying_price <= 0:
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال سعر شراء صحيح!")
            return

        if selling_price <= 0:
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال سعر بيع صحيح!")
            return

        item_name = item_data['name']
        item_size = item_data['size']
        
        # ✅ الحل الثاني: إذا كان المنتج جديداً (قيم صفرية)، ننشئ نسخة جديدة ونحذف الأصل
        if (item_data['buying_price'] == 0.0 and 
            item_data['selling_price'] == 0.0 and 
            item_data['quantity'] == 0):

            # إنشاء نسخة جديدة من المنتج بالقيم المدخلة
            new_item_id = str(random.randint(1000, 9999))
            new_item_data = item_data.copy()
            new_item_data['item_id'] = new_item_id
            new_item_data['buying_price'] = buying_price
            new_item_data['selling_price'] = selling_price
            new_item_data['quantity'] = quantity

            # إضافة النسخة الجديدة إلى الجدول الافتراضي
            self.virtual_table.append(new_item_data)

            # حذف المنتج الأصلي ذو القيم الصفرية من الجدول الافتراضي
            for i, item in enumerate(self.virtual_table):
                if item['item_id'] == item_data['item_id']:
                    del self.virtual_table[i]
                    break

            # استخدام النسخة الجديدة كبيانات المنتج للسلة
            item_data_for_cart = new_item_data
            print(f"✅ تم إضافة منتج جديد: {item_name} ({item_size})")

        else:
            # ✅ البحث عن منتج مطابق تماماً في الجدول الافتراضي
            matching_item = self.find_matching_item_in_virtual_table(
                item_name, item_size, buying_price, selling_price
            )
            
            if matching_item:
                # ✅ 1. مطابقة تامة - تحديث كمية المنتج الموجود
                print(f"✅ تطابق تام - تحديث الكمية للمنتج الموجود: {item_name}")
                self.update_item_quantity_in_virtual_table(matching_item['item_id'], quantity)
                item_data_for_cart = matching_item.copy()
            else:
                # ✅ 2. منتج موجود بأسعار مختلفة - إنشاء منتج جديد
                new_item_id = str(random.randint(1000, 9999))
                new_item_data = {
                    'item_id': new_item_id,
                    'name': item_name,
                    'size': item_size,
                    'unit': item_data.get('unit', 'عدد'),
                    'buying_price': buying_price,
                    'selling_price': selling_price,
                    'quantity': quantity
                }
                
                # إضافة المنتج الجديد إلى الجدول الافتراضي
                self.virtual_table.append(new_item_data)
                item_data_for_cart = new_item_data
                print(f"✅ منتج بأسعار مختلفة - تم إنشاء منتج جديد: {item_name}")

        # إنشاء عنصر السلة
        cart_item = {
            'item_id': item_data_for_cart['item_id'],
            'name': item_data_for_cart['name'],
            'size': item_data_for_cart['size'],
            'unit': item_data_for_cart.get('unit', 'عدد'),
            'quantity': quantity,
            'buying_price': buying_price,
            'selling_price': selling_price,
            'buying_total': buying_price * quantity,
            'selling_total': selling_price * quantity
        }

        self.cart_items.append(cart_item)
        self.update_cart_display()

        # تحديث قائمة المنتجات لتعكس التغييرات
        self.load_items_combo()

        # إعادة تعيين الحقول
        self.quantity_spin.setValue(1)
        self.buying_price_input.setValue(0.0)
        self.selling_price_input.setValue(0.0)

        print(f"✅ تمت إضافة {quantity} من {item_name} إلى السلة")

    # ✅ دالة جديدة: إعادة تعيين الجدول الافتراضي
    def reset_virtual_table(self):
        """إعادة تعيين الجدول الافتراضي"""
        self.virtual_table = None
        self.virtual_table_changes = {}

    # ✅ دالة جديدة: تحديث المخزون الحقيقي من التغييرات الافتراضية
    def update_real_inventory(self):
        """تحديث المخزون الحقيقي من التغييرات الافتراضية"""
        try:
            if not self.virtual_table:
                print("❌ لا يوجد جدول افتراضي لتحديث المخزون الحقيقي")
                return False

            # جلب المخزون الحقيقي
            real_items = self.db.load_items()
            print(f"🔍 جلب {len(real_items)} عنصر من المخزون الحقيقي")

            # تطبيق التغييرات من الجدول الافتراضي
            items_added = []  # المنتجات المضافة
            items_updated = []  # المنتجات المحدثة
            
            for virtual_item in self.virtual_table:
                item_found = False
                
                # البحث عن العنصر في المخزون الحقيقي
                for real_item in real_items:
                    if real_item['item_id'] == virtual_item['item_id']:
                        # ✅ 1. مطابقة تامة - تحديث الكمية فقط
                        real_item['quantity'] = virtual_item['quantity']
                        items_updated.append(real_item['name'])
                        item_found = True
                        break
                    elif (real_item['name'] == virtual_item['name'] and 
                          real_item['size'] == virtual_item['size'] and
                          abs(real_item['buying_price'] - virtual_item['buying_price']) < 0.01 and
                          abs(real_item['selling_price'] - virtual_item['selling_price']) < 0.01):
                        # ✅ 2. مطابقة بالاسم والمقاس والأسعار - إضافة الكمية
                        real_item['quantity'] += virtual_item['quantity']
                        items_updated.append(real_item['name'])
                        item_found = True
                        break

                # ✅ 3. إذا لم يتم العثور على العنصر، إضافته كمنتج جديد
                if not item_found:
                    real_items.append(virtual_item.copy())
                    items_added.append(virtual_item['name'])

            # حفظ التغييرات
            self.db.save_items(real_items)
            
            # عرض تقرير التحديث
            print(f"✅ تم تحديث المخزون الحقيقي:")
            if items_updated:
                print(f"   - تم تحديث: {', '.join(items_updated)}")
            if items_added:
                print(f"   - تم إضافة: {', '.join(items_added)}")
            
            return True

        except Exception as e:
            print(f"❌ خطأ في تحديث المخزون الحقيقي: {e}")
            import traceback
            traceback.print_exc()
            return False

    # ✅ تعديل دالة save_import_invoice لتفعيل زر حفظ المخزن بعد حفظ الفاتورة
    def save_import_invoice(self):
        """حفظ فاتورة الاستيراد"""
        try:
            if not self.cart_items:
                QMessageBox.warning(self, "تحذير", "لا توجد منتجات في السلة!")
                return

            # إنشاء رقم فاتورة فريد
            imports_history = self.load_imports_history()
            existing_ids = {inv['import_id'] for inv in imports_history}

            while True:
                import_id = f"IMP{random.randint(10000, 99999)}"
                if import_id not in existing_ids:
                    break

            date_str = self.date_input.date().toString('yyyy-MM-dd')

            # حساب المدفوع والمتبقي
            amount_paid = self.amount_paid_input.value()
            remaining = self.total_cumulative - amount_paid

            # تحديد حالة الدفع
            if amount_paid <= 0:
                payment_status = "غير مدفوع"
            elif amount_paid >= self.total_cumulative:
                payment_status = "مدفوع بالكامل"
            else:
                payment_status = "سداد قسط"

            invoice_data = {
                'import_id': import_id,
                'supplier_id': self.current_supplier_id,
                'supplier_name': self.current_supplier_name,
                'supplier_phone': self.phone_input.text().strip(),
                'supplier_address': self.supplier_address,
                'date': date_str,
                'due_date': self.due_date,
                'products': self.cart_items.copy(),
                'total': self.current_total,
                'selling_total': sum(item['selling_total'] for item in self.cart_items),
                'amount_paid': amount_paid,
                'remaining': remaining,
                'payment_status': payment_status,
                'notes': self.notes_input_step3.toPlainText().strip(),
                'original_import_id': import_id,
                'payment_count': 0,
                'payment_amount': amount_paid
            }

            # حفظ في ملف CSV
            self.save_import_to_csv(invoice_data)

            # ✅ تمكين زر حفظ في المخزن
            self.save_inventory_btn.setEnabled(True)

            QMessageBox.information(self, "نجاح", 
                                  f"تم حفظ فاتورة الاستيراد!\n\n"
                                  f"رقم الفاتورة: {import_id}\n"
                                  f"البائع: {self.current_supplier_name}\n"
                                  f"الإجمالي: {self.total_cumulative:.2f} ج.م\n"
                                  f"المدفوع: {amount_paid:.2f} ج.م\n"
                                  f"المتبقي: {remaining:.2f} ج.م")

        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حفظ الفاتورة:\n{str(e)}")

    # ✅ تعديل دالة update_inventory لتطبيق التغييرات من الجدول الافتراضي
    def update_inventory(self):
        """تحديث المخزون بمنتجات الاستيراد من الجدول الافتراضي"""
        try:
            # ✅ تطبيق التغييرات من الجدول الافتراضي إلى المخزون الحقيقي
            if not self.update_real_inventory():
                QMessageBox.warning(self, "خطأ", "فشل تحديث المخزون الحقيقي!")
                return

            # تعطيل الزر بعد الحفظ
            self.save_inventory_btn.setEnabled(False)
            self.save_inventory_btn.setText("✅ تم الحفظ في المخزن")

            # عرض رسالة تأكيد
            QMessageBox.information(self, "نجاح", 
                                  "تم تحديث المخزون الحقيقي بنجاح!\n"
                                  "تم تطبيق جميع التغييرات من الجدول الافتراضي.")

        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحديث المخزون:\n{str(e)}")

    # ✅ تعديل دالة next_step لإنشاء الجدول الافتراضي عند الانتقال للخطوة 2
    def next_step(self):
        """الانتقال للخطوة التالية"""
        if self.current_step == 1:
            # التحقق من اسم البائع
            supplier_name = self.supplier_name_input.text().strip()
            if not supplier_name:
                QMessageBox.warning(self, "تحذير", "الرجاء إدخال اسم البائع!")
                return

            # إنشاء كود جديد إذا لم يكن موجوداً
            self.current_supplier_name = supplier_name
            if not self.supplier_code_input.text().strip():
                self.current_supplier_id = f"SUP{random.randint(1000, 9999)}"
                self.supplier_code_input.setText(self.current_supplier_id)
            else:
                self.current_supplier_id = self.supplier_code_input.text().strip()

            self.supplier_address = self.address_input.text().strip()
            self.due_date = self.due_date_input.date().toString('yyyy-MM-dd')
            self.supplier_notes = self.notes_input_step1.toPlainText().strip()

            # ✅ إنشاء الجدول الافتراضي عند الانتقال للخطوة 2
            if not self.create_virtual_table():
                QMessageBox.warning(self, "تحذير", "فشل تحميل المخزون الافتراضي!")

        elif self.current_step == 2:
            # التحقق من السلة
            if not self.cart_items:
                QMessageBox.warning(self, "تحذير", "الرجاء إضافة منتجات للسلة!")
                return

            # تحديث الإجماليات
            self.calculate_totals()

        if self.current_step < 3:
            self.current_step += 1
            self.update_step()

    # ✅ إضافة دالة closeEvent لتنظيف الجدول الافتراضي عند الإغلاق
    def closeEvent(self, event):
        """إغلاق النافذة مع إعادة تعيين الجدول الافتراضي"""
        self.reset_virtual_table()
        event.accept()

    # === الدوال الحالية بدون تغيير (باستثناء تعديلات طفيفة للتوافق) ===

    def check_supplier_existence(self):
        """التحقق من وجود البائع في سجل الاستيرادات"""
        supplier_name = self.supplier_name_input.text().strip()
        if not supplier_name:
            self.supplier_info_label.setText("")
            return

        try:
            # ✅ استخدام الدالة الجديدة لحساب المتبقي الصحيح
            supplier_total_remaining = self.get_supplier_true_remaining(supplier_name)
            
            # حساب عدد الفواتير الأصلية
            imports_history = self.load_imports_history()
            invoice_count = 0
            for invoice in imports_history:
                if invoice.get('supplier_name', '').strip().lower() == supplier_name.lower():
                    import_id = invoice.get('import_id', '')
                    if '.' not in import_id or import_id.startswith('REM_'):
                        invoice_count += 1

            if not imports_history or invoice_count == 0:
                # لا توجد فواتير سابقة
                self.existing_supplier = False
                self.supplier_info_label.setText("🆕 بائع جديد - لا توجد فواتير سابقة")
                self.supplier_info_label.setStyleSheet("color: #e67e22; font-weight: bold; background-color: #fff3cd; padding: 5px; border-radius: 3px; border: 1px solid #ffeaa7;")
                return

            # البحث عن أول فاتورة للبائع للحصول على البيانات
            first_invoice = None
            for invoice in imports_history:
                if invoice.get('supplier_name', '').strip().lower() == supplier_name.lower():
                    first_invoice = invoice
                    break

            if first_invoice:
                # البائع موجود
                self.existing_supplier = True
                self.current_supplier_id = first_invoice.get('supplier_id', '')
                self.supplier_code_input.setText(self.current_supplier_id)

                # جلب بيانات البائع إن وجدت
                if not self.phone_input.text():
                    self.phone_input.setText(first_invoice.get('supplier_phone', ''))
                if not self.address_input.text():
                    self.address_input.setText(first_invoice.get('supplier_address', ''))

                # ✅ عرض المتبقي الصحيح
                if supplier_total_remaining > 0:
                    self.supplier_info_label.setText(
                        f"✅ البائع موجود في السجلات\n"
                        f"المتبقي السابق: {supplier_total_remaining:.2f} ج.م\n"
                        f"عدد الفواتير الأصلية: {invoice_count}"
                    )
                    self.supplier_info_label.setStyleSheet("color: #e74c3c; font-weight: bold; background-color: #ffeaea; padding: 5px; border-radius: 3px; border: 1px solid #e74c3c;")
                else:
                    self.supplier_info_label.setText(
                        f"✅ البائع موجود في السجلات\n"
                        f"لا يوجد متبقي سابق\n"
                        f"عدد الفواتير الأصلية: {invoice_count}"
                    )
                    self.supplier_info_label.setStyleSheet("color: #27ae60; font-weight: bold; background-color: #d4edda; padding: 5px; border-radius: 3px; border: 1px solid #c3e6cb;")
                    
            else:
                # إذا وصلنا إلى هنا، البائع جديد
                self.existing_supplier = False
                self.supplier_info_label.setText("🆕 بائع جديد - سيتم إنشاء معرف جديد")
                self.supplier_info_label.setStyleSheet("color: #e67e22; font-weight: bold; background-color: #fff3cd; padding: 5px; border-radius: 3px; border: 1px solid #ffeaa7;")

        except Exception as e:
            print(f"خطأ في التحقق من وجود البائع: {e}")
            self.existing_supplier = False
            self.supplier_info_label.setText(f"⚠️ خطأ في تحميل البيانات: {str(e)}")
            self.supplier_info_label.setStyleSheet("color: #e74c3c; font-weight: bold; background-color: #f8d7da; padding: 5px; border-radius: 3px; border: 1px solid #f5c6cb;")

    def search_supplier_in_history(self):
        """البحث عن البائع في سجل الاستيرادات"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("البحث عن البائع")
            dialog.setGeometry(200, 200, 500, 400)

            layout = QVBoxLayout()

            layout.addWidget(QLabel("اكتب اسم البائع للبحث:"))
            search_input = QLineEdit()
            layout.addWidget(search_input)

            table = QTableWidget()
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["اسم البائع", "الكود", "الهاتف", "آخر فاتورة", "المتبقي"])
            table.setAlternatingRowColors(True)
            layout.addWidget(table)

            def search_suppliers():
                try:
                    search_text = search_input.text().strip().lower()
                    table.setRowCount(0)

                    imports_history = self.load_imports_history()

                    # تجميع البائعين الفريدين
                    suppliers_dict = {}
                    for invoice in imports_history:
                        supplier_name = invoice.get('supplier_name', '').strip()
                        supplier_id = invoice.get('supplier_id', '')

                        if not supplier_name:
                            continue

                        if search_text and search_text not in supplier_name.lower():
                            continue

                        if supplier_name not in suppliers_dict:
                            suppliers_dict[supplier_name] = {
                                'id': supplier_id,
                                'phone': invoice.get('supplier_phone', ''),
                                'last_invoice': invoice.get('date', ''),
                                'remaining': float(invoice.get('remaining', 0))
                            }
                        else:
                            # تحديث آخر فاتورة وأكبر متبقي
                            if invoice.get('date', '') > suppliers_dict[supplier_name]['last_invoice']:
                                suppliers_dict[supplier_name]['last_invoice'] = invoice.get('date', '')

                            # استخدام المتبقي من الفاتورة الأصلية (بدون نقطة)
                            if '.' not in invoice.get('import_id', ''):
                                suppliers_dict[supplier_name]['remaining'] = float(invoice.get('remaining', 0))

                    # عرض النتائج
                    table.setRowCount(len(suppliers_dict))
                    for i, (name, data) in enumerate(suppliers_dict.items()):
                        table.setItem(i, 0, QTableWidgetItem(name))
                        table.setItem(i, 1, QTableWidgetItem(data['id']))
                        table.setItem(i, 2, QTableWidgetItem(data['phone']))
                        table.setItem(i, 3, QTableWidgetItem(data['last_invoice']))
                        table.setItem(i, 4, QTableWidgetItem(f"{data['remaining']:.2f} ج.م"))

                except Exception as e:
                    print(f"خطأ في البحث عن البائعين: {e}")
                    QMessageBox.warning(dialog, "خطأ", f"حدث خطأ أثناء البحث:\n{str(e)}")

            search_input.textChanged.connect(search_suppliers)
            search_suppliers()

            def select_supplier():
                try:
                    selected = table.currentRow()
                    if selected >= 0:
                        # التحقق من وجود العناصر قبل الوصول إليها
                        supplier_name_item = table.item(selected, 0)
                        supplier_id_item = table.item(selected, 1)

                        if supplier_name_item and supplier_id_item:
                            supplier_name = supplier_name_item.text()
                            supplier_id = supplier_id_item.text()

                            self.supplier_name_input.setText(supplier_name)
                            self.supplier_code_input.setText(supplier_id)
                            self.check_supplier_existence()
                            dialog.close()
                        else:
                            QMessageBox.warning(dialog, "تحذير", "لم يتم تحديد بائع صالح!")
                except Exception as e:
                    print(f"خطأ في تحديد البائع: {e}")
                    QMessageBox.warning(dialog, "خطأ", f"حدث خطأ أثناء التحديد:\n{str(e)}")

            select_btn = QPushButton("تحديد")
            select_btn.clicked.connect(select_supplier)
            layout.addWidget(select_btn)

            dialog.setLayout(layout)
            dialog.exec()

        except Exception as e:
            print(f"خطأ في فتح نافذة البحث: {e}")
            QMessageBox.warning(self, "خطأ", f"حدث خطأ في فتح نافذة البحث:\n{str(e)}")

    def load_sizes_combo(self):
        """تحميل المقاسات الفريدة"""
        try:
            all_items = self.virtual_table if self.virtual_table else self.db.load_items()
            self.size_filter_combo.clear()

            unique_sizes = set()
            for item in all_items:
                size = item.get('size', '').strip()
                if size:
                    unique_sizes.add(size)

            self.size_filter_combo.addItem("جميع المقاسات")
            for size in sorted(unique_sizes):
                self.size_filter_combo.addItem(size)

            self.size_filter_combo.setCurrentIndex(0)

        except Exception as e:
            print(f"خطأ في تحميل المقاسات: {e}")

    def filter_items_combo(self, text):
        """فلترة أثناء الكتابة"""
        try:
            if not text.strip():
                for i in range(self.item_combo.count()):
                    self.item_combo.setItemHidden(i, False)
                return

            search_text = text.strip().lower()
            for i in range(self.item_combo.count()):
                item_text = self.item_combo.itemText(i).lower()
                self.item_combo.setItemHidden(i, search_text not in item_text)

        except Exception as e:
            print(f"خطأ في الفلترة: {e}")

    def search_in_combo(self, combo_box):
        """فتح نافذة بحث"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("بحث")
            dialog.setGeometry(200, 200, 400, 300)

            layout = QVBoxLayout()
            layout.addWidget(QLabel("اكتب للبحث:"))

            search_input = QLineEdit()
            search_input.textChanged.connect(lambda text: self.filter_search_results(combo_box, text, result_list))
            layout.addWidget(search_input)

            result_list = QListWidget()
            layout.addWidget(result_list)

            # تحميل جميع العناصر
            for i in range(combo_box.count()):
                result_list.addItem(combo_box.itemText(i))
                result_list.item(i).setData(Qt.ItemDataRole.UserRole, i)

            select_btn = QPushButton("تحديد")
            select_btn.clicked.connect(lambda: self.select_search_result(combo_box, result_list, dialog))
            layout.addWidget(select_btn)

            dialog.setLayout(layout)
            dialog.exec()

        except Exception as e:
            print(f"خطأ في البحث: {e}")

    def filter_search_results(self, combo_box, text, result_list):
        """فلترة نتائج البحث"""
        result_list.clear()
        search_text = text.strip().lower()

        if not search_text:
            for i in range(combo_box.count()):
                result_list.addItem(combo_box.itemText(i))
                result_list.item(result_list.count() - 1).setData(Qt.ItemDataRole.UserRole, i)
            return

        for i in range(combo_box.count()):
            item_text = combo_box.itemText(i).lower()
            if search_text in item_text:
                result_list.addItem(combo_box.itemText(i))
                result_list.item(result_list.count() - 1).setData(Qt.ItemDataRole.UserRole, i)

    def select_search_result(self, combo_box, result_list, dialog):
        """تحديد نتيجة البحث"""
        try:
            selected_item = result_list.currentItem()
            if selected_item:
                index = selected_item.data(Qt.ItemDataRole.UserRole)
                if index is not None:
                    # تحديد العنصر في الـ ComboBox
                    combo_box.setCurrentIndex(index)
                    dialog.close()
        except Exception as e:
            print(f"خطأ في تحديد العنصر: {e}")

    def update_cart_display(self):
        """تحديث عرض السلة"""
        self.cart_table.setRowCount(len(self.cart_items))

        total_buying = 0
        total_selling = 0

        for i, item in enumerate(self.cart_items):
            # الرقم التسلسلي
            self.cart_table.setItem(i, 0, QTableWidgetItem(str(i+1)))

            # الصنف
            self.cart_table.setItem(i, 1, QTableWidgetItem(item['name']))

            # المقاس
            self.cart_table.setItem(i, 2, QTableWidgetItem(item['size']))

            # الكمية
            self.cart_table.setItem(i, 3, QTableWidgetItem(str(item['quantity'])))

            # سعر الشراء
            self.cart_table.setItem(i, 4, QTableWidgetItem(f"{item['buying_price']} ج.م"))

            # سعر البيع
            self.cart_table.setItem(i, 5, QTableWidgetItem(f"{item['selling_price']} ج.م"))

            # الإجمالي شراء
            self.cart_table.setItem(i, 6, QTableWidgetItem(f"{item['buying_total']} ج.م"))

            # الإجمالي بيع
            self.cart_table.setItem(i, 7, QTableWidgetItem(f"{item['selling_total']} ج.م"))

            total_buying += item['buying_total']
            total_selling += item['selling_total']

        self.current_total = total_buying
        self.cart_total_label.setText(f"إجمالي السلة (شراء): {total_buying:.2f} ج.م")
        self.cart_selling_total_label.setText(f"إجمالي السلة (بيع): {total_selling:.2f} ج.م")

        # تحديث الإجماليات في الخطوة 3
        self.current_total_label.setText(f"{total_buying:.2f} ج.م")
        self.current_selling_total_label.setText(f"{total_selling:.2f} ج.م")

        self.calculate_totals()

    def get_supplier_true_remaining(self, supplier_name):
        """الحصول على المتبقي الحقيقي للبائع - من آخر قسط فقط لكل فاتورة"""
        try:
            supplier_name_lower = supplier_name.strip().lower()
            imports_history = self.load_imports_history()
            
            if not imports_history:
                return 0.0
            
            # تجميع الفواتير الأصلية
            original_invoices = {}
            for invoice in imports_history:
                invoice_supplier_name = invoice.get('supplier_name', '').strip().lower()
                if invoice_supplier_name != supplier_name_lower:
                    continue
                
                import_id = invoice.get('import_id', '')
                
                # نأخذ الفواتير الأصلية فقط (بدون أقساط وبدون سجلات REM_)
                if '.' not in import_id and not import_id.startswith('REM_'):
                    original_invoices[import_id] = {
                        'original_invoice': invoice,
                        'last_payment': invoice  # بداية، الفاتورة الأصلية هي آخر سجل
                    }
            
            # البحث عن آخر قسط لكل فاتورة
            for invoice in imports_history:
                invoice_supplier_name = invoice.get('supplier_name', '').strip().lower()
                if invoice_supplier_name != supplier_name_lower:
                    continue
                
                import_id = invoice.get('import_id', '')
                
                # إذا كانت فاتورة قسط (تحتوي على نقطة)
                if '.' in import_id:
                    parts = import_id.split('.')
                    if len(parts) >= 2:
                        original_id = parts[0]
                        
                        if original_id in original_invoices:
                            # استخراج رقم القسط
                            try:
                                payment_number = int(parts[1])
                            except:
                                payment_number = 0
                            
                            # الحصول على آخر قسط مسجل حالياً
                            last_payment = original_invoices[original_id]['last_payment']
                            last_payment_id = last_payment.get('import_id', '')
                            
                            # استخراج رقم آخر قسط
                            last_payment_number = 0
                            if '.' in last_payment_id:
                                try:
                                    last_parts = last_payment_id.split('.')
                                    if len(last_parts) >= 2:
                                        last_payment_number = int(last_parts[1])
                                except:
                                    pass
                            
                            # إذا كان هذا القسط أحدث، نجعله آخر قسط
                            if payment_number > last_payment_number:
                                original_invoices[original_id]['last_payment'] = invoice
            
            # حساب المتبقي الإجمالي من آخر قسط لكل فاتورة
            total_remaining = 0.0
            
            for original_id, data in original_invoices.items():
                last_payment = data['last_payment']
                
                # نجمع المتبقي من آخر قسط فقط
                try:
                    remaining = float(last_payment.get('remaining', 0))
                    total_remaining += remaining
                except:
                    pass
            
            # إضافة سجلات REM_ (المتبقي غير المسجل)
            for invoice in imports_history:
                invoice_supplier_name = invoice.get('supplier_name', '').strip().lower()
                if invoice_supplier_name != supplier_name_lower:
                    continue
                
                import_id = invoice.get('import_id', '')
                
                # إضافة سجلات REM_ مباشرة
                if import_id.startswith('REM_'):
                    try:
                        remaining = float(invoice.get('remaining', 0))
                        total_remaining += remaining
                    except:
                        pass
            
            return total_remaining
            
        except Exception as e:
            print(f"خطأ في حساب المتبقي الحقيقي: {e}")
            # نسخة احتياطية أبسط
            try:
                supplier_name_lower = supplier_name.strip().lower()
                imports_history = self.load_imports_history()
                total_remaining = 0.0
                
                for invoice in imports_history:
                    if invoice.get('supplier_name', '').strip().lower() == supplier_name_lower:
                        try:
                            remaining = float(invoice.get('remaining', 0))
                            total_remaining += remaining
                        except:
                            pass
                
                return total_remaining
            except:
                return 0.0

    def remove_from_cart(self):
        """حذف منتج من السلة"""
        selected = self.cart_table.currentRow()
        if selected >= 0:
            self.cart_items.pop(selected)
            self.update_cart_display()

    def calculate_totals(self):
        """حساب جميع الإجماليات"""
        # الإجمالي الحالي من السلة
        current_total_buying = sum(item['buying_total'] for item in self.cart_items)
        current_total_selling = sum(item['selling_total'] for item in self.cart_items)

        # الإجمالي الكلي
        self.total_cumulative = current_total_buying

        # تحديث العناوين
        self.current_total_label.setText(f"{current_total_buying:.2f} ج.م")
        self.current_selling_total_label.setText(f"{current_total_selling:.2f} ج.م")
        self.cumulative_total_label.setText(f"{self.total_cumulative:.2f} ج.م")

        # تحديث مدى الدفع
        self.amount_paid_input.setMaximum(self.total_cumulative)

        # تحديث ملخص الدفع
        self.update_payment_summary()

        # تحديث معلومات البائع
        self.update_supplier_summary()

    def update_supplier_summary(self):
        """تحديث ملخص البائع"""
        supplier_name = self.supplier_name_input.text().strip()
        if not supplier_name:
            supplier_name = "غير محدد"

        supplier_type = "موجود سابقاً" if self.existing_supplier else "جديد"

        self.supplier_summary_label.setText(
            f"البائع: {supplier_name}\n"
            f"الحالة: {supplier_type}\n"
            f"عدد المنتجات في السلة: {len(self.cart_items)}"
        )

    def update_payment_summary(self):
        """تحديث ملخص الدفع"""
        amount_paid = self.amount_paid_input.value()

        # حساب المتبقي
        remaining = self.total_cumulative - amount_paid
        self.total_remaining = remaining

        # تحديث العناوين
        self.remaining_invoice_label.setText(f"{remaining:.2f} ج.م")
        self.remaining_total_label.setText(f"{remaining:.2f} ج.م")

        # تحديث حالة الدفع
        if remaining <= 0:
            payment_status = "مدفوع بالكامل"
            color = "#27ae60"
        elif amount_paid == 0:
            payment_status = "غير مدفوع"
            color = "#e74c3c"
        else:
            payment_status = "سداد قسط"
            color = "#9b59b6"  # بنفسجي للسداد القسط

        self.payment_status_label.setText(payment_status)
        self.payment_status_label.setStyleSheet(f"""
            font-size: 18px; 
            font-weight: bold; 
            color: {color};
            padding: 10px;
            text-align: center;
            border: 2px solid {color};
            border-radius: 5px;
            background-color: #fff;
        """)

        # تحديث النطاق المسموح
        self.range_label.setText(f"المبلغ المسموح دفعه: 0.00 - {self.total_cumulative:.2f} ج.م")

    def prev_step(self):
        """الانتقال للخطوة السابقة"""
        if self.current_step > 1:
            self.current_step -= 1
            self.update_step()

    def update_step(self):
        """تحديث عرض الخطوة الحالية"""
        self.stacked_widget.setCurrentIndex(self.current_step - 1)

        step_titles = [
            "الخطوة 1: معلومات البائع",
            "الخطوة 2: اختيار المنتجات",
            "الخطوة 3: الدفع والإجماليات"
        ]
        self.step_label.setText(step_titles[self.current_step - 1])

        self.prev_btn.setEnabled(self.current_step > 1)

        if self.current_step == 3:
            self.next_btn.setText("إنهاء")
        else:
            self.next_btn.setText("التالي ←")

    def load_imports_history(self):
        """تحميل سجل الاستيراد من ملف CSV مخصص - معدلة"""
        imports_file = "imports_history.csv"
        imports = []

        if not os.path.exists(imports_file):
            print(f"📁 [CreateImportWindow.load_imports_history] الملف {imports_file} غير موجود")
            return imports

        try:
            with open(imports_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # التحقق من وجود الحقول الأساسية
                if reader.fieldnames is None:
                    print("⚠️ الملف فارغ أو تالف")
                    return imports

                print(f"📊 [CreateImportWindow.load_imports_history] حقول الملف: {reader.fieldnames}")

                # الحقول الرقمية المحتملة
                numeric_fields = ['total', 'selling_total', 'previous_balance', 'total_cumulative', 
                                 'amount_paid', 'remaining', 'payment_amount']

                for row_num, row in enumerate(reader, 1):
                    try:
                        # تحويل الحقول الرقمية مع معالجة القيم الفارغة
                        for field in numeric_fields:
                            if field in row and row[field]:
                                try:
                                    # تنظيف القيمة من النصوص غير الرقمية
                                    clean_value = str(row[field]).strip()
                                    import re
                                    numeric_part = re.sub(r'[^\d\.]', '', clean_value)
                                    if numeric_part:
                                        row[field] = float(numeric_part)
                                    else:
                                        row[field] = 0.0
                                except (ValueError, TypeError) as e:
                                    print(f"⚠️ خطأ في تحويل {field} في السطر {row_num}: '{row[field]}' -> {e}")
                                    row[field] = 0.0
                            else:
                                row[field] = 0.0

                        # تحويل المنتجات من JSON
                        if 'products' in row and row['products']:
                            try:
                                row['products'] = json.loads(row['products'])
                            except (json.JSONDecodeError, TypeError) as e:
                                print(f"⚠️ خطأ في تحويل products في السطر {row_num}: {e}")
                                row['products'] = []
                        else:
                            row['products'] = []

                        # معالجة الحقول الأخرى
                        if 'payment_count' not in row:
                            row['payment_count'] = 0
                        else:
                            try:
                                row['payment_count'] = int(float(row['payment_count']))
                            except (ValueError, TypeError):
                                row['payment_count'] = 0

                        if 'original_import_id' not in row:
                            row['original_import_id'] = row.get('import_id', '')

                        if 'payment_status' not in row:
                            # تحديد الحالة تلقائياً
                            amount_paid = float(row.get('amount_paid', 0))
                            total = float(row.get('total', 0))

                            if amount_paid <= 0:
                                row['payment_status'] = 'غير مدفوع'
                            elif amount_paid >= total:
                                row['payment_status'] = 'مدفوع بالكامل'
                            else:
                                row['payment_status'] = 'سداد قسط'

                        imports.append(row)

                    except Exception as e:
                        print(f"⚠️ خطأ في معالجة السطر {row_num}: {e}")
                        continue

                print(f"✅ [CreateImportWindow.load_imports_history] تم تحميل {len(imports)} فاتورة من {imports_file}")

        except Exception as e:
            print(f"❌ [CreateImportWindow.load_imports_history] خطأ في تحميل سجل الاستيراد: {e}")
            import traceback
            traceback.print_exc()

        return imports

    def save_import_to_csv(self, invoice_data):
        """حفظ فاتورة الاستيراد في ملف CSV"""
        imports_file = "imports_history.csv"

        # تحضير البيانات للتخزين
        invoice_to_save = invoice_data.copy()
        invoice_to_save['products'] = json.dumps(invoice_to_save['products'], ensure_ascii=False)

        # التحقق إذا كان الملف موجوداً
        file_exists = os.path.exists(imports_file)

        # قراءة الحقول الموجودة إذا كان الملف موجوداً
        fieldnames = []
        if file_exists:
            try:
                with open(imports_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    if header:
                        fieldnames = header
            except:
                pass

        # إذا لم نتمكن من قراءة الحقول أو الملف غير موجود
        if not fieldnames:
            # الحقول الأساسية مع الحقول الإضافية
            fieldnames = [
                'import_id', 'supplier_id', 'supplier_name', 'supplier_phone',
                'supplier_address', 'date', 'due_date', 'products', 'total',
                'selling_total', 'previous_balance', 'total_cumulative', 'amount_paid', 
                'remaining', 'payment_status', 'notes', 'original_import_id', 
                'payment_count', 'payment_amount'
            ]

        # إضافة أي حقول مفقودة من البيانات
        for key in invoice_to_save.keys():
            if key not in fieldnames:
                fieldnames.append(key)

        # التأكد من وجود جميع الحقول في البيانات
        for field in fieldnames:
            if field not in invoice_to_save:
                if field in ['previous_balance', 'total_cumulative']:
                    invoice_to_save[field] = 0.0
                elif field == 'notes':
                    invoice_to_save[field] = ''

        with open(imports_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(invoice_to_save)

        print(f"✅ [CreateImportWindow.save_import_to_csv] تم حفظ فاتورة {invoice_data['import_id']} في {imports_file}")

class ImportsHistoryWindow(QWidget):
    """نافذة سجل الاستيراد"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.is_editing = False
        self.init_ui()
        self.load_imports_history()
    
    def init_ui(self):
        self.setWindowTitle('سجل الاستيراد')
        self.setGeometry(150, 150, 1400, 750)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout()
        
        # العنوان
        title = QLabel("سجل فواتير الاستيراد")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        # البحث والفلتر
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("بحث:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث برقم الفاتورة أو اسم البائع أو الهاتف")
        self.search_input.textChanged.connect(self.filter_history)
        filter_layout.addWidget(self.search_input)
        
        filter_layout.addWidget(QLabel("فلتر حسب البائع:"))
        self.supplier_filter = QComboBox()
        self.supplier_filter.addItem("جميع البائعين", None)
        self.supplier_filter.currentIndexChanged.connect(self.filter_history)
        filter_layout.addWidget(self.supplier_filter)
        
        # فلتر التاريخ
        filter_layout.addWidget(QLabel("من تاريخ:"))
        self.date_from_filter = QDateEdit()
        self.date_from_filter.setDate(QDate.currentDate().addDays(-30))
        self.date_from_filter.setDisplayFormat("yyyy-MM-dd")
        self.date_from_filter.setCalendarPopup(True)
        self.date_from_filter.dateChanged.connect(self.filter_history)
        filter_layout.addWidget(self.date_from_filter)
        
        filter_layout.addWidget(QLabel("إلى تاريخ:"))
        self.date_to_filter = QDateEdit()
        self.date_to_filter.setDate(QDate.currentDate())
        self.date_to_filter.setDisplayFormat("yyyy-MM-dd")
        self.date_to_filter.setCalendarPopup(True)
        self.date_to_filter.dateChanged.connect(self.filter_history)
        filter_layout.addWidget(self.date_to_filter)
        
        # فلتر حالة الدفع
        filter_layout.addWidget(QLabel("حالة الدفع:"))
        self.payment_status_filter = QComboBox()
        self.payment_status_filter.addItem("جميع الحالات", "all")
        self.payment_status_filter.addItem("مدفوع بالكامل", "paid")
        self.payment_status_filter.addItem("سداد قسط", "payment")
        self.payment_status_filter.addItem("لم يدفع", "unpaid")
        self.payment_status_filter.currentIndexChanged.connect(self.filter_history)
        filter_layout.addWidget(self.payment_status_filter)
        
        layout.addLayout(filter_layout)
        
        # زر دفع للبائع مع مجموع المتبقي
        payment_layout = QHBoxLayout()
        
        # خانة دفع للبائع
        payment_to_supplier_layout = QVBoxLayout()
        payment_to_supplier_layout.addWidget(QLabel("دفع للبائع:"))
        
        self.payment_to_supplier_input = QDoubleSpinBox()
        self.payment_to_supplier_input.setDecimals(2)
        self.payment_to_supplier_input.setMinimum(0.0)
        self.payment_to_supplier_input.setMaximum(999999.99)
        self.payment_to_supplier_input.setPrefix("ج.م ")
        self.payment_to_supplier_input.setValue(0.0)
        payment_to_supplier_layout.addWidget(self.payment_to_supplier_input)
        
        payment_layout.addLayout(payment_to_supplier_layout)
        
        # زر تأكيد الدفع
        confirm_payment_btn = QPushButton("💳 تأكيد الدفع")
        confirm_payment_btn.setToolTip("توزيع المبلغ على فواتير البائع المحدد")
        confirm_payment_btn.setFixedWidth(120)
        confirm_payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 8px 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        confirm_payment_btn.clicked.connect(self.process_bulk_payment)
        payment_layout.addWidget(confirm_payment_btn)
        
        # خانة عرض مجموع المتبقي التلقائي
        self.remaining_sum_label = QLabel("مجموع المتبقي: 0.00 ج.م")
        self.remaining_sum_label.setStyleSheet("""
            QLabel {
                background-color: #2c3e50;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 250px;
                text-align: center;
                font-size: 14px;
            }
        """)
        payment_layout.addWidget(self.remaining_sum_label)
        
        # زر حساب مجموع المتبقي
        self.calculate_btn = QPushButton("🧮 حساب مجموع المتبقي")
        self.calculate_btn.setToolTip("حساب مجموع المتبقي للبائع المحدد")
        self.calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.calculate_btn.clicked.connect(self.calculate_supplier_remaining)
        payment_layout.addWidget(self.calculate_btn)
        
        # إضافة خانة "إضافة للمتبقي"
        add_remaining_layout = QVBoxLayout()
        add_remaining_layout.addWidget(QLabel("إضافة للمتبقي:"))
        
        self.add_remaining_input = QDoubleSpinBox()
        self.add_remaining_input.setDecimals(2)
        self.add_remaining_input.setMinimum(0.0)
        self.add_remaining_input.setMaximum(999999.99)
        self.add_remaining_input.setPrefix("ج.م ")
        self.add_remaining_input.setValue(0.0)
        add_remaining_layout.addWidget(self.add_remaining_input)
        
        payment_layout.addLayout(add_remaining_layout)
        
        # زر إضافة للمتبقي
        add_remaining_btn = QPushButton("➕ إضافة للمتبقي")
        add_remaining_btn.setToolTip("إضافة قيمة للمتبقي العام للعميل (للفواتير غير المسجلة)")
        add_remaining_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 8px 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        add_remaining_btn.clicked.connect(self.add_to_remaining)
        payment_layout.addWidget(add_remaining_btn)
        
        payment_layout.addStretch()
        layout.addLayout(payment_layout)
        
        # الجدول مع الأعمدة الجديدة
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "رقم الفاتورة",
            "رقم البائع",
            "اسم البائع",
            "التاريخ",
            "المنتجات",
            "إجمالي الفاتورة",
            "المدفوع",
            "المتبقي الحالي",
            "الحالة"
        ])
        
        # ضبط عرض الأعمدة
        self.table.setColumnWidth(0, 140)  # رقم الفاتورة
        self.table.setColumnWidth(1, 100)  # رقم البائع
        self.table.setColumnWidth(2, 150)  # اسم البائع
        self.table.setColumnWidth(3, 120)  # التاريخ
        self.table.setColumnWidth(4, 350)  # المنتجات
        self.table.setColumnWidth(5, 120)  # إجمالي الفاتورة
        self.table.setColumnWidth(6, 100)  # المدفوع
        self.table.setColumnWidth(7, 120)  # المتبقي الحالي
        # العمود 8 سيتمدد تلقائياً
        
        # تعيين ارتفاع الصفوف لاستيعاب المنتجات
        self.table.verticalHeader().setDefaultSectionSize(100)
        
        self.table.setStyleSheet(self.get_table_style())
        layout.addWidget(self.table)
        
        # إحصائيات
        stats_layout = QHBoxLayout()
        
        self.total_invoices_label = QLabel("عدد الفواتير: 0")
        self.total_amount_label = QLabel("إجمالي المبالغ: 0.00 ج.م")
        self.total_paid_label = QLabel("إجمالي المدفوع: 0.00 ج.م")
        self.total_remaining_label = QLabel("إجمالي المتبقي: 0.00 ج.م")
        
        for label in [self.total_invoices_label, self.total_amount_label, 
                     self.total_paid_label, self.total_remaining_label]:
            label.setStyleSheet("""
                QLabel {
                    background-color: #34495e;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12px;
                    margin: 2px;
                }
            """)
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # أزرار التحكم
        button_layout = QHBoxLayout()
        
        # زر سداد قسط
        payment_btn = QPushButton("💰 سداد قسط")
        payment_btn.setToolTip("سداد قسط للفاتورة المحددة")
        payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        payment_btn.clicked.connect(self.process_payment)
        button_layout.addWidget(payment_btn)
        
        # زر تعديل
        edit_btn = QPushButton("✏️ تعديل")
        edit_btn.setToolTip("تفعيل/تعطيل وضع التعديل")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        edit_btn.clicked.connect(self.toggle_edit_mode)
        button_layout.addWidget(edit_btn)
        
        # زر إضافة
        add_btn = QPushButton("➕ إضافة")
        add_btn.setToolTip("إضافة فاتورة جديدة")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        add_btn.clicked.connect(self.add_new_invoice)
        button_layout.addWidget(add_btn)
        
        # زر حذف
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.setToolTip("حذف الفاتورة المحددة")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_invoice)
        button_layout.addWidget(delete_btn)
        
        # زر حفظ
        save_btn = QPushButton("💾 حفظ")
        save_btn.setToolTip("حفظ جميع التغييرات")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        save_btn.clicked.connect(self.save_changes)
        button_layout.addWidget(save_btn)
        
        button_layout.addStretch()
        
        # زر الخروج
        exit_btn = QPushButton("خروج")
        exit_btn.setToolTip("إغلاق النافذة")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6c7b7d;
            }
        """)
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_table_style(self):
        return """
            QTableWidget {
                background-color: #1f2327;
                alternate-background-color: #272a2d;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """
    
    def load_imports_history(self):
        """تحميل سجل الاستيراد"""
        imports = self.load_imports_from_csv()
        
        # ترتيب الفواتير: الفواتير الأصلية أولاً ثم الأقساط مرتبة
        sorted_imports = self.sort_invoices_hierarchically(imports)
        self.all_imports = sorted_imports
        
        # تحديث قائمة البائعين مع السماح بالكتابة الحرة
        self.supplier_filter.clear()
        self.supplier_filter.setEditable(True)
        self.supplier_filter.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        self.supplier_filter.lineEdit().setPlaceholderText("اكتب للبحث أو اختر من القائمة")
        
        # إضافة خيار "جميع البائعين"
        self.supplier_filter.addItem("جميع البائعين", None)
        
        # إضافة البائعين الفريدين
        suppliers = {}
        for invoice in imports:
            supplier_name = invoice.get('supplier_name', '')
            supplier_id = invoice.get('supplier_id', '')
            if supplier_name and supplier_id:
                if supplier_id not in suppliers:
                    suppliers[supplier_id] = supplier_name
        
        for sid, sname in sorted(suppliers.items(), key=lambda x: x[1]):
            display_text = f"{sname} ({sid})"
            self.supplier_filter.addItem(display_text, sid)
        
        self.display_imports(self.all_imports)
        self.update_statistics()
        self.update_remaining_summary()
    
    def sort_invoices_hierarchically(self, invoices):
        """ترتيب الفواتير هرمياً: الفواتير الأصلية ثم الأقساط مرتبة"""
        # فصل الفواتير الأصلية عن الأقساط
        original_invoices = []
        payment_invoices = []
        
        for invoice in invoices:
            import_id = invoice.get('import_id', '')
            if '.' in import_id:
                payment_invoices.append(invoice)
            else:
                original_invoices.append(invoice)
        
        # ترتيب الفواتير الأصلية حسب التاريخ (الأحدث أولاً)
        original_invoices.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # ترتيب الأقساط حسب الفاتورة الأصلية ورقم القسط
        payment_invoices.sort(key=lambda x: (
            x.get('original_import_id', ''),
            self.extract_payment_number(x.get('import_id', ''))
        ))
        
        # دمج القوائم مع إدراج الأقساط تحت الفواتير الأصلية
        sorted_invoices = []
        
        for original in original_invoices:
            sorted_invoices.append(original)
            original_id = original.get('import_id', '')
            
            # إضافة أقساط هذه الفاتورة
            for payment in payment_invoices:
                if payment.get('original_import_id', '') == original_id:
                    sorted_invoices.append(payment)
        
        return sorted_invoices
    
    def extract_payment_number(self, import_id):
        """استخراج رقم القسط من معرف الفاتورة"""
        if '.' in import_id:
            try:
                return int(import_id.split('.')[-1])
            except:
                return 0
        return 0
    
    def load_imports_from_csv(self):
        """تحميل فواتير الاستيراد من CSV"""
        imports_file = "imports_history.csv"
        imports = []
        
        if not os.path.exists(imports_file):
            return imports
        
        try:
            with open(imports_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # تحويل الحقول الرقمية
                    numeric_fields = ['total', 'selling_total', 'previous_balance', 
                                   'total_cumulative', 'amount_paid', 'remaining', 'payment_amount']
                    for field in numeric_fields:
                        if field in row and row[field]:
                            try:
                                row[field] = float(row[field])
                            except (ValueError, TypeError):
                                row[field] = 0.0
                    
                    # تحويل المنتجات من JSON
                    if 'products' in row and row['products']:
                        try:
                            row['products'] = json.loads(row['products'])
                        except json.JSONDecodeError:
                            row['products'] = []
                    
                    # معالجة الحقول الجديدة
                    if 'original_import_id' not in row:
                        row['original_import_id'] = row.get('import_id', '')
                    
                    if 'payment_count' not in row:
                        row['payment_count'] = 0
                    else:
                        try:
                            row['payment_count'] = int(row['payment_count'])
                        except (ValueError, TypeError):
                            row['payment_count'] = 0
                    
                    if 'payment_amount' not in row:
                        row['payment_amount'] = 0.0
                    else:
                        try:
                            row['payment_amount'] = float(row['payment_amount'])
                        except (ValueError, TypeError):
                            row['payment_amount'] = 0.0
                    
                    imports.append(row)
        except Exception as e:
            print(f"خطأ في تحميل سجل الاستيراد: {e}")
        
        return imports
    
    def display_imports(self, imports):
        """عرض فواتير الاستيراد في الجدول"""
        self.table.setRowCount(len(imports))
        
        for i, invoice in enumerate(imports):
            # رقم الفاتورة
            import_id = invoice['import_id']
            import_item = QTableWidgetItem(import_id)
            
            # تمييز الفواتير الأصلية عن الأقساط
            if '.' in import_id:
                import_item.setBackground(QColor("#e8f4f8"))  # لون فاتح للأقساط
                import_item.setForeground(QColor("#3498db"))  # لون أزرق

            elif import_id.startswith('REM_'):  # <-- هذا السطر المضافة
                # فاتورة رصيد غير مسجل (إضافة للمتبقي)
                import_item.setBackground(QColor("#F5DEB3"))  # لون بني فاتح
                import_item.setForeground(QColor("#8B4513"))  # لون بني داكن

            else:
                import_item.setBackground(QColor("#e8f6e8"))  # لون فاتح للفواتير الأصلية
                import_item.setForeground(QColor("#27ae60"))  # لون أخضر
            
            self.table.setItem(i, 0, import_item)
            
            # رقم البائع
            self.table.setItem(i, 1, QTableWidgetItem(invoice['supplier_id']))
            
            # اسم البائع
            self.table.setItem(i, 2, QTableWidgetItem(invoice['supplier_name']))
            
            # التاريخ
            self.table.setItem(i, 3, QTableWidgetItem(invoice['date']))
            
            # المنتجات
            products_text = self.format_products_text(invoice['products'])
            products_item = QTableWidgetItem(products_text)
            products_item.setTextAlignment(Qt.AlignmentFlag.AlignTop)
            self.table.setItem(i, 4, products_item)
            
            # إجمالي الفاتورة
            total_item = QTableWidgetItem(f"{invoice['total']:.2f} ج.م")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 5, total_item)
            
            # المدفوع
            amount_paid = float(invoice.get('amount_paid', 0))
            paid_item = QTableWidgetItem(f"{amount_paid:.2f} ج.م")
            paid_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if amount_paid > 0:
                paid_item.setForeground(QColor("#27ae60"))
            self.table.setItem(i, 6, paid_item)
            
            # المتبقي الحالي
            remaining = float(invoice.get('remaining', 0))
            remaining_item = QTableWidgetItem(f"{remaining:.2f} ج.م")
            remaining_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if remaining > 0:
                remaining_item.setForeground(QColor("#e74c3c"))
            self.table.setItem(i, 7, remaining_item)
            
            # الحالة
            payment_status = invoice.get('payment_status', 'غير مدفوع')
            
            # تحويل حالة "دفع جزئي" إلى "سداد قسط"
            if payment_status == "دفع جزئي":
                payment_status = "سداد قسط"
            
            status_item = QTableWidgetItem(payment_status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # تلوين حسب الحالة
            if payment_status == "مدفوع بالكامل":
                status_item.setBackground(QColor("#27ae60"))
            elif payment_status == "سداد قسط":
                status_item.setBackground(QColor("#9b59b6"))
            else:
                status_item.setBackground(QColor("#e74c3c"))
            
            status_item.setForeground(QColor("white"))
            self.table.setItem(i, 8, status_item)
            
            # حفظ بيانات الفاتورة كبيانات إضافية للصف
            self.table.item(i, 0).setData(Qt.ItemDataRole.UserRole, invoice)
    
    def format_products_text(self, products):
        """تنسيق نص المنتجات للعرض في خلية واحدة"""
        if not products:
            return "لا توجد منتجات"
        
        lines = []
        for product in products:
            line = f"[{product['name']}, المقاس:{product['size']}, الشراء:{product['buying_price']} ج.م, الكمية:{product['quantity']}]"
            lines.append(line)
        
        return "\n".join(lines)
    
    def filter_history(self):
        """فلترة السجل مع دعم البحث بالاسم والكود"""
        search_text = self.search_input.text().strip().lower()
        selected_supplier = self.supplier_filter.currentData()
        payment_status_filter = self.payment_status_filter.currentText()
        date_from = self.date_from_filter.date().toString("yyyy-MM-dd")
        date_to = self.date_to_filter.date().toString("yyyy-MM-dd")
        
        filtered = []
        
        for invoice in self.all_imports:
            # 1. فلتر البحث
            if search_text:
                search_match = False
                
                fields_to_search = [
                    invoice.get('import_id', ''),
                    invoice.get('supplier_name', ''),
                    invoice.get('supplier_id', ''),
                    invoice.get('supplier_phone', ''),
                    invoice.get('supplier_address', ''),
                    invoice.get('notes', '')
                ]
                
                for field in fields_to_search:
                    if search_text in str(field).lower():
                        search_match = True
                        break
                
                if not search_match:
                    continue
            
            # 2. فلتر البائع
            if selected_supplier and invoice.get('supplier_id') != selected_supplier:
                continue
            
            # 3. فلتر التاريخ
            invoice_date = invoice.get('date', '')
            if invoice_date:
                try:
                    inv_date = QDate.fromString(invoice_date, "yyyy-MM-dd")
                    from_date = QDate.fromString(date_from, "yyyy-MM-dd")
                    to_date = QDate.fromString(date_to, "yyyy-MM-dd")
                    
                    if inv_date < from_date or inv_date > to_date:
                        continue
                except:
                    continue
            
            # 4. فلتر حالة الدفع
            if payment_status_filter != "جميع الحالات":
                current_status = invoice.get('payment_status', 'غير مدفوع')
                
                if current_status == "دفع جزئي":
                    current_status = "سداد قسط"
                
                if current_status != payment_status_filter:
                    continue
            
            filtered.append(invoice)
        
        self.display_imports(filtered)
        self.update_statistics()
        self.update_remaining_summary()
    
    def update_statistics(self):
        """تحديث الإحصائيات - معدلة لحساب المتبقي من آخر قسط فقط لكل فاتورة"""
        filtered_count = self.table.rowCount()
        
        # استخدام قائمة الفواتير المفلترة بدلاً من الجدول
        filtered_invoices = []
        for row in range(filtered_count):
            invoice = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            if invoice:
                filtered_invoices.append(invoice)
        
        total_invoices = 0
        total_amount = 0
        total_paid = 0
        total_remaining = 0
        
        # تجميع الفواتير الأصلية
        original_invoices = {}
        for invoice in filtered_invoices:
            import_id = invoice.get('import_id', '')
            
            if '.' not in import_id:  # فاتورة أصلية
                original_import_id = import_id
                original_invoices[original_import_id] = {
                    'invoice': invoice,
                    'last_payment': invoice  # الفاتورة الأصلية هي آخر سجل افتراضي
                }
        
        # البحث عن آخر قسط لكل فاتورة
        for invoice in filtered_invoices:
            import_id = invoice.get('import_id', '')
            
            if '.' in import_id:  # سجل قسط
                original_import_id = invoice.get('original_import_id', '')
                if original_import_id in original_invoices:
                    # استخراج رقم القسط
                    payment_number = self.extract_payment_number(import_id)
                    # استخراج رقم آخر قسط مسجل
                    last_payment_id = original_invoices[original_import_id]['last_payment']['import_id']
                    last_payment_number = self.extract_payment_number(last_payment_id)
                    
                    # إذا كان هذا القسط أحدث
                    if payment_number > last_payment_number:
                        original_invoices[original_import_id]['last_payment'] = invoice
        
        # حساب الإحصائيات بناءً على آخر قسط لكل فاتورة
        for original_import_id, data in original_invoices.items():
            total_invoices += 1  # كل فاتورة أصلية تحسب مرة واحدة
            
            # إجمالي الفاتورة من الفاتورة الأصلية
            original_invoice = data['invoice']
            total_amount += float(original_invoice.get('total', 0))
            
            # استخدام آخر قسط للحساب
            last_payment = data['last_payment']
            
            # إجمالي المدفوع من آخر قسط
            last_payment_paid = float(last_payment.get('amount_paid', 0))
            total_paid += last_payment_paid
            
            # المتبقي من آخر قسط
            last_payment_remaining = float(last_payment.get('remaining', 0))
            total_remaining += last_payment_remaining
        
        # تحديث العناوين
        self.total_invoices_label.setText(f"عدد الفواتير: {total_invoices}")
        self.total_amount_label.setText(f"إجمالي المبالغ: {total_amount:.2f} ج.م")
        self.total_paid_label.setText(f"إجمالي المدفوع: {total_paid:.2f} ج.م")
        self.total_remaining_label.setText(f"إجمالي المتبقي: {total_remaining:.2f} ج.م")
        # تحديث ملخص المتبقي في الأعلى
        self.update_remaining_summary()
    
    def calculate_supplier_remaining(self):
        """حساب مجموع المتبقي للبائع المحدد - من آخر قسط فقط لكل فاتورة"""
        selected_supplier = self.supplier_filter.currentData()
        
        if not selected_supplier:
            QMessageBox.warning(self, "تحذير", "الرجاء تحديد بائع أولاً!")
            return
        
        total_remaining = 0
        total_paid = 0
        supplier_name = ""
        original_invoices = {}
        
        # تجميع فواتير البائع المحدد
        for invoice in self.all_imports:
            if invoice.get('supplier_id') == selected_supplier:
                import_id = invoice.get('import_id', '')
                
                if '.' not in import_id:  # فاتورة أصلية
                    original_import_id = import_id
                    original_invoices[original_import_id] = {
                        'invoice': invoice,
                        'last_payment': invoice  # الفاتورة الأصلية هي آخر سجل افتراضي
                    }
                    if not supplier_name:
                        supplier_name = invoice.get('supplier_name', '')
        
        # البحث عن آخر قسط لكل فاتورة
        for invoice in self.all_imports:
            if invoice.get('supplier_id') == selected_supplier:
                import_id = invoice.get('import_id', '')
                
                if '.' in import_id:  # سجل قسط
                    original_import_id = invoice.get('original_import_id', '')
                    if original_import_id in original_invoices:
                        # استخراج رقم القسط
                        payment_number = self.extract_payment_number(import_id)
                        # استخراج رقم آخر قسط مسجل
                        last_payment_id = original_invoices[original_import_id]['last_payment']['import_id']
                        last_payment_number = self.extract_payment_number(last_payment_id)
                        
                        # إذا كان هذا القسط أحدث
                        if payment_number > last_payment_number:
                            original_invoices[original_import_id]['last_payment'] = invoice
        
        # حساب المتبقي والإجماليات بناءً على آخر قسط
        for original_import_id, data in original_invoices.items():
            # استخدام آخر قسط للحساب
            last_payment = data['last_payment']
            
            # إجمالي المدفوع من آخر قسط
            last_payment_paid = float(last_payment.get('amount_paid', 0))
            total_paid += last_payment_paid
            
            # المتبقي من آخر قسط
            last_payment_remaining = float(last_payment.get('remaining', 0))
            total_remaining += last_payment_remaining
        
        # تحديث ملخص المتبقي
        self.update_remaining_summary()
        
        # عرض النتيجة
        result_text = f"البائع: {supplier_name}\n"
        result_text += f"عدد الفواتير الأصلية: {len(original_invoices)}\n"
        result_text += f"إجمالي المتبقي (من آخر قسط لكل فاتورة): {total_remaining:.2f} ج.م\n"
        result_text += f"إجمالي المدفوع (من آخر قسط لكل فاتورة): {total_paid:.2f} ج.م"
        
        QMessageBox.information(self, "نتيجة الحساب", result_text)
    
    def update_remaining_summary(self):
        """تحديث ملخص المتبقي للبائع المحدد - استخدام نفس قيمة الأسفل"""
        selected_supplier = self.supplier_filter.currentData()
        
        if not selected_supplier:
            self.remaining_sum_label.setText("مجموع المتبقي: 0.00 ج.م")
            self.payment_to_supplier_input.setMaximum(0.0)
            self.add_remaining_input.setMaximum(0.0)
            return
        
        # الحصول على إجمالي المتبقي من الإحصائيات الأخيرة
        total_remaining_text = self.total_remaining_label.text()
        
        # استخراج الرقم من النص "إجمالي المتبقي: XXX.XX ج.م"
        try:
            # إزالة النص وترك الأرقام فقط
            import re
            # البحث عن الرقم (قد يحتوي على فواصل)
            match = re.search(r'([\d,.]+)', total_remaining_text)
            if match:
                # إزالة الفواصل وتحويل إلى float
                number_str = match.group(1).replace(',', '')
                total_remaining = float(number_str)
            else:
                # إذا لم نجد رقماً، استخدم 0
                total_remaining = 0.0
        except ValueError:
            total_remaining = 0.0
        
        # الحصول على اسم البائع
        supplier_name = ""
        for invoice in self.all_imports:
            if invoice.get('supplier_id') == selected_supplier:
                supplier_name = invoice.get('supplier_name', '')
                break
        
        self.remaining_sum_label.setText(f"مجموع المتبقي لـ {supplier_name}: {total_remaining:.2f} ج.م")
        self.payment_to_supplier_input.setMaximum(total_remaining)
        self.add_remaining_input.setMaximum(999999.99)  # السماح بإضافة أي مبلغ للمتبقي
    
    def process_payment(self):
        """معالجة سداد قسط - مع الحفاظ على المتبقي الأصلي ثابتاً"""
        selected = self.table.currentRow()
        if selected >= 0:
            import_id = self.table.item(selected, 0).text()
            invoice = next((inv for inv in self.all_imports if inv['import_id'] == import_id), None)
            
            if not invoice:
                QMessageBox.warning(self, "تحذير", "لم يتم العثور على الفاتورة!")
                return
            
            # تحديد الفاتورة الأصلية
            original_import_id = invoice.get('original_import_id', invoice['import_id'])
            
            # البحث عن الفاتورة الأصلية
            original_invoice = None
            for inv in self.all_imports:
                if inv['import_id'] == original_import_id:
                    original_invoice = inv
                    break
            
            if not original_invoice:
                QMessageBox.warning(self, "تحذير", "لم يتم العثور على الفاتورة الأصلية!")
                return
            
            # حساب المتبقي الإجمالي للفاتورة الأصلية
            # المتبقي الإجمالي = المتبقي في الفاتورة الأصلية - مجموع المدفوع في الأقساط
            total_paid_in_payments = 0
            for inv in self.all_imports:
                if (inv.get('original_import_id') == original_import_id and 
                    inv['import_id'] != original_import_id):  # جميع الأقساط
                    total_paid_in_payments += float(inv.get('amount_paid', 0))
            
            # المتبقي المتبقي للدفع = المتبقي الأصلي - إجمالي المدفوع في الأقساط
            original_remaining = float(original_invoice.get('remaining', 0))
            current_remaining = original_remaining - total_paid_in_payments
            
            if current_remaining <= 0:
                QMessageBox.warning(self, "تحذير", "هذه الفاتورة مدفوعة بالكامل!")
                return
            
            # نافذة سداد القسط
            dialog = QDialog(self)
            dialog.setWindowTitle(f"سداد قسط - فاتورة {original_import_id}")
            dialog.setGeometry(200, 200, 400, 350)
            dialog.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            
            layout = QVBoxLayout()
            
            # معلومات الفاتورة
            info_label = QLabel(
                f"فاتورة أصلية: {original_import_id}\n"
                f"البائع: {original_invoice['supplier_name']}\n"
                f"المتبقي الأصلي: {original_remaining:.2f} ج.م\n"
                f"المدفوع في الأقساط: {total_paid_in_payments:.2f} ج.م\n"
                f"المتبقي المتبقي للدفع: {current_remaining:.2f} ج.م\n"
                f"عدد الأقساط السابقة: {original_invoice.get('payment_count', 0)}"
            )
            info_label.setStyleSheet("font-weight: bold; padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
            layout.addWidget(info_label)
            
            # مبلغ السداد
            layout.addWidget(QLabel("مبلغ السداد:"))
            payment_amount = QDoubleSpinBox()
            payment_amount.setDecimals(2)
            payment_amount.setMinimum(0.01)
            payment_amount.setMaximum(current_remaining)
            payment_amount.setPrefix("ج.م ")
            layout.addWidget(payment_amount)
            
            # تاريخ السداد
            layout.addWidget(QLabel("تاريخ السداد:"))
            payment_date = QDateEdit()
            payment_date.setDate(QDate.currentDate())
            payment_date.setCalendarPopup(True)
            payment_date.setDisplayFormat("yyyy-MM-dd")
            layout.addWidget(payment_date)
            
            # ملاحظات
            layout.addWidget(QLabel("ملاحظات:"))
            payment_notes = QTextEdit()
            payment_notes.setMaximumHeight(60)
            payment_notes.setPlaceholderText("ملاحظات حول السداد...")
            layout.addWidget(payment_notes)
            
            # أزرار
            button_layout = QHBoxLayout()
            
            save_btn = QPushButton("💾 حفظ السداد")
            save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
            """)
            
            def save_payment():
                try:
                    amount = payment_amount.value()
                    date = payment_date.date().toString('yyyy-MM-dd')
                    notes = payment_notes.toPlainText()
                    
                    if amount <= 0:
                        QMessageBox.warning(dialog, "تحذير", "الرجاء إدخال مبلغ صحيح!")
                        return
                    
                    if amount > current_remaining:
                        QMessageBox.warning(dialog, "تحذير", "المبلغ أكبر من المتبقي المتبقي للدفع!")
                        return
                    
                    # حساب رقم القسط التالي
                    payment_count = original_invoice.get('payment_count', 0) + 1
                    
                    # تحديث عدد الدفعات في الفاتورة الأصلية
                    original_invoice['payment_count'] = payment_count
                    
                    # إنشاء ID جديد للمستند المنسوخ
                    new_import_id = f"{original_import_id}.{payment_count}"
                    
                    # التحقق من عدم وجود هذا الرقم مسبقاً
                    existing_ids = {inv['import_id'] for inv in self.all_imports}
                    counter = 1
                    while new_import_id in existing_ids:
                        payment_count += 1
                        new_import_id = f"{original_import_id}.{payment_count}"
                        counter += 1
                        if counter > 100:
                            raise Exception("تعذر إنشاء رقم فاتورة جديد")
                    
                    # إنشاء سجل منسوخ للسداد
                    payment_invoice = original_invoice.copy()
                    payment_invoice['import_id'] = new_import_id
                    payment_invoice['date'] = date
                    payment_invoice['original_import_id'] = original_import_id
                    payment_invoice['payment_amount'] = amount
                    payment_invoice['payment_count'] = payment_count
                    
                    # المدفوع في سجل القسط = المبلغ المدفوع في هذه الدفعة
                    payment_invoice['amount_paid'] = amount
                    
                    # حساب المتبقي المتبقي بعد هذه الدفعة
                    remaining_after_payment = current_remaining - amount
                    payment_invoice['remaining'] = remaining_after_payment
                    
                    # تحديث حالة الدفع لسجل القسط
                    if remaining_after_payment <= 0:
                        payment_invoice['payment_status'] = "مدفوع بالكامل"
                    else:
                        payment_invoice['payment_status'] = "سداد قسط"
                    
                    # إضافة ملاحظات السداد
                    if notes:
                        old_notes = str(payment_invoice.get('notes', ''))
                        if old_notes:
                            payment_invoice['notes'] = f"{old_notes}\nسداد: {amount} ج.م - {date} - {notes}"
                        else:
                            payment_invoice['notes'] = f"سداد: {amount} ج.م - {date} - {notes}"
                    
                    # إضافة سجل القسط إلى القائمة
                    self.all_imports.append(payment_invoice)
                    
                    # إعادة ترتيب الفواتير
                    self.all_imports = self.sort_invoices_hierarchically(self.all_imports)
                    
                    # حفظ التغييرات
                    self.save_all_imports()
                    
                    # تحديث الملخص
                    self.update_remaining_summary()
                    
                    QMessageBox.information(dialog, "نجاح", 
                                        f"تم حفظ السداد بنجاح!\n\n"
                                        f"رقم سجل القسط: {new_import_id}\n"
                                        f"الفاتورة الأصلية: {original_import_id}\n"
                                        f"المبلغ المدفوع: {amount:.2f} ج.م\n"
                                        f"المتبقي المتبقي بعد السداد: {remaining_after_payment:.2f} ج.م")
                    
                    dialog.close()
                    self.load_imports_history()
                    
                except Exception as e:
                    QMessageBox.critical(dialog, "خطأ", f"حدث خطأ أثناء حفظ السداد:\n{str(e)}")
            
            save_btn.clicked.connect(save_payment)
            button_layout.addWidget(save_btn)
            self.update_remaining_summary()
            cancel_btn = QPushButton("إلغاء")
            cancel_btn.clicked.connect(dialog.close)
            button_layout.addWidget(cancel_btn)
            
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec()
    
    def process_bulk_payment(self):
        """معالجة دفع مبلغ للبائع المحدد - العمل على آخر قسط فقط"""
        selected_supplier = self.supplier_filter.currentData()
        
        if not selected_supplier:
            QMessageBox.warning(self, "تحذير", "الرجاء تحديد بائع أولاً!")
            return
        
        payment_amount = self.payment_to_supplier_input.value()
        
        if payment_amount <= 0:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال مبلغ صحيح للدفع!")
            return
        
        # تجميع آخر قسط لكل فاتورة للبائع المحدد
        original_invoices = {}
        supplier_name = ""
        
        # أولاً: تجميع الفواتير الأصلية
        for invoice in self.all_imports:
            if invoice.get('supplier_id') == selected_supplier:
                import_id = invoice.get('import_id', '')
                
                if '.' not in import_id:  # فاتورة أصلية
                    original_import_id = import_id
                    original_invoices[original_import_id] = {
                        'invoice': invoice,
                        'last_payment': invoice  # الفاتورة الأصلية هي آخر سجل افتراضي
                    }
                    if not supplier_name:
                        supplier_name = invoice.get('supplier_name', '')
        
        # ثانياً: البحث عن آخر قسط لكل فاتورة
        for invoice in self.all_imports:
            if invoice.get('supplier_id') == selected_supplier:
                import_id = invoice.get('import_id', '')
                
                if '.' in import_id:  # سجل قسط
                    original_import_id = invoice.get('original_import_id', '')
                    if original_import_id in original_invoices:
                        # استخراج رقم القسط
                        payment_number = self.extract_payment_number(import_id)
                        # استخراج رقم آخر قسط مسجل
                        last_payment_id = original_invoices[original_import_id]['last_payment']['import_id']
                        last_payment_number = self.extract_payment_number(last_payment_id)
                        
                        # إذا كان هذا القسط أحدث
                        if payment_number > last_payment_number:
                            original_invoices[original_import_id]['last_payment'] = invoice
        
        # تحويل إلى قائمة وترتيب حسب التاريخ
        last_payments_list = []
        for original_import_id, data in original_invoices.items():
            last_payment = data['last_payment']
            last_payments_list.append(last_payment)
        
        # ترتيب حسب التاريخ (الأقدم أولاً)
        last_payments_list.sort(key=lambda x: x.get('date', ''))
        
        # توزيع المبلغ على الفواتير بناءً على آخر قسط
        remaining_payment = payment_amount
        payment_records = []
        current_date = QDate.currentDate().toString('yyyy-MM-dd')
        
        for last_payment in last_payments_list:
            if remaining_payment <= 0:
                break
            
            payment_remaining = float(last_payment.get('remaining', 0))
            if payment_remaining <= 0:
                continue
            
            # حساب المبلغ المدفوع لهذه الفاتورة
            amount_to_pay = min(remaining_payment, payment_remaining)
            
            # الحصول على الفاتورة الأصلية
            original_import_id = last_payment.get('original_import_id', last_payment['import_id'])
            original_invoice = None
            for inv in self.all_imports:
                if inv['import_id'] == original_import_id:
                    original_invoice = inv
                    break
            
            if not original_invoice:
                continue
            
            # حساب رقم القسط التالي
            payment_count = original_invoice.get('payment_count', 0) + 1
            
            # تحديث عدد الدفعات في الفاتورة الأصلية
            original_invoice['payment_count'] = payment_count
            
            # إنشاء سجل القسط الجديد
            new_import_id = f"{original_import_id}.{payment_count}"
            new_payment_invoice = original_invoice.copy()
            new_payment_invoice['import_id'] = new_import_id
            new_payment_invoice['date'] = current_date
            new_payment_invoice['original_import_id'] = original_import_id
            new_payment_invoice['payment_amount'] = amount_to_pay
            new_payment_invoice['payment_count'] = payment_count
            new_payment_invoice['amount_paid'] = amount_to_pay
            
            # حساب المتبقي الجديد
            new_remaining = payment_remaining - amount_to_pay
            new_payment_invoice['remaining'] = new_remaining
            
            # تحديث حالة الدفع
            if new_remaining <= 0:
                new_payment_invoice['payment_status'] = "مدفوع بالكامل"
            else:
                new_payment_invoice['payment_status'] = "سداد قسط"
            
            # إضافة ملاحظات
            new_payment_invoice['notes'] = f"دفع جماعي للبائع: {amount_to_pay} ج.م - {current_date}"
            
            # تسجيل عملية الدفع
            payment_records.append({
                'original_invoice': original_invoice,
                'new_payment_invoice': new_payment_invoice,
                'amount_paid': amount_to_pay,
                'new_remaining': new_remaining
            })
            
            # إضافة سجل القسط الجديد
            self.all_imports.append(new_payment_invoice)
            
            remaining_payment -= amount_to_pay
        
        # إعادة ترتيب الفواتير
        self.all_imports = self.sort_invoices_hierarchically(self.all_imports)
        
        # حفظ التغييرات
        self.save_all_imports()
        
        # إعادة تعيين حقل الدفع
        self.payment_to_supplier_input.setValue(0.0)
        
        # عرض ملخص الدفع
        summary = f"تم توزيع المبلغ على فواتير البائع:\n\n"
        summary += f"البائع: {supplier_name}\n"
        summary += f"المبلغ المدفوع: {payment_amount:.2f} ج.م\n"
        summary += f"عدد الفواتير المدفوعة: {len(payment_records)}\n\n"
        
        if remaining_payment > 0:
            summary += f"ملاحظة: لم يتم استخدام {remaining_payment:.2f} ج.م لأن المبلغ أكبر من إجمالي المتبقي\n\n"
        
        for i, record in enumerate(payment_records, 1):
            original_invoice = record['original_invoice']
            summary += f"{i}. فاتورة {original_invoice['import_id']}: {record['amount_paid']:.2f} ج.م (متبقي بعد الدفع: {record['new_remaining']:.2f} ج.م)\n"
        
        QMessageBox.information(self, "ملخص الدفع", summary)
        
        # إعادة تحميل البيانات
        self.load_imports_history()
        self.update_remaining_summary()
    
    def add_to_remaining(self):
        """إضافة مبلغ للمتبقي للبائع المحدد"""
        selected_supplier = self.supplier_filter.currentData()
        
        if not selected_supplier:
            QMessageBox.warning(self, "تحذير", "الرجاء تحديد بائع أولاً!")
            return
        
        add_amount = self.add_remaining_input.value()
        
        if add_amount <= 0:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال مبلغ صحيح للإضافة!")
            return
        
        # الحصول على اسم البائع
        supplier_name = ""
        for invoice in self.all_imports:
            if invoice.get('supplier_id') == selected_supplier:
                supplier_name = invoice.get('supplier_name', '')
                break
        
        # إنشاء فاتورة جديدة للمتبقي (رصيد غير مسجل)
        current_date = QDate.currentDate().toString('yyyy-MM-dd')
        
        # إنشاء ID فريد للمتبقي
        import_id = f"REM_{int(time.time() % 10000)}"
        
        # إنشاء فاتورة المتبقي
        remaining_invoice = {
            'import_id': import_id,
            'supplier_id': selected_supplier,
            'supplier_name': supplier_name,
            'date': current_date,
            'due_date': current_date,
            'products': [{
                'name': 'رصيد غير مسجل',
                'size': '',
                'buying_price': add_amount,
                'quantity': 1
            }],
            'total': add_amount,
            'selling_total': add_amount,
            'previous_balance': 0.0,
            'total_cumulative': add_amount,
            'amount_paid': 0.0,
            'remaining': add_amount,
            'payment_status': 'لم يدفع',
            'notes': f'إضافة للمتبقي: {add_amount:.2f} ج.م - {current_date}',
            'original_import_id': import_id,
            'payment_count': 0,
            'payment_amount': 0.0
        }
        
        # إضافة الفاتورة الجديدة
        self.all_imports.append(remaining_invoice)
        
        # إعادة ترتيب الفواتير
        self.all_imports = self.sort_invoices_hierarchically(self.all_imports)
        
        # حفظ التغييرات
        self.save_all_imports()
        
        # إعادة تعيين حقل الإضافة
        self.add_remaining_input.setValue(0.0)
        
        # عرض رسالة نجاح
        QMessageBox.information(self, "نجاح الإضافة", 
                              f"تم إضافة مبلغ للمتبقي بنجاح!\n\n"
                              f"البائع: {supplier_name}\n"
                              f"المبلغ المضاف: {add_amount:.2f} ج.م\n"
                              f"رقم الفاتورة: {import_id}\n"
                              f"التاريخ: {current_date}")
        
        # إعادة تحميل البيانات
        self.load_imports_history()
        self.update_remaining_summary()  # <-- إضافة هذا إذا لم يكن موجوداً

    def toggle_edit_mode(self):
        """تفعيل/تعطيل وضع التعديل"""
        self.is_editing = not self.is_editing
        
        if self.is_editing:
            # تفعيل وضع التعديل
            self.table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | 
                                     QAbstractItemView.EditTrigger.EditKeyPressed)
            
            # تمكين تحرير الأعمدة المحددة فقط
            for row in range(self.table.rowCount()):
                # السماح بتعديل المدفوع والمتبقي فقط
                for col in [6, 7]:  # المدفوع والمتبقي
                    item = self.table.item(row, col)
                    if item:
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            
            QMessageBox.information(self, "وضع التعديل", 
                                  "تم تفعيل وضع التعديل\n\n"
                                  "يمكنك الآن تعديل قيم المدفوع والمتبقي\n"
                                  "سيتم حفظ التغييرات عند الضغط على زر الحفظ")
        else:
            # تعطيل وضع التعديل
            self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            
            QMessageBox.information(self, "وضع التعديل", "تم تعطيل وضع التعديل")
    
    def add_new_invoice(self):
        """إضافة فاتورة جديدة"""
        self.create_window = CreateImportWindow(self.db)
        self.create_window.show()
        self.close()
    
    def delete_selected_invoice(self):
        """حذف الفاتورة المحددة"""
        selected = self.table.currentRow()
        if selected >= 0:
            import_id = self.table.item(selected, 0).text()
            invoice = next((inv for inv in self.all_imports if inv['import_id'] == import_id), None)
            
            if not invoice:
                QMessageBox.warning(self, "خطأ", "لم يتم العثور على الفاتورة!")
                return
            
            supplier_name = invoice.get('supplier_name', 'غير معروف')
            
            # التحقق إذا كانت فاتورة سداد
            if '.' in import_id:
                original_id = import_id.split('.')[0]
                reply = QMessageBox.question(self, "تأكيد الحذف",
                                           f"هل أنت متأكد من حذف سجل السداد هذا؟\n\n"
                                           f"رقم الفاتورة: {import_id}\n"
                                           f"البائع: {supplier_name}\n\n"
                                           f"ملاحظة: هذا سجل سداد للفاتورة الأصلية {original_id}",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    # حذف سجل السداد فقط
                    self.all_imports = [inv for inv in self.all_imports if inv['import_id'] != import_id]
                    
                    # حفظ التغييرات
                    self.save_all_imports()
                    
                    QMessageBox.information(self, "نجاح", "تم حذف سجل السداد بنجاح!")
                    self.load_imports_history()
            else:
                # فاتورة أصلية - التحقق من وجود أقساط
                has_payments = any(inv for inv in self.all_imports 
                                 if inv.get('original_import_id') == import_id and inv['import_id'] != import_id)
                
                if has_payments:
                    reply = QMessageBox.question(self, "تأكيد الحذف",
                                               f"تحذير: هذه الفاتورة لها سجلات سداد مرتبطة بها!\n\n"
                                               f"رقم الفاتورة: {import_id}\n"
                                               f"البائع: {supplier_name}\n\n"
                                               f"هل تريد حذف الفاتورة وسجلات السداد المرتبطة بها؟",
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        # حذف الفاتورة الأصلية وجميع سجلات السداد المرتبطة بها
                        self.all_imports = [inv for inv in self.all_imports 
                                          if inv.get('original_import_id') != import_id]
                        
                        # حفظ التغييرات
                        self.save_all_imports()
                        
                        QMessageBox.information(self, "نجاح", "تم حذف الفاتورة وسجلات السداد المرتبطة بها بنجاح!")
                        self.load_imports_history()
                else:
                    reply = QMessageBox.question(self, "تأكيد الحذف",
                                               f"هل أنت متأكد من حذف فاتورة الاستيراد؟\n\n"
                                               f"رقم الفاتورة: {import_id}\n"
                                               f"البائع: {supplier_name}",
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        # حذف الفاتورة الأصلية فقط
                        self.all_imports = [inv for inv in self.all_imports if inv['import_id'] != import_id]
                        
                        # حفظ التغييرات
                        self.save_all_imports()
                        
                        QMessageBox.information(self, "نجاح", "تم حذف الفاتورة بنجاح!")
                        self.load_imports_history()
    
    def save_changes(self):
        """حفظ جميع التغييرات"""
        try:
            if self.is_editing:
                # تحديث البيانات من الجدول
                for row in range(self.table.rowCount()):
                    import_id = self.table.item(row, 0).text()
                    invoice = next((inv for inv in self.all_imports if inv['import_id'] == import_id), None)
                    
                    if invoice:
                        try:
                            # تحديث المدفوع
                            paid_text = self.table.item(row, 6).text().replace(" ج.م", "").strip()
                            new_paid = float(paid_text)
                            
                            # تحديث المتبقي
                            remaining_text = self.table.item(row, 7).text().replace(" ج.م", "").strip()
                            new_remaining = float(remaining_text)
                            
                            # حساب الفرق في المدفوع
                            old_paid = float(invoice.get('amount_paid', 0))
                            payment_diff = new_paid - old_paid
                            
                            if payment_diff != 0:
                                # تحديث المبلغ المدفوع في هذه الفاتورة
                                invoice['amount_paid'] = new_paid
                                invoice['remaining'] = new_remaining
                                
                                # تحديث حالة الدفع
                                if new_remaining <= 0:
                                    invoice['payment_status'] = "مدفوع بالكامل"
                                elif new_paid > 0:
                                    invoice['payment_status'] = "سداد قسط"
                                else:
                                    invoice['payment_status'] = "غير مدفوع"
                                    
                        except (ValueError, AttributeError):
                            continue
                
                # تعطيل وضع التعديل
                self.is_editing = False
                self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            
            # حفظ التغييرات في الملف
            self.save_all_imports()
            
            QMessageBox.information(self, "نجاح", "تم حفظ جميع التغييرات بنجاح!")
            self.load_imports_history()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ:\n{str(e)}")
    
    def save_all_imports(self):
        """حفظ جميع فواتير الاستيراد في ملف CSV"""
        imports_file = "imports_history.csv"
        
        if not self.all_imports:
            # إذا كانت القائمة فارغة، إنشاء ملف فارغ
            fieldnames = [
                'import_id', 'supplier_id', 'supplier_name', 'supplier_phone',
                'supplier_address', 'date', 'due_date', 'products', 'total',
                'selling_total', 'previous_balance', 'total_cumulative',
                'amount_paid', 'remaining', 'payment_status', 'notes',
                'original_import_id', 'payment_count', 'payment_amount'
            ]
            
            with open(imports_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        # تحضير البيانات للحفظ
        imports_to_save = []
        for invoice in self.all_imports:
            invoice_copy = invoice.copy()
            if 'products' in invoice_copy and isinstance(invoice_copy['products'], list):
                invoice_copy['products'] = json.dumps(invoice_copy['products'], ensure_ascii=False)
            
            # التأكد من وجود الحقول المطلوبة وتحويلها إلى النوع الصحيح
            if 'payment_amount' not in invoice_copy:
                invoice_copy['payment_amount'] = 0.0
            
            if 'payment_count' not in invoice_copy:
                invoice_copy['payment_count'] = 0
            elif isinstance(invoice_copy['payment_count'], str):
                try:
                    invoice_copy['payment_count'] = int(invoice_copy['payment_count'])
                except ValueError:
                    invoice_copy['payment_count'] = 0
            
            imports_to_save.append(invoice_copy)
        
        # الحقول
        fieldnames = [
            'import_id', 'supplier_id', 'supplier_name', 'supplier_phone',
            'supplier_address', 'date', 'due_date', 'products', 'total',
            'selling_total', 'previous_balance', 'total_cumulative',
            'amount_paid', 'remaining', 'payment_status', 'notes',
            'original_import_id', 'payment_count', 'payment_amount'
        ]
        
        with open(imports_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(imports_to_save)
                               

import os
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import csv
import json

class CreateReceiptWindow(QWidget):
    """إنشاء فاتورة محسّن مع نظام الأقساط"""
    
    def __init__(self, db, items_manager=None):
        super().__init__()
        self.db = db
        self.items_manager = items_manager  # إضافة مرجع إلى مدير المخزون
        self.current_step = 1
        self.cart_items = []
        self.current_customer_id = None
        self.current_customer_name = None
        self.current_representative_id = None
        self.customer_address = ""
        self.due_date = ""
        self.customer_notes = ""
        self.customer_previous_balance = 0
        self.current_total = 0
        self.total_paid_now = 0
        self.total_cumulative = 0
        self.total_remaining = 0
        self.current_balance = 0
        self.preview_receipt_data = None
        
        # ✅ نظام الجدول الافتراضي
        self.virtual_table = None  # النسخة الافتراضية من المخزون
        self.virtual_table_changes = {}  # تعقب التغييرات في الجدول الافتراضي
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('إنشاء فاتورة')
        self.setMinimumSize(900, 650)  # زيادة الحجم ليكون مثل CreateImportWindow
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.layout = QVBoxLayout()
        
        # مؤشر الخطوة
        self.step_label = QLabel("الخطوة 1: معلومات العميل")
        self.step_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db; padding: 10px;")
        self.layout.addWidget(self.step_label)
        
        # الخطوات
        self.stacked_widget = QStackedWidget()
        
        self.step1_widget = self.create_step1()
        self.stacked_widget.addWidget(self.step1_widget)
        
        self.step2_widget = self.create_step2()
        self.stacked_widget.addWidget(self.step2_widget)
        
        self.step3_widget = self.create_step3()  # الخطوة الجديدة للمدفوعات
        self.stacked_widget.addWidget(self.step3_widget)
        
        self.step4_widget = self.create_step4()  # تأكيد الفاتورة
        self.stacked_widget.addWidget(self.step4_widget)
        
        self.layout.addWidget(self.stacked_widget)
        
        # أزرار التنقل
        nav_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("→ السابق")
        self.prev_btn.clicked.connect(self.prev_step)
        self.prev_btn.setEnabled(False)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        nav_layout.addWidget(self.prev_btn)
        
        nav_layout.addStretch()
        
        self.next_btn = QPushButton("التالي ←")
        self.next_btn.clicked.connect(self.next_step)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        nav_layout.addWidget(self.next_btn)
        
        self.layout.addLayout(nav_layout)
        self.setLayout(self.layout)
    
    def create_step1(self):
        """الخطوة 1: معلومات العميل مع الحقول الجديدة"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # الكود / العميل
        customer_layout = QHBoxLayout()
        customer_layout.addWidget(QLabel("الكود / العميل:"))
        self.customer_code_input = QLineEdit()
        self.customer_code_input.setPlaceholderText("كود العميل")
        self.customer_code_input.setFixedWidth(100)
        customer_layout.addWidget(self.customer_code_input)
        
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("اسم العميل")
        self.customer_name_input.textChanged.connect(self.check_customer_existence)
        customer_layout.addWidget(self.customer_name_input)
        
        # زر البحث في العملاء
        search_btn = QPushButton("🔍")
        search_btn.setToolTip("البحث عن العميل في السجلات")
        search_btn.setFixedWidth(40)
        search_btn.clicked.connect(self.search_customer_in_history)
        customer_layout.addWidget(search_btn)
        
        customer_layout.addStretch()
        form_layout.addRow(customer_layout)
        
        # العنوان
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("عنوان العميل")
        form_layout.addRow("العنوان:", self.address_input)
        
        # الملاحظات
        self.notes_input_step1 = QTextEdit()
        self.notes_input_step1.setMaximumHeight(80)
        self.notes_input_step1.setPlaceholderText("ملاحظات إضافية...")
        form_layout.addRow("ملاحظات:", self.notes_input_step1)
        
        # التاريخ
        date_layout = QHBoxLayout()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.date_input)
        
        now_btn = QPushButton("الآن")
        now_btn.clicked.connect(lambda: self.date_input.setDate(QDate.currentDate()))
        now_btn.setFixedWidth(60)
        date_layout.addWidget(now_btn)
        date_layout.addStretch()
        form_layout.addRow("التاريخ:", date_layout)
        
        # نتيجة البحث عن العميل
        self.customer_info_label = QLabel("")
        self.customer_info_label.setStyleSheet("""
            color: #2c3e50; 
            font-weight: bold; 
            padding: 5px; 
            border-radius: 3px;
            background-color: #1f262d;
        """)
        form_layout.addRow("", self.customer_info_label)
        
        # ملاحظة
        note_label = QLabel("ملاحظة: عند إدخال اسم عميل موجود سابقاً، سيتم جلب بياناته تلقائياً")
        note_label.setStyleSheet("color: #7f8c8d; font-size: 11px; font-style: italic;")
        form_layout.addRow("", note_label)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_step2(self):
        """الخطوة 2: اختيار المنتجات مع سعر البيع التلقائي - معدل ليشبه CreateImportWindow"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # اختيار المنتج مع فلترة المقاس (مثل CreateImportWindow)
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # إضافة خانة اختيار/بحث المقاس
        size_search_layout = QHBoxLayout()
        size_search_layout.addWidget(QLabel("اختر/ابحث بالمقاس:"))
        
        self.size_filter_combo = QComboBox()
        self.size_filter_combo.setEditable(True)
        self.size_filter_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.load_sizes_combo()
        self.size_filter_combo.currentTextChanged.connect(self.filter_items_by_size)
        self.size_filter_combo.lineEdit().setPlaceholderText("اكتب للبحث أو اختر من القائمة")
        size_search_layout.addWidget(self.size_filter_combo)
        
        size_search_btn = QPushButton("🔍")
        size_search_btn.setToolTip("بحث في المقاسات")
        size_search_btn.setMaximumWidth(30)
        size_search_btn.clicked.connect(lambda: self.search_in_combo(self.size_filter_combo))
        size_search_layout.addWidget(size_search_btn)
        form_layout.addRow(size_search_layout)
        
        # إضافة خانة اختيار/بحث المنتج
        item_search_layout = QHBoxLayout()
        item_search_layout.addWidget(QLabel("اختر/ابحث بالمنتج:"))
        
        self.item_combo = QComboBox()
        self.item_combo.setEditable(True)
        self.item_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.load_items_combo()
        self.item_combo.lineEdit().setPlaceholderText("اكتب للبحث أو اختر من القائمة")
        self.item_combo.currentIndexChanged.connect(self.auto_fill_selling_price_on_select)
        item_search_layout.addWidget(self.item_combo)
        
        item_search_btn = QPushButton("🔍")
        item_search_btn.setToolTip("بحث في المنتجات")
        item_search_btn.setMaximumWidth(30)
        item_search_btn.clicked.connect(lambda: self.search_in_combo(self.item_combo))
        item_search_layout.addWidget(item_search_btn)
        form_layout.addRow(item_search_layout)
        
        # الكمية
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(999)
        form_layout.addRow("الكمية:", self.quantity_spin)
        
        # سعر البيع فقط (تم إزالة سعر الشراء) مع زر ملء تلقائي
        selling_price_layout = QHBoxLayout()
        selling_price_layout.addWidget(QLabel("سعر البيع:"))
        
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setDecimals(2)
        self.selling_price_input.setMinimum(0.0)
        self.selling_price_input.setMaximum(999999.99)
        self.selling_price_input.setPrefix("ج.م ")  # ✅ تم إرجاع "ج.م"
        selling_price_layout.addWidget(self.selling_price_input)
        
        # زر ملء تلقائي
        auto_fill_btn = QPushButton("ملء تلقائي")
        auto_fill_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        auto_fill_btn.clicked.connect(self.auto_fill_selling_price_from_btn)
        selling_price_layout.addWidget(auto_fill_btn)
        form_layout.addRow(selling_price_layout)
        
        add_btn = QPushButton("إضافة للسلة")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        add_btn.clicked.connect(self.add_to_cart)
        form_layout.addRow("", add_btn)
        
        layout.addLayout(form_layout)
        
        # عرض السلة
        layout.addWidget(QLabel("المنتجات في السلة:"))
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(7)
        self.cart_table.setHorizontalHeaderLabels(["الرقم", "الصنف", "المقاس", "الكمية", "سعر البيع", "الإجمالي شراء", "الإجمالي بيع"])
        self.cart_table.setAlternatingRowColors(True)
        
        # تغيير خلفية جدول السلة
        self.cart_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1f24;
                alternate-background-color: #202427;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white ;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #2b2f30;
                border-bottom: 1px solid #2b2f300;
            }
            QTableWidget::item:hover {
                background-color: #2b2f30;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """)
        layout.addWidget(self.cart_table)
        
        # إجمالي السلة (على أساس سعر البيع فقط)
        self.cart_total_label = QLabel("إجمالي السلة (بيع):")
        self.cart_total_label.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 16px; background-color: #2c3e50; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.cart_total_label)
        
        # زر الحذف
        remove_btn = QPushButton("حذف المحدد")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        remove_btn.clicked.connect(self.remove_from_cart)
        layout.addWidget(remove_btn)
        
        widget.setLayout(layout)
        return widget
    
    # ✅ دالة جديدة: إنشاء الجدول الافتراضي
    def create_virtual_table(self):
        """إنشاء نسخة افتراضية من جدول المخزون"""
        try:
            if self.items_manager:
                # استلام نسخة من جدول المخزون الحقيقي
                self.virtual_table = self.items_manager.get_virtual_table()
                self.virtual_table_changes = {}
                return True
            else:
                # بديل: جلب البيانات مباشرة من قاعدة البيانات
                self.virtual_table = self.db.load_items()
                self.virtual_table_changes = {}
                return True
        except Exception as e:
            print(f"خطأ في إنشاء الجدول الافتراضي: {e}")
            return False
    
    # ✅ دالة جديدة: تحديث الكمية في الجدول الافتراضي
    def update_virtual_quantity(self, item_id, quantity_to_deduct):
        """
        تحديث الكمية في الجدول الافتراضي
        quantity_to_deduct: الكمية المطلوب خصمها (تكون سالبة للخصم)
        """
        try:
            if not self.virtual_table:
                return False
            
            # البحث عن العنصر في الجدول الافتراضي
            for item in self.virtual_table:
                if str(item.get('item_id', '')) == str(item_id):
                    current_qty = item.get('quantity', 0)
                    new_qty = current_qty - quantity_to_deduct  # نخصم الكمية المضافة للسلة
                    
                    # التأكد من أن الكمية لا تكون سالبة
                    if new_qty < 0:
                        new_qty = 0
                    
                    # تحديث الكمية في الجدول الافتراضي
                    item['quantity'] = new_qty
                    
                    # تسجيل التغيير
                    key = f"{item.get('name')}_{item.get('size')}"
                    if key in self.virtual_table_changes:
                        self.virtual_table_changes[key] -= quantity_to_deduct
                    else:
                        self.virtual_table_changes[key] = -quantity_to_deduct
                    
                    return True
            return False
        except Exception as e:
            print(f"خطأ في تحديث الكمية الافتراضية: {e}")
            return False
    
    # ✅ دالة جديدة: استعادة الكمية في الجدول الافتراضي
    def restore_virtual_quantity(self, item_id, quantity_to_restore):
        """
        استعادة الكمية في الجدول الافتراضي عند إزالة عنصر من السلة
        """
        try:
            if not self.virtual_table:
                return False
            
            # البحث عن العنصر في الجدول الافتراضي
            for item in self.virtual_table:
                if str(item.get('item_id', '')) == str(item_id):
                    current_qty = item.get('quantity', 0)
                    new_qty = current_qty + quantity_to_restore
                    
                    # تحديث الكمية في الجدول الافتراضي
                    item['quantity'] = new_qty
                    
                    # تحديث سجل التغييرات
                    key = f"{item.get('name')}_{item.get('size')}"
                    if key in self.virtual_table_changes:
                        self.virtual_table_changes[key] += quantity_to_restore
                        if self.virtual_table_changes[key] == 0:
                            del self.virtual_table_changes[key]
                    
                    return True
            return False
        except Exception as e:
            print(f"خطأ في استعادة الكمية الافتراضية: {e}")
            return False
    
    # ✅ دالة جديدة: الحصول على الكمية المتاحة من الجدول الافتراضي
    def get_virtual_quantity(self, item_name, item_size):
        """الحصول على الكمية المتاحة من الجدول الافتراضي"""
        try:
            if not self.virtual_table:
                return 0
            
            for item in self.virtual_table:
                if (item.get('name', '') == item_name and 
                    item.get('size', '') == item_size):
                    return item.get('quantity', 0)
            return 0
        except Exception as e:
            print(f"خطأ في الحصول على الكمية الافتراضية: {e}")
            return 0
    
    # ✅ دالة جديدة: إعادة تعيين الجدول الافتراضي عند الإلغاء
    def reset_virtual_table(self):
        """إعادة تعيين الجدول الافتراضي"""
        self.virtual_table = None
        self.virtual_table_changes = {}
    
    def check_customer_existence(self):
        """التحقق من وجود العميل في السجلات وتحديث الحقول"""
        customer_name = self.customer_name_input.text().strip()
        
        if not customer_name:
            self.customer_info_label.setText("")
            self.customer_info_label.setStyleSheet("""
                padding: 5px; 
                border-radius: 3px;
                font-size: 12px;
                min-height: 40px;
            """)
            return
        
        try:
            # ✅ استخدام الدالة البسيطة الجديدة
            customer_total_remaining = self.get_customer_true_remaining(customer_name)
            
            # حساب عدد الفواتير الأصلية
            history = self.db.load_history()
            invoice_count = 0
            for invoice in history:
                if invoice.get('customer_name', '').strip().lower() == customer_name.lower():
                    receipt_id = invoice.get('receipt_id', '')
                    if '.' not in receipt_id or receipt_id.startswith('REM_'):
                        invoice_count += 1
            
            if invoice_count == 0:
                # العميل جديد غير مسجل
                self.customer_info_label.setText("<span style='color: #27ae60; font-weight: bold;'>⚠ عميل جديد - غير مسجل مسبقاً</span>")
                self.customer_info_label.setStyleSheet("""
                    background-color: #e8f8f5;
                    color: #27ae60;
                    padding: 8px;
                    border-radius: 5px;
                    border: 1px solid #27ae60;
                    font-weight: bold;
                    font-size: 12px;
                    min-height: 40px;
                """)
                
                # اقتراح كود تلقائي للعميل الجديد
                self.generate_customer_code(customer_name)
                
            else:
                # تحديث حقل الكود إذا وجدنا معرف موجود للعميل
                customer_id = None
                for invoice in history:
                    if invoice.get('customer_name', '').strip().lower() == customer_name.lower():
                        customer_id = invoice.get('customer_id', '')
                        if customer_id:
                            break
                
                if customer_id:
                    self.customer_code_input.setText(customer_id)
                
                # العميل موجود - نحدد نوعه بناءً على الرصيد
                if customer_total_remaining > 0:
                    # عميل له رصيد
                    self.customer_info_label.setText(
                        f"<span style='color: #e74c3c; font-weight: bold;'>✅ العميل مسجل</span><br>"
                        f"<span style='color: #c0392b;'>المتبقي السابق: {customer_total_remaining:.2f} ج.م | عدد الفواتير: {invoice_count}</span>"
                    )
                    self.customer_info_label.setStyleSheet("""
                        background-color: #ffeaea;
                        color: #e74c3c;
                        padding: 8px;
                        border-radius: 5px;
                        border: 1px solid #e74c3c;
                        font-weight: bold;
                        font-size: 12px;
                        min-height: 40px;
                    """)
                else:
                    # عميل مسجل بدون رصيد
                    self.customer_info_label.setText(
                        f"<span style='color: #2980b9; font-weight: bold;'>✅ العميل مسجل</span><br>"
                        f"<span style='color: #1c5a7a;'>لا يوجد متبقي سابق | عدد الفواتير: {invoice_count}</span>"
                    )
                    self.customer_info_label.setStyleSheet("""
                        background-color: #e8f4fc;
                        color: #2980b9;
                        padding: 8px;
                        border-radius: 5px;
                        border: 1px solid #2980b9;
                        font-weight: bold;
                        font-size: 12px;
                        min-height: 40px;
                    """)
                    
        except Exception as e:
            # في حالة حدوث خطأ
            self.customer_info_label.setText(f"<span style='color: #e74c3c;'>خطأ في التحقق: {str(e)[:50]}...</span>")
            self.customer_info_label.setStyleSheet("""
                background-color: #ffeaea;
                color: #e74c3c;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #e74c3c;
                font-weight: bold;
                font-size: 12px;
                min-height: 40px;
            """)
    
    def generate_customer_code(self, customer_name):
        """توليد كود تلقائي للعميل الجديد"""
        try:
            # ✅ لا نولد كوداً إذا كان هناك كود مكتوب بالفعل
            if self.customer_code_input.text().strip():
                return
            
            # ✅ لا نولد كوداً إذا كان العميل موجوداً بالفعل في السجلات
            customer_name_text = self.customer_name_input.text().strip()
            if not customer_name_text:
                return
            
            # التحقق من وجود العميل في السجلات
            history = self.db.load_history()
            if history:
                for record in history:
                    if record.get('customer_name', '').strip().lower() == customer_name_text.lower():
                        # إذا كان العميل موجوداً، استخدم كوده الموجود
                        if record.get('customer_id'):
                            self.customer_code_input.setText(record.get('customer_id'))
                        return
            
            # ✅ فقط للعملاء الجدد حقاً، نولد كوداً جديداً
            if not history:
                # إذا لم توجد سجلات، نستخدم C1001 كبداية
                new_code = "C1001"
            else:
                # البحث عن أعلى كود عميل موجود
                max_code_num = 0
                for record in history:
                    customer_id = str(record.get('customer_id', '')).strip()
                    if customer_id.startswith('C'):
                        try:
                            # استخراج الرقم من الكود CXXXX
                            num_part = customer_id[1:]
                            num = int(num_part)
                            if num > max_code_num:
                                max_code_num = num
                        except:
                            continue
                
                new_code = f"C{max_code_num + 1:04d}"
            
            self.customer_code_input.setText(new_code)
            
        except Exception as e:
            print(f"خطأ في توليد الكود: {e}")
    
    def search_customer_in_history(self):
        """البحث عن العميل في سجل المبيعات"""
        dialog = QDialog(self)
        dialog.setWindowTitle("البحث عن العميل")
        dialog.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("اكتب اسم العميل للبحث:"))
        search_input = QLineEdit()
        layout.addWidget(search_input)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["اسم العميل", "الكود", "آخر فاتورة", "المتبقي"])
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #1f2327;
                alternate-background-color: #272a2d;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """)
        layout.addWidget(table)
        
        def search_customers():
            search_text = search_input.text().strip().lower()
            table.setRowCount(0)
            
            history = self.db.load_history()
            
            # تجميع العملاء الفريدين
            customers_dict = {}
            for invoice in history:
                customer_name = invoice.get('customer_name', '').strip()
                customer_id = invoice.get('customer_id', '')
                
                if not customer_name:
                    continue
                
                if search_text and search_text not in customer_name.lower():
                    continue
                
                if customer_name not in customers_dict:
                    customers_dict[customer_name] = {
                        'id': customer_id,
                        'phone': invoice.get('customer_phone', ''),
                        'last_invoice': invoice.get('date', ''),
                        'remaining': float(invoice.get('remaining', 0))
                    }
                else:
                    # تحديث آخر فاتورة وأكبر متبقي
                    if invoice.get('date', '') > customers_dict[customer_name]['last_invoice']:
                        customers_dict[customer_name]['last_invoice'] = invoice.get('date', '')
                    
                    # جمع المتبقي من جميع الفواتير
                    customers_dict[customer_name]['remaining'] += float(invoice.get('remaining', 0))
        
            # عرض النتائج
            table.setRowCount(len(customers_dict))
            for i, (name, data) in enumerate(customers_dict.items()):
                table.setItem(i, 0, QTableWidgetItem(name))
                table.setItem(i, 1, QTableWidgetItem(data['id']))
                table.setItem(i, 2, QTableWidgetItem(data['last_invoice']))
                table.setItem(i, 3, QTableWidgetItem(f"{data['remaining']:.2f} ج.م"))
        
        search_input.textChanged.connect(search_customers)
        search_customers()
        
        def select_customer():
            selected = table.currentRow()
            if selected >= 0:
                customer_name = table.item(selected, 0).text()
                customer_id = table.item(selected, 1).text()
                
                self.customer_name_input.setText(customer_name)
                self.customer_code_input.setText(customer_id)
                self.check_customer_existence()
                dialog.close()
        
        select_btn = QPushButton("تحديد")
        select_btn.clicked.connect(select_customer)
        layout.addWidget(select_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def auto_fill_selling_price_on_select(self):
        """ملء سعر البيع تلقائياً عند اختيار المنتج"""
        try:
            item_data = self.item_combo.currentData()
            if item_data:
                selling_price = item_data.get('selling_price', 0.0)
                # ملء السعر تلقائياً عند اختيار منتج جديد
                self.selling_price_input.setValue(selling_price)
        except Exception as e:
            print(f"خطأ في ملء السعر التلقائي: {e}")
    
    def auto_fill_selling_price_from_btn(self):
        """ملء سعر البيع من زر التعبئة التلقائية"""
        try:
            item_data = self.item_combo.currentData()
            if item_data:
                selling_price = item_data.get('selling_price', 0.0)
                self.selling_price_input.setValue(selling_price)
                QMessageBox.information(self, "تم", "تم ملء سعر البيع من المخزن")
        except Exception as e:
            print(f"خطأ في ملء السعر من الزر: {e}")
    
    def load_sizes_combo(self):
        """تحميل المقاسات الفريدة"""
        try:
            all_items = self.db.load_items()
            self.size_filter_combo.clear()
            
            unique_sizes = set()
            for item in all_items:
                size = item.get('size', '').strip()
                if size:
                    unique_sizes.add(size)
            
            self.size_filter_combo.addItem("جميع المقاسات")
            for size in sorted(unique_sizes):
                self.size_filter_combo.addItem(size)
            
            self.size_filter_combo.setCurrentIndex(0)
            
        except Exception as e:
            print(f"خطأ في تحميل المقاسات: {e}")
    
    def load_items_combo(self):
        """تحميل المنتجات في الكومبو مع الكميات من الجدول الافتراضي"""
        try:
            items = self.virtual_table if self.virtual_table else self.db.load_items()
            self.item_combo.clear()
            
            if not items:
                self.item_combo.addItem("لا توجد منتجات في المخزون", None)
                return
            
            for item in items:
                name = item.get('name', 'غير معروف')
                size = item.get('size', '')
                buying_price = item.get('buying_price', 0.0)
                selling_price = item.get('selling_price', 0.0)
                quantity = item.get('quantity', 0)
                
                # ✅ تحديث: عرض الكمية من الجدول الافتراضي
                display_text = f"{name} ({size}) - شراء: {buying_price} ج.م - بيع: {selling_price} ج.م - متوفر: {quantity}"
                self.item_combo.addItem(display_text, item)
            
            if self.item_combo.count() > 0:
                self.item_combo.setCurrentIndex(0)
                
        except Exception as e:
            print(f"خطأ في تحميل المنتجات: {e}")
    
    def filter_items_by_size(self, selected_size):
        """فلترة المنتجات حسب المقاس"""
        try:
            items = self.virtual_table if self.virtual_table else self.db.load_items()
            self.item_combo.clear()
            
            if selected_size == "جميع المقاسات" or not selected_size:
                # عرض جميع المنتجات
                for item in items:
                    name = item.get('name', 'غير معروف')
                    size = item.get('size', '')
                    buying_price = item.get('buying_price', 0.0)
                    selling_price = item.get('selling_price', 0.0)
                    quantity = item.get('quantity', 0)
                    
                    display_text = f"{name} ({size}) - شراء: {buying_price} ج.م - بيع: {selling_price} ج.م - متوفر: {quantity}"
                    self.item_combo.addItem(display_text, item)
                return
            
            # فلترة حسب المقاس المحدد
            filtered_items = []
            for item in items:
                if item.get('size', '') == selected_size:
                    filtered_items.append(item)
            
            if not filtered_items:
                self.item_combo.addItem(f"لا توجد منتجات بالمقاس: {selected_size}", None)
                return
            
            for item in filtered_items:
                name = item.get('name', 'غير معروف')
                size = item.get('size', '')
                buying_price = item.get('buying_price', 0.0)
                selling_price = item.get('selling_price', 0.0)
                quantity = item.get('quantity', 0)
                
                display_text = f"{name} ({size}) - شراء: {buying_price} ج.م - بيع: {selling_price} ج.م - متوفر: {quantity}"
                self.item_combo.addItem(display_text, item)
            
            self.item_combo.setCurrentIndex(0)
            
        except Exception as e:
            print(f"خطأ في فلترة المنتجات: {e}")
    
    def filter_items_combo(self, text):
        """فلترة أثناء الكتابة"""
        try:
            if not text.strip():
                for i in range(self.item_combo.count()):
                    self.item_combo.setItemHidden(i, False)
                return
            
            search_text = text.strip().lower()
            for i in range(self.item_combo.count()):
                item_text = self.item_combo.itemText(i).lower()
                self.item_combo.setItemHidden(i, search_text not in item_text)
                
        except Exception as e:
            print(f"خطأ في الفلترة: {e}")
    
    def search_in_combo(self, combo_box):
        """فتح نافذة بحث"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("بحث")
            dialog.setGeometry(200, 200, 400, 300)
            
            layout = QVBoxLayout()
            layout.addWidget(QLabel("اكتب للبحث:"))
            
            search_input = QLineEdit()
            search_input.textChanged.connect(lambda text: self.filter_search_results(combo_box, text, result_list))
            layout.addWidget(search_input)
            
            result_list = QListWidget()
            layout.addWidget(result_list)
            
            # تحميل جميع العناصر
            for i in range(combo_box.count()):
                result_list.addItem(combo_box.itemText(i))
                result_list.item(i).setData(Qt.ItemDataRole.UserRole, i)
            
            select_btn = QPushButton("تحديد")
            select_btn.clicked.connect(lambda: self.select_search_result(combo_box, result_list, dialog))
            layout.addWidget(select_btn)
            
            dialog.setLayout(layout)
            dialog.exec()
            
        except Exception as e:
            print(f"خطأ في البحث: {e}")
    
    def filter_search_results(self, combo_box, text, result_list):
        """فلترة نتائج البحث"""
        result_list.clear()
        search_text = text.strip().lower()
        
        if not search_text:
            for i in range(combo_box.count()):
                result_list.addItem(combo_box.itemText(i))
                result_list.item(result_list.count() - 1).setData(Qt.ItemDataRole.UserRole, i)
            return
        
        for i in range(combo_box.count()):
            item_text = combo_box.itemText(i).lower()
            if search_text in item_text:
                result_list.addItem(combo_box.itemText(i))
                result_list.item(result_list.count() - 1).setData(Qt.ItemDataRole.UserRole, i)
    
    def add_to_cart(self):
        """إضافة منتج للسلة مع تحديث الجدول الافتراضي"""
        item_data = self.item_combo.currentData()
        
        if item_data is None:
            QMessageBox.warning(self, "خطأ", "لا توجد منتجات متاحة!")
            return
        
        quantity = self.quantity_spin.value()
        selling_price = self.selling_price_input.value()
        
        if selling_price <= 0:
            QMessageBox.warning(self, "خطأ", "الرجاء إدخال سعر بيع صحيح!")
            return
        
        # ✅ التحقق من الكمية المتاحة في الجدول الافتراضي
        item_name = item_data['name']
        item_size = item_data['size']
        available_quantity = self.get_virtual_quantity(item_name, item_size)
        
        if quantity > available_quantity:
            QMessageBox.warning(
                self, 
                "خطأ في الكمية", 
                f"الكمية المطلوبة ({quantity}) تتجاوز الكمية المتاحة ({available_quantity})!"
            )
            return
        
        # ✅ تحديث الجدول الافتراضي (خصم الكمية المضافة)
        if not self.update_virtual_quantity(item_data['item_id'], quantity):
            QMessageBox.warning(self, "خطأ", "فشل تحديث المخزون الافتراضي!")
            return
        
        cart_item = {
            'item_id': item_data['item_id'],
            'name': item_data['name'],
            'size': item_data['size'],
            'unit': item_data.get('unit', 'عدد'),
            'quantity': quantity,
            'buying_price': item_data['buying_price'],
            'selling_price': selling_price,  # ✅ السعر المعدل من المستخدم
            'buying_total': item_data['buying_price'] * quantity,
            'selling_total': selling_price * quantity
        }
        
        self.cart_items.append(cart_item)
        self.update_cart_display()
        
        # ✅ تحديث قائمة المنتجات لتعكس الكمية المحدثة
        self.load_items_combo()
        
        # إعادة تعيين الحقول
        self.quantity_spin.setValue(1)
        self.selling_price_input.setValue(0.0)
    
    def update_cart_display(self):
        """تحديث عرض السلة"""
        self.cart_table.setRowCount(len(self.cart_items))
        
        total_buying = 0
        total_selling = 0
        
        for i, item in enumerate(self.cart_items):
            # الرقم التسلسلي
            self.cart_table.setItem(i, 0, QTableWidgetItem(str(i+1)))
            
            # الصنف
            self.cart_table.setItem(i, 1, QTableWidgetItem(item['name']))
            
            # المقاس
            self.cart_table.setItem(i, 2, QTableWidgetItem(item['size']))
            
            # الكمية
            self.cart_table.setItem(i, 3, QTableWidgetItem(str(item['quantity'])))
            
            # سعر البيع
            self.cart_table.setItem(i, 4, QTableWidgetItem(f"{item['selling_price']:.2f} ج.م"))
            
            # الإجمالي شراء
            self.cart_table.setItem(i, 5, QTableWidgetItem(f"{item['buying_total']:.2f} ج.م"))
            
            # الإجمالي بيع
            self.cart_table.setItem(i, 6, QTableWidgetItem(f"{item['selling_total']:.2f} ج.م"))
            
            total_buying += item['buying_total']
            total_selling += item['selling_total']
        
        self.current_total = total_selling
        self.cart_total_label.setText(f"إجمالي السلة (بيع): {total_selling:.2f} ج.م")
        
        # تحديث الإجماليات في الخطوة 3
        if hasattr(self, 'current_total_label'):
            self.current_total_label.setText(f"{total_selling:.2f} ج.م")
        
        if hasattr(self, 'calculate_totals'):
            self.calculate_totals()
    
    def update_real_inventory_directly(self):
        """تحديث المخزون الحقيقي مباشرة بدون مرور عبر items_manager"""
        try:
            # جلب العناصر الحالية من قاعدة البيانات
            items = self.db.load_items()
            
            for cart_item in self.cart_items:
                item_id = cart_item['item_id']
                quantity_sold = cart_item['quantity']
                
                # البحث عن العنصر في المخزون
                item_found = False
                for item in items:
                    if str(item.get('item_id', '')) == str(item_id):
                        current_qty = item.get('quantity', 0)
                        new_qty = current_qty - quantity_sold
                        
                        if new_qty < 0:
                            new_qty = 0
                            print(f"تحذير: الكمية أصبحت سالبة للعنصر {item_id}")
                        
                        item['quantity'] = new_qty
                        item_found = True
                        print(f"تم تحديث العنصر {item_id}: {current_qty} → {new_qty}")
                        break
                
                if not item_found:
                    print(f"تحذير: العنصر {item_id} غير موجود في المخزون")
            
            # حفظ التغييرات
            self.db.save_items(items)
            print("تم حفظ التغييرات في المخزون الحقيقي")
            return True
            
        except Exception as e:
            print(f"خطأ في تحديث المخزون المباشر: {e}")
            return False

    def remove_from_cart(self):
        """حذف منتج من السلة مع استعادة الكمية في الجدول الافتراضي"""
        selected = self.cart_table.currentRow()
        if selected >= 0:
            # الحصول على بيانات العنصر المحدد
            cart_item = self.cart_items[selected]
            item_id = cart_item['item_id']
            quantity = cart_item['quantity']
            
            # ✅ استعادة الكمية في الجدول الافتراضي
            if not self.restore_virtual_quantity(item_id, quantity):
                print(f"فشل استعادة الكمية للعنصر {item_id}")
            
            # حذف العنصر من السلة
            self.cart_items.pop(selected)
            self.update_cart_display()
            
            # ✅ تحديث قائمة المنتجات لتعكس الكمية المستعادة
            self.load_items_combo()
    
    def create_step3(self):
        """الخطوة 3: الدفع والإجماليات"""
        # إنشاء Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #1f242b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #3498db;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #2980b9;
            }
        """)
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # عنوان الخطوة
        title = QLabel("الدفع والإجماليات")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; text-align: center; padding: 10px;")
        layout.addWidget(title)
        
        # معلومات العميل - بدون إطار
        customer_layout = QVBoxLayout()
        
        self.customer_summary_label = QLabel("")
        self.customer_summary_label.setStyleSheet("""
            font-size: 12px; 
            color: #34495e; 
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        """)
        customer_layout.addWidget(self.customer_summary_label)
        
        layout.addLayout(customer_layout)
        
        # الإجماليات - بدون إطار
        totals_layout = QFormLayout()
        
        # الإجمالي الحالي (سعر البيع)
        self.current_total_label = QLabel("0.00 ج.م")
        self.current_total_label.setStyleSheet("font-size: 14px; color: #2c3e50; font-weight: bold;")
        totals_layout.addRow("الإجمالي الحالي (بيع):", self.current_total_label)
        
        # الرصيد السابق
        previous_balance_layout = QHBoxLayout()
        previous_balance_layout.addWidget(QLabel("الرصيد السابق:"))
        
        self.previous_balance_input = QDoubleSpinBox()
        self.previous_balance_input.setDecimals(2)
        self.previous_balance_input.setMinimum(0.0)
        self.previous_balance_input.setMaximum(999999.99)
        self.previous_balance_input.setPrefix("ج.م ")  # ✅ تم إرجاع "ج.م"
        self.previous_balance_input.valueChanged.connect(self.calculate_totals)
        
        # ربط حدث تغيير النص لإرجاع القيمة لـ 0 عند المسح
        line_edit = self.previous_balance_input.lineEdit()
        line_edit.textChanged.connect(lambda text: self.handle_balance_text_change(text, self.previous_balance_input))
        
        previous_balance_layout.addWidget(self.previous_balance_input)
        
        # زر جلب تلقائي للرصيد السابق
        auto_fill_balance_btn = QPushButton("جلب تلقائي")
        auto_fill_balance_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        auto_fill_balance_btn.clicked.connect(self.auto_fill_previous_balance)
        previous_balance_layout.addWidget(auto_fill_balance_btn)
        
        totals_layout.addRow(previous_balance_layout)
        
        # الإجمالي الكلي
        self.cumulative_total_label = QLabel("0.00 ج.م")
        self.cumulative_total_label.setStyleSheet("font-size: 16px; color: #c0392b; font-weight: bold;")
        totals_layout.addRow("الإجمالي الكلي:", self.cumulative_total_label)
        
        layout.addLayout(totals_layout)
        
        # الدفع الحالي - بدون إطار
        payment_layout = QVBoxLayout()
        
        # مدى الدفع المسموح
        self.range_label = QLabel("المبلغ المسموح دفعه: 0.00 - 0.00 ج.م")
        self.range_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        payment_layout.addWidget(self.range_label)
        
        # إدخال المبلغ المدفوع
        paid_layout = QHBoxLayout()
        paid_layout.addWidget(QLabel("المبلغ المدفوع الآن:"))
        
        self.amount_paid_input = QDoubleSpinBox()
        self.amount_paid_input.setDecimals(2)
        self.amount_paid_input.setMinimum(0.0)
        self.amount_paid_input.setMaximum(0.0)
        self.amount_paid_input.setPrefix("ج.م ")  # ✅ تم إرجاع "ج.م"
        self.amount_paid_input.valueChanged.connect(self.update_payment_summary)
        
        # ربط حدث تغيير النص لإرجاع القيمة لـ 0 عند المسح
        paid_line_edit = self.amount_paid_input.lineEdit()
        paid_line_edit.textChanged.connect(lambda text: self.handle_balance_text_change(text, self.amount_paid_input))
        
        paid_layout.addWidget(self.amount_paid_input)
        
        payment_layout.addLayout(paid_layout)
        
        # المبلغ المتبقي للفاتورة
        remaining_invoice_layout = QHBoxLayout()
        remaining_invoice_layout.addWidget(QLabel("متبقي الفاتورة:"))
        
        self.remaining_invoice_label = QLabel("0.00 ج.م")
        self.remaining_invoice_label.setStyleSheet("font-size: 14px; color: #e74c3c; font-weight: bold;")
        remaining_invoice_layout.addWidget(self.remaining_invoice_label)
        remaining_invoice_layout.addStretch()
        payment_layout.addLayout(remaining_invoice_layout)
        
        # المبلغ المتبقي الكلي
        remaining_total_layout = QHBoxLayout()
        remaining_total_layout.addWidget(QLabel("المتبقي الكلي:"))
        
        self.remaining_total_label = QLabel("0.00 ج.م")
        self.remaining_total_label.setStyleSheet("font-size: 16px; color: #e74c3c; font-weight: bold;")
        remaining_total_layout.addWidget(self.remaining_total_label)
        remaining_total_layout.addStretch()
        payment_layout.addLayout(remaining_total_layout)
        
        layout.addLayout(payment_layout)
        
        # حالة الدفع - بدون إطار
        payment_status_layout = QVBoxLayout()
        
        payment_status_title = QLabel("حالة الدفع:")
        payment_status_title.setStyleSheet("font-weight: bold; color: #e74c3c; font-size: 14px; padding-top: 10px;")
        payment_status_layout.addWidget(payment_status_title)
        
        self.payment_status_label = QLabel("غير مدفوع")
        self.payment_status_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #e74c3c;
            padding: 10px;
            text-align: center;
            border: 1px solid #e74c3c;
            border-radius: 5px;
            background-color: #fff;
            margin-top: 5px;
        """)
        payment_status_layout.addWidget(self.payment_status_label)
        
        layout.addLayout(payment_status_layout)
        
        # ملاحظات إضافية - بدون إطار
        notes_layout = QVBoxLayout()
        
        notes_title = QLabel("ملاحظات إضافية:")
        notes_title.setStyleSheet("font-weight: bold; color: #3498db; font-size: 14px; padding-top: 10px;")
        notes_layout.addWidget(notes_title)
        
        self.notes_input_step3 = QTextEdit()
        self.notes_input_step3.setMaximumHeight(80)
        self.notes_input_step3.setPlaceholderText("أدخل ملاحظات إضافية هنا...")
        self.notes_input_step3.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                margin-top: 5px;
            }
            QTextEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        notes_layout.addWidget(self.notes_input_step3)
        
        layout.addLayout(notes_layout)
        
        # فاصل
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #ddd; margin: 15px 0;")
        layout.addWidget(line)
        
        widget.setLayout(layout)
        scroll_area.setWidget(widget)
        
        return scroll_area
    
    def handle_balance_text_change(self, text, spin_box):
        """معالجة تغيير النص في spin box"""
        if text == "":
            # إذا تم مسح النص بالكامل، تعيين القيمة إلى 0
            spin_box.setValue(0.0)
    
    def get_customer_true_remaining(self, customer_name):
        """الحصول على المتبقي الحقيقي للعميل - من آخر قسط فقط لكل فاتورة"""
        try:
            customer_name_lower = customer_name.strip().lower()
            history = self.db.load_history()
            
            if not history:
                return 0.0
            
            # تجميع الفواتير الأصلية
            original_invoices = {}
            for invoice in history:
                invoice_customer_name = invoice.get('customer_name', '').strip().lower()
                if invoice_customer_name != customer_name_lower:
                    continue
                
                receipt_id = invoice.get('receipt_id', '')
                
                # نأخذ الفواتير الأصلية فقط (بدون أقساط وبدون سجلات REM_)
                if '.' not in receipt_id and not receipt_id.startswith('REM_'):
                    original_invoices[receipt_id] = {
                        'original_invoice': invoice,
                        'last_payment': invoice  # بداية، الفاتورة الأصلية هي آخر سجل
                    }
            
            # البحث عن آخر قسط لكل فاتورة
            for invoice in history:
                invoice_customer_name = invoice.get('customer_name', '').strip().lower()
                if invoice_customer_name != customer_name_lower:
                    continue
                
                receipt_id = invoice.get('receipt_id', '')
                
                # إذا كانت فاتورة قسط (تحتوي على نقطة)
                if '.' in receipt_id:
                    parts = receipt_id.split('.')
                    if len(parts) >= 2:
                        original_id = parts[0]
                        
                        if original_id in original_invoices:
                            # استخراج رقم القسط
                            try:
                                payment_number = int(parts[1])
                            except:
                                payment_number = 0
                            
                            # الحصول على آخر قسط مسجل حالياً
                            last_payment = original_invoices[original_id]['last_payment']
                            last_payment_id = last_payment.get('receipt_id', '')
                            
                            # استخراج رقم آخر قسط
                            last_payment_number = 0
                            if '.' in last_payment_id:
                                try:
                                    last_parts = last_payment_id.split('.')
                                    if len(last_parts) >= 2:
                                        last_payment_number = int(last_parts[1])
                                except:
                                    pass
                            
                            # إذا كان هذا القسط أحدث، نجعله آخر قسط
                            if payment_number > last_payment_number:
                                original_invoices[original_id]['last_payment'] = invoice
            
            # حساب المتبقي الإجمالي من آخر قسط لكل فاتورة
            total_remaining = 0.0
            
            for original_id, data in original_invoices.items():
                last_payment = data['last_payment']
                
                # ✅ نجمع المتبقي من آخر قسط فقط
                try:
                    remaining = float(last_payment.get('remaining', 0))
                    total_remaining += remaining
                except:
                    pass
            
            # إضافة سجلات REM_ (المتبقي غير المسجل)
            for invoice in history:
                invoice_customer_name = invoice.get('customer_name', '').strip().lower()
                if invoice_customer_name != customer_name_lower:
                    continue
                
                receipt_id = invoice.get('receipt_id', '')
                
                # إضافة سجلات REM_ مباشرة
                if receipt_id.startswith('REM_'):
                    try:
                        remaining = float(invoice.get('remaining', 0))
                        total_remaining += remaining
                    except:
                        pass
            
            return total_remaining
            
        except Exception as e:
            print(f"خطأ في حساب المتبقي الحقيقي: {e}")
            # نسخة احتياطية أبسط
            try:
                customer_name_lower = customer_name.strip().lower()
                history = self.db.load_history()
                total_remaining = 0.0
                
                for invoice in history:
                    if invoice.get('customer_name', '').strip().lower() == customer_name_lower:
                        try:
                            remaining = float(invoice.get('remaining', 0))
                            total_remaining += remaining
                        except:
                            pass
                
                return total_remaining
            except:
                return 0.0

    def auto_fill_previous_balance(self):
        """جلب الرصيد السابق تلقائياً من الفواتير الأصلية فقط"""
        customer_name = self.customer_name_input.text().strip()
        if not customer_name:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال اسم العميل أولاً!")
            return
        
        try:
            # ✅ ✅ ✅ التصحيح هنا - تأكد من اسم الدالة الصحيح
            customer_total_remaining = self.get_customer_true_remaining(customer_name)  # ✅ ليس get() !!
            
            # حساب عدد الفواتير الأصلية والمبلغ المدفوع
            history = self.db.load_history()
            invoice_count = 0
            total_invoices_amount = 0.0
            total_paid_amount = 0.0
            
            for invoice in history:
                if invoice.get('customer_name', '').strip().lower() == customer_name.lower():
                    receipt_id = invoice.get('receipt_id', '')
                    if '.' not in receipt_id or receipt_id.startswith('REM_'):
                        invoice_count += 1
                        
                        # حساب إجمالي الفاتورة
                        try:
                            total_amount = float(invoice.get('total', 0))
                            total_invoices_amount += total_amount
                        except:
                            pass
                        
                        # حساب المدفوع
                        try:
                            paid_amount = float(invoice.get('amount_paid', 0))
                            total_paid_amount += paid_amount
                        except:
                            pass
            
            if invoice_count == 0:
                QMessageBox.information(self, "معلومات", 
                                    "لا توجد فواتير سابقة لهذا العميل")
                return
            
            # الحصول على معرف العميل
            customer_id = None
            for invoice in history:
                if invoice.get('customer_name', '').strip().lower() == customer_name.lower():
                    customer_id = invoice.get('customer_id', '')
                    if customer_id:
                        break
            
            # تعيين القيمة في الحقل
            self.previous_balance_input.setValue(customer_total_remaining)
            
            # عرض معلومات العميل
            info_text = f"✅ تم جلب متبقي العميل\n\n"
            info_text += f"اسم العميل: {customer_name}\n"
            if customer_id:
                info_text += f"رقم العميل: {customer_id}\n"
            info_text += f"عدد الفواتير الأصلية: {invoice_count}\n"
            info_text += f"إجمالي الفواتير: {total_invoices_amount:.2f} ج.م\n"
            info_text += f"إجمالي المدفوع: {total_paid_amount:.2f} ج.م\n"
            info_text += f"المتبقي السابق: {customer_total_remaining:.2f} ج.م"
            
            # تحديث ملاحظة النتيجة
            QMessageBox.information(self, "معلومات العميل", info_text)
            
            # تحديث ملخص العميل في الخطوة 3
            if hasattr(self, 'customer_summary_label'):
                self.customer_summary_label.setText(
                    f"العميل: {customer_name} | عدد الفواتير: {invoice_count} | "
                    f"المتبقي السابق: {customer_total_remaining:.2f} ج.م"
                )
            
            # تحديث الحسابات
            if hasattr(self, 'calculate_totals'):
                self.calculate_totals()
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء جلب بيانات العميل:\n{str(e)}")
    
    def calculate_totals(self):
        """حساب جميع الإجماليات"""
        # الإجمالي الحالي من السلة (سعر البيع)
        current_total_selling = sum(item['selling_total'] for item in self.cart_items)
        
        # الرصيد السابق
        self.customer_previous_balance = self.previous_balance_input.value()
        
        # الإجمالي الكلي
        self.total_cumulative = self.customer_previous_balance + current_total_selling
        
        # تحديث العناوين
        if hasattr(self, 'current_total_label'):
            self.current_total_label.setText(f"{current_total_selling:.2f} ج.م")
        
        if hasattr(self, 'cumulative_total_label'):
            self.cumulative_total_label.setText(f"{self.total_cumulative:.2f} ج.م")
        
        # تحديث مدى الدفع
        if hasattr(self, 'amount_paid_input'):
            self.amount_paid_input.setMaximum(current_total_selling)
        
        # تحديث ملخص الدفع
        if hasattr(self, 'update_payment_summary'):
            self.update_payment_summary()
        
        # تحديث معلومات العميل
        if hasattr(self, 'update_supplier_summary'):
            self.update_supplier_summary()
    
    def update_payment_summary(self):
        """تحديث ملخص الدفع"""
        if not hasattr(self, 'amount_paid_input'):
            return
        
        amount_paid = self.amount_paid_input.value()
        
        # حساب المتبقي
        remaining = self.total_cumulative - amount_paid
        self.total_remaining = remaining
        
        # تحديث العناوين
        if hasattr(self, 'remaining_invoice_label'):
            self.remaining_invoice_label.setText(f"{remaining:.2f} ج.م")
        
        if hasattr(self, 'remaining_total_label'):
            self.remaining_total_label.setText(f"{remaining:.2f} ج.م")
        
        # تحديث حالة الدفع
        if remaining <= 0:
            payment_status = "مدفوع بالكامل"
            color = "#27ae60"
        elif amount_paid == 0:
            payment_status = "غير مدفوع"
            color = "#e74c3c"
        else:
            payment_status = "سداد قسط"
            color = "#9b59b6"  # بنفسجي للسداد القسط
        
        if hasattr(self, 'payment_status_label'):
            self.payment_status_label.setText(payment_status)
            self.payment_status_label.setStyleSheet(f"""
                font-size: 18px; 
                font-weight: bold; 
                color: {color};
                padding: 10px;
                text-align: center;
                border: 2px solid {color};
                border-radius: 5px;
                background-color: #fff;
            """)
        
        # تحديث النطاق المسموح
        if hasattr(self, 'range_label'):
            self.range_label.setText(f"المبلغ المسموح دفعه: 0.00 - {self.total_cumulative:.2f} ج.م")
    
    def create_step4(self):
        """الخطوة 4: تأكيد الفاتورة"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # عنوان الخطوة
        step_title = QLabel("الخطوة الرابعة: مراجعة الفاتورة")
        step_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                text-align: center;
                background-color: #f8f9fa;
                border-radius: 10px;
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(step_title)
        
        # معاينة الفاتورة
        self.receipt_preview_label = QLabel("جاري إنشاء معاينة الفاتورة...")
        self.receipt_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.receipt_preview_label.setMinimumHeight(350)
        self.receipt_preview_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                color: #666;
            }
        """)
        layout.addWidget(self.receipt_preview_label)
        
        # فاصل
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #ccc; margin: 15px 0;")
        layout.addWidget(line)
        
        # معلومات إضافية
        info_widget = QWidget()
        info_layout = QHBoxLayout(info_widget)
        
        # طريقة الدفع
        payment_group = QGroupBox("طريقة الدفع")
        payment_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; border: 1px solid #3498db; border-radius: 5px; }")
        payment_layout = QVBoxLayout()
        
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["نقدي", "بطاقة ائتمان", "بطاقة خصم", "تحويل بنكي"])
        self.payment_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px;
                min-height: 25px;
            }
            QComboBox:hover {
                border: 1px solid #3498db;
            }
        """)
        payment_layout.addWidget(self.payment_combo)
        payment_group.setLayout(payment_layout)
        info_layout.addWidget(payment_group)
        
        info_layout.addStretch()
        layout.addWidget(info_widget)
        
        # أزرار الإجراءات
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        
        # زر إنشاء فاتورة جديدة
        self.new_receipt_btn = QPushButton("📝 إنشاء فاتورة جديدة")
        self.new_receipt_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.new_receipt_btn.clicked.connect(self.create_new_receipt)
        actions_layout.addWidget(self.new_receipt_btn)
        
        # ✅ زر حفظ مع تطبيق التغييرات الافتراضية
        self.save_db_btn = QPushButton("💾 حفظ في قاعدة البيانات")
        self.save_db_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                cursor: not-allowed;
            }
        """)
        self.save_db_btn.clicked.connect(self.save_receipt_with_virtual_commit)
        self.save_db_btn.setEnabled(False)
        actions_layout.addWidget(self.save_db_btn)
        
        # زر تحميل PDF
        self.download_image_btn = QPushButton("📥 تحميل PDF")
        self.download_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                cursor: not-allowed;
            }
        """)
        self.download_image_btn.clicked.connect(self.download_receipt_image)
        self.download_image_btn.setEnabled(False)
        actions_layout.addWidget(self.download_image_btn)
        
        # زر معاينة
        self.preview_btn = QPushButton("👁️ معاينة")
        self.preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                cursor: not-allowed;
            }
        """)
        self.preview_btn.clicked.connect(self.preview_receipt)
        self.preview_btn.setEnabled(False)
        actions_layout.addWidget(self.preview_btn)
        
        # زر إنهاء
        self.finish_btn = QPushButton("إنهاء")
        self.finish_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #6c7b7d;
            }
        """)
        self.finish_btn.clicked.connect(self.close)
        actions_layout.addWidget(self.finish_btn)
        
        actions_layout.addStretch()
        layout.addWidget(actions_widget)
        
        widget.setLayout(layout)
        return widget
    
    def generate_receipt_preview(self):
        """إنشاء معاينة الفاتورة كصورة باستخدام المولد الجديد"""
        try:
            # إنشاء بيانات الفاتورة
            receipt_data = self.create_receipt_data()
            
            # استخدام المولد العربي الجديد لإنشاء صورة PNG
            try:
                from arabic_receipt_generator_new import ArabicReceiptGenerator
                
                # إنشاء صورة مؤقتة للمعاينة فقط
                import tempfile
                temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                temp_path = temp_file.name
                temp_file.close()
                
                # إنشاء صورة PNG باستخدام المولد الجديد
                image_path = ArabicReceiptGenerator.generate_receipt(receipt_data, temp_path)
                
                if image_path and os.path.exists(image_path):
                    try:
                        # تحميل الصورة وعرضها
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            scaled_pixmap = pixmap.scaled(
                                650, 
                                350, 
                                Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation
                            )
                            
                            # تحديث ال label بالصورة
                            self.receipt_preview_label.setPixmap(scaled_pixmap)
                            
                            # حفظ بيانات الفاتورة
                            self.preview_receipt_data = receipt_data
                            
                            # تفعيل الأزرار
                            self.save_db_btn.setEnabled(True)
                            self.download_image_btn.setEnabled(True)
                            self.preview_btn.setEnabled(True)
                            
                            print(f" تم إنشاء معاينة الفاتورة: {image_path}")
                            
                            # تنظيف الملف المؤقت
                            try:
                                os.unlink(temp_path)
                            except:
                                pass
                            
                            return True
                        else:
                            print(" فشل تحميل الصورة: pixmap فارغ")
                            self.show_text_preview(receipt_data)
                            return False
                            
                    except Exception as pixmap_error:
                        print(f" خطأ في تحميل الصورة: {pixmap_error}")
                        self.show_text_preview(receipt_data)
                        return False
                        
                else:
                    print(" فشل إنشاء الصورة: الملف غير موجود")
                    self.show_text_preview(receipt_data)
                    return False
                    
            except ImportError as import_error:
                # إذا لم يتوفر المولد الجديد، استخدم المولد القديم كبديل
                print(f"المولد العربي الجديد غير متوفر: {import_error}")
                self.show_text_preview(receipt_data)
                return False
                
            # إذا فشل إنشاء الصورة
            self.show_text_preview(receipt_data)
            return False
            
        except Exception as e:
            print(f" خطأ في إنشاء المعاينة: {e}")
            import traceback
            traceback.print_exc()
            
            # إنشاء بيانات الفاتورة وعرضها كنص
            try:
                receipt_data = self.create_receipt_data()
                self.show_text_preview(receipt_data)
                return False  # معاينة نصية فقط
            except:
                self.receipt_preview_label.setText("فشل إنشاء معاينة الفاتورة")
                return False
    
    def show_text_preview(self, receipt_data=None):
        """عرض معاينة نصية للفاتورة"""
        try:
            if receipt_data is None:
                receipt_data = self.create_receipt_data()
            
            receipt_text = self.create_receipt_text(receipt_data)
            
            # إنشاء واجهة النص
            text_widget = QTextEdit()
            text_widget.setPlainText(receipt_text)
            text_widget.setReadOnly(True)
            text_widget.setStyleSheet("""
                QTextEdit {
                    font-family: 'Courier New', monospace;
                    font-size: 11px;
                    background-color: white;
                    border: 1px solid #ddd;
                    padding: 10px;
                }
            """)
            
            # استبدال ال label بالنص
            if self.receipt_preview_label.parent():
                layout = self.receipt_preview_label.parent().layout()
                if layout:
                    for i in range(layout.count()):
                        if layout.itemAt(i).widget() == self.receipt_preview_label:
                            layout.replaceWidget(self.receipt_preview_label, text_widget)
                            self.receipt_preview_label.deleteLater()
                            self.receipt_preview_label = text_widget
                            break
            
            # حفظ بيانات الفاتورة
            self.preview_receipt_data = receipt_data
            
            # تفعيل الأزرار
            self.save_db_btn.setEnabled(True)
            self.download_image_btn.setEnabled(True)
            self.preview_btn.setEnabled(True)
            
        except Exception as e:
            print(f"خطأ في المعاينة النصية: {e}")
            QMessageBox.warning(self, "خطأ", "فشل إنشاء معاينة الفاتورة!")
    
    def create_receipt_data(self):
        """إنشاء بيانات الفاتورة مع الحقول الجديدة"""
        import random
        
        receipt_id = f"INV{random.randint(10000, 99999)}"
        customer_name = self.current_customer_name or "غير محدد"
        
        # استخدام customer_code كـ customer_id إذا كان متاحاً
        customer_code = self.customer_code_input.text().strip()
        if customer_code:
            customer_id = customer_code
        else:
            customer_id = self.current_customer_id or (self.db.find_customer_id(customer_name) if hasattr(self.db, 'find_customer_id') else None)
        
        # إذا لم يكن هناك معرف، أنشئ واحداً
        if not customer_id:
            customer_id = f"C{random.randint(1000, 9999)}"
        
        date_str = self.date_input.date().toString('yyyy-MM-dd')
        
        # الحصول على البيانات الجديدة
        customer_address = self.address_input.text().strip() or "غير محدد"
        customer_notes = self.notes_input_step1.toPlainText().strip()
        
        # ✅ حساب المتبقي للعرض (الإجمالي + الرصيد السابق - المدفوع)
        remaining_for_display = self.total_cumulative - self.total_paid_now
        if remaining_for_display < 0:
            remaining_for_display = 0
        
        # ✅ حساب المتبقي للتخزين (إجمالي الفاتورة فقط - المدفوع)
        receipt_remaining = self.current_total - self.total_paid_now
        if receipt_remaining < 0:
            receipt_remaining = 0
        
        # حالة الدفع
        if remaining_for_display <= 0:
            payment_status = "مدفوع بالكامل"
        elif self.total_paid_now == 0:
            payment_status = "غير مدفوع"
        else:
            payment_status = "مدفوع جزئيا"
        
        return {
            'receipt_id': receipt_id,
            'customer_id': customer_id,
            'customer_code': customer_code,
            'customer_name': customer_name,
            'date': date_str,
            'customer_address': customer_address,
            'customer_notes': customer_notes,
            'items': self.cart_items.copy(),
            'total': self.current_total,  # إجمالي الفاتورة الحالية
            'payment_method': self.payment_combo.currentText(),
            'previous_balance': self.customer_previous_balance,  # الرصيد السابق
            'total_cumulative': self.total_cumulative,  # الإجمالي الكلي (الفاتورة + الرصيد السابق)
            'amount_paid': self.total_paid_now,  # المدفوع من هذه الفاتورة
            'remaining': receipt_remaining,  # ⬅️ متبقي هذه الفاتورة فقط (هذا ما يتم تخزينه)
            'remaining_display': remaining_for_display,  # ✅ متبقي للعرض (الفاتورة + الرصيد السابق - المدفوع)
            'payment_status': payment_status,
            'notes': self.notes_input_step3.toPlainText().strip()  # ملاحظات إضافية
        }

    def create_receipt_text(self, receipt_data):
        """إنشاء نص الفاتورة من البيانات"""
        try:
            # ✅ استخدام المتبقي للعرض (الإجمالي + الرصيد السابق - المدفوع)
            remaining_display = receipt_data.get('remaining_display', 
                receipt_data['total'] + receipt_data['previous_balance'] - receipt_data['amount_paid'])
            
            if remaining_display < 0:
                remaining_display = 0
            
            receipt_text = f"""
    
            فاتورة بيع
   
    رقم الفاتورة: {receipt_data['receipt_id']}
    التاريخ: {receipt_data['date']}
    
    العميل: {receipt_data['customer_name']}
    رقم العميل: {receipt_data['customer_id']}
    العنوان: {receipt_data['customer_address']}
   
    المنتجات:
    """
            
            for i, item in enumerate(receipt_data['items'], 1):
                receipt_text += f"    {i}. {item['name']} ({item['size']}) - {item['quantity']} × {item['selling_price']} ج.م = {item['quantity'] * item['selling_price']:.2f} ج.م\n"
            
            receipt_text += f"""
    
    إجمالي الفاتورة الحالي: {receipt_data['total']:.2f} ج.م
    الرصيد السابق: {receipt_data['previous_balance']:.2f} ج.م
    المجموع الكلي: {receipt_data['total_cumulative']:.2f} ج.م
    
    المبلغ المدفوع: {receipt_data['amount_paid']:.2f} ج.م
    المبلغ المتبقي: {remaining_display:.2f} ج.م
    
    طريقة الدفع: {receipt_data['payment_method']}
    حالة الدفع: {receipt_data['payment_status']}
    
    الملاحظات: {receipt_data['notes']}

    """
            return receipt_text
        except Exception as e:
            return f"خطأ في إنشاء الفاتورة: {str(e)}"
    
    # ✅ دالة جديدة: حفظ الفاتورة مع تطبيق التغييرات الافتراضية
    def save_receipt_with_virtual_commit(self):
        """حفظ الفاتورة مع تطبيق التغييرات من الجدول الافتراضي"""
        try:
            if not self.preview_receipt_data:
                QMessageBox.warning(self, "تحذير", "الرجاء إنشاء الفاتورة أولاً!")
                return False
        
            # ✅ تحديث المخزون الحقيقي مباشرة
            if not self.update_real_inventory_directly():
                QMessageBox.warning(self, "تحذير", "فشل تحديث المخزون الحقيقي!")
                return False

            # ✅ تطبيق التغييرات من الجدول الافتراضي على الجدول الحقيقي
            if self.items_manager and self.virtual_table:
                # تحديث كل عنصر في المخزون الحقيقي
                for cart_item in self.cart_items:
                    item_id = cart_item['item_id']
                    quantity_sold = cart_item['quantity']
                    
                    # استخدام الدالة المباشرة لتحديث المخزون
                    success = self.items_manager.update_item_quantity(
                        item_id, 
                        -quantity_sold  # سالب لأننا نخفض الكمية
                    )
                    
                    if not success:
                        print(f"تحذير: فشل تحديث المخزون للعنصر {item_id}")
            
            # ⚠️ ⚠️ ⚠️ التعديل المهم: استخدام متبقي الفاتورة فقط للتخزين
            # نحسب متبقي الفاتورة فقط (بدون الرصيد السابق) للتخزين
            receipt_remaining = self.current_total - self.total_paid_now
            if receipt_remaining < 0:
                receipt_remaining = 0
            
            # ✅ حساب المتبقي للعرض (الإجمالي الكلي - المدفوع)
            remaining_for_display = self.total_cumulative - self.total_paid_now
            if remaining_for_display < 0:
                remaining_for_display = 0
            
            # إنشاء نسخة من بيانات الفاتورة مع المتبقي الصحيح
            receipt_data = self.preview_receipt_data.copy()
            receipt_data['remaining'] = receipt_remaining  # ⬅️ متبقي هذه الفاتورة فقط (هذا ما يتم تخزينه)
            receipt_data['remaining_display'] = remaining_for_display  # ✅ متبقي للعرض
            
            # تنظيف البيانات
            cleaned_data = self.clean_receipt_data(receipt_data)
            
            # إذا لم يكن هناك customer_id، استخدم customer_code
            customer_code = cleaned_data.get('customer_code', '')
            if not cleaned_data.get('customer_id') and customer_code:
                cleaned_data['customer_id'] = customer_code
            
            # حفظ في قاعدة البيانات
            success = self.db.add_history_record(cleaned_data)
            
            if success:
                # ✅ التعديل: إبقاء الأزرار مفعلة بعد الحفظ
                QMessageBox.information(
                    self,
                    "تم الحفظ",
                    f"✅ تم حفظ الفاتورة في قاعدة البيانات!\n"
                    f"رقم الفاتورة: {cleaned_data['receipt_id']}\n"
                    f"متبقي الفاتورة (للتخزين): {receipt_remaining:.2f} ج.م\n"
                    f"متبقي للعرض: {remaining_for_display:.2f} ج.م"
                )
                
                # ✅ تعطيل زر الحفظ فقط وترك الأزرار الأخرى مفعلة
                self.save_db_btn.setEnabled(False)
                self.save_db_btn.setText(" ✅ تم الحفظ")
                
                # إعادة تحميل سجل المبيعات إذا كان مفتوحاً
                self.refresh_history_window()
                
                # ✅ إعادة تعيين الجدول الافتراضي بعد الحفظ الناجح
                self.reset_virtual_table()
                
                return True
            else:
                QMessageBox.warning(self, "خطأ", "فشل حفظ الفاتورة في قاعدة البيانات!")
                return False
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ غير متوقع:\n{str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_receipt_to_database(self):
        """الاسم القديم للدالة، استدعاء الدالة الجديدة"""
        return self.save_receipt_with_virtual_commit()
    
    def refresh_history_window(self):
        """إعادة تحميل نافذة سجل المبيعات إذا كانت مفتوحة"""
        try:
            # محاولة العثور على نافذة سجل المبيعات المفتوحة
            for widget in QApplication.topLevelWidgets():
                if widget.__class__.__name__ == 'HistoryWindow':
                    widget.load_history()
                    print(" تم تحديث سجل المبيعات")
                    break
        except:
            pass
    
    def clean_receipt_data(self, data):
        """تنظيف بيانات الفاتورة"""
        try:
            from arabic_receipt_generator_new import ArabicReceiptGenerator
            
            # تنظيف النصوص
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = ArabicReceiptGenerator.safe_text(value)
            
            # تنظيف المنتجات
            if 'items' in data:
                for item in data['items']:
                    for k, v in item.items():
                        if isinstance(v, str):
                            item[k] = ArabicReceiptGenerator.safe_text(v)
            
        except ImportError:
            # تنظيف يدوي
            def simple_clean(text):
                if not text:
                    return ""
                # إزالة الرموز غير الآمنة
                replacements = {
                    '⚠': '[تحذير]',
                    '✅': '[صح]',
                    '❌': '[خطأ]',
                    '💾': '[حفظ]',
                    '📥': '[تحميل]',
                    '👁️': '[عرض]',
                    '🖨️': '[طباعة]',
                }
                
                result = str(text)
                for symbol, replacement in replacements.items():
                    result = result.replace(symbol, replacement)
                
                return result
            
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = simple_clean(value)
            
            if 'items' in data:
                for item in data['items']:
                    for k, v in item.items():
                        if isinstance(v, str):
                            item[k] = simple_clean(v)
        
        return data
    
    def download_receipt_image(self):
        """تحميل الفاتورة كملف PDF باستخدام المولد الجديد"""
        try:
            if not self.preview_receipt_data:
                QMessageBox.warning(self, "تحذير", "الرجاء إنشاء الفاتورة أولاً!")
                return False
            
            # استخدام المولد العربي الجديد
            try:
                from arabic_receipt_generator_new import ArabicReceiptGenerator
                
                # اسم الملف الافتراضي
                receipt_id = self.preview_receipt_data.get('receipt_id', 'UNKNOWN')
                default_name = f"فاتورة_{receipt_id}.pdf"
                
                # اختيار مكان الحفظ
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "حفظ الفاتورة كملف PDF",
                    default_name,
                    "ملفات PDF (*.pdf);;جميع الملفات (*)"
                )
                
                if not file_path:
                    return False
                
                if not file_path.lower().endswith('.pdf'):
                    file_path += '.pdf'
                
                # إنشاء الفاتورة وحفظها باستخدام المولد الجديد
                output_path = ArabicReceiptGenerator.generate_receipt(
                    self.preview_receipt_data, 
                    file_path
                )
                
                if output_path and os.path.exists(output_path):
                    QMessageBox.information(
                        self,
                        "تم التحميل",
                        f"تم حفظ الفاتورة بنجاح كملف PDF\n\nالموقع: {output_path}"
                    )
                    return True
                else:
                    QMessageBox.warning(self, "خطأ", "فشل إنشاء الفاتورة!")
                    return False
                    
            except ImportError:
                QMessageBox.warning(self, "غير متاح", "مولد الفواتير الجديد غير متوفر!")
                return False
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ:\n{str(e)}")
            return False
    
    def preview_receipt(self):
        """معاينة الفاتورة في نافذة منفصلة"""
        try:
            if not self.preview_receipt_data:
                QMessageBox.warning(self, "تحذير", "الرجاء إنشاء الفاتورة أولاً!")
                return
            
            # إنشاء نافذة المعاينة
            dialog = QDialog(self)
            dialog.setWindowTitle(f"معاينة الفاتورة - {self.preview_receipt_data['receipt_id']}")
            dialog.setFixedSize(800, 600)
            dialog.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            
            layout = QVBoxLayout()
            
            # عنوان النافذة
            title_label = QLabel(f"معاينة الفاتورة رقم: {self.preview_receipt_data['receipt_id']}")
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #2c3e50;
                    padding: 10px;
                    text-align: center;
                    background-color: #f8f9fa;
                    border-bottom: 2px solid #3498db;
                }
            """)
            layout.addWidget(title_label)
            
            # عرض الفاتورة كنص
            receipt_text = self.create_receipt_text(self.preview_receipt_data)
            
            text_edit = QTextEdit()
            text_edit.setPlainText(receipt_text)
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet("""
                QTextEdit {
                    font-family: 'Courier New', monospace;
                    font-size: 11px;
                    background-color: white;
                    border: 1px solid #ddd;
                    padding: 15px;
                    line-height: 1.4;
                    color: #333;
                }
            """)
            
            # إضافة إلى Scroll Area
            scroll_area = QScrollArea()
            scroll_area.setWidget(text_edit)
            scroll_area.setWidgetResizable(True)
            layout.addWidget(scroll_area)
            
            # أزرار
            button_layout = QHBoxLayout()
            
            # زر نسخ النص
            copy_btn = QPushButton("📋 نسخ النص")
            copy_btn.clicked.connect(lambda: text_edit.selectAll() or text_edit.copy())
            copy_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            button_layout.addWidget(copy_btn)
            
            button_layout.addStretch()
            
            # زر إغلاق
            close_btn = QPushButton("إغلاق")
            close_btn.clicked.connect(dialog.close)
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)
            button_layout.addWidget(close_btn)
            
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            
            # عرض النافذة
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل معاينة الفاتورة: {str(e)}")
    
    def update_receipt_info(self):
        """تحديث معلومات الفاتورة في الخطوة 4"""
        if not self.cart_items:
            self.receipt_preview_label.setText("لا توجد منتجات في السلة")
            return
        
        # إنشاء وعرض معاينة الفاتورة
        success = self.generate_receipt_preview()
        
        if not success:
            self.receipt_preview_label.setText("فشل إنشاء معاينة الفاتورة")
    
    def get_table_style(self):
        """إرجاع تنسيق موحد لجميع الجداول"""
        return """
            QTableWidget {
                background-color: white;
                alternate-background-color: #f5f5f5;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """
    
    def prev_step(self):
        if self.current_step > 1:
            self.current_step -= 1
            self.update_step()
    
    def next_step(self):
        if self.current_step == 1:
            # التحقق من اسم العميل
            customer_name = self.customer_name_input.text().strip()
            if not customer_name:
                QMessageBox.warning(self, "تحذير", "الرجاء إدخال اسم العميل!")
                return
            self.current_customer_name = customer_name
            
            # ✅ إنشاء الجدول الافتراضي عند الانتقال للخطوة 2
            if not self.create_virtual_table():
                QMessageBox.warning(self, "تحذير", "فشل تحميل المخزون الافتراضي!")
                return
            
            # حفظ البيانات من الحقول الجديدة
            self.current_customer_id = self.customer_code_input.text().strip() or (self.db.find_customer_id(customer_name) if hasattr(self.db, 'find_customer_id') else None)
            self.customer_address = self.address_input.text().strip()
            self.customer_notes = self.notes_input_step1.toPlainText().strip()
            
        elif self.current_step == 2:
            # التحقق من السلة
            if not self.cart_items:
                QMessageBox.warning(self, "تحذير", "الرجاء إضافة منتجات للسلة!")
                return
            
            # تحديث الإجماليات للخطوة 3
            if hasattr(self, 'calculate_totals'):
                self.calculate_totals()
            
        elif self.current_step == 3:
            # التحقق من المبلغ المدفوع
            amount_paid = self.amount_paid_input.value()
            if amount_paid < 0 or amount_paid > self.total_cumulative:
                QMessageBox.warning(self, "تحذير", "المبلغ المدفوع غير صحيح!")
                return
            
            self.total_paid_now = amount_paid
            self.total_remaining = self.total_cumulative - amount_paid
        
        if self.current_step < 4:
            self.current_step += 1
            self.update_step()
            
            # إذا انتقلنا للخطوة 4، نحدث عرض الفاتورة
            if self.current_step == 4:
                self.update_receipt_info()
    
    def update_step(self):
        self.stacked_widget.setCurrentIndex(self.current_step - 1)
        
        step_titles = [
            "الخطوة 1: معلومات العميل",
            "الخطوة 2: اختيار المنتجات",
            "الخطوة 3: الدفع والإجماليات",
            "الخطوة 4: تأكيد الفاتورة"
        ]
        self.step_label.setText(step_titles[self.current_step - 1])
        
        self.prev_btn.setEnabled(self.current_step > 1)
        
        if self.current_step == 4:
            # إخفاء زر التالي وإظهار الأزرار الجديدة في الخطوة 4
            self.next_btn.setVisible(False)
        else:
            self.next_btn.setVisible(True)
            self.next_btn.setText("التالي ←")
    
    def create_new_receipt(self):
        """إنشاء فاتورة جديدة"""
        # إعادة تعيين النموذج
        self.reset_form()
        
        # العودة إلى الخطوة الأولى
        self.current_step = 1
        self.update_step()
    
    def reset_form(self):
        """إعادة تعيين النموذج"""
        # مسح البيانات
        self.cart_items = []
        self.preview_receipt_data = None
        
        # ✅ إعادة تعيين الجدول الافتراضي
        self.reset_virtual_table()
        
        # إعادة تعيين الحقول الجديدة
        self.customer_code_input.clear()
        self.address_input.clear()
        self.notes_input_step1.clear()
        self.customer_name_input.clear()
        
        # إعادة تعيين حقول الخطوة 3
        self.previous_balance_input.setValue(0)
        self.amount_paid_input.setValue(0)
        
        # إعادة تعيين معلومات العميل
        self.current_customer_name = None
        self.current_customer_id = None
        self.customer_address = ""
        self.customer_notes = ""
        self.customer_previous_balance = 0
        
        # إعادة تعيين الإجماليات
        self.current_total = 0
        self.total_paid_now = 0
        self.total_cumulative = 0
        self.total_remaining = 0
        
        # إعادة تعيين الواجهة
        if isinstance(self.receipt_preview_label, QTextEdit):
            # إذا كان QTextEdit، إنشاء QLabel جديد
            layout = self.receipt_preview_label.parent().layout()
            if layout:
                for i in range(layout.count()):
                    widget = layout.itemAt(i).widget()
                    if widget == self.receipt_preview_label:
                        new_label = QLabel("جاري إنشاء معاينة الفاتورة...")
                        new_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        new_label.setMinimumHeight(350)
                        new_label.setStyleSheet("""
                            QLabel {
                                background-color: white;
                                border: 2px solid #ddd;
                                border-radius: 8px;
                                padding: 15px;
                                font-size: 14px;
                                color: #666;
                            }
                        """)
                        layout.replaceWidget(widget, new_label)
                        widget.deleteLater()
                        self.receipt_preview_label = new_label
                        break
        
        # ✅ تعطيل زر الحفظ فقط وإعادة تفعيل الأزرار الأخرى
        self.save_db_btn.setEnabled(False)
        self.download_image_btn.setEnabled(False)
        self.preview_btn.setEnabled(False)
        
        # إعادة تعيين النصوص
        self.save_db_btn.setText("💾 حفظ في قاعدة البيانات")
        
        # إظهار زر التالي
        self.next_btn.setVisible(True)
        
        # تحديث عرض السلة
        if hasattr(self, 'update_cart_display'):
            self.update_cart_display()
        
        # تحديث حقل المقاس
        if hasattr(self, 'size_filter_combo'):
            self.size_filter_combo.blockSignals(True)
            self.size_filter_combo.setCurrentIndex(0)
            self.size_filter_combo.blockSignals(False)
        
        # ✅ تحديث قائمة المنتجات (ستعرض الكميات الأصلية)
        if hasattr(self, 'item_combo'):
            self.load_items_combo()
        
        # تحديث معلومات العميل
        if hasattr(self, 'customer_info_label'):
            self.customer_info_label.setText("")
        
        # تحديث حقول الخطوة 3
        if hasattr(self, 'customer_summary_label'):
            self.customer_summary_label.setText("")
        
        if hasattr(self, 'current_total_label'):
            self.current_total_label.setText("0.00 ج.م")
        
        if hasattr(self, 'cumulative_total_label'):
            self.cumulative_total_label.setText("0.00 ج.م")
        
        if hasattr(self, 'remaining_invoice_label'):
            self.remaining_invoice_label.setText("0.00 ج.م")
        
        if hasattr(self, 'remaining_total_label'):
            self.remaining_total_label.setText("0.00 ج.م")
        
        if hasattr(self, 'payment_status_label'):
            self.payment_status_label.setText("غير مدفوع")
        
        if hasattr(self, 'range_label'):
            self.range_label.setText("المبلغ المسموح دفعه: 0.00 - 0.00 ج.م")
        
        # إعادة تعيين سعر البيع
        if hasattr(self, 'selling_price_input'):
            self.selling_price_input.setValue(0)
    
    def closeEvent(self, event):
        """❌ إغلاق النافذة مع إعادة تعيين الجدول الافتراضي"""
        # ✅ إعادة تعيين الجدول الافتراضي عند الإغلاق
        self.reset_virtual_table()
        event.accept()
    


    # ✅ دوال جديدة لحساب المتبقي الصحيح


class HistoryWindow(QWidget):
    """نافذة سجل المبيعات المحسنة بنظام الأقساط"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.is_editing = False
        self.original_only_mode = False  # متغير جديد للوضع الخاص
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        self.setWindowTitle('سجل المبيعات')
        self.setGeometry(150, 150, 1400, 750)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout()
        
        # العنوان
        title = QLabel("سجل فواتير المبيعات")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        # البحث والفلتر
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("بحث:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث برقم الفاتورة أو اسم العميل أو الكود")
        self.search_input.textChanged.connect(self.filter_history)
        filter_layout.addWidget(self.search_input)
        
        filter_layout.addWidget(QLabel("فلتر حسب العميل:"))
        self.customer_filter = QComboBox()
        self.customer_filter.addItem("جميع العملاء", None)
        self.customer_filter.setEditable(True)
        self.customer_filter.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        self.customer_filter.lineEdit().setPlaceholderText("اكتب للبحث أو اختر من القائمة")
        self.customer_filter.currentIndexChanged.connect(self.filter_history)
        filter_layout.addWidget(self.customer_filter)
        
        # فلتر التاريخ
        filter_layout.addWidget(QLabel("من تاريخ:"))
        self.date_from_filter = QDateEdit()
        self.date_from_filter.setDate(QDate.currentDate().addDays(-30))
        self.date_from_filter.setDisplayFormat("yyyy-MM-dd")
        self.date_from_filter.setCalendarPopup(True)
        self.date_from_filter.dateChanged.connect(self.filter_history)
        filter_layout.addWidget(self.date_from_filter)
        
        filter_layout.addWidget(QLabel("إلى تاريخ:"))
        self.date_to_filter = QDateEdit()
        self.date_to_filter.setDate(QDate.currentDate())
        self.date_to_filter.setDisplayFormat("yyyy-MM-dd")
        self.date_to_filter.setCalendarPopup(True)
        self.date_to_filter.dateChanged.connect(self.filter_history)
        filter_layout.addWidget(self.date_to_filter)
        
        # فلتر حالة الدفع - تم التصحيح
        filter_layout.addWidget(QLabel("حالة الدفع:"))
        self.payment_status_filter = QComboBox()
        self.payment_status_filter.addItem("جميع الحالات", "all")
        self.payment_status_filter.addItem("مدفوع بالكامل", "paid")
        self.payment_status_filter.addItem("سداد قسط", "payment")
        self.payment_status_filter.addItem("غير مدفوع", "unpaid")  # تم التصحيح من "لم يدفع" إلى "غير مدفوع"
        self.payment_status_filter.currentIndexChanged.connect(self.filter_history)
        filter_layout.addWidget(self.payment_status_filter)
        
        # زر فلتر الفواتير الأصلية فقط
        self.original_filter_btn = QPushButton("📋 الفواتير الأصلية فقط")
        self.original_filter_btn.setToolTip("إظهار الفواتير الأصلية فقط (بدون سجلات الأقساط)")
        self.original_filter_btn.setCheckable(True)  # جعله زر قابل للتحديد
        self.original_filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #bdc3c7;
                color: #2c3e50;
                padding: 8px 12px;
                border-radius: 5px;
                font-weight: bold;
                border: 2px solid #95a5a6;
            }
            QPushButton:checked {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
            }
            QPushButton:hover:!checked {
                background-color: #ecf0f1;
            }
        """)
        self.original_filter_btn.clicked.connect(self.toggle_original_filter)
        filter_layout.addWidget(self.original_filter_btn)
        
        layout.addLayout(filter_layout)
        
        # زر دفع للعميل مع مجموع المتبقي
        payment_layout = QHBoxLayout()
        
        # خانة دفع للعميل - بدون "ج.م"
        payment_to_customer_layout = QVBoxLayout()
        payment_to_customer_layout.addWidget(QLabel("دفع من العميل:"))
        
        self.payment_to_customer_input = QDoubleSpinBox()
        self.payment_to_customer_input.setDecimals(2)
        self.payment_to_customer_input.setMinimum(0.0)
        self.payment_to_customer_input.setMaximum(999999.99)
        # تم إزالة السطر التالي لإزالة "ج.م"
        # self.payment_to_customer_input.setPrefix("ج.م ")
        self.payment_to_customer_input.setValue(0.0)
        payment_to_customer_layout.addWidget(self.payment_to_customer_input)
        
        payment_layout.addLayout(payment_to_customer_layout)
        
        # ✅ (1) إضافة خانة "إضافة للمتبقي"
        add_to_remaining_layout = QVBoxLayout()
        add_to_remaining_layout.addWidget(QLabel("إضافة للمتبقي:"))
        
        self.add_to_remaining_input = QDoubleSpinBox()
        self.add_to_remaining_input.setDecimals(2)
        self.add_to_remaining_input.setMinimum(-999999.99)
        self.add_to_remaining_input.setMaximum(999999.99)
        self.add_to_remaining_input.setValue(0.0)
        add_to_remaining_layout.addWidget(self.add_to_remaining_input)
        
        # زر إضافة للمتبقي
        self.add_to_remaining_btn = QPushButton("➕ إضافة")
        self.add_to_remaining_btn.setToolTip("إضافة قيمة للمتبقي العام للعميل (للفواتير غير المسجلة)")
        self.add_to_remaining_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 8px 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.add_to_remaining_btn.clicked.connect(self.add_to_customer_remaining)
        add_to_remaining_layout.addWidget(self.add_to_remaining_btn)
        
        payment_layout.addLayout(add_to_remaining_layout)
        
        # زر تأكيد الدفع
        confirm_payment_btn = QPushButton("💳 تأكيد الدفع")
        confirm_payment_btn.setToolTip("توزيع المبلغ على فواتير العميل المحدد")
        confirm_payment_btn.setFixedWidth(120)
        confirm_payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 8px 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        confirm_payment_btn.clicked.connect(self.process_bulk_payment)
        payment_layout.addWidget(confirm_payment_btn)
        
        # خانة عرض مجموع المتبقي التلقائي
        self.remaining_sum_label = QLabel("مجموع المتبقي: 0.00 ج.م")
        self.remaining_sum_label.setStyleSheet("""
            QLabel {
                background-color: #2c3e50;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 250px;
                text-align: center;
                font-size: 14px;
            }
        """)
        payment_layout.addWidget(self.remaining_sum_label)
        
        # تم إزالة زر "حساب مجموع المتبقي" كما طلبت
        # self.calculate_btn = QPushButton("🧮 حساب مجموع المتبقي")
        # self.calculate_btn.setToolTip("حساب مجموع المتبقي للعميل المحدد")
        # self.calculate_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #3498db;
        #         color: white;
        #         padding: 8px 15px;
        #         border-radius: 5px;
        #         font-weight: bold;
        #     }
        #     QPushButton:hover {
        #         background-color: #2980b9;
        #     }
        # """)
        # self.calculate_btn.clicked.connect(self.calculate_customer_remaining)
        # payment_layout.addWidget(self.calculate_btn)
        
        # زر طباعة الكشف
        self.print_disclosure_btn = QPushButton("📋 طباعة الكشف")
        self.print_disclosure_btn.setToolTip("طباعة كشف حساب للعميل المحدد")
        self.print_disclosure_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.print_disclosure_btn.clicked.connect(self.generate_disclosure)
        payment_layout.addWidget(self.print_disclosure_btn)
        
        payment_layout.addStretch()
        layout.addLayout(payment_layout)
        
        # الجدول
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "رقم الفاتورة",
            "رقم العميل",
            "اسم العميل",
            "التاريخ",
            "المنتجات",
            "إجمالي الفاتورة",
            "المدفوع",
            "المتبقي",
            "الحالة",
            "طريقة الدفع"
        ])
        
        # ضبط عرض الأعمدة
        self.table.setColumnWidth(0, 140)  # رقم الفاتورة
        self.table.setColumnWidth(1, 100)  # رقم العميل
        self.table.setColumnWidth(2, 150)  # اسم العميل
        self.table.setColumnWidth(3, 120)  # التاريخ
        self.table.setColumnWidth(4, 350)  # المنتجات
        self.table.setColumnWidth(5, 120)  # إجمالي الفاتورة
        self.table.setColumnWidth(6, 100)  # المدفوع
        self.table.setColumnWidth(7, 120)  # المتبقي
        self.table.setColumnWidth(8, 100)  # الحالة
        self.table.setColumnWidth(9, 120)  # طريقة الدفع
        
        # تعيين ارتفاع الصفوف لاستيعاب المنتجات
        self.table.verticalHeader().setDefaultSectionSize(100)
        
        self.table.setStyleSheet(self.get_table_style())
        layout.addWidget(self.table)
        
        # إحصائيات
        stats_layout = QHBoxLayout()
        
        self.total_invoices_label = QLabel("عدد الفواتير: 0")
        self.total_amount_label = QLabel("إجمالي المبالغ: 0.00 ج.م")
        self.total_paid_label = QLabel("إجمالي المدفوع: 0.00 ج.م")
        self.total_remaining_label = QLabel("إجمالي المتبقي: 0.00 ج.م")
        
        for label in [self.total_invoices_label, self.total_amount_label, 
                    self.total_paid_label, self.total_remaining_label]:
            label.setStyleSheet("""
                QLabel {
                    background-color: #34495e;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 12px;
                    margin: 2px;
                }
            """)
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # أزرار التحكم
        button_layout = QHBoxLayout()
        
        # زر سداد قسط
        payment_btn = QPushButton("💰 سداد قسط")
        payment_btn.setToolTip("سداد قسط للفاتورة المحددة")
        payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        payment_btn.clicked.connect(self.process_payment)
        button_layout.addWidget(payment_btn)
        
        # زر طباعة PDF - تم التعديل
        print_pdf_btn = QPushButton("📄 طباعة PDF")
        print_pdf_btn.setToolTip("طباعة الفاتورة المحددة كـ PDF")
        print_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        print_pdf_btn.clicked.connect(self.print_selected_invoice_pdf_new)  # ✅ تغيير الدالة
        button_layout.addWidget(print_pdf_btn)
        
        # زر تعديل
        edit_btn = QPushButton("✏️ تعديل")
        edit_btn.setToolTip("تفعيل/تعطيل وضع التعديل")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        edit_btn.clicked.connect(self.toggle_edit_mode)
        button_layout.addWidget(edit_btn)
        
        # زر إضافة
        add_btn = QPushButton("➕ إضافة")
        add_btn.setToolTip("إضافة فاتورة جديدة")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        add_btn.clicked.connect(self.add_new_invoice)
        button_layout.addWidget(add_btn)
        
        # زر حذف
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.setToolTip("حذف الفاتورة المحددة")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_invoice)
        button_layout.addWidget(delete_btn)
        
        # زر حفظ
        save_btn = QPushButton("💾 حفظ")
        save_btn.setToolTip("حفظ جميع التغييرات")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        save_btn.clicked.connect(self.save_changes)
        button_layout.addWidget(save_btn)
        
        button_layout.addStretch()
        
        # زر الخروج
        exit_btn = QPushButton("خروج")
        exit_btn.setToolTip("إغلاق النافذة")
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6c7b7d;
            }
        """)
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def toggle_original_filter(self):
        """تبديل فلتر الفواتير الأصلية فقط"""
        self.original_only_mode = self.original_filter_btn.isChecked()
        
        if self.original_only_mode:
            self.original_filter_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 5px;
                    font-weight: bold;
                    border: 2px solid #2980b9;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            QMessageBox.information(self, "فلتر الفواتير الأصلية", 
                                  "تم تفعيل فلتر الفواتير الأصلية فقط\n\n"
                                  "سيتم إظهار الفواتير الأصلية فقط (بدون سجلات الأقساط)")
        else:
            self.original_filter_btn.setStyleSheet("""
                QPushButton {
                    background-color: #bdc3c7;
                    color: #2c3e50;
                    padding: 8px 12px;
                    border-radius: 5px;
                    font-weight: bold;
                    border: 2px solid #95a5a6;
                }
                QPushButton:hover {
                    background-color: #ecf0f1;
                }
            """)
        
        # تطبيق الفلتر الحالي
        self.filter_history()
    
    # ✅ (1) دالة جديدة: إضافة قيمة للمتبقي
    def add_to_customer_remaining(self):
        """إضافة قيمة للمتبقي العام للعميل (للفواتير غير المسجلة)"""
        selected_customer = self.customer_filter.currentData()
        
        if not selected_customer:
            QMessageBox.warning(self, "تحذير", "الرجاء تحديد عميل أولاً!")
            return
        
        amount = self.add_to_remaining_input.value()
        
        if amount == 0:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال قيمة للمتبقي!")
            return
        
        # الحصول على اسم العميل
        customer_name = ""
        for invoice in self.all_history:
            customer_id = invoice.get('customer_id', '')
            customer_code = invoice.get('customer_code', '')
            
            if customer_id == selected_customer or customer_code == selected_customer:
                customer_name = invoice.get('customer_name', '')
                break
        
        if not customer_name:
            QMessageBox.warning(self, "تحذير", "لم يتم العثور على بيانات العميل!")
            return
        
        # التحقق من وجود سجل متبقي غير مسجل للعميل
        remaining_found = False
        remaining_record = None
        
        for invoice in self.all_history:
            if (invoice.get('customer_id') == selected_customer or 
                invoice.get('customer_code') == selected_customer):
                receipt_id = invoice.get('receipt_id', '')
                if receipt_id.startswith('REM_'):  # سجل متبقي غير مسجل
                    remaining_found = True
                    remaining_record = invoice
                    break
        
        if remaining_found and remaining_record:
            # تحديث السجل الموجود
            old_remaining = float(remaining_record.get('remaining', 0))
            new_remaining = old_remaining + amount
            
            # تحديث القيمة
            remaining_record['remaining'] = new_remaining
            remaining_record['total'] = new_remaining  # الإجمالي نفس المتبقي
            
            # تحديث حالة الدفع
            if new_remaining <= 0:
                remaining_record['payment_status'] = "مدفوع بالكامل"
            else:
                remaining_record['payment_status'] = "غير مدفوع"
            
            # إضافة ملاحظة
            old_notes = remaining_record.get('notes', '')
            new_note = f"إضافة للمتبقي: {amount:+.2f} ج.م - {QDate.currentDate().toString('yyyy-MM-dd')}"
            if old_notes:
                remaining_record['notes'] = f"{old_notes}\n{new_note}"
            else:
                remaining_record['notes'] = new_note
        else:
            # إنشاء سجل جديد للمتبقي غير المسجل
            from datetime import datetime
            import random
            
            # إنشاء ID للسجل
            receipt_id = f"REM_{random.randint(1000, 9999)}"
            
            remaining_record = {
                'receipt_id': receipt_id,
                'customer_id': selected_customer,
                'customer_code': selected_customer,
                'customer_name': customer_name,
                'date': QDate.currentDate().toString('yyyy-MM-dd'),
                'items': json.dumps([{"name": "رصيد غير مسجل", "quantity": 1, "selling_price": amount}], ensure_ascii=False),
                'total': amount,
                'amount_paid': 0,
                'remaining': amount,
                'payment_status': "غير مدفوع" if amount > 0 else "مدفوع بالكامل",
                'payment_method': "نقدي",
                'notes': f"رصيد غير مسجل - إضافة: {amount:+.2f} ج.م",
                'original_receipt_id': "",
                'payment_amount': 0,
                'payment_count': 0
            }
            
            # إضافة السجل الجديد
            self.all_history.append(remaining_record)
        
        # حفظ التغييرات
        self.save_all_history()
        
        # إعادة تعيين الحقل
        self.add_to_remaining_input.setValue(0.0)
        
        # تحديث العرض
        self.load_history()
        
        # عرض رسالة تأكيد
        action = "مضافة" if amount > 0 else "مخصومة"
        QMessageBox.information(
            self, 
            "تمت العملية",
            f"تم {action} مبلغ {abs(amount):.2f} ج.م للمتبقي العام للعميل {customer_name}\n\n"
            f"المتبقي الجديد: {remaining_record['remaining']:.2f} ج.م"
        )
    
    def filter_history(self):
        """فلترة السجل مع دعم البحث بالاسم والكود"""
        search_text = self.search_input.text().strip().lower()
        selected_customer = self.customer_filter.currentData()
        payment_status_filter = self.payment_status_filter.currentText()
        date_from = self.date_from_filter.date().toString("yyyy-MM-dd")
        date_to = self.date_to_filter.date().toString("yyyy-MM-dd")
        
        filtered = []
        
        for invoice in self.all_history:
            # 1. فلتر البحث
            if search_text:
                search_match = False
                
                fields_to_search = [
                    invoice.get('receipt_id', ''),
                    invoice.get('customer_name', ''),
                    invoice.get('customer_id', ''),
                    invoice.get('customer_code', ''),
                    invoice.get('notes', '')
                ]
                
                for field in fields_to_search:
                    if search_text in str(field).lower():
                        search_match = True
                        break
                
                if not search_match:
                    continue
            
            # 2. فلتر العميل
            if selected_customer:
                customer_id = invoice.get('customer_id', '')
                customer_code = invoice.get('customer_code', '')
                if customer_id != selected_customer and customer_code != selected_customer:
                    continue
            
            # 3. فلتر التاريخ
            invoice_date = invoice.get('date', '')
            if invoice_date:
                try:
                    inv_date = QDate.fromString(invoice_date, "yyyy-MM-dd")
                    from_date = QDate.fromString(date_from, "yyyy-MM-dd")
                    to_date = QDate.fromString(date_to, "yyyy-MM-dd")
                    
                    if inv_date < from_date or inv_date > to_date:
                        continue
                except:
                    continue
            
            # 4. فلتر حالة الدفع
            if payment_status_filter != "جميع الحالات":
                current_status = invoice.get('payment_status', 'غير مدفوع')
                
                if current_status == "دفع جزئي":
                    current_status = "سداد قسط"
                
                if current_status != payment_status_filter:
                    continue
            
            # 5. فلتر الفواتير الأصلية فقط (إذا كان مفعل)
            if self.original_only_mode:
                receipt_id = invoice.get('receipt_id', '')
                if '.' in receipt_id:  # إذا كانت فاتورة قسط
                    continue
            
            filtered.append(invoice)
        
        self.display_history(filtered)
        self.update_statistics()
        self.update_remaining_summary()
    
    # ✅ (3) دالة جديدة لطباعة PDF بنفس دالة CreateReceiptWindow
    def print_selected_invoice_pdf_new(self):
        """طباعة الفاتورة المحددة كـ PDF باستخدام نفس دالة CreateReceiptWindow"""
        selected = self.table.currentRow()
        if selected >= 0:
            receipt_id = self.table.item(selected, 0).text()
            invoice = next((inv for inv in self.all_history if inv['receipt_id'] == receipt_id), None)
            
            if not invoice:
                QMessageBox.warning(self, "تحذير", "لم يتم العثور على الفاتورة!")
                return
            
            # إذا كانت فاتورة قسط، استخدم الفاتورة الأصلية
            if '.' in receipt_id:
                original_id = receipt_id.split('.')[0]
                original_invoice = next((inv for inv in self.all_history if inv['receipt_id'] == original_id), None)
                if original_invoice:
                    invoice = original_invoice
                else:
                    QMessageBox.warning(self, "تحذير", "لم يتم العثور على الفاتورة الأصلية!")
                    return
            
            # تحويل البيانات إلى تنسيق CreateReceiptWindow
            receipt_data = self.prepare_receipt_data_for_print_new(invoice)
            
            if not receipt_data:
                QMessageBox.warning(self, "تحذير", "فشل تحضير بيانات الفاتورة!")
                return
            
            # استخدام arabic_receipt_generator_new لإنشاء PDF بنفس الطريقة
            try:
                from arabic_receipt_generator_new import ArabicReceiptGenerator
                
                # اسم الملف الافتراضي
                default_name = f"فاتورة_{receipt_data['receipt_id']}.pdf"
                
                # اختيار مكان الحفظ
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "حفظ الفاتورة كملف PDF",
                    default_name,
                    "ملفات PDF (*.pdf);;جميع الملفات (*)"
                )
                
                if not file_path:
                    return False
                
                if not file_path.lower().endswith('.pdf'):
                    file_path += '.pdf'
                
                # إنشاء الفاتورة وحفظها باستخدام المولد الجديد
                output_path = ArabicReceiptGenerator.generate_receipt(
                    receipt_data, 
                    file_path
                )
                
                if output_path and os.path.exists(output_path):
                    QMessageBox.information(
                        self,
                        "تم التحميل",
                        f"تم حفظ الفاتورة بنجاح كملف PDF\n\nالموقع: {output_path}"
                    )
                    return True
                else:
                    QMessageBox.warning(self, "خطأ", "فشل إنشاء الفاتورة!")
                    return False
                    
            except ImportError:
                QMessageBox.warning(self, "غير متاح", "مولد الفواتير الجديد غير متوفر!")
                return False
        else:
            QMessageBox.warning(self, "تحذير", "الرجاء تحديد فاتورة أولاً!")
            return False

    # ✅ دالة جديدة لتحضير البيانات بنفس تنسيق CreateReceiptWindow
    def prepare_receipt_data_for_print_new(self, invoice):
        """تحضير بيانات الفاتورة للطباعة بنفس تنسيق CreateReceiptWindow"""
        try:
            # استخراج البيانات الأساسية
            receipt_id = invoice.get('receipt_id', '')
            customer_name = invoice.get('customer_name', 'غير محدد')
            customer_id = invoice.get('customer_id', '')
            date = invoice.get('date', datetime.now().strftime('%Y-%m-%d'))
            total = float(invoice.get('total', 0))
            amount_paid = float(invoice.get('amount_paid', 0))
            remaining = float(invoice.get('remaining', 0))
            payment_method = invoice.get('payment_method', 'نقدي')
            payment_status = invoice.get('payment_status', 'غير مدفوع')
            notes = invoice.get('notes', '')
            
            # الحقول الجديدة
            customer_code = invoice.get('customer_code', customer_id)
            customer_address = invoice.get('customer_address', '')
            customer_notes = invoice.get('customer_notes', '')
            receipt_code = invoice.get('receipt_code', receipt_id)
            
            # حساب الرصيد السابق والحالي
            previous_balance = 0
            current_balance = remaining
            
            # الحصول على فواتير العميل السابقة (قبل تاريخ هذه الفاتورة)
            customer_invoices = [inv for inv in self.all_history 
                            if (inv.get('customer_id') == customer_id or 
                                inv.get('customer_code') == customer_code) and 
                            inv.get('date', '') < date and
                            '.' not in inv.get('receipt_id', '')]  # فقط الفواتير الأصلية
            
            if customer_invoices:
                # حساب الرصيد السابق من الفواتير السابقة
                latest_previous_invoice = max(customer_invoices, key=lambda x: x.get('date', ''))
                previous_balance = float(latest_previous_invoice.get('remaining', 0))
            
            # تحويل المنتجات
            items_data = invoice.get('items', [])
            if isinstance(items_data, str):
                try:
                    items_data = json.loads(items_data)
                except:
                    items_data = []
            
            items = []
            for item in items_data:
                if isinstance(item, dict):
                    items.append({
                        'name': item.get('name', ''),
                        'size': item.get('size', ''),
                        'unit': item.get('unit', 'عدد'),
                        'quantity': int(item.get('quantity', 0)),
                        'selling_price': float(item.get('selling_price', 0))
                    })
                elif isinstance(item, list) and len(item) >= 3:
                    # تنسيق قديم للمنتجات
                    items.append({
                        'name': item[0] if len(item) > 0 else '',
                        'size': item[1] if len(item) > 1 else '',
                        'unit': 'عدد',
                        'quantity': int(item[2]) if len(item) > 2 else 0,
                        'selling_price': float(item[3]) if len(item) > 3 else 0
                    })
            
            # إذا لم يكن هناك منتجات، إضافة منتج افتراضي
            if not items:
                items.append({
                    'name': 'منتجات متنوعة',
                    'size': 'مختلف',
                    'unit': 'عدد',
                    'quantity': 1,
                    'selling_price': total
                })
            
            # حساب total_cumulative (الإجمالي الكلي)
            total_cumulative = previous_balance + total
            
            # إعداد بيانات الفاتورة الكاملة - بنفس تنسيق CreateReceiptWindow
            receipt_data = {
                'receipt_id': receipt_id,
                'customer_name': customer_name,
                'customer_id': customer_id,
                'customer_code': customer_code,
                'customer_address': customer_address,
                'date': date,
                'due_date': date,
                'customer_notes': customer_notes,
                'profit': 0,
                'receipt_code': receipt_code,
                'items': items,
                'total': total,
                'previous_balance': previous_balance,
                'total_cumulative': total_cumulative,
                'current_balance': current_balance,
                'amount_paid': amount_paid,
                'remaining': remaining,
                'payment_method': payment_method,
                'payment_status': payment_status,
                'notes': notes
            }
            
            return receipt_data
            
        except Exception as e:
            print(f"خطأ في تحضير بيانات الفاتورة: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_changes(self):
        """حفظ جميع التغييرات"""
        try:
            if self.is_editing:
                # تحديث البيانات من الجدول
                for row in range(self.table.rowCount()):
                    receipt_id = self.table.item(row, 0).text()
                    invoice = next((inv for inv in self.all_history if inv['receipt_id'] == receipt_id), None)
                    
                    if invoice:
                        try:
                            # تحديث المدفوع
                            paid_text = self.table.item(row, 6).text().replace(" ج.م", "").strip()
                            new_paid = float(paid_text)
                            
                            # تحديث المتبقي
                            remaining_text = self.table.item(row, 7).text().replace(" ج.م", "").strip()
                            new_remaining = float(remaining_text)
                            
                            # حساب الفرق في المدفوع
                            old_paid = float(invoice.get('amount_paid', 0))
                            payment_diff = new_paid - old_paid
                            
                            if payment_diff != 0:
                                # تحديث المبلغ المدفوع في هذه الفاتورة
                                invoice['amount_paid'] = new_paid
                                
                                # حساب المتبقي الجديد - التأكد من أنه لا يقل عن صفر
                                total_amount = float(invoice.get('total', 0))
                                new_remaining_calculated = total_amount - new_paid
                                
                                if new_remaining_calculated < 0:
                                    # إذا دفع أكثر من إجمالي الفاتورة، فالمتبقي يكون صفر
                                    new_remaining_calculated = 0
                                    # لا نغير المدفوع، نتركه كما هو للمستخدم
                                
                                invoice['remaining'] = new_remaining_calculated
                                
                                # تحديث حالة الدفع
                                if new_remaining_calculated <= 0:
                                    invoice['payment_status'] = "مدفوع بالكامل"
                                elif new_paid > 0:
                                    invoice['payment_status'] = "سداد قسط"
                                else:
                                    invoice['payment_status'] = "غير مدفوع"
                                    
                        except (ValueError, AttributeError):
                            continue
                
                # تعطيل وضع التعديل
                self.is_editing = False
                self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            
            # حفظ التغييرات في الملف
            self.save_all_history()
            
            QMessageBox.information(self, "نجاح", "تم حفظ جميع التغييرات بنجاح!")
            self.load_history()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ:\n{str(e)}")

    def get_table_style(self):
        return """
            QTableWidget {
                background-color: #1f2327;
                alternate-background-color: #272a2d;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """
    
    def save_all_history(self):
        """حفظ جميع فواتير المبيعات في قاعدة البيانات"""
        try:
            # تحضير البيانات للحفظ
            history_to_save = []
            
            for invoice in self.all_history:
                invoice_copy = invoice.copy()
                
                # تحويل العناصر إلى JSON إذا كانت list/dict
                if 'items' in invoice_copy and isinstance(invoice_copy['items'], (list, dict)):
                    import json
                    invoice_copy['items'] = json.dumps(invoice_copy['items'], ensure_ascii=False)
                
                # تحويل الأرقام إلى strings للتخزين في CSV
                numeric_fields = ['total', 'profit', 'amount_paid', 'remaining', 
                                'previous_balance', 'total_cumulative', 'current_balance']
                
                for field in numeric_fields:
                    if field in invoice_copy:
                        if isinstance(invoice_copy[field], (int, float)):
                            invoice_copy[field] = str(invoice_copy[field])
                        elif invoice_copy[field] is None:
                            invoice_copy[field] = '0'
                
                history_to_save.append(invoice_copy)
            
            # حفظ في قاعدة البيانات
            self.db.save_history(history_to_save)
            
            print(f"تم حفظ {len(history_to_save)} فاتورة في قاعدة البيانات")
            
        except Exception as e:
            print(f"خطأ في حفظ التاريخ: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def load_history(self):
        """تحميل سجل المبيعات"""
        history = self.db.load_history()
        
        # ترتيب الفواتير: الفواتير الأصلية أولاً ثم الأقساط مرتبة
        sorted_history = self.sort_invoices_hierarchically(history)
        self.all_history = sorted_history  # حفظ في المتغير العام
        
        # تحديث قائمة العملاء مع السماح بالكتابة الحرة
        self.customer_filter.clear()
        self.customer_filter.setEditable(True)
        self.customer_filter.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        self.customer_filter.lineEdit().setPlaceholderText("اكتب للبحث أو اختر من القائمة")
        
        # إضافة خيار "جميع العملاء"
        self.customer_filter.addItem("جميع العملاء", None)
        
        # إضافة العملاء الفريدين
        customers = {}
        for invoice in history:
            customer_name = invoice.get('customer_name', '')
            customer_id = invoice.get('customer_id', '')
            if customer_name and customer_id:
                if customer_id not in customers:
                    customers[customer_id] = customer_name
        
        for cid, cname in sorted(customers.items(), key=lambda x: x[1]):
            display_text = f"{cname} ({cid})"
            self.customer_filter.addItem(display_text, cid)
        
        self.display_history(self.all_history)
        self.update_statistics()
    
    def sort_invoices_hierarchically(self, invoices):
        """ترتيب الفواتير هرمياً: الفواتير الأصلية ثم الأقساط مرتبة"""
        try:
            if not invoices:
                return []
            
            # فصل الفواتير الأصلية عن الأقساط
            original_invoices = []
            payment_invoices = []
            
            for invoice in invoices:
                if not invoice:
                    continue
                    
                receipt_id = invoice.get('receipt_id', '')
                if '.' in receipt_id:
                    payment_invoices.append(invoice)
                else:
                    original_invoices.append(invoice)
            
            # ترتيب الفواتير الأصلية حسب التاريخ (الأحدث أولاً)
            original_invoices.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            # ترتيب الأقساط حسب الفاتورة الأصلية ورقم القسط
            payment_invoices.sort(key=lambda x: (
                x.get('original_receipt_id', x.get('receipt_id', '')),
                self.extract_payment_number(x.get('receipt_id', ''))
            ))
            
            # دمج القوائم مع إدراج الأقساط تحت الفواتير الأصلية
            sorted_invoices = []
            
            for original in original_invoices:
                sorted_invoices.append(original)
                original_id = original.get('receipt_id', '')
                
                # إضافة أقساط هذه الفاتورة
                for payment in payment_invoices:
                    payment_original_id = payment.get('original_receipt_id', '')
                    if not payment_original_id and '.' in payment.get('receipt_id', ''):
                        payment_original_id = payment['receipt_id'].split('.')[0]
                    
                    if payment_original_id == original_id:
                        sorted_invoices.append(payment)
            
            return sorted_invoices
            
        except Exception as e:
            print(f"خطأ في ترتيب الفواتير: {e}")
            return invoices
    
    def extract_payment_number(self, receipt_id):
        """استخراج رقم القسط من معرف الفاتورة"""
        if '.' in receipt_id:
            try:
                return int(receipt_id.split('.')[-1])
            except:
                return 0
        return 0
    
    def display_history(self, history):
        """عرض فواتير المبيعات في الجدول"""
        self.table.setRowCount(len(history))
        
        for i, invoice in enumerate(history):
            # رقم الفاتورة
            receipt_id = invoice['receipt_id']
            receipt_item = QTableWidgetItem(receipt_id)
            
            # تمييز الفواتير الأصلية عن الأقساط
            if '.' in receipt_id:
                receipt_item.setBackground(QColor("#e8f4f8"))  # لون فاتح للأقساط
                receipt_item.setForeground(QColor("#3498db"))  # لون أزرق
            elif receipt_id.startswith('REM_'):  # ✅ سجل متبقي غير مسجل
                receipt_item.setBackground(QColor("#fff3cd"))  # لون أصفر فاتح
                receipt_item.setForeground(QColor("#856404"))  # لون بني غامق
            else:
                receipt_item.setBackground(QColor("#e8f6e8"))  # لون فاتح للفواتير الأصلية
                receipt_item.setForeground(QColor("#27ae60"))  # لون أخضر
            
            self.table.setItem(i, 0, receipt_item)
            
            # رقم العميل
            customer_id = invoice.get('customer_id', '')
            if not customer_id:
                customer_id = invoice.get('customer_code', '')
            self.table.setItem(i, 1, QTableWidgetItem(customer_id))
            
            # اسم العميل
            self.table.setItem(i, 2, QTableWidgetItem(invoice.get('customer_name', '')))
            
            # التاريخ
            self.table.setItem(i, 3, QTableWidgetItem(invoice.get('date', '')))
            
            # المنتجات - تنسيق جديد
            items_data = invoice.get('items', [])
            if isinstance(items_data, str):
                try:
                    items_data = json.loads(items_data)
                except:
                    items_data = []
            
            products_text = self.format_products_text(items_data)
            products_item = QTableWidgetItem(products_text)
            products_item.setTextAlignment(Qt.AlignmentFlag.AlignTop)
            self.table.setItem(i, 4, products_item)
            
            # إجمالي الفاتورة (نستخدم total فقط، بدون previous_balance)
            total = float(invoice.get('total', 0))
            total_item = QTableWidgetItem(f"{total:.2f} ج.م")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 5, total_item)
            
            # المدفوع
            amount_paid = float(invoice.get('amount_paid', 0))
            paid_item = QTableWidgetItem(f"{amount_paid:.2f} ج.م")
            paid_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if amount_paid > 0:
                paid_item.setForeground(QColor("#27ae60"))
            self.table.setItem(i, 6, paid_item)
            
            # المتبقي للفاتورة فقط (بدون المتبقي الكلي)
            remaining = float(invoice.get('remaining', 0))
            remaining_item = QTableWidgetItem(f"{remaining:.2f} ج.م")
            remaining_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if remaining > 0:
                remaining_item.setForeground(QColor("#e74c3c"))
            self.table.setItem(i, 7, remaining_item)
            
            # الحالة
            payment_status = invoice.get('payment_status', 'غير مدفوع')
            
            # تحويل حالة "دفع جزئي" إلى "سداد قسط"
            if payment_status == "دفع جزئي":
                payment_status = "سداد قسط"
            
            status_item = QTableWidgetItem(payment_status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # تلوين حسب الحالة
            if payment_status == "مدفوع بالكامل":
                status_item.setBackground(QColor("#27ae60"))
            elif payment_status == "سداد قسط":
                status_item.setBackground(QColor("#9b59b6"))
            else:
                status_item.setBackground(QColor("#e74c3c"))
            
            status_item.setForeground(QColor("white"))
            self.table.setItem(i, 8, status_item)
            
            # طريقة الدفع
            payment_method = invoice.get('payment_method', 'نقدي')
            self.table.setItem(i, 9, QTableWidgetItem(payment_method))
            
            # حفظ بيانات الفاتورة كبيانات إضافية للصف
            self.table.item(i, 0).setData(Qt.ItemDataRole.UserRole, invoice)
    
    def format_products_text(self, items):
        """تنسيق نص المنتجات للعرض في خلية واحدة - التنسيق الجديد"""
        if not items:
            return "لا توجد منتجات"
        
        lines = []
        for product in items:
            if isinstance(product, dict):
                name = product.get('name', 'غير معروف')
                size = product.get('size', '')
                selling_price = product.get('selling_price', 0.0)
                quantity = product.get('quantity', 0)
                
                line = f"[{name}, المقاس:{size}, البيع:{selling_price:.2f}, الكمية:{quantity}]"
            else:
                line = str(product)
            lines.append(line)
        
        return "\n".join(lines)
    
    def update_statistics(self):
        """تحديث الإحصائيات - حساب المتبقي من آخر قسط فقط لكل فاتورة"""
        filtered_count = self.table.rowCount()
        
        # استخدام قائمة الفواتير المفلترة
        filtered_invoices = []
        for row in range(filtered_count):
            invoice = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            if invoice:
                filtered_invoices.append(invoice)
        
        total_invoices = 0
        total_amount = 0
        total_paid = 0
        total_remaining = 0
        
        # تجميع الفواتير الأصلية
        original_invoices = {}
        for invoice in filtered_invoices:
            receipt_id = invoice.get('receipt_id', '')
            
            if '.' not in receipt_id:  # فاتورة أصلية
                original_receipt_id = receipt_id
                original_invoices[original_receipt_id] = {
                    'invoice': invoice,
                    'last_payment': invoice  # الفاتورة الأصلية هي آخر سجل افتراضي
                }
        
        # البحث عن آخر قسط لكل فاتورة
        for invoice in filtered_invoices:
            receipt_id = invoice.get('receipt_id', '')
            
            if '.' in receipt_id:  # سجل قسط
                original_receipt_id = invoice.get('original_receipt_id', '')
                if not original_receipt_id:
                    # محاولة استخراج الرقم الأصلي من ID
                    parts = receipt_id.split('.')
                    if len(parts) > 1:
                        original_receipt_id = parts[0]
                
                if original_receipt_id in original_invoices:
                    # استخراج رقم القسط
                    payment_number = self.extract_payment_number(receipt_id)
                    # استخراج رقم آخر قسط مسجل
                    last_payment_id = original_invoices[original_receipt_id]['last_payment']['receipt_id']
                    last_payment_number = self.extract_payment_number(last_payment_id)
                    
                    # إذا كان هذا القسط أحدث
                    if payment_number > last_payment_number:
                        original_invoices[original_receipt_id]['last_payment'] = invoice
        
        # حساب الإحصائيات بناءً على آخر قسط لكل فاتورة
        for original_receipt_id, data in original_invoices.items():
            total_invoices += 1  # كل فاتورة أصلية تحسب مرة واحدة
            
            # إجمالي الفاتورة من الفاتورة الأصلية
            original_invoice = data['invoice']
            total_amount += float(original_invoice.get('total', 0))
            
            # استخدام آخر قسط للحساب
            last_payment = data['last_payment']
            
            # إجمالي المدفوع من آخر قسط
            last_payment_paid = float(last_payment.get('amount_paid', 0))
            total_paid += last_payment_paid
            
            # المتبقي من آخر قسط
            last_payment_remaining = float(last_payment.get('remaining', 0))
            total_remaining += last_payment_remaining
        
        # تحديث العناوين
        self.total_invoices_label.setText(f"عدد الفواتير: {total_invoices}")
        self.total_amount_label.setText(f"إجمالي المبالغ: {total_amount:.2f} ج.م")
        self.total_paid_label.setText(f"إجمالي المدفوع: {total_paid:.2f} ج.م")
        self.total_remaining_label.setText(f"إجمالي المتبقي: {total_remaining:.2f} ج.م")
    
    def calculate_customer_remaining(self):
        """حساب مجموع المتبقي للعميل المحدد - من آخر قسط فقط لكل فاتورة"""
        selected_customer = self.customer_filter.currentData()
        
        if not selected_customer:
            QMessageBox.warning(self, "تحذير", "الرجاء تحديد عميل أولاً!")
            return
        
        total_remaining = 0
        total_paid = 0
        customer_name = ""
        original_invoices = {}
        
        # تجميع فواتير العميل المحدد
        for invoice in self.all_history:
            customer_id = invoice.get('customer_id', '')
            customer_code = invoice.get('customer_code', '')
            
            if customer_id == selected_customer or customer_code == selected_customer:
                receipt_id = invoice.get('receipt_id', '')
                
                if '.' not in receipt_id:  # فاتورة أصلية
                    original_receipt_id = receipt_id
                    original_invoices[original_receipt_id] = {
                        'invoice': invoice,
                        'last_payment': invoice  # الفاتورة الأصلية هي آخر سجل افتراضي
                    }
                    if not customer_name:
                        customer_name = invoice.get('customer_name', '')
        
        # البحث عن آخر قسط لكل فاتورة
        for invoice in self.all_history:
            customer_id = invoice.get('customer_id', '')
            customer_code = invoice.get('customer_code', '')
            
            if customer_id == selected_customer or customer_code == selected_customer:
                receipt_id = invoice.get('receipt_id', '')
                
                if '.' in receipt_id:  # سجل قسط
                    original_receipt_id = invoice.get('original_receipt_id', '')
                    if not original_receipt_id:
                        parts = receipt_id.split('.')
                        if len(parts) > 1:
                            original_receipt_id = parts[0]
                    
                    if original_receipt_id in original_invoices:
                        # استخراج رقم القسط
                        payment_number = self.extract_payment_number(receipt_id)
                        # استخراج رقم آخر قسط مسجل
                        last_payment_id = original_invoices[original_receipt_id]['last_payment']['receipt_id']
                        last_payment_number = self.extract_payment_number(last_payment_id)
                        
                        # إذا كان هذا القسط أحدث
                        if payment_number > last_payment_number:
                            original_invoices[original_receipt_id]['last_payment'] = invoice
        
        # حساب المتبقي والإجماليات بناءً على آخر قسط
        for original_receipt_id, data in original_invoices.items():
            # استخدام آخر قسط للحساب
            last_payment = data['last_payment']
            
            # إجمالي المدفوع من آخر قسط
            last_payment_paid = float(last_payment.get('amount_paid', 0))
            total_paid += last_payment_paid
            
            # المتبقي من آخر قسط
            last_payment_remaining = float(last_payment.get('remaining', 0))
            total_remaining += last_payment_remaining
        
        # تحديث ملخص المتبقي
        self.update_remaining_summary()
        
        # عرض النتيجة
        result_text = f"العميل: {customer_name}\n"
        result_text += f"عدد الفواتير الأصلية: {len(original_invoices)}\n"
        result_text += f"إجمالي المتبقي (من آخر قسط لكل فاتورة): {total_remaining:.2f} ج.م\n"
        result_text += f"إجمالي المدفوع (من آخر قسط لكل فاتورة): {total_paid:.2f} ج.م"
        
        QMessageBox.information(self, "نتيجة الحساب", result_text)
    
    def update_remaining_summary(self):
        """تحديث ملخص المتبقي للعميل المحدد - من آخر قسط فقط"""
        selected_customer = self.customer_filter.currentData()
        
        if not selected_customer:
            self.remaining_sum_label.setText("مجموع المتبقي: 0.00 ج.م")
            self.payment_to_customer_input.setMaximum(0.0)
            self.print_disclosure_btn.setEnabled(False)
            self.add_to_remaining_btn.setEnabled(False)
            return
        
        # بدلاً من إعادة الحساب، استخدم نفس قيمة "إجمالي المتبقي" الموجودة في الأسفل
        # يمكننا استخراج القيمة من الملصق الموجود في الأسفل
        
        # الحصول على قيمة "إجمالي المتبقي" من الملصق في الأسفل
        total_remaining_text = self.total_remaining_label.text()
        
        # استخراج الرقم من النص باستخدام regex
        import re
        match = re.search(r'([\d,]+\.?\d*)', total_remaining_text)
        
        if match:
            # تحويل الرقم من نص (قد يحتوي على فواصل) إلى float
            total_remaining_str = match.group(1).replace(',', '')
            total_remaining = float(total_remaining_str)
        else:
            # إذا لم نتمكن من استخراج الرقم، استخدم الحساب القديم كبديل
            total_remaining = 0
            # (يمكنك إبقاء كود الحساب القديم هنا كنسخة احتياطية)
        
        # الحصول على اسم العميل للعرض
        customer_name = ""
        for invoice in self.all_history:
            customer_id = invoice.get('customer_id', '')
            customer_code = invoice.get('customer_code', '')
            
            if customer_id == selected_customer or customer_code == selected_customer:
                customer_name = invoice.get('customer_name', '')
                break
        
        # تحديث الملصق في الأعلى بنفس القيمة الموجودة في الأسفل
        self.remaining_sum_label.setText(f"مجموع المتبقي لـ {customer_name}: {total_remaining:.2f} ج.م")
        self.payment_to_customer_input.setMaximum(total_remaining)
        self.print_disclosure_btn.setEnabled(total_remaining > 0)
        self.add_to_remaining_btn.setEnabled(True)  # ✅ تفعيل زر إضافة للمتبقي
    
    def process_payment(self):
        """معالجة سداد قسط - مع الحفاظ على المتبقي الأصلي ثابتاً"""
        selected = self.table.currentRow()
        if selected >= 0:
            receipt_id = self.table.item(selected, 0).text()
            
            # البحث في جميع الفواتير
            invoice = None
            for inv in self.all_history:
                if inv['receipt_id'] == receipt_id:
                    invoice = inv
                    break
            
            if not invoice:
                QMessageBox.warning(self, "تحذير", "لم يتم العثور على الفاتورة!")
                return
            
            # تحديد الفاتورة الأصلية
            original_receipt_id = invoice.get('original_receipt_id', '')
            
            # إذا كانت فاتورة قسط، نحتاج إلى معرف الفاتورة الأصلية
            if '.' in receipt_id:
                # استخراج الرقم الأصلي من رقم الفاتورة
                parts = receipt_id.split('.')
                if len(parts) > 1:
                    original_receipt_id = parts[0]
            
            # إذا لم يكن هناك original_receipt_id، نستخدم receipt_id الحالي
            if not original_receipt_id:
                original_receipt_id = receipt_id
            
            # البحث عن الفاتورة الأصلية
            original_invoice = None
            for inv in self.all_history:
                if inv['receipt_id'] == original_receipt_id:
                    original_invoice = inv
                    break
            
            if not original_invoice:
                # إذا لم نجد الفاتورة الأصلية، نستخدم الفاتورة الحالية
                original_invoice = invoice
                original_receipt_id = receipt_id.split('.')[0] if '.' in receipt_id else receipt_id
            
            # حساب المتبقي الإجمالي للفاتورة الأصلية
            total_paid_in_payments = 0
            
            # حساب إجمالي المدفوع في الأقساط
            for inv in self.all_history:
                inv_id = inv.get('receipt_id', '')
                
                # إذا كانت فاتورة قسط تابعة للفاتورة الأصلية
                if '.' in inv_id:
                    parts = inv_id.split('.')
                    if len(parts) > 1 and parts[0] == original_receipt_id:
                        total_paid_in_payments += float(inv.get('amount_paid', 0))
                # أو إذا كانت تحمل original_receipt_id
                elif inv.get('original_receipt_id') == original_receipt_id:
                    total_paid_in_payments += float(inv.get('amount_paid', 0))
            
            # المتبقي الأصلي من الفاتورة الأصلية
            original_remaining = float(original_invoice.get('remaining', 0))
            
            # المتبقي المتبقي للدفع = المتبقي الأصلي - إجمالي المدفوع في الأقساط
            current_remaining = original_remaining - total_paid_in_payments
            
            # التأكد من أن current_remaining ليس سالباً
            if current_remaining < 0:
                current_remaining = 0
            
            if current_remaining <= 0:
                QMessageBox.warning(self, "تحذير", "هذه الفاتورة مدفوعة بالكامل!")
                return
            
            # نافذة سداد القسط
            dialog = QDialog(self)
            dialog.setWindowTitle(f"سداد قسط - فاتورة {original_receipt_id}")
            dialog.setGeometry(200, 200, 400, 350)
            dialog.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            
            layout = QVBoxLayout()
            
            # معلومات الفاتورة
            info_text = f"فاتورة أصلية: {original_receipt_id}\n"
            info_text += f"العميل: {original_invoice['customer_name']}\n"
            info_text += f"المتبقي الأصلي: {original_remaining:.2f} ج.م\n"
            info_text += f"المدفوع في الأقساط: {total_paid_in_payments:.2f} ج.م\n"
            info_text += f"المتبقي المتبقي للدفع: {current_remaining:.2f} ج.م\n"
            
            # حساب عدد الأقساط السابقة
            payment_count = 0
            for inv in self.all_history:
                if ('.' in inv.get('receipt_id', '') and 
                    inv['receipt_id'].split('.')[0] == original_receipt_id):
                    payment_count += 1
            
            info_text += f"عدد الأقساط السابقة: {payment_count}"
            
            info_label = QLabel(info_text)
            info_label.setStyleSheet("font-weight: bold; padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
            layout.addWidget(info_label)
            
            # مبلغ السداد - بدون "ج.م"
            layout.addWidget(QLabel("مبلغ السداد:"))
            payment_amount = QDoubleSpinBox()
            payment_amount.setDecimals(2)
            payment_amount.setMinimum(0.01)
            payment_amount.setMaximum(current_remaining)
            # تم إزالة السطر التالي
            # payment_amount.setPrefix("ج.م ")
            payment_amount.setValue(0.0)
            layout.addWidget(payment_amount)
            
            # تاريخ السداد
            layout.addWidget(QLabel("تاريخ السداد:"))
            payment_date = QDateEdit()
            payment_date.setDate(QDate.currentDate())
            payment_date.setCalendarPopup(True)
            payment_date.setDisplayFormat("yyyy-MM-dd")
            layout.addWidget(payment_date)
            
            # طريقة الدفع
            layout.addWidget(QLabel("طريقة الدفع:"))
            payment_method_combo = QComboBox()
            payment_method_combo.addItems(["نقدي", "شيك", "تحويل بنكي", "بطاقة ائتمان"])
            layout.addWidget(payment_method_combo)
            
            # ملاحظات
            layout.addWidget(QLabel("ملاحظات:"))
            payment_notes = QTextEdit()
            payment_notes.setMaximumHeight(60)
            payment_notes.setPlaceholderText("ملاحظات حول السداد...")
            layout.addWidget(payment_notes)
            
            # أزرار
            button_layout = QHBoxLayout()
            
            save_btn = QPushButton("💾 حفظ السداد")
            save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
            """)
            
            def save_payment():
                try:
                    amount = payment_amount.value()
                    date = payment_date.date().toString('yyyy-MM-dd')
                    method = payment_method_combo.currentText()
                    notes = payment_notes.toPlainText()
                    
                    if amount <= 0:
                        QMessageBox.warning(dialog, "تحذير", "الرجاء إدخال مبلغ صحيح!")
                        return
                    
                    if amount > current_remaining:
                        QMessageBox.warning(dialog, "تحذير", "المبلغ أكبر من المتبقي المتبقي للدفع!")
                        return
                    
                    # حساب رقم القسط التالي
                    new_payment_count = payment_count + 1
                    
                    # إنشاء ID جديد للمستند المنسوخ - تحويل new_payment_count إلى str
                    new_receipt_id = f"{original_receipt_id}.{str(new_payment_count)}"
                    
                    # التحقق من عدم وجود هذا الرقم مسبقاً
                    existing_ids = {inv['receipt_id'] for inv in self.all_history}
                    counter = 1
                    while new_receipt_id in existing_ids:
                        new_payment_count += 1
                        new_receipt_id = f"{original_receipt_id}.{str(new_payment_count)}"
                        counter += 1
                        if counter > 100:
                            raise Exception("تعذر إنشاء رقم فاتورة جديد")
                    
                    # إنشاء سجل منسوخ للسداد
                    payment_invoice = original_invoice.copy()
                    payment_invoice['receipt_id'] = new_receipt_id
                    payment_invoice['date'] = date
                    payment_invoice['original_receipt_id'] = original_receipt_id
                    payment_invoice['payment_amount'] = amount
                    payment_invoice['payment_count'] = new_payment_count
                    payment_invoice['payment_method'] = method
                    
                    # المدفوع في سجل القسط = المبلغ المدفوع في هذه الدفعة
                    payment_invoice['amount_paid'] = amount
                    
                    # حساب المتبقي المتبقي بعد هذه الدفعة
                    remaining_after_payment = current_remaining - amount
                    payment_invoice['remaining'] = remaining_after_payment
                    
                    # تحديث حالة الدفع لسجل القسط
                    if remaining_after_payment <= 0:
                        payment_invoice['payment_status'] = "مدفوع بالكامل"
                    else:
                        payment_invoice['payment_status'] = "سداد قسط"
                    
                    # إضافة ملاحظات السداد
                    if notes:
                        old_notes = str(payment_invoice.get('notes', ''))
                        if old_notes:
                            payment_invoice['notes'] = f"{old_notes}\nسداد: {amount} ج.م - {date} - {method} - {notes}"
                        else:
                            payment_invoice['notes'] = f"سداد: {amount} ج.م - {date} - {method} - {notes}"
                    
                    # إضافة سجل القسط إلى القائمة
                    self.all_history.append(payment_invoice)
                    
                    # إعادة ترتيب الفواتير
                    self.all_history = self.sort_invoices_hierarchically(self.all_history)
                    
                    # حفظ التغييرات
                    self.save_all_history()
                    
                    # تحديث الملخص
                    self.update_remaining_summary()
                    
                    QMessageBox.information(dialog, "نجاح", 
                                        f"تم حفظ السداد بنجاح!\n\n"
                                        f"رقم سجل القسط: {new_receipt_id}\n"
                                        f"الفاتورة الأصلية: {original_receipt_id}\n"
                                        f"المبلغ المدفوع: {amount:.2f} ج.م\n"
                                        f"المتبقي المتبقي بعد السداد: {remaining_after_payment:.2f} ج.م")
                    
                    dialog.close()
                    self.load_history()
                    
                except Exception as e:
                    QMessageBox.critical(dialog, "خطأ", f"حدث خطأ أثناء حفظ السداد:\n{str(e)}")
            
            save_btn.clicked.connect(save_payment)
            button_layout.addWidget(save_btn)
            
            cancel_btn = QPushButton("إلغاء")
            cancel_btn.clicked.connect(dialog.close)
            button_layout.addWidget(cancel_btn)
            
            layout.addLayout(button_layout)
            dialog.setLayout(layout)
            dialog.exec()
    
    # ✅ (2) تعديل دالة process_bulk_payment
    def process_bulk_payment(self):
        """معالجة دفع مبلغ من العميل المحدد - العمل على آخر قسط فقط"""
        try:
            selected_customer = self.customer_filter.currentData()
            
            if not selected_customer:
                QMessageBox.warning(self, "تحذير", "الرجاء تحديد عميل أولاً!")
                return
            
            payment_amount = self.payment_to_customer_input.value()
            
            if payment_amount <= 0:
                QMessageBox.warning(self, "تحذير", "الرجاء إدخال مبلغ صحيح للدفع!")
                return
            
            # الحصول على اسم العميل
            customer_name = ""
            for invoice in self.all_history:
                customer_id = invoice.get('customer_id', '')
                customer_code = invoice.get('customer_code', '')
                
                if customer_id == selected_customer or customer_code == selected_customer:
                    customer_name = invoice.get('customer_name', '')
                    break
            
            if not customer_name:
                QMessageBox.warning(self, "تحذير", "لم يتم العثور على بيانات العميل!")
                return
            
            # التحقق من حالة جميع الفواتير
            all_invoices_paid = True
            original_invoices = {}
            
            # تجميع فواتير العميل المحدد
            for invoice in self.all_history:
                customer_id = invoice.get('customer_id', '')
                customer_code = invoice.get('customer_code', '')
                
                if customer_id == selected_customer or customer_code == selected_customer:
                    receipt_id = invoice.get('receipt_id', '')
                    
                    if '.' not in receipt_id and not receipt_id.startswith('REM_'):  # فاتورة أصلية
                        # التحقق من حالة الدفع
                        payment_status = invoice.get('payment_status', 'غير مدفوع')
                        if payment_status != "مدفوع بالكامل":
                            all_invoices_paid = False
                            original_receipt_id = receipt_id
                            original_invoices[original_receipt_id] = {
                                'invoice': invoice,
                                'last_payment': invoice  # الفاتورة الأصلية هي آخر سجل افتراضي
                            }
            
            # ✅ الحالة (2): إذا كانت جميع الفواتير مدفوعة بالكامل والمتبقي لا يساوي صفر
            if all_invoices_paid:
                # البحث عن سجل المتبقي غير المسجل (REM_)
                remaining_record = None
                for invoice in self.all_history:
                    if (invoice.get('customer_id') == selected_customer or 
                        invoice.get('customer_code') == selected_customer):
                        receipt_id = invoice.get('receipt_id', '')
                        if receipt_id.startswith('REM_'):
                            remaining_record = invoice
                            break
                
                if remaining_record:
                    # خصم المبلغ من سجل المتبقي غير المسجل
                    old_remaining = float(remaining_record.get('remaining', 0))
                    
                    if payment_amount > old_remaining:
                        QMessageBox.warning(
                            self,
                            "تحذير",
                            f"المبلغ المدفوع ({payment_amount:.2f} ج.م) أكبر من المتبقي ({old_remaining:.2f} ج.م)!"
                        )
                        return
                    
                    new_remaining = old_remaining - payment_amount
                    
                    # تحديث سجل المتبقي
                    remaining_record['remaining'] = new_remaining
                    remaining_record['amount_paid'] = float(remaining_record.get('amount_paid', 0)) + payment_amount
                    
                    # تحديث حالة الدفع
                    if new_remaining <= 0:
                        remaining_record['payment_status'] = "مدفوع بالكامل"
                    else:
                        remaining_record['payment_status'] = "سداد قسط"
                    
                    # إضافة ملاحظة
                    old_notes = remaining_record.get('notes', '')
                    new_note = f"دفع من العميل: {payment_amount:.2f} ج.م - {QDate.currentDate().toString('yyyy-MM-dd')}"
                    if old_notes:
                        remaining_record['notes'] = f"{old_notes}\n{new_note}"
                    else:
                        remaining_record['notes'] = new_note
                    
                    # حفظ التغييرات
                    self.save_all_history()
                    
                    # إعادة تعيين الحقل
                    self.payment_to_customer_input.setValue(0.0)
                    
                    # تحديث العرض
                    self.load_history()
                    
                    QMessageBox.information(
                        self,
                        "تمت العملية",
                        f"تم خصم مبلغ {payment_amount:.2f} ج.م من المتبقي العام\n\n"
                        f"المتبقي الجديد: {new_remaining:.2f} ج.م"
                    )
                    return
                else:
                    # لا يوجد سجل متبقي، إنشاء سجل جديد
                    from datetime import datetime
                    import random
                    
                    receipt_id = f"REM_{random.randint(1000, 9999)}"
                    
                    remaining_record = {
                        'receipt_id': receipt_id,
                        'customer_id': selected_customer,
                        'customer_code': selected_customer,
                        'customer_name': customer_name,
                        'date': QDate.currentDate().toString('yyyy-MM-dd'),
                        'items': json.dumps([{"name": "رصيد غير مسجل", "quantity": 1, "selling_price": -payment_amount}], ensure_ascii=False),
                        'total': -payment_amount,
                        'amount_paid': payment_amount,
                        'remaining': -payment_amount,
                        'payment_status': "مدفوع بالكامل",
                        'payment_method': "نقدي",
                        'notes': f"دفع من العميل: {payment_amount:.2f} ج.م - جميع الفواتير مدفوعة",
                        'original_receipt_id': "",
                        'payment_amount': 0,
                        'payment_count': 0
                    }
                    
                    # إضافة السجل الجديد
                    self.all_history.append(remaining_record)
                    
                    # حفظ التغييرات
                    self.save_all_history()
                    
                    # إعادة تعيين الحقل
                    self.payment_to_customer_input.setValue(0.0)
                    
                    # تحديث العرض
                    self.load_history()
                    
                    QMessageBox.information(
                        self,
                        "تمت العملية",
                        f"تم تسجيل دفع {payment_amount:.2f} ج.م كرصيد زائد للعميل\n\n"
                        f"تم إنشاء سجل رصيد جديد: {receipt_id}"
                    )
                    return
            
            # إذا كانت هناك فواتير غير مدفوعة، المتابعة بالطريقة العادية
            # تجميع آخر قسط لكل فاتورة للعميل المحدد
            
            # أولاً: تجميع الفواتير الأصلية
            for invoice in self.all_history:
                customer_id = invoice.get('customer_id', '')
                customer_code = invoice.get('customer_code', '')
                
                if customer_id == selected_customer or customer_code == selected_customer:
                    receipt_id = invoice.get('receipt_id', '')
                    
                    if '.' not in receipt_id and not receipt_id.startswith('REM_'):  # فاتورة أصلية
                        original_receipt_id = receipt_id
                        original_invoices[original_receipt_id] = {
                            'invoice': invoice,
                            'last_payment': invoice  # الفاتورة الأصلية هي آخر سجل افتراضي
                        }
            
            # ثانياً: البحث عن آخر قسط لكل فاتورة
            for invoice in self.all_history:
                customer_id = invoice.get('customer_id', '')
                customer_code = invoice.get('customer_code', '')
                
                if customer_id == selected_customer or customer_code == selected_customer:
                    receipt_id = invoice.get('receipt_id', '')
                    
                    if '.' in receipt_id:  # سجل قسط
                        # استخراج الرقم الأصلي
                        parts = receipt_id.split('.')
                        if len(parts) > 1:
                            original_receipt_id = parts[0]
                            
                            if original_receipt_id in original_invoices:
                                # استخراج رقم القسط
                                try:
                                    payment_number = int(parts[1])
                                except ValueError:
                                    payment_number = 0
                                
                                # استخراج رقم آخر قسط مسجل
                                last_payment = original_invoices[original_receipt_id]['last_payment']
                                last_payment_id = last_payment.get('receipt_id', '')
                                
                                if '.' in last_payment_id:
                                    try:
                                        last_payment_parts = last_payment_id.split('.')
                                        if len(last_payment_parts) > 1:
                                            last_payment_number = int(last_payment_parts[1])
                                        else:
                                            last_payment_number = 0
                                    except ValueError:
                                        last_payment_number = 0
                                else:
                                    last_payment_number = 0
                                
                                # إذا كان هذا القسط أحدث
                                if payment_number > last_payment_number:
                                    original_invoices[original_receipt_id]['last_payment'] = invoice
            
            # تحويل إلى قائمة وترتيب حسب التاريخ
            last_payments_list = []
            for original_receipt_id, data in original_invoices.items():
                last_payment = data['last_payment']
                last_payments_list.append(last_payment)
            
            # ترتيب حسب التاريخ (الأقدم أولاً)
            last_payments_list.sort(key=lambda x: x.get('date', ''))
            
            # توزيع المبلغ على الفواتير بناءً على آخر قسط
            remaining_payment = payment_amount
            payment_records = []
            current_date = QDate.currentDate().toString('yyyy-MM-dd')
            
            for last_payment in last_payments_list:
                if remaining_payment <= 0:
                    break
                
                # الحصول على المتبقي من آخر قسط
                payment_remaining = float(last_payment.get('remaining', 0))
                if payment_remaining <= 0:
                    continue
                
                # حساب المبلغ المدفوع لهذه الفاتورة
                amount_to_pay = min(remaining_payment, payment_remaining)
                
                # الحصول على الفاتورة الأصلية
                receipt_id = last_payment.get('receipt_id', '')
                original_receipt_id = last_payment.get('original_receipt_id', '')
                
                # إذا كانت فاتورة قسط، استخرج الرقم الأصلي
                if '.' in receipt_id:
                    parts = receipt_id.split('.')
                    if len(parts) > 1:
                        original_receipt_id = parts[0]
                
                # إذا لم يكن هناك original_receipt_id، استخدم receipt_id
                if not original_receipt_id:
                    original_receipt_id = receipt_id.split('.')[0] if '.' in receipt_id else receipt_id
                
                # البحث عن الفاتورة الأصلية
                original_invoice = None
                for inv in self.all_history:
                    if inv['receipt_id'] == original_receipt_id:
                        original_invoice = inv
                        break
                
                if not original_invoice:
                    continue
                
                # حساب عدد الدفعات الحالية
                current_payment_count = 0
                for inv in self.all_history:
                    inv_id = inv.get('receipt_id', '')
                    if '.' in inv_id:
                        parts = inv_id.split('.')
                        if len(parts) > 1 and parts[0] == original_receipt_id:
                            current_payment_count += 1
                
                # حساب رقم القسط التالي
                payment_count = current_payment_count + 1
                
                # إنشاء سجل القسط الجديد
                new_receipt_id = f"{original_receipt_id}.{payment_count}"
                new_payment_invoice = original_invoice.copy()
                new_payment_invoice['receipt_id'] = new_receipt_id
                new_payment_invoice['date'] = current_date
                new_payment_invoice['original_receipt_id'] = original_receipt_id
                new_payment_invoice['payment_amount'] = amount_to_pay
                new_payment_invoice['payment_count'] = payment_count
                new_payment_invoice['amount_paid'] = amount_to_pay
                new_payment_invoice['payment_method'] = "نقدي"  # طريقة الدفع الافتراضية للدفع الجماعي
                
                # حساب المتبقي الجديد
                new_remaining = payment_remaining - amount_to_pay
                new_payment_invoice['remaining'] = new_remaining
                
                # تحديث حالة الدفع
                if new_remaining <= 0:
                    new_payment_invoice['payment_status'] = "مدفوع بالكامل"
                else:
                    new_payment_invoice['payment_status'] = "سداد قسط"
                
                # إضافة ملاحظات
                new_payment_invoice['notes'] = f"دفع جماعي من العميل: {amount_to_pay} ج.م - {current_date}"
                
                # تسجيل عملية الدفع
                payment_records.append({
                    'original_invoice': original_invoice,
                    'new_payment_invoice': new_payment_invoice,
                    'amount_paid': amount_to_pay,
                    'new_remaining': new_remaining
                })
                
                # إضافة سجل القسط الجديد
                self.all_history.append(new_payment_invoice)
                
                remaining_payment -= amount_to_pay
            
            # إعادة ترتيب الفواتير
            self.all_history = self.sort_invoices_hierarchically(self.all_history)
            
            # حفظ التغييرات
            self.save_all_history()
            
            # إعادة تعيين حقل الدفع
            self.payment_to_customer_input.setValue(0.0)
            
            # عرض ملخص الدفع
            summary = f"تم توزيع المبلغ على فواتير العميل:\n\n"
            summary += f"العميل: {customer_name}\n"
            summary += f"المبلغ المدفوع: {payment_amount:.2f} ج.م\n"
            summary += f"عدد الفواتير المدفوعة: {len(payment_records)}\n\n"
            
            if remaining_payment > 0:
                summary += f"ملاحظة: لم يتم استخدام {remaining_payment:.2f} ج.م لأن المبلغ أكبر من إجمالي المتبقي\n\n"
            
            for i, record in enumerate(payment_records, 1):
                original_invoice = record['original_invoice']
                summary += f"{i}. فاتورة {original_invoice['receipt_id']}: {record['amount_paid']:.2f} ج.م (متبقي بعد الدفع: {record['new_remaining']:.2f} ج.م)\n"
            
            QMessageBox.information(self, "ملخص الدفع", summary)
            
            # إعادة تحميل البيانات
            self.load_history()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء معالجة الدفع الجماعي:\n{str(e)}\n\nتفاصيل الخطأ: {traceback.format_exc()}")
            import traceback
            traceback.print_exc()
    
    def toggle_edit_mode(self):
        """تفعيل/تعطيل وضع التعديل"""
        self.is_editing = not self.is_editing
        
        if self.is_editing:
            # تفعيل وضع التعديل
            self.table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | 
                                     QAbstractItemView.EditTrigger.EditKeyPressed)
            
            # تمكين تحرير الأعمدة المحددة فقط
            for row in range(self.table.rowCount()):
                # السماح بتعديل المدفوع والمتبقي فقط
                for col in [6, 7]:  # المدفوع والمتبقي
                    item = self.table.item(row, col)
                    if item:
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            
            QMessageBox.information(self, "وضع التعديل", 
                                  "تم تفعيل وضع التعديل\n\n"
                                  "يمكنك الآن تعديل قيم المدفوع والمتبقي\n"
                                  "سيتم حفظ التغييرات عند الضغط على زر الحفظ")
        else:
            # تعطيل وضع التعديل
            self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            
            QMessageBox.information(self, "وضع التعديل", "تم تعطيل وضع التعديل")
    
    def add_new_invoice(self):
        """إضافة فاتورة جديدة"""
        self.create_window = CreateReceiptWindow(self.db)
        self.create_window.show()
        self.close()
    
    def delete_selected_invoice(self):
        """حذف الفاتورة المحددة"""
        selected = self.table.currentRow()
        if selected >= 0:
            receipt_id = self.table.item(selected, 0).text()
            invoice = next((inv for inv in self.all_history if inv['receipt_id'] == receipt_id), None)
            
            if not invoice:
                QMessageBox.warning(self, "خطأ", "لم يتم العثور على الفاتورة!")
                return
            
            customer_name = invoice.get('customer_name', 'غير معروف')
            
            # التحقق إذا كانت فاتورة سداد
            if '.' in receipt_id:
                original_id = receipt_id.split('.')[0]
                reply = QMessageBox.question(self, "تأكيد الحذف",
                                           f"هل أنت متأكد من حذف سجل السداد هذا؟\n\n"
                                           f"رقم الفاتورة: {receipt_id}\n"
                                           f"العميل: {customer_name}\n\n"
                                           f"ملاحظة: هذا سجل سداد للفاتورة الأصلية {original_id}",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    # حذف سجل السداد فقط
                    self.all_history = [inv for inv in self.all_history if inv['receipt_id'] != receipt_id]
                    
                    # حفظ التغييرات
                    self.save_all_history()
                    
                    QMessageBox.information(self, "نجاح", "تم حذف سجل السداد بنجاح!")
                    self.load_history()
            else:
                # فاتورة أصلية - التحقق من وجود أقساط
                has_payments = any(inv for inv in self.all_history 
                                 if (inv.get('original_receipt_id') == receipt_id or 
                                     ('.' in inv.get('receipt_id', '') and 
                                      inv['receipt_id'].split('.')[0] == receipt_id)) and 
                                 inv['receipt_id'] != receipt_id)
                
                if has_payments:
                    reply = QMessageBox.question(self, "تأكيد الحذف",
                                               f"تحذير: هذه الفاتورة لها سجلات سداد مرتبطة بها!\n\n"
                                               f"رقم الفاتورة: {receipt_id}\n"
                                               f"العميل: {customer_name}\n\n"
                                               f"هل تريد حذف الفاتورة وسجلات السداد المرتبطة بها؟",
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        # حذف الفاتورة الأصلية وجميع سجلات السداد المرتبطة بها
                        self.all_history = [inv for inv in self.all_history 
                                          if (inv.get('original_receipt_id') != receipt_id and 
                                              not ('.' in inv.get('receipt_id', '') and 
                                                   inv['receipt_id'].split('.')[0] == receipt_id))]
                        
                        # حفظ التغييرات
                        self.save_all_history()
                        
                        QMessageBox.information(self, "نجاح", "تم حذف الفاتورة وسجلات السداد المرتبطة بها بنجاح!")
                        self.load_history()
                else:
                    reply = QMessageBox.question(self, "تأكيد الحذف",
                                               f"هل أنت متأكد من حذف فاتورة المبيعات؟\n\n"
                                               f"رقم الفاتورة: {receipt_id}\n"
                                               f"العميل: {customer_name}",
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        # حذف الفاتورة الأصلية فقط
                        self.all_history = [inv for inv in self.all_history if inv['receipt_id'] != receipt_id]
                        
                        # حفظ التغييرات
                        self.save_all_history()
                        
                        QMessageBox.information(self, "نجاح", "تم حذف الفاتورة بنجاح!")
                        self.load_history()
    
    def save_changes(self):
        """حفظ جميع التغييرات"""
        try:
            if self.is_editing:
                # تحديث البيانات من الجدول
                for row in range(self.table.rowCount()):
                    receipt_id = self.table.item(row, 0).text()
                    invoice = next((inv for inv in self.all_history if inv['receipt_id'] == receipt_id), None)
                    
                    if invoice:
                        try:
                            # تحديث المدفوع
                            paid_text = self.table.item(row, 6).text().replace(" ج.م", "").strip()
                            new_paid = float(paid_text)
                            
                            # تحديث المتبقي
                            remaining_text = self.table.item(row, 7).text().replace(" ج.م", "").strip()
                            new_remaining = float(remaining_text)
                            
                            # حساب الفرق في المدفوع
                            old_paid = float(invoice.get('amount_paid', 0))
                            payment_diff = new_paid - old_paid
                            
                            if payment_diff != 0:
                                # تحديث المبلغ المدفوع في هذه الفاتورة
                                invoice['amount_paid'] = new_paid
                                
                                # حساب المتبقي الجديد - التأكد من أنه لا يقل عن صفر
                                total_amount = float(invoice.get('total', 0))
                                new_remaining_calculated = total_amount - new_paid
                                
                                if new_remaining_calculated < 0:
                                    # إذا دفع أكثر من إجمالي الفاتورة، فالمتبقي يكون صفر
                                    new_remaining_calculated = 0
                                    # لا نغير المدفوع، نتركه كما هو للمستخدم
                                
                                invoice['remaining'] = new_remaining_calculated
                                
                                # تحديث حالة الدفع
                                if new_remaining_calculated <= 0:
                                    invoice['payment_status'] = "مدفوع بالكامل"
                                elif new_paid > 0:
                                    invoice['payment_status'] = "سداد قسط"
                                else:
                                    invoice['payment_status'] = "غير مدفوع"
                                    
                        except (ValueError, AttributeError):
                            continue
                
                # تعطيل وضع التعديل
                self.is_editing = False
                self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            
            # حفظ التغييرات في الملف
            self.save_all_history()
            
            QMessageBox.information(self, "نجاح", "تم حفظ جميع التغييرات بنجاح!")
            self.load_history()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ:\n{str(e)}")
    
    def save_all_history(self):
        """حفظ جميع فواتير المبيعات في قاعدة البيانات"""
        # حفظ في قاعدة البيانات
        self.db.save_history(self.all_history)
    
    def generate_disclosure(self):
        """إنشاء كشف حساب للعميل المحدد"""
        from generate_disclosure_record import GenerateDisclosureRecord
        
        selected_customer = self.customer_filter.currentData()
        
        if not selected_customer:
            QMessageBox.warning(self, "تحذير", "الرجاء تحديد عميل أولاً!")
            return
        
        # الحصول على جميع فواتير العميل
        customer_invoices = []
        for invoice in self.all_history:
            customer_id = invoice.get('customer_id', '')
            customer_code = invoice.get('customer_code', '')
            
            if customer_id == selected_customer or customer_code == selected_customer:
                customer_invoices.append(invoice)
        
        if not customer_invoices:
            QMessageBox.warning(self, "تحذير", "لا توجد فواتير لهذا العميل!")
            return
        
        # استخراج الفواتير الأصلية فقط
        original_invoices = [inv for inv in customer_invoices if '.' not in inv.get('receipt_id', '')]
        
        if not original_invoices:
            QMessageBox.warning(self, "تحذير", "لا توجد فواتير أصلية لهذا العميل!")
            return
        
        # الحصول على اسم العميل
        customer_name = original_invoices[0].get('customer_name', '')
        
        # إنشاء كشف الحساب
        generator = GenerateDisclosureRecord()
        output_path = generator.generate_disclosure(
            customer_name=customer_name,
            customer_id=selected_customer,
            all_invoices=customer_invoices,  # جميع الفواتير (الأصلية والأقساط)
            original_invoices=original_invoices,  # الفواتير الأصلية فقط
            date_from=self.date_from_filter.date().toString("yyyy-MM-dd"),
            date_to=self.date_to_filter.date().toString("yyyy-MM-dd")
        )
        
        if output_path:
            QMessageBox.information(self, "نجاح", f"تم إنشاء كشف الحساب:\n{output_path}")
        else:
            QMessageBox.warning(self, "تحذير", "فشل إنشاء كشف الحساب!")

class ProfitAnalysisWindow(QWidget):
    """نافذة تحليل الأرباح مع تفاصيل المنتجات"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_analysis()
    
    def init_ui(self):
        self.setWindowTitle('تحليل الأرباح')
        self.setGeometry(150, 150, 1200, 700)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout()
        
        # العنوان
        title = QLabel("تحليل الأرباح بالتفصيل")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        # البحث والفلتر
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("بحث:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث برقم الفاتورة أو اسم العميل أو المنتج")
        self.search_input.textChanged.connect(self.filter_analysis)
        filter_layout.addWidget(self.search_input)
        
        filter_layout.addWidget(QLabel("من تاريخ:"))
        self.from_date = QDateEdit()
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        self.from_date.setCalendarPopup(True)
        filter_layout.addWidget(self.from_date)
        
        filter_layout.addWidget(QLabel("إلى تاريخ:"))
        self.to_date = QDateEdit()
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setCalendarPopup(True)
        filter_layout.addWidget(self.to_date)
        
        filter_btn = QPushButton("تطبيق الفلتر")
        filter_btn.clicked.connect(self.load_analysis)
        filter_layout.addWidget(filter_btn)
        
        layout.addLayout(filter_layout)
        
        # جدول تحليل الأرباح مع الأعمدة الجديدة
        self.table = QTableWidget()
        self.table.setColumnCount(10)  # 10 أعمدة بدلاً من 6 أو 7
        self.table.setHorizontalHeaderLabels([
            "رقم الفاتورة",
            "اسم العميل",    # العمود الجديد
            "التاريخ",
            "اسم المنتج",    # العمود الجديد
            "الكمية",        # العمود الجديد
            "سعر الشراء",
            "سعر البيع",
            "إجمالي البيع",
            "إجمالي الشراء",
            "الربح"
        ])
        self.table.setAlternatingRowColors(True)
        
        # ضبط عرض الأعمدة
        self.table.setColumnWidth(0, 100)  # رقم الفاتورة
        self.table.setColumnWidth(1, 150)  # اسم العميل
        self.table.setColumnWidth(2, 100)  # التاريخ
        self.table.setColumnWidth(3, 150)  # اسم المنتج
        self.table.setColumnWidth(4, 80)   # الكمية
        self.table.setColumnWidth(5, 100)  # سعر الشراء
        self.table.setColumnWidth(6, 100)  # سعر البيع
        self.table.setColumnWidth(7, 100)  # إجمالي البيع
        self.table.setColumnWidth(8, 100)  # إجمالي الشراء
        self.table.setColumnWidth(9, 100)  # الربح
        
        # تنسيق الجدول - الألوان القديمة (أسود وأزرق داكن)
        self.table.setStyleSheet(self.get_table_style())
        
        layout.addWidget(self.table)
        
        # الإحصائيات - 4 عناصر جديدة
        stats_layout = QHBoxLayout()
        
        self.total_profit_label = QLabel("إجمالي الأرباح: 0.00 ج.م")
        self.total_sales_label = QLabel("إجمالي المبيعات: 0.00 ج.م")
        self.total_items_label = QLabel("إجمالي المنتجات: 0")
        self.avg_profit_label = QLabel("متوسط الربح: 0.00 ج.م")
        
        for label in [self.total_profit_label, self.total_sales_label, 
                     self.total_items_label, self.avg_profit_label]:
            label.setStyleSheet("""
                QLabel {
                    background-color: #2c3e50;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                    margin: 2px;
                }
            """)
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        # أزرار بسيطة
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_btn.clicked.connect(self.load_analysis)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("إغلاق")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6c7b7d;
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_table_style(self):
        """إرجاع تنسيق موحد لجميع الجداول - الألوان القديمة"""
        return """
            QTableWidget {
                background-color: #1f2327;
                alternate-background-color: #272a2d;
                gridline-color: #d0d0d0;
                font-size: 11px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 6px;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #d0d0d0;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-right: 1px solid #34495e;
                border-bottom: 1px solid #34495e;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """
    
    def load_analysis(self):
        """تحميل وتحليل بيانات الأرباح"""
        try:
            # تحميل سجل المبيعات
            history = self.db.load_history()
            
            # فلترة حسب التاريخ
            from_date = self.from_date.date().toString('yyyy-MM-dd')
            to_date = self.to_date.date().toString('yyyy-MM-dd')
            
            # تحليل البيانات لكل منتج في كل فاتورة
            analysis_data = []
            total_profit = 0
            total_sales = 0
            total_items = 0
            
            for record in history:
                record_date = record.get('date', '')
                
                # تطبيق فلترة التاريخ
                if not (from_date <= record_date <= to_date):
                    continue
                
                receipt_id = record.get('receipt_id', '')
                customer_name = record.get('customer_name', 'غير محدد')
                
                items = record.get('items', [])
                
                for item in items:
                    item_name = item.get('name', 'غير معروف')
                    quantity = item.get('quantity', 0)
                    buying_price = item.get('buying_price', 0)
                    selling_price = item.get('selling_price', 0)
                    
                    # حسابات الربح
                    total_buying = buying_price * quantity
                    total_selling = selling_price * quantity
                    profit = total_selling - total_buying
                    
                    analysis_data.append({
                        'receipt_id': receipt_id,
                        'customer_name': customer_name,
                        'date': record_date,
                        'item_name': item_name,
                        'quantity': quantity,
                        'buying_price': buying_price,
                        'selling_price': selling_price,
                        'total_selling': total_selling,
                        'total_buying': total_buying,
                        'profit': profit
                    })
                    
                    # تحديث الإحصائيات
                    total_profit += profit
                    total_sales += total_selling
                    total_items += quantity
            
            # عرض البيانات في الجدول
            self.display_analysis(analysis_data)
            
            # تحديث الإحصائيات
            self.update_statistics(total_profit, total_sales, total_items, len(analysis_data))
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل تحميل التحليل: {str(e)}")
    
    def display_analysis(self, analysis_data):
        """عرض بيانات التحليل في الجدول"""
        self.table.setRowCount(len(analysis_data))
        
        for i, data in enumerate(analysis_data):
            # رقم الفاتورة
            self.table.setItem(i, 0, QTableWidgetItem(data['receipt_id']))
            
            # اسم العميل
            self.table.setItem(i, 1, QTableWidgetItem(data['customer_name']))
            
            # التاريخ
            self.table.setItem(i, 2, QTableWidgetItem(data['date']))
            
            # اسم المنتج
            self.table.setItem(i, 3, QTableWidgetItem(data['item_name']))
            
            # الكمية
            qty_item = QTableWidgetItem(str(data['quantity']))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 4, qty_item)
            
            # سعر الشراء
            buying_item = QTableWidgetItem(f"{data['buying_price']} ج.م")
            buying_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 5, buying_item)
            
            # سعر البيع
            selling_item = QTableWidgetItem(f"{data['selling_price']} ج.م")
            selling_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 6, selling_item)
            
            # إجمالي البيع
            total_selling_item = QTableWidgetItem(f"{data['total_selling']} ج.م")
            total_selling_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 7, total_selling_item)
            
            # إجمالي الشراء
            total_buying_item = QTableWidgetItem(f"{data['total_buying']} ج.م")
            total_buying_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 8, total_buying_item)
            
            # الربح مع تلوين
            profit_item = QTableWidgetItem(f"{data['profit']} ج.م")
            profit_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
            if data['profit'] > 0:
                profit_item.setForeground(QColor("#27ae60"))  # أخضر للربح
            elif data['profit'] < 0:
                profit_item.setForeground(QColor("#e74c3c"))  # أحمر للخسارة
            else:
                profit_item.setForeground(QColor("#7f8c8d"))  # رمادي
            
            self.table.setItem(i, 9, profit_item)
        
        # ترتيب حسب التاريخ (الأحدث أولاً)
        self.table.sortItems(2, Qt.SortOrder.DescendingOrder)
    
    def update_statistics(self, total_profit, total_sales, total_items, total_records):
        """تحديث الإحصائيات"""
        self.total_profit_label.setText(f"إجمالي الأرباح: {total_profit} ج.م")
        self.total_sales_label.setText(f"إجمالي المبيعات: {total_sales} ج.م")
        self.total_items_label.setText(f"إجمالي المنتجات: {total_items}")
        
        avg_profit = total_profit / total_records if total_records > 0 else 0
        self.avg_profit_label.setText(f"متوسط الربح: {avg_profit} ج.م")
    
    def filter_analysis(self):
        """فلترة البيانات حسب البحث"""
        search_text = self.search_input.text().strip().lower()
        
        if not search_text:
            # إذا كان البحث فارغاً، إعادة تحميل جميع البيانات
            self.load_analysis()
            return
        
        # فلترة البيانات المعروضة حالياً
        filtered_data = []
        
        # تجميع البيانات من الجدول الحالي
        for i in range(self.table.rowCount()):
            receipt_id = self.table.item(i, 0).text().lower()
            customer_name = self.table.item(i, 1).text().lower()
            item_name = self.table.item(i, 3).text().lower()
            
            # البحث في جميع الحقول
            if (search_text in receipt_id or 
                search_text in customer_name or 
                search_text in item_name):
                
                # استخراج البيانات من الصف
                data = {
                    'receipt_id': self.table.item(i, 0).text(),
                    'customer_name': self.table.item(i, 1).text(),
                    'date': self.table.item(i, 2).text(),
                    'item_name': self.table.item(i, 3).text(),
                    'quantity': int(self.table.item(i, 4).text()),
                    'buying_price': float(self.table.item(i, 5).text().replace(' ج.م', '')),
                    'selling_price': float(self.table.item(i, 6).text().replace(' ج.م', '')),
                    'total_selling': float(self.table.item(i, 7).text().replace(' ج.م', '')),
                    'total_buying': float(self.table.item(i, 8).text().replace(' ج.م', '')),
                    'profit': float(self.table.item(i, 9).text().replace(' ج.م', ''))
                }
                filtered_data.append(data)
        
        # إعادة حساب الإحصائيات للبيانات المفلترة
        total_profit = sum(item['profit'] for item in filtered_data)
        total_sales = sum(item['total_selling'] for item in filtered_data)
        total_items = sum(item['quantity'] for item in filtered_data)
        
        # عرض البيانات المفلترة
        self.table.setRowCount(len(filtered_data))
        
        for i, data in enumerate(filtered_data):
            # عرض البيانات بنفس الطريقة
            self.table.setItem(i, 0, QTableWidgetItem(data['receipt_id']))
            self.table.setItem(i, 1, QTableWidgetItem(data['customer_name']))
            self.table.setItem(i, 2, QTableWidgetItem(data['date']))
            self.table.setItem(i, 3, QTableWidgetItem(data['item_name']))
            
            qty_item = QTableWidgetItem(str(data['quantity']))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 4, qty_item)
            
            buying_item = QTableWidgetItem(f"{data['buying_price']} ج.م")
            buying_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 5, buying_item)
            
            selling_item = QTableWidgetItem(f"{data['selling_price']} ج.م")
            selling_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 6, selling_item)
            
            total_selling_item = QTableWidgetItem(f"{data['total_selling']} ج.م")
            total_selling_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 7, total_selling_item)
            
            total_buying_item = QTableWidgetItem(f"{data['total_buying']} ج.م")
            total_buying_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 8, total_buying_item)
            
            profit_item = QTableWidgetItem(f"{data['profit']} ج.م")
            profit_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            
            if data['profit'] > 0:
                profit_item.setForeground(QColor("#27ae60"))
            elif data['profit'] < 0:
                profit_item.setForeground(QColor("#e74c3c"))
            else:
                profit_item.setForeground(QColor("#7f8c8d"))
            
            self.table.setItem(i, 9, profit_item)
        
        # تحديث الإحصائيات
        self.update_statistics(total_profit, total_sales, total_items, len(filtered_data))



def convert_csv_to_utf8():
    """تحويل ملفات CSV إلى ترميز UTF-8"""
    files = ["history.csv", "items.csv", "imports.csv", "suppliers.csv"]
    
    for file in files:
        if os.path.exists(file):
            try:
                # قراءة الملف بترميزات مختلفة
                content = None
                encodings_to_try = ['utf-8-sig', 'utf-8', 'cp1256', 'cp1252', 'iso-8859-6']
                
                for encoding in encodings_to_try:
                    try:
                        with open(file, 'r', encoding=encoding) as f:
                            content = f.read()
                        print(f"[INFO] Read {file} with encoding: {encoding}")
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        continue
                
                if content is None:
                    print(f"[ERROR] Failed to read {file} with any encoding")
                    continue
                
                # كتابة الملف بترميز UTF-8
                with open(file, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                print(f"[SUCCESS] Converted {file} to UTF-8")
                
            except Exception as e:
                print(f"[ERROR] Error converting {file}: {str(e)}")


# ============================================================================
# التطبيق الرئيسي
# ============================================================================
# ============================================================================
# دوال مساعدة للترميز
# ============================================================================

def safe_encode(text: str) -> str:
    """ترميز آمن للنصوص العربية"""
    if not text:
        return ""
    # إزالة الرموز غير القابلة للطباعة والحفاظ على العربية
    return ''.join(char for char in str(text) 
                  if ord(char) < 10000 and (char.isprintable() or char.isalpha()))
def fix_encoding_issue():
    """إصلاح مشاكل الترميز في Windows"""
    import sys
    import io
    
    # تجاوز مشكلة الترميز في Windows
    if sys.platform == "win32":
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        except:
            pass
def main():
    app = QApplication(sys.argv)
    
    # إصلاح مشاكل الترميز
    fix_encoding_issue()
    
    # تعيين نمط التطبيق
    app.setStyle('Fusion')
    
    # تحويل ملفات CSV إلى UTF-8 قبل بدء التطبيق
    convert_csv_to_utf8()
    
    # إنشاء وعرض نافذة الرئيسية مباشرة
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())
if __name__ == '__main__':
    main()