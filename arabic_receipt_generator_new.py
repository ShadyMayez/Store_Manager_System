"""
arabic_receipt_generator_new.py - مولد فواتير عربية بالتنسيق النهائي المضغوط المعدل
"""

import os
import tempfile
from typing import Dict
from datetime import datetime

# Try to use WeasyPrint first
try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("WeasyPrint غير مثبت. جاري التثبيت التلقائي...")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint"])
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        WEASYPRINT_AVAILABLE = True
        print("تم تثبيت WeasyPrint بنجاح!")
    except:
        print("فشل تثبيت WeasyPrint. سأستخدم طريقة بديلة.")
        WEASYPRINT_AVAILABLE = False

# Fallback imports
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display


class ArabicReceiptGenerator:
    """مولد فواتير عربية بالتنسيق النهائي المضغوط المعدل"""
    
    @staticmethod
    def safe_text(text: str) -> str:
        """تنظيف النص بطريقة آمنة"""
        if not text:
            return ""
        
        # استبدال الرموز فقط، بدون تغيير النص العربي
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
            
            # فقط للنصوص العربية
            arabic_chars = set('ء-ي')
            has_arabic = any(c for c in str(text) if c in arabic_chars)
            
            if has_arabic:
                reshaped = arabic_reshaper.reshape(str(text))
                return get_display(reshaped)
            
            return str(text)
        except:
            return str(text)
    
    @staticmethod
    def number_to_arabic_words(number):
        """تحويل الرقم إلى نص عربي"""
        try:
            # تحقق إذا كان الرقم به كسور
            if isinstance(number, float):
                integer_part = int(number)
                decimal_part = int((number - integer_part) * 100)
                
                integer_words = ArabicReceiptGenerator._convert_integer_to_arabic(integer_part)
                
                if decimal_part > 0:
                    decimal_words = ArabicReceiptGenerator._convert_integer_to_arabic(decimal_part)
                    return f"{integer_words} جنيهاً و{decimal_words} قرشاً فقط لا غير"
                else:
                    return f"{integer_words} جنيهاً فقط لا غير"
            else:
                integer_words = ArabicReceiptGenerator._convert_integer_to_arabic(number)
                return f"{integer_words} جنيهاً فقط لا غير"
        except:
            return str(number)
    
    @staticmethod
    def _convert_integer_to_arabic(n):
        """تحويل الأعداد الصحيحة إلى كلمات عربية"""
        if n == 0:
            return "صفر"
        
        ones = ["", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة"]
        tens = ["", "عشرة", "عشرون", "ثلاثون", "أربعون", "خمسون", "ستون", "سبعون", "ثمانون", "تسعون"]
        hundreds = ["", "مائة", "مائتان", "ثلاثمائة", "أربعمائة", "خمسمائة", "ستمائة", "سبعمائة", "ثمانمائة", "تسعمائة"]
        
        def convert_below_thousand(num):
            if num == 0:
                return ""
            elif num < 10:
                return ones[num]
            elif num < 20:
                if num == 10:
                    return "عشرة"
                elif num == 11:
                    return "أحد عشر"
                elif num == 12:
                    return "اثنا عشر"
                else:
                    return ones[num-10] + " عشر"
            elif num < 100:
                if num % 10 == 0:
                    return tens[num//10]
                else:
                    return ones[num%10] + " و" + tens[num//10]
            elif num < 1000:
                if num % 100 == 0:
                    return hundreds[num//100]
                else:
                    return hundreds[num//100] + " و" + convert_below_thousand(num%100)
        
        if n < 1000:
            return convert_below_thousand(n)
        elif n < 1000000:
            thousands = n // 1000
            remainder = n % 1000
            if thousands == 1:
                thousand_text = "ألف"
            elif thousands == 2:
                thousand_text = "ألفين"
            elif thousands < 11:
                thousand_text = ones[thousands] + " آلاف"
            else:
                thousand_text = convert_below_thousand(thousands) + " ألفاً"
            
            if remainder == 0:
                return thousand_text
            else:
                return thousand_text + " و" + convert_below_thousand(remainder)
        else:
            # للأرقام الكبيرة جداً
            return str(n)
    
    @staticmethod
    def create_html_receipt_final(receipt_data: Dict) -> str:
        """إنشاء HTML بالتنسيق النهائي الجديد المضغوط المعدل"""
        
        # استخراج البيانات
        receipt_id = receipt_data.get('receipt_id', '')
        customer_name = receipt_data.get('customer_name', '')
        customer_id = receipt_data.get('customer_id', '')
        customer_code = receipt_data.get('customer_code', customer_id)
        representative_name = receipt_data.get('representative_name', '')
        representative_code = receipt_data.get('representative_code', '')
        customer_address = receipt_data.get('customer_address', '')
        date_str = receipt_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        due_date_str = receipt_data.get('due_date', date_str)
        customer_notes = receipt_data.get('customer_notes', '')
        
        # الحقول الجديدة
        profit = receipt_data.get('profit', 0)
        receipt_code = receipt_data.get('receipt_code', receipt_id)
        
        items = receipt_data.get('items', [])
        total = receipt_data.get('total', 0)
        
        previous_balance = receipt_data.get('previous_balance', 0)
        current_balance = receipt_data.get('current_balance', 0)
        amount_paid = receipt_data.get('amount_paid', 0)
        remaining = receipt_data.get('remaining', 0)
        
        # حساب المبلغ المتبقي الصحيح للعرض في PDF (الفاتورة + الرصيد السابق - المدفوع)
        total_cumulative = total + previous_balance
        display_remaining = total_cumulative - amount_paid
        
        # تحويل الرقم إلى نص عربي
        total_arabic_words = ArabicReceiptGenerator.number_to_arabic_words(total)
        
        # بناء جدول المنتجات
        products_rows = ""
        for idx, item in enumerate(items):
            subtotal = item.get('selling_price', 0) * item.get('quantity', 0)
            item_name = item.get('name', '')
            size = item.get('size', '')
            unit = item.get('unit', 'عدد')
            
            item_display = ArabicReceiptGenerator.safe_text(item_name)
            if len(item_display) > 20:
                item_display = item_display[:18] + "..."
            
            products_rows += f"""
            <tr>
                <td class="row-number">{idx + 1}</td>
                <td class="product-name">{item_display} ({size})</td>
                <td class="unit">{unit}</td>
                <td class="quantity">{item.get('quantity', 0)}</td>
                <td class="price">{item.get('selling_price', 0):.2f}</td>
                <td class="total">{subtotal:.2f}</td>
            </tr>
            """
        
        # HTML بالتنسيق المعدل
        html_template = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فاتورة {receipt_id}</title>
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
        
        .receipt-container {{
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
        
        /* قسم معلومات العميل المصغرة */
        .compact-info-section {{
            margin-bottom: 15px;
            padding: 8px;
            border: 2px solid #000000;
            border-radius: 5px;
            background: #f9f9f9;
        }}
        
        .compact-info-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            font-size: 12px;
            line-height: 1.2;
        }}
        
        .compact-info-item {{
            padding: 3px 5px;
            border-bottom: 1px dotted #ccc;
        }}
        
        .compact-info-label {{
            font-weight: bold;
            color: #000000;
            margin-left: 5px;
            font-size: 11px;
        }}
        
        .compact-info-value {{
            color: #000000;
            font-weight: normal;
            text-align: left;
            direction: ltr;
            font-size: 11px;
        }}
        
        /* عنوان جدول المنتجات */
        .products-title {{
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 12px 0 8px 0;
            padding: 8px;
            color: #000000;
            border-bottom: 2px solid #000000;
        }}
        
        /* جدول المنتجات */
        .products-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0 0 15px 0;
            font-size: 14px;
            border: 2px solid #000000;
        }}
        
        .products-table th {{
            background: #f0f0f0;
            color: #000000;
            padding: 8px 6px;
            text-align: center;
            font-weight: bold;
            border: 2px solid #000000;
            font-size: 15px;
        }}
        
        .products-table td {{
            padding: 6px 5px;
            text-align: center;
            border: 1px solid #000000;
            font-size: 14px;
            color: #000000;
        }}
        
        .row-number {{
            width: 40px;
            font-weight: bold;
        }}
        
        .product-name {{
            text-align: right;
            padding-right: 8px !important;
            min-width: 160px;
            font-weight: bold;
        }}
        
        .unit {{
            width: 70px;
            font-weight: bold;
        }}
        
        .quantity {{
            width: 70px;
            font-weight: bold;
        }}
        
        .price {{
            width: 90px;
            text-align: left;
            direction: ltr;
            font-weight: bold;
        }}
        
        .total {{
            width: 100px;
            text-align: left;
            direction: ltr;
            font-weight: bold;
        }}
        
        /* الإجماليات */
        .totals-section {{
            padding: 15px 0;
            margin: 15px 0;
        }}
        
        .total-main {{
            margin: 12px 0;
            padding: 10px 0;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            border-top: 3px solid #000000;
            border-bottom: 3px solid #000000;
            color: #000000;
        }}
        
        .arabic-words {{
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            color: #000000;
            padding: 8px 0;
            margin: 8px 0;
            border: 1px solid #000000;
            background: #f9f9f9;
        }}
        
        /* قسم المدفوع والمتبقي */
        .payment-grid {{
            margin: 15px 0;
            padding: 12px 0;
        }}
        
        .payment-row {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 6px 0;
            font-size: 16px;
        }}
        
        .payment-item {{
            flex: 1;
            text-align: center;
            padding: 0 10px;
        }}
        
        .payment-label {{
            font-weight: bold;
            color: #000000;
            margin-bottom: 4px;
            font-size: 16px;
        }}
        
        .payment-value {{
            font-weight: bold;
            color: #000000;
            direction: ltr;
            text-align: center;
            font-size: 16px;
        }}
        
        @media print {{
            body {{
                width: 100%;
                margin: 0;
                padding: 0;
                font-size: 15px;
            }}
            .receipt-container {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="receipt-container">
        <!-- عنوان الشركة -->
        <div class="company-header">
            <div class="company-name">مكة المكرمة</div>
            <div class="company-subtitle">الاستيراد و التجارة و التوزيع</div>
        </div>
        
        <!-- قسم معلومات العميل المصغرة -->
        <div class="compact-info-section">
            <div class="compact-info-grid">
                <div class="compact-info-item">
                    <span class="compact-info-label">الرقم المسلسل:</span>
                    <span class="compact-info-value">{receipt_id}</span>
                </div>
                <div class="compact-info-item">
                    <span class="compact-info-label">التاريخ:</span>
                    <span class="compact-info-value">{date_str}</span>
                </div>
                <div class="compact-info-item">
                    <span class="compact-info-label">الوقت:</span>
                    <span class="compact-info-value">{datetime.now().strftime('%H:%M')}</span>
                </div>
                <div class="compact-info-item">
                    <span class="compact-info-label">الكود / العميل:</span>
                    <span class="compact-info-value">{customer_code}</span>
                </div>
                <div class="compact-info-item">
                    <span class="compact-info-label">اسم العميل:</span>
                    <span class="compact-info-label">{customer_name[:15]}{'...' if len(customer_name) > 15 else ''}</span>
                </div>
                <div class="compact-info-item" style="grid-column: span 3;">
                    <span class="compact-info-label">عنوان العميل:</span>
                    <span class="compact-info-label">{customer_address[:40]}{'...' if len(customer_address) > 40 else ''}</span>
                </div>
                <div class="compact-info-item" style="grid-column: span 3;">
                    <span class="compact-info-label">الملاحظات:</span>
                    <span class="compact-info-label">{customer_notes[:40]}{'...' if len(customer_notes) > 40 else ''}</span>
                </div>
            </div>
        </div>
        
        <!-- جدول المنتجات -->
        <div class="products-title">تفاصيل الفاتورة</div>
        
        <table class="products-table">
            <thead>
                <tr>
                    <th></th>
                    <th>الصنف</th>
                    <th>الوحدة</th>
                    <th>الكمية</th>
                    <th>سعر البيع</th>
                    <th>الإجمالي</th>
                </tr>
            </thead>
            <tbody>
                {products_rows}
            </tbody>
        </table>
        
        <!-- الإجمالي -->
        <div class="totals-section">
            <div class="total-main">
                الإجمالي: {total:.2f}ج.م
            </div>
            <div class="arabic-words">
                {total_arabic_words}
            </div>
        </div>
        
        <!-- قسم المدفوع والمتبقي -->
        <div class="payment-grid">
            <div class="payment-row">
                <div class="payment-item">
                    <div class="payment-label">الرصيد السابق</div>
                    <div class="payment-value">{previous_balance:.2f} ج.م</div>
                </div>
                <div class="payment-item">
                    <div class="payment-label">المبلغ المدفوع</div>
                    <div class="payment-value">{amount_paid:.2f} ج.م</div>
                </div>
                <div class="payment-item">
                    <div class="payment-label">المبلغ المتبقي</div>
                    <div class="payment-value">{display_remaining:.2f} ج.م</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        return html_template
    
    @staticmethod
    def generate_receipt(receipt_data: Dict, output_path: str = None):
        """إنشاء الفاتورة كملف PDF"""
        try:
            if not WEASYPRINT_AVAILABLE:
                return ArabicReceiptGenerator.generate_fallback(receipt_data, output_path)
            
            html_content = ArabicReceiptGenerator.create_html_receipt_final(receipt_data)
            
            if output_path is None:
                receipt_id = receipt_data.get('receipt_id', 'UNKNOWN')
                receipts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "الفواتير")
                if not os.path.exists(receipts_dir):
                    os.makedirs(receipts_dir)
                output_path = os.path.join(receipts_dir, f"فاتورة_{receipt_id}.pdf")
            
            if not output_path.lower().endswith('.pdf'):
                output_path = output_path.rsplit('.', 1)[0] + '.pdf'
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html_path = f.name
            
            try:
                html = HTML(filename=temp_html_path)
                
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
                .receipt-container {
                    page-break-inside: avoid;
                    page-break-after: avoid;
                }
                """
                
                font_config = FontConfiguration()
                css = CSS(string=css_string, font_config=font_config)
                
                html.write_pdf(output_path, stylesheets=[css])
                print(f"✓ تم إنشاء الفاتورة PDF: {output_path}")
                
                try:
                    os.unlink(temp_html_path)
                except:
                    pass
                
                return output_path
                
            except Exception as e:
                print(f"خطأ في WeasyPrint: {e}")
                return ArabicReceiptGenerator.generate_fallback(receipt_data, output_path)
                
        except Exception as e:
            print(f"✗ خطأ في إنشاء الفاتورة: {e}")
            import traceback
            traceback.print_exc()
            return ArabicReceiptGenerator.generate_fallback(receipt_data, output_path)
    
    @staticmethod
    def generate_fallback(receipt_data: Dict, output_path: str = None):
        """الطريقة البديلة"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            cleaned_data = receipt_data.copy()
            for key, value in cleaned_data.items():
                if isinstance(value, str):
                    cleaned_data[key] = ArabicReceiptGenerator.safe_text(value)
            
            if 'items' in cleaned_data:
                for item in cleaned_data['items']:
                    for k, v in item.items():
                        if isinstance(v, str):
                            item[k] = ArabicReceiptGenerator.safe_text(v)
            
            receipt_id = cleaned_data.get('receipt_id', '')
            customer_name = cleaned_data.get('customer_name', '')
            customer_id = cleaned_data.get('customer_id', '')
            customer_code = cleaned_data.get('customer_code', customer_id)
            customer_address = cleaned_data.get('customer_address', '')
            date_str = cleaned_data.get('date', '')
            customer_notes = cleaned_data.get('customer_notes', '')
            
            items = cleaned_data.get('items', [])
            total = cleaned_data.get('total', 0)
            
            previous_balance = cleaned_data.get('previous_balance', 0)
            amount_paid = cleaned_data.get('amount_paid', 0)
            remaining = cleaned_data.get('remaining', 0)
            
            # حساب المبلغ المتبقي الصحيح للعرض في PDF (الفاتورة + الرصيد السابق - المدفوع)
            total_cumulative = total + previous_balance
            display_remaining = total_cumulative - amount_paid
            
            if output_path is None:
                receipt_id = receipt_data.get('receipt_id', 'UNKNOWN')
                receipts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "الفواتير")
                if not os.path.exists(receipts_dir):
                    os.makedirs(receipts_dir)
                output_path = os.path.join(receipts_dir, f"فاتورة_{receipt_id}.png")
            
            img_width = 850
            margin = 45
            line_height = 28
            
            base_height = 70 + len(items) * 28 + 100
            img_height = min(1000, margin * 2 + base_height)
            
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
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
            font_small = ImageFont.truetype(font.path, 10) if hasattr(font, 'path') else font
            
            y = margin
            
            company_title = "مكة المكرمة"
            company_subtitle = "الاستيراد و التجارة و التوزيع"
            
            company_title_width = draw.textlength(company_title, font=ImageFont.truetype(font.path, 22) if hasattr(font, 'path') else font)
            company_subtitle_width = draw.textlength(company_subtitle, font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            
            draw.text(((img_width - company_title_width) // 2, y), company_title, fill='black', 
                     font=ImageFont.truetype(font.path, 22) if hasattr(font, 'path') else font)
            y += line_height
            
            draw.text(((img_width - company_subtitle_width) // 2, y), company_subtitle, fill='black', 
                     font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            y += line_height + 10
            
            info_box_height = line_height * 2.5
            info_box_y_start = y
            
            draw.rectangle([(margin, y), (img_width - margin, y + info_box_height)], 
                          outline='black', width=2, fill='#f9f9f9')
            
            info_y = y + 8
            
            row1_items = [
                (f"الرقم المسلسل: {receipt_id}", margin + 10),
                (f"التاريخ: {date_str}", img_width//2 - 40),
                (f"الوقت: {datetime.now().strftime('%H:%M')}", img_width - margin - 120)
            ]
            
            for text, x_pos in row1_items:
                draw.text((x_pos, info_y), text, fill='black', font=font_small)
            
            info_y += line_height * 0.7
            
            short_name = customer_name[:15] + "..." if len(customer_name) > 15 else customer_name
            row2_items = [
                (f"الكود/العميل: {customer_code}", margin + 10),
                (f"اسم العميل: {short_name}", img_width//2),
            ]
            
            for text, x_pos in row2_items:
                draw.text((x_pos, info_y), text, fill='black', font=font_small)
            
            info_y += line_height * 0.7
            
            short_address = customer_address[:40] + "..." if len(customer_address) > 40 else customer_address
            draw.text((margin + 10, info_y), f"عنوان العميل: {short_address}", fill='black', font=font_small)
            
            info_y += line_height * 0.7
            
            short_notes = customer_notes[:40] + "..." if len(customer_notes) > 40 else customer_notes
            draw.text((margin + 10, info_y), f"الملاحظات: {short_notes}", fill='black', font=font_small)
            
            y += info_box_height + 10
            
            table_title = "تفاصيل الفاتورة"
            title_width = draw.textlength(table_title, font=font_bold)
            draw.text(((img_width - title_width) // 2, y), table_title, fill='black', font=font_bold)
            y += line_height
            
            draw.line([(margin, y), (img_width - margin, y)], fill='black', width=2)
            y += 8
            
            headers = ["", "الصنف", "الوحدة", "الكمية", "سعر البيع", "الإجمالي"]
            col_widths = [35, 200, 70, 70, 90, 100]
            col_positions = [img_width - margin - sum(col_widths[:i+1]) for i in range(6)]
            
            for i, header in enumerate(headers):
                if i == 0:
                    continue
                header_width = draw.textlength(header, font=font_bold)
                draw.text((col_positions[i] - col_widths[i]//2 + header_width//2, y), header, fill='black', font=font_bold)
            
            y += line_height - 3
            
            draw.line([(margin, y), (img_width - margin, y)], fill='black', width=2)
            y += 5
            
            for idx, item in enumerate(items):
                item_name = item.get('name', '')
                size = item.get('size', '')
                unit = item.get('unit', 'عدد')
                qty = item.get('quantity', 0)
                price = item.get('selling_price', 0)
                subtotal = qty * price
                
                num_text = str(idx + 1)
                num_width = draw.textlength(num_text, font=font_bold)
                draw.text((col_positions[0] - col_widths[0]//2 + num_width//2, y), num_text, fill='black', font=font_bold)
                
                product_text = f"{item_name} ({size})"
                text_width = draw.textlength(product_text, font=font)
                if text_width > col_widths[1]:
                    product_text = product_text[:18] + "..."
                    text_width = draw.textlength(product_text, font=font)
                draw.text((col_positions[1] - text_width, y), product_text, fill='black', font=font)
                
                unit_text = unit
                unit_width = draw.textlength(unit_text, font=font)
                draw.text((col_positions[2] - col_widths[2]//2 + unit_width//2, y), unit_text, fill='black', font=font)
                
                qty_text = str(qty)
                qty_width = draw.textlength(qty_text, font=font)
                draw.text((col_positions[3] - col_widths[3]//2 + qty_width//2, y), qty_text, fill='black', font=font)
                
                price_text = f"{price:.2f}"
                price_width = draw.textlength(price_text, font=font)
                draw.text((col_positions[4] - col_widths[4]//2 + price_width//2, y), price_text, fill='black', font=font)
                
                subtotal_text = f"{subtotal:.2f}"
                subtotal_width = draw.textlength(subtotal_text, font=font)
                draw.text((col_positions[5] - col_widths[5]//2 + subtotal_width//2, y), subtotal_text, fill='black', font=font)
                
                y += line_height - 5
            
            y += 10
            
            draw.line([(margin, y), (img_width - margin, y)], fill='black', width=3)
            y += 12
            
            total_label = "الإجمالي:"
            total_value = f"{total:.2f}ج.م"
            
            label_width = draw.textlength(total_label, font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            value_width = draw.textlength(total_value, font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            
            total_x = (img_width - (label_width + value_width + 15)) // 2
            draw.text((total_x, y), total_label, fill='black', 
                     font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            draw.text((total_x + label_width + 15, y), total_value, fill='black', 
                     font=ImageFont.truetype(font.path, 16) if hasattr(font, 'path') else font)
            
            draw.line([(total_x - 15, y-8), (total_x + label_width + value_width + 30, y-8)], fill='black', width=3)
            draw.line([(total_x - 15, y+25), (total_x + label_width + value_width + 30, y+25)], fill='black', width=3)
            
            y += line_height + 5
            
            arabic_words = ArabicReceiptGenerator.number_to_arabic_words(total)
            arabic_width = draw.textlength(arabic_words, font=font)
            draw.text(((img_width - arabic_width) // 2, y), arabic_words, fill='black', font=font)
            y += line_height + 10
            
            draw.rectangle([(margin, y-line_height-2), (img_width - margin, y-2)], outline='black', width=1, fill='#f9f9f9')
            
            y += 8
            
            section_width = (img_width - margin * 2) // 3
            
            prev_label = "الرصيد السابق:"
            prev_value = f"{previous_balance:.2f} ج.م"
            
            prev_x = margin + section_width//2
            prev_label_width = draw.textlength(prev_label, font=font)
            prev_value_width = draw.textlength(prev_value, font=font_bold)
            draw.text((prev_x - (prev_label_width + prev_value_width + 5)//2, y), prev_label, fill='black', font=font)
            draw.text((prev_x - (prev_label_width + prev_value_width + 5)//2 + prev_label_width + 5, y), prev_value, fill='black', font=font_bold)
            
            paid_label = "المبلغ المدفوع:"
            paid_value = f"{amount_paid:.2f} ج.م"
            
            paid_x = margin + section_width + section_width//2
            paid_label_width = draw.textlength(paid_label, font=font)
            paid_value_width = draw.textlength(paid_value, font=font_bold)
            draw.text((paid_x - (paid_label_width + paid_value_width + 5)//2, y), paid_label, fill='black', font=font)
            draw.text((paid_x - (paid_label_width + paid_value_width + 5)//2 + paid_label_width + 5, y), paid_value, fill='black', font=font_bold)
            
            rem_label = "المبلغ المتبقي:"
            rem_value = f"{display_remaining:.2f} ج.م"
            
            rem_x = margin + section_width * 2 + section_width//2
            rem_label_width = draw.textlength(rem_label, font=font)
            rem_value_width = draw.textlength(rem_value, font=font_bold)
            draw.text((rem_x - (rem_label_width + rem_value_width + 5)//2, y), rem_label, fill='black', font=font)
            draw.text((rem_x - (rem_label_width + rem_value_width + 5)//2 + rem_label_width + 5, y), rem_value, fill='black', font=font_bold)
            
            y += line_height + 10
            
            img.save(output_path, 'PNG', quality=95)
            print(f"✓ تم إنشاء الفاتورة (بديل): {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"✗ خطأ في الطريقة البديلة: {e}")
            import traceback
            traceback.print_exc()
            return None


def create_arabic_receipt(receipt_data: Dict, output_path: str = None):
    """واجهة مبسطة لإنشاء فاتورة عربية"""
    return ArabicReceiptGenerator.generate_receipt(receipt_data, output_path)