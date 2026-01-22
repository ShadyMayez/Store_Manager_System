"""
generate_disclosure_record.py - مولد كشف حساب العميل (الإصدار المعدل)
"""

import os
import tempfile
from typing import List, Dict
from datetime import datetime

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display


class GenerateDisclosureRecord:
    """مولد كشف حساب العميل"""
    
    @staticmethod
    def safe_text(text: str) -> str:
        """تنظيف النص بطريقة آمنة"""
        if not text:
            return ""
        
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
    
    @staticmethod
    def format_arabic_simple(text: str) -> str:
        """تشكيل النص العربي بطريقة بسيطة"""
        try:
            if not text:
                return ""
            
            arabic_chars = set('ء-ي')
            has_arabic = any(c for c in str(text) if c in arabic_chars)
            
            if has_arabic:
                reshaped = arabic_reshaper.reshape(str(text))
                return get_display(reshaped)
            
            return str(text)
        except:
            return str(text)
    
    @staticmethod
    def extract_payment_records(all_invoices: List[Dict], original_receipt_id: str) -> List[Dict]:
        """استخراج سجلات الدفع (الأقساط) للفاتورة الأصلية"""
        payment_records = []
        
        for invoice in all_invoices:
            receipt_id = invoice.get('receipt_id', '')
            
            # التحقق إذا كان هذا سجل دفع للفاتورة الأصلية
            if '.' in receipt_id:
                # استخراج الرقم الأصلي من رقم الفاتورة
                parts = receipt_id.split('.')
                if len(parts) > 1 and parts[0] == original_receipt_id:
                    payment_records.append({
                        'receipt_id': receipt_id,
                        'date': invoice.get('date', ''),
                        'amount_paid': float(invoice.get('amount_paid', 0)),
                        'remaining': float(invoice.get('remaining', 0)),
                        'payment_status': invoice.get('payment_status', ''),
                        'payment_method': invoice.get('payment_method', '')
                    })
        
        # ترتيب الأقساط تصاعدياً حسب الرقم
        payment_records.sort(key=lambda x: int(x['receipt_id'].split('.')[1]) if '.' in x['receipt_id'] else 0)
        
        return payment_records
    
    @staticmethod
    def calculate_payment_status(amount_paid: float, remaining: float, total: float) -> str:
        """حساب حالة الدفع بناءً على المبالغ"""
        if amount_paid == 0:
            return "غير مدفوع"
        elif remaining != total and remaining != 0:
            return "مدفوع جزئيا"
        elif remaining == 0 and amount_paid == total:
            return "مدفوع بالكامل"
        else:
            return "غير مدفوع"
    
    @staticmethod
    def create_html_disclosure(customer_name: str, customer_id: str, 
                              all_invoices: List[Dict], original_invoices: List[Dict], 
                              date_from: str, date_to: str) -> str:
        """إنشاء HTML لكشف الحساب بالتنسيق الجديد"""
        
        # تنظيف النصوص
        customer_name_display = GenerateDisclosureRecord.safe_text(customer_name)
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # بناء جدول الفواتير
        invoices_html = ""
        total_all_amount = 0
        total_all_paid = 0
        total_all_remaining = 0
        
        for idx, original_invoice in enumerate(original_invoices):
            receipt_id = original_invoice.get('receipt_id', '')
            date = original_invoice.get('date', '')
            total = float(original_invoice.get('total', 0))
            amount_paid = float(original_invoice.get('amount_paid', 0))
            remaining = float(original_invoice.get('remaining', 0))
            
            # حساب حالة الدفع بناءً على المبالغ
            payment_status = GenerateDisclosureRecord.calculate_payment_status(amount_paid, remaining, total)
            
            # تحويل حالة الدفع
            if payment_status == "دفع جزئي":
                payment_status = "سداد قسط"
            
            # الحصول على سجلات الدفع لهذه الفاتورة
            payment_records = GenerateDisclosureRecord.extract_payment_records(all_invoices, receipt_id)
            
            # حساب المدفوع والمتبقي من الأقساط
            total_paid_from_payments = sum(p['amount_paid'] for p in payment_records)
            if payment_records:
                # استخدام آخر قسط للحساب
                last_payment = payment_records[-1]
                remaining = float(last_payment.get('remaining', 0))
                amount_paid = total_paid_from_payments
            
            # إعادة حساب حالة الدفع بعد التحديث
            payment_status = GenerateDisclosureRecord.calculate_payment_status(amount_paid, remaining, total)
            
            # إضافة إلى الإجماليات
            total_all_amount += total
            total_all_paid += amount_paid
            total_all_remaining += remaining
            
            # بناء جدول المنتجات لهذه الفاتورة
            items_data = original_invoice.get('items', [])
            if isinstance(items_data, str):
                try:
                    import json
                    items_data = json.loads(items_data)
                except:
                    items_data = []
            
            products_html = ""
            if items_data:
                products_html = """
                <table class="products-table">
                    <thead>
                        <tr>
                            <th>الصنف (المقاس)</th>
                            <th>الوحدة</th>
                            <th>الكمية</th>
                            <th>السعر</th>
                            <th>الإجمالي</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                
                for item in items_data:
                    if isinstance(item, dict):
                        name = GenerateDisclosureRecord.safe_text(item.get('name', ''))
                        size = item.get('size', '')
                        unit = item.get('unit', 'عدد')
                        quantity = item.get('quantity', 0)
                        selling_price = item.get('selling_price', 0.0)
                        subtotal = quantity * selling_price
                        
                        products_html += f"""
                        <tr>
                            <td>{name} ({size})</td>
                            <td>{unit}</td>
                            <td>{quantity}</td>
                            <td>{selling_price:.2f}</td>
                            <td>{subtotal:.2f}</td>
                        </tr>
                        """
                
                products_html += """
                    </tbody>
                </table>
                """
            
            # بناء جدول الأقساط
            payments_html = ""
            if payment_records:
                payments_html = """
                <div class="payments-section">
                    <div class="payments-title">جدول الأقساط</div>
                    <table class="payments-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>التاريخ</th>
                                <th>المبلغ المدفوع</th>
                                <th>المتبقي</th>
                                <th>الحالة</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                
                for i, payment in enumerate(payment_records, 1):
                    payment_status_display = payment.get('payment_status', '')
                    if payment_status_display == "دفع جزئي":
                        payment_status_display = "سداد قسط"
                    
                    payments_html += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{payment.get('date', '')}</td>
                        <td>{payment.get('amount_paid', 0):.2f} ج.م</td>
                        <td>{payment.get('remaining', 0):.2f} ج.م</td>
                        <td>{payment_status_display}</td>
                    </tr>
                    """
                
                payments_html += """
                        </tbody>
                    </table>
                </div>
                """
            
            # ملخص الفاتورة في سطر واحد
            summary_html = f"""
            <div class="invoice-summary-single">
                <span class="summary-item">إجمالي الفاتورة: {total:.2f} ج.م</span>
                <span class="summary-item">المدفوع: {amount_paid:.2f} ج.م</span>
                <span class="summary-item">المتبقي: {remaining:.2f} ج.م</span>
                <span class="summary-item">حالة الدفع: {payment_status}</span>
            </div>
            """
            
            invoices_html += f"""
            <div class="invoice-section">
                <div class="invoice-header">
                    <span class="invoice-id">فاتورة رقم: {receipt_id}</span>
                    <span class="invoice-date">التاريخ: {date}</span>
                </div>
                
                <div class="invoice-products">
                    {products_html}
                </div>
                
                {payments_html}
                
                {summary_html}
                
                <div class="invoice-divider"></div>
            </div>
            """
        
        # HTML النهائي
        html_template = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>كشف حساب - {customer_name_display}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Lateef:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4 portrait;
            margin: 8mm 12mm 8mm 12mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Amiri', 'Lateef', serif;
            line-height: 1.3;
            color: #000000;
        }}
        
        body {{
            font-family: 'Amiri', serif;
            direction: rtl;
            text-align: right;
            background: white;
            color: #000000;
            padding: 0;
            width: 100%;
            max-width: 210mm;
            margin: 0 auto;
            font-size: 14px;
        }}
        
        .disclosure-container {{
            width: 100%;
            padding: 0;
            background: white;
        }}
        
        /* عنوان الشركة */
        .company-header {{
            text-align: center;
            margin-bottom: 10px;
            padding: 8px 0;
        }}
        
        .company-name {{
            font-size: 28px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 3px;
        }}
        
        .company-subtitle {{
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        }}
        
        /* عنوان الكشف */
        .disclosure-title {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 12px 0;
            color: #000000;
        }}
        
        /* معلومات العميل */
        .customer-info {{
            text-align: center;
            padding: 12px;
            margin-bottom: 15px;
            border: 2px solid #000000;
            border-radius: 5px;
            background: #f8f9fa;
            page-break-inside: avoid;
        }}
        
        .customer-name {{
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        }}
        
        .customer-id {{
            font-size: 16px;
            color: #000000;
        }}
        
        .date-range {{
            font-size: 15px;
            color: #000000;
            margin-top: 6px;
        }}
        
        /* قسم الفاتورة */
        .invoice-section {{
            margin-bottom: 22px;
            padding: 12px;
            border: 2px solid #000000;
            border-radius: 5px;
        }}
        
        .invoice-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #000000;
        }}
        
        .invoice-id {{
            font-weight: bold;
            color: #000000;
            font-size: 16px;
        }}
        
        .invoice-date {{
            color: #000000;
            font-size: 16px;
        }}
        
        /* جدول المنتجات */
        .products-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 14px;
            border: 2px solid #000000;
        }}
        
        .products-table th {{
            background: #f0f0f0;
            color: #000000;
            padding: 8px 5px;
            text-align: center;
            font-weight: bold;
            border: 2px solid #000000;
            font-size: 15px;
        }}
        
        .products-table td {{
            padding: 7px 5px;
            text-align: center;
            border: 1px solid #000000;
            font-size: 14px;
            color: #000000;
        }}
        
        /* قسم الأقساط */
        .payments-section {{
            margin: 18px 0;
        }}
        
        .payments-title {{
            font-size: 16px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 2px solid #000000;
        }}
        
        .payments-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8px 0;
            font-size: 13px;
            border: 2px solid #000000;
        }}
        
        .payments-table th {{
            background: #e8f4f8;
            color: #000000;
            padding: 6px 4px;
            text-align: center;
            font-weight: bold;
            border: 2px solid #000000;
            font-size: 14px;
        }}
        
        .payments-table td {{
            padding: 5px 4px;
            text-align: center;
            border: 1px solid #000000;
            font-size: 13px;
            color: #000000;
        }}
        
        /* ملخص الفاتورة في سطر واحد */
        .invoice-summary-single {{
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin: 18px 0 8px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            border: 2px solid #000000;
        }}
        
        .summary-item {{
            margin: 0 8px;
            font-weight: bold;
            font-size: 14px;
            color: #000000;
        }}
        
        .invoice-divider {{
            border-top: 2px dashed #000000;
            margin: 18px 0;
        }}
        
        /* الإجماليات النهائية */
        .final-totals {{
            margin: 25px 0;
            padding: 18px;
            border: 3px solid #000000;
            border-radius: 5px;
            background: #f8f9fa;
        }}
        
        .final-total {{
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin: 8px 0;
        }}
        
        .total-label {{
            color: #000000;
        }}
        
        .total-value {{
            color: #000000;
            font-weight: bolder;
        }}
        
        /* الطباعة - إصلاح تقسيم الصفحات */
        @media print {{
            body {{
                width: 100%;
                margin: 0;
                padding: 0;
                font-size: 14px;
            }}
            .disclosure-container {{
                page-break-inside: auto;
            }}
            .customer-info {{
                page-break-after: avoid;
                page-break-inside: avoid;
            }}
            .invoice-section {{
                page-break-inside: auto;
                page-break-before: auto;
                page-break-after: auto;
            }}
            .products-table, .payments-table {{
                page-break-inside: auto;
            }}
            tr, td, th {{
                page-break-inside: auto;
                page-break-after: auto;
            }}
        }}
    </style>
</head>
<body>
    <div class="disclosure-container">
        <!-- عنوان الشركة -->
        <div class="company-header">
            <div class="company-name">مكة المكرمة</div>
            <div class="company-subtitle">الاستيراد و التجارة و التوزيع</div>
        </div>
        
        <!-- عنوان الكشف -->
        <div class="disclosure-title">كشف حساب عميل</div>
        
        <!-- معلومات العميل -->
        <div class="customer-info">
            <div class="customer-name">{customer_name_display}</div>
            <div class="customer-id">كود العميل: {customer_id}</div>
            <div class="date-range">من: {date_from} إلى: {date_to}</div>
            <div class="date-range">تاريخ الطباعة: {current_date}</div>
        </div>
        
        <!-- الفواتير -->
        {invoices_html}
        
        <!-- الإجماليات النهائية -->
        <div class="final-totals">
            <div class="final-total">
                <span class="total-label">إجمالي المبالغ:</span>
                <span class="total-value"> {total_all_amount:.2f} ج.م</span>
            </div>
            <div class="final-total">
                <span class="total-label">إجمالي المدفوع:</span>
                <span class="total-value"> {total_all_paid:.2f} ج.م</span>
            </div>
            <div class="final-total">
                <span class="total-label">إجمالي المتبقي:</span>
                <span class="total-value"> {total_all_remaining:.2f} ج.م</span>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        return html_template
    
    def generate_disclosure(self, customer_name: str, customer_id: str, 
                           all_invoices: List[Dict], original_invoices: List[Dict],
                           date_from: str, date_to: str):
        """إنشاء كشف حساب كملف PDF"""
        try:
            if not WEASYPRINT_AVAILABLE:
                return self.generate_fallback_disclosure(customer_name, customer_id, 
                                                       all_invoices, original_invoices,
                                                       date_from, date_to)
            
            # إنشاء HTML
            html_content = self.create_html_disclosure(customer_name, customer_id, 
                                                      all_invoices, original_invoices,
                                                      date_from, date_to)
            
            # تحديد مسار الإخراج
            receipts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "كشوف_الحساب")
            if not os.path.exists(receipts_dir):
                os.makedirs(receipts_dir)
            
            safe_name = "".join(c for c in customer_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_path = os.path.join(receipts_dir, f"كشف_حساب_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            
            # حفظ HTML مؤقت
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html_path = f.name
            
            try:
                # استخدام WeasyPrint
                html = HTML(filename=temp_html_path)
                
                # CSS للتحكم في الحجم وتقسيم الصفحات
                css_string = """
                @page {
                    size: A4 portrait;
                    margin: 8mm 12mm 8mm 12mm;
                }
                body {
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    max-width: 210mm;
                    font-size: 14pt;
                    line-height: 1.3;
                }
                .customer-info {
                    page-break-after: avoid;
                    page-break-inside: avoid;
                }
                .invoice-section {
                    page-break-inside: auto;
                    page-break-before: auto;
                }
                .products-table, .payments-table {
                    page-break-inside: auto;
                }
                tr, td, th {
                    page-break-inside: auto;
                }
                """
                
                font_config = FontConfiguration()
                css = CSS(string=css_string, font_config=font_config)
                
                # إنشاء PDF
                html.write_pdf(output_path, stylesheets=[css])
                print(f" تم إنشاء كشف الحساب PDF: {output_path}")
                
                try:
                    os.unlink(temp_html_path)
                except:
                    pass
                
                return output_path
                
            except Exception as e:
                print(f"خطأ في WeasyPrint: {e}")
                return self.generate_fallback_disclosure(customer_name, customer_id, 
                                                       all_invoices, original_invoices,
                                                       date_from, date_to)
                
        except Exception as e:
            print(f" خطأ في إنشاء كشف الحساب: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_fallback_disclosure(self, customer_name: str, customer_id: str, 
                                    all_invoices: List[Dict], original_invoices: List[Dict],
                                    date_from: str, date_to: str):
        """الطريقة البديلة لإنشاء كشف الحساب"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # تنظيف النصوص
            customer_name_display = self.safe_text(customer_name)
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            # إنشاء الصورة
            img_width = 850
            margin = 45
            line_height = 28
            
            # حساب الارتفاع بشكل ديناميكي بناءً على البيانات
            total_height_needed = margin * 2
            
            # ارتفاع عنوان الشركة
            total_height_needed += 100
            
            # ارتفاع معلومات العميل
            total_height_needed += 120
            
            # حساب ارتفاع كل فاتورة
            for original_invoice in original_invoices:
                receipt_id = original_invoice.get('receipt_id', '')
                
                # ارتفاع عنوان الفاتورة
                total_height_needed += 40
                
                # ارتفاع خط تحت العنوان
                total_height_needed += 20
                
                # ارتفاع رؤوس جدول المنتجات
                items_data = original_invoice.get('items', [])
                if isinstance(items_data, str):
                    try:
                        import json
                        items_data = json.loads(items_data)
                    except:
                        items_data = []
                
                if items_data:
                    # رؤوس الجدول
                    total_height_needed += 35
                    
                    # بيانات المنتجات
                    total_height_needed += len(items_data) * 25
                    
                    # مسافة بعد الجدول
                    total_height_needed += 15
                
                # جدول الأقساط
                payment_records = self.extract_payment_records(all_invoices, receipt_id)
                if payment_records:
                    # عنوان جدول الأقساط
                    total_height_needed += 35
                    
                    # رؤوس الجدول
                    total_height_needed += 35
                    
                    # بيانات الأقساط
                    total_height_needed += len(payment_records) * 25
                    
                    # مسافة بعد الجدول
                    total_height_needed += 15
                
                # ملخص الفاتورة
                total_height_needed += 50
                
                # خط فاصل
                total_height_needed += 30
            
            # ارتفاع الإجماليات النهائية
            total_height_needed += 150
            
            # إضافة هامش إضافي
            total_height_needed += 100
            
            img_height = min(4000, total_height_needed)
            
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # البحث عن خط
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/tahoma.ttf",
                "C:/Windows/Fonts/arabtype.ttf",
                "arial.ttf",
                "tahoma.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
            
            font = None
            for path in font_paths:
                if os.path.exists(path):
                    try:
                        font = ImageFont.truetype(path, 13)
                        break
                    except:
                        continue
            
            if font is None:
                font = ImageFont.load_default()
            
            font_bold = font
            font_large = ImageFont.load_default()
            
            # البدء في الرسم
            y = margin
            
            # عنوان الشركة
            company_title = "مكة المكرمة"
            company_subtitle = "الاستيراد و التجارة و التوزيع"
            
            company_title_width = draw.textlength(company_title, font=ImageFont.truetype(font.path, 22) if hasattr(font, 'path') else font)
            company_subtitle_width = draw.textlength(company_subtitle, font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            
            draw.text(((img_width - company_title_width) // 2, y), company_title, fill='black', 
                     font=ImageFont.truetype(font.path, 22) if hasattr(font, 'path') else font)
            y += line_height + 8
            
            draw.text(((img_width - company_subtitle_width) // 2, y), company_subtitle, fill='black', 
                     font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            y += line_height + 12
            
            # عنوان الكشف
            disclosure_title = "كشف حساب عميل"
            title_width = draw.textlength(disclosure_title, font=font_bold)
            draw.text(((img_width - title_width) // 2, y), disclosure_title, fill='black', font=font_bold)
            y += line_height + 12
            
            # معلومات العميل
            draw.rectangle([(margin, y), (img_width - margin, y + 90)], outline='black', width=2, fill='#f8f9fa')
            y += 12
            
            customer_line = f"العميل: {customer_name_display}"
            draw.text((margin + 25, y), customer_line, fill='black', font=font_bold)
            y += line_height
            
            customer_id_line = f"كود العميل: {customer_id}"
            draw.text((margin + 25, y), customer_id_line, fill='black', font=font)
            y += line_height
            
            date_line = f"من: {date_from} إلى: {date_to}"
            draw.text((margin + 25, y), date_line, fill='black', font=font)
            y += line_height
            
            print_date_line = f"تاريخ الطباعة: {current_date}"
            draw.text((margin + 25, y), print_date_line, fill='black', font=font)
            y += 35
            
            # الفواتير
            total_all_amount = 0
            total_all_paid = 0
            total_all_remaining = 0
            
            for original_invoice in original_invoices:
                receipt_id = original_invoice.get('receipt_id', '')
                date = original_invoice.get('date', '')
                total = float(original_invoice.get('total', 0))
                amount_paid = float(original_invoice.get('amount_paid', 0))
                remaining = float(original_invoice.get('remaining', 0))
                
                # حساب حالة الدفع بناءً على المبالغ
                payment_status = self.calculate_payment_status(amount_paid, remaining, total)
                
                # الحصول على سجلات الدفع
                payment_records = self.extract_payment_records(all_invoices, receipt_id)
                
                # حساب المدفوع والمتبقي من الأقساط
                total_paid_from_payments = sum(p['amount_paid'] for p in payment_records)
                if payment_records:
                    last_payment = payment_records[-1]
                    remaining = float(last_payment.get('remaining', 0))
                    amount_paid = total_paid_from_payments
                
                # إعادة حساب حالة الدفع بعد التحديث
                payment_status = self.calculate_payment_status(amount_paid, remaining, total)
                
                # إضافة إلى الإجماليات
                total_all_amount += total
                total_all_paid += amount_paid
                total_all_remaining += remaining
                
                # عنوان الفاتورة
                invoice_header = f"فاتورة رقم: {receipt_id} - التاريخ: {date}"
                draw.text((margin, y), invoice_header, fill='black', font=font_bold)
                y += line_height
                
                # خط تحت العنوان
                draw.line([(margin, y), (img_width - margin, y)], fill='black', width=2)
                y += 12
                
                # المنتجات
                items_data = original_invoice.get('items', [])
                if isinstance(items_data, str):
                    try:
                        import json
                        items_data = json.loads(items_data)
                    except:
                        items_data = []
                
                if items_data:
                    # رؤوس الجدول
                    headers = ["الصنف (المقاس)", "الوحدة", "الكمية", "السعر", "الإجمالي"]
                    col_widths = [220, 90, 70, 90, 110]
                    col_positions = [img_width - margin - sum(col_widths[:i+1]) for i in range(5)]
                    
                    for i, header in enumerate(headers):
                        header_width = draw.textlength(header, font=font)
                        draw.text((col_positions[i] - col_widths[i]//2 + header_width//2, y), 
                                 header, fill='black', font=font)
                    
                    y += line_height
                    
                    # خط تحت الرؤوس
                    draw.line([(margin, y), (img_width - margin, y)], fill='black', width=2)
                    y += 8
                    
                    # بيانات المنتجات
                    for item in items_data:
                        if isinstance(item, dict):
                            name = self.safe_text(item.get('name', ''))
                            size = item.get('size', '')
                            unit = item.get('unit', 'عدد')
                            quantity = item.get('quantity', 0)
                            selling_price = item.get('selling_price', 0.0)
                            subtotal = quantity * selling_price
                            
                            product_text = f"{name} ({size})"
                            text_width = draw.textlength(product_text, font=font)
                            if text_width > col_widths[0]:
                                product_text = product_text[:18] + "..."
                            
                            # الصنف
                            draw.text((col_positions[0] - text_width, y), product_text, fill='black', font=font)
                            
                            # الوحدة
                            unit_text = unit
                            unit_width = draw.textlength(unit_text, font=font)
                            draw.text((col_positions[1] - col_widths[1]//2 + unit_width//2, y), 
                                     unit_text, fill='black', font=font)
                            
                            # الكمية
                            qty_text = str(quantity)
                            qty_width = draw.textlength(qty_text, font=font)
                            draw.text((col_positions[2] - col_widths[2]//2 + qty_width//2, y), 
                                     qty_text, fill='black', font=font)
                            
                            # السعر
                            price_text = f"{selling_price:.2f}"
                            price_width = draw.textlength(price_text, font=font)
                            draw.text((col_positions[3] - col_widths[3]//2 + price_width//2, y), 
                                     price_text, fill='black', font=font)
                            
                            # الإجمالي
                            subtotal_text = f"{subtotal:.2f}"
                            subtotal_width = draw.textlength(subtotal_text, font=font)
                            draw.text((col_positions[4] - col_widths[4]//2 + subtotal_width//2, y), 
                                     subtotal_text, fill='black', font=font)
                            
                            y += line_height - 5
                    
                    y += 12
                
                # جدول الأقساط
                if payment_records:
                    # عنوان جدول الأقساط
                    payments_title = "جدول الأقساط"
                    draw.text((margin, y), payments_title, fill='black', font=font_bold)
                    y += line_height
                    
                    # رؤوس جدول الأقساط
                    payment_headers = ["#", "التاريخ", "المبلغ المدفوع", "المتبقي", "الحالة"]
                    payment_col_widths = [35, 110, 110, 110, 90]
                    payment_col_positions = [img_width - margin - sum(payment_col_widths[:i+1]) for i in range(5)]
                    
                    for i, header in enumerate(payment_headers):
                        header_width = draw.textlength(header, font=font)
                        draw.text((payment_col_positions[i] - payment_col_widths[i]//2 + header_width//2, y), 
                                 header, fill='black', font=font)
                    
                    y += line_height
                    
                    # خط تحت الرؤوس
                    draw.line([(margin, y), (img_width - margin, y)], fill='black', width=2)
                    y += 8
                    
                    # بيانات الأقساط
                    for i, payment in enumerate(payment_records, 1):
                        payment_status_display = payment.get('payment_status', '')
                        if payment_status_display == "دفع جزئي":
                            payment_status_display = "سداد قسط"
                        
                        # الرقم التسلسلي
                        num_text = str(i)
                        num_width = draw.textlength(num_text, font=font)
                        draw.text((payment_col_positions[0] - payment_col_widths[0]//2 + num_width//2, y), 
                                 num_text, fill='black', font=font)
                        
                        # التاريخ
                        date_text = payment.get('date', '')
                        date_width = draw.textlength(date_text, font=font)
                        draw.text((payment_col_positions[1] - payment_col_widths[1]//2 + date_width//2, y), 
                                 date_text, fill='black', font=font)
                        
                        # المبلغ المدفوع
                        paid_text = f"{payment.get('amount_paid', 0):.2f}"
                        paid_width = draw.textlength(paid_text, font=font)
                        draw.text((payment_col_positions[2] - payment_col_widths[2]//2 + paid_width//2, y), 
                                 paid_text, fill='black', font=font)
                        
                        # المتبقي
                        remaining_text = f"{payment.get('remaining', 0):.2f}"
                        remaining_width = draw.textlength(remaining_text, font=font)
                        draw.text((payment_col_positions[3] - payment_col_widths[3]//2 + remaining_width//2, y), 
                                 remaining_text, fill='black', font=font)
                        
                        # الحالة
                        status_text = payment_status_display
                        status_width = draw.textlength(status_text, font=font)
                        draw.text((payment_col_positions[4] - payment_col_widths[4]//2 + status_width//2, y), 
                                 status_text, fill='black', font=font)
                        
                        y += line_height - 5
                    
                    y += 12
                
                # ملخص الفاتورة في سطر واحد
                summary_text = f"إجمالي الفاتورة: {total:.2f} ج.م  |  المدفوع: {amount_paid:.2f} ج.م  |  المتبقي: {remaining:.2f} ج.م  |  حالة الدفع: {payment_status}"
                
                # خلفية للملخص
                draw.rectangle([(margin, y), (img_width - margin, y + 30)], fill='#f8f9fa', outline='black', width=2)
                
                # حساب عرض النص
                text_width = draw.textlength(summary_text, font=font_bold)
                text_x = (img_width - text_width) // 2
                draw.text((text_x, y + 8), summary_text, fill='black', font=font_bold)
                
                y += 40
                
                # خط فاصل بين الفواتير
                draw.line([(margin, y), (img_width - margin, y)], fill='black', width=1, dash=(5, 5))
                y += 22
            
            # الإجماليات النهائية
            y += 12
            draw.rectangle([(margin, y), (img_width - margin, y + 130)], outline='black', width=3, fill='#f8f9fa')
            y += 25
            
            final_lines = [
                (f"إجمالي المبالغ:", f"{total_all_amount:.2f} ج.م"),
                (f"إجمالي المدفوع:", f"{total_all_paid:.2f} ج.م"),
                (f"إجمالي المتبقي:", f"{total_all_remaining:.2f} ج.م")
            ]
            
            for label, value in final_lines:
                label_width = draw.textlength(label, font=font_bold)
                value_width = draw.textlength(value, font=font_bold)
                
                center_x = (img_width - (label_width + value_width + 25)) // 2
                draw.text((center_x, y), label, fill='black', font=font_bold)
                draw.text((center_x + label_width + 25, y), value, fill='black', font=font_bold)
                y += line_height + 8
            
            # الحفظ
            receipts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "كشوف_الحساب")
            if not os.path.exists(receipts_dir):
                os.makedirs(receipts_dir)
            
            safe_name = "".join(c for c in customer_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_path = os.path.join(receipts_dir, f"كشف_حساب_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            img.save(output_path, 'PNG', quality=95)
            print(f" تم إنشاء كشف الحساب (بديل): {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f" خطأ في الطريقة البديلة: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    # اختبار المولد
    generator = GenerateDisclosureRecord()
    
    # بيانات تجريبية
    sample_all_invoices = [
        # فاتورة أصلية 1
        {
            'receipt_id': 'INV22201',
            'customer_name': 'شركة النخبة',
            'customer_id': 'C4017',
            'date': '2026-01-01',
            'total': 1500.00,
            'amount_paid': 1000.00,
            'remaining': 500.00,
            'payment_status': 'سداد قسط',
            'items': [
                {'name': 'قميص رجالي', 'size': 'وسط', 'unit': 'عدد', 'quantity': 5, 'selling_price': 150.00},
                {'name': 'بنطلون جينز', 'size': '32', 'unit': 'عدد', 'quantity': 3, 'selling_price': 250.00},
            ]
        },
        # أقساط الفاتورة 1
        {
            'receipt_id': 'INV22201.1',
            'customer_name': 'شركة النخبة',
            'customer_id': 'C4017',
            'date': '2026-01-10',
            'amount_paid': 500.00,
            'remaining': 1000.00,
            'payment_status': 'سداد قسط',
            'payment_method': 'نقدي'
        },
        {
            'receipt_id': 'INV22201.2',
            'customer_name': 'شركة النخبة',
            'customer_id': 'C4017',
            'date': '2026-01-20',
            'amount_paid': 500.00,
            'remaining': 500.00,
            'payment_status': 'سداد قسط',
            'payment_method': 'نقدي'
        },
        # فاتورة أصلية 2
        {
            'receipt_id': 'INV22202',
            'customer_name': 'شركة النخبة',
            'customer_id': 'C4017',
            'date': '2026-01-02',
            'total': 2000.00,
            'amount_paid': 500.00,
            'remaining': 1500.00,
            'payment_status': 'سداد قسط',
            'items': [
                {'name': 'حذاء رياضي', 'size': '42', 'unit': 'عدد', 'quantity': 2, 'selling_price': 400.00},
                {'name': 'جاكيت', 'size': 'كبير', 'unit': 'عدد', 'quantity': 3, 'selling_price': 400.00},
            ]
        },
        # أقساط الفاتورة 2
        {
            'receipt_id': 'INV22202.1',
            'customer_name': 'شركة النخبة',
            'customer_id': 'C4017',
            'date': '2026-01-15',
            'amount_paid': 500.00,
            'remaining': 1500.00,
            'payment_status': 'سداد قسط',
            'payment_method': 'شيك'
        },
    ]
    
    # استخراج الفواتير الأصلية فقط
    sample_original_invoices = [inv for inv in sample_all_invoices if '.' not in inv.get('receipt_id', '')]
    
    print("جاري اختبار مولد كشف الحساب...")
    
    path = generator.generate_disclosure(
        customer_name="شركة النخبة",
        customer_id="C4017",
        all_invoices=sample_all_invoices,
        original_invoices=sample_original_invoices,
        date_from="2026-01-01",
        date_to="2026-01-31"
    )
    
    if path:
        print(f" تم إنشاء كشف الحساب بنجاح: {path}")
    else:
        print(" فشل إنشاء كشف الحساب")