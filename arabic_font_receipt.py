"""
arabic_font_receipt.py - مولد فواتير بدعم الخط العربي (بدون Selenium)
يستخدم PIL فقط - خفيف وسريع
"""

import os
from typing import Dict
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

class ArabicReceiptGenerator:
    """مولد فواتير بدعم الخط العربي الكامل - JPEG"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """تنظيف النص من الرموز غير المدعومة"""
        if not text:
            return ""
        
        # استبدال الرموز Emoji بنصوص آمنة
        emoji_replacements = {
            '✓': 'تم', '✅': 'تم', '❌': 'خطأ',
            '⚠️': 'تحذير', '💾': 'حفظ', '📥': 'تحميل',
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # إزالة أي أحرف غير قابلة للطباعة
        cleaned = ''.join(char for char in text if char.isprintable() or char.isspace())
        return cleaned.strip()
    
    @staticmethod
    def format_arabic_text(text: str) -> str:
        """إعادة تشكيل النص العربي"""
        if not text or not isinstance(text, str):
            return str(text) if text else ""
        try:
            clean_text = ArabicReceiptGenerator.clean_text(text)
            reshaped_text = arabic_reshaper.reshape(clean_text)
            return get_display(reshaped_text)
        except Exception as e:
            return text
    
    @staticmethod
    def generate_receipt(receipt_data: Dict, output_path: str = None):
        """إنشاء فاتورة كصورة JPEG مع دعم عربي كامل"""
        try:
            # تنظيف بيانات الفاتورة
            cleaned_data = receipt_data.copy()
            for key, value in cleaned_data.items():
                if isinstance(value, str):
                    cleaned_data[key] = ArabicReceiptGenerator.clean_text(value)
            
            if 'items' in cleaned_data:
                for item in cleaned_data['items']:
                    for k, v in item.items():
                        if isinstance(v, str):
                            item[k] = ArabicReceiptGenerator.clean_text(v)
            
            # استخراج البيانات
            receipt_id = cleaned_data.get('receipt_id', '')
            customer_name = cleaned_data.get('customer_name', '')
            customer_id = cleaned_data.get('customer_id', '')
            date_str = cleaned_data.get('date', '')
            
            items = cleaned_data.get('items', [])
            current_total = cleaned_data.get('total', 0)
            previous_balance = cleaned_data.get('previous_balance', 0)
            total_cumulative = cleaned_data.get('total_cumulative', current_total)
            amount_paid = cleaned_data.get('amount_paid', 0)
            remaining = cleaned_data.get('remaining', 0)
            payment_method = cleaned_data.get('payment_method', 'نقدي')
            notes = cleaned_data.get('notes', '')
            
            # تحديد حالة الدفع
            if remaining == 0:
                payment_status = "مدفوع بالكامل"
            elif amount_paid == 0:
                payment_status = "غير مدفوع"
            else:
                payment_status = "مدفوع جزئياً"
            
            # إنشاء مسار الحفظ
            if output_path is None:
                receipts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts")
                if not os.path.exists(receipts_dir):
                    os.makedirs(receipts_dir)
                output_path = os.path.join(receipts_dir, f"receipt_{receipt_id}.jpg")
            
            # التأكد من أن المسار ينتهي بـ .jpg
            if not output_path.lower().endswith('.jpg'):
                output_path = output_path.rsplit('.', 1)[0] + '.jpg'
            
            # إعدادات الصورة
            img_width = 800
            margin = 50
            line_height = 35
            small_line = 28
            
            # حساب ارتفاع الصورة
            num_items = len(items)
            base_height = 800
            items_height = num_items * small_line + 100
            img_height = base_height + items_height
            
            # إنشاء صورة
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # تحميل الخطوط
            font_small = ArabicReceiptGenerator.get_arabic_font(14)
            font_normal = ArabicReceiptGenerator.get_arabic_font(16)
            font_bold = ArabicReceiptGenerator.get_arabic_font(18)
            font_large = ArabicReceiptGenerator.get_arabic_font(24)
            font_xlarge = ArabicReceiptGenerator.get_arabic_font(32)
            
            y = margin
            
            # ═══════════════════════════════════════
            # الهيدر - اسم الشركة
            # ═══════════════════════════════════════
            company_name = ArabicReceiptGenerator.format_arabic_text("شركة مكة المكرمة")
            w = draw.textlength(company_name, font=font_xlarge)
            draw.text(((img_width - w) // 2, y), company_name, fill='#000', font=font_xlarge)
            y += line_height + 5
            
            subtitle = ArabicReceiptGenerator.format_arabic_text("الاستيراد والتجارة والتوزيع")
            w = draw.textlength(subtitle, font=font_bold)
            draw.text(((img_width - w) // 2, y), subtitle, fill='#333', font=font_bold)
            y += line_height
            
            owner = ArabicReceiptGenerator.format_arabic_text("أشرف حافظ")
            w = draw.textlength(owner, font=font_normal)
            draw.text(((img_width - w) // 2, y), owner, fill='#555', font=font_normal)
            y += line_height + 10
            
            # خط أفقي
            draw.line((margin, y, img_width - margin, y), fill='#000', width=3)
            y += 20
            
            # ═══════════════════════════════════════
            # معلومات الفاتورة
            # ═══════════════════════════════════════
            info_items = [
                ("رقم الفاتورة:", receipt_id),
                ("التاريخ:", date_str),
                ("اسم العميل:", customer_name),
                ("معرف العميل:", customer_id),
            ]
            
            for label, value in info_items:
                label_ar = ArabicReceiptGenerator.format_arabic_text(label)
                value_ar = ArabicReceiptGenerator.format_arabic_text(value)
                
                draw.text((margin + 20, y), label_ar, fill='#000', font=font_bold)
                draw.text((margin + 200, y), value_ar, fill='#333', font=font_normal)
                y += small_line
            
            y += 15
            draw.line((margin, y, img_width - margin, y), fill='#ccc', width=2)
            y += 25
            
            # ═══════════════════════════════════════
            # عنوان جدول المنتجات
            # ═══════════════════════════════════════
            products_title = ArabicReceiptGenerator.format_arabic_text("المنتجات")
            w = draw.textlength(products_title, font=font_large)
            draw.text(((img_width - w) // 2, y), products_title, fill='#000', font=font_large)
            y += line_height
            
            # رأس الجدول
            headers = ["اسم المنتج", "الكمية", "السعر", "الإجمالي"]
            col_widths = [300, 100, 120, 130]
            x_positions = [margin + 30]
            for i in range(3):
                x_positions.append(x_positions[-1] + col_widths[i])
            
            # خلفية رأس الجدول
            draw.rectangle([margin + 20, y - 5, img_width - margin - 20, y + small_line], 
                          fill='#2c3e50')
            
            for i, header in enumerate(headers):
                h_ar = ArabicReceiptGenerator.format_arabic_text(header)
                w = draw.textlength(h_ar, font=font_bold)
                x = x_positions[i] + (col_widths[i] - w) // 2
                draw.text((x, y), h_ar, fill='#fff', font=font_bold)
            
            y += small_line + 10
            
            # المنتجات
            for item in items:
                name = item.get('name', '')
                size = item.get('size', '')
                qty = item.get('quantity', 0)
                price = item.get('selling_price', 0)
                subtotal = qty * price
                
                # تقصير الاسم
                if len(name) > 25:
                    name = name[:22] + "..."
                
                full_name = f"{name} ({size})" if size else name
                
                row_data = [
                    ArabicReceiptGenerator.format_arabic_text(full_name),
                    ArabicReceiptGenerator.format_arabic_text(str(qty)),
                    ArabicReceiptGenerator.format_arabic_text(f"{price:.2f}"),
                    ArabicReceiptGenerator.format_arabic_text(f"{subtotal:.2f}"),
                ]
                
                for i, data in enumerate(row_data):
                    w = draw.textlength(data, font=font_small)
                    x = x_positions[i] + (col_widths[i] - w) // 2
                    draw.text((x, y), data, fill='#333', font=font_small)
                
                y += small_line
            
            y += 15
            draw.line((margin + 20, y, img_width - margin - 20, y), fill='#000', width=2)
            y += 25
            
            # ═══════════════════════════════════════
            # الإجماليات
            # ═══════════════════════════════════════
            totals_title = ArabicReceiptGenerator.format_arabic_text("الإجماليات")
            w = draw.textlength(totals_title, font=font_large)
            draw.text(((img_width - w) // 2, y), totals_title, fill='#000', font=font_large)
            y += line_height + 10
            
            totals_data = [
                ("الإجمالي الحالي:", f"{current_total:.2f} ج.م"),
                ("الرصيد السابق:", f"{previous_balance:.2f} ج.م"),
                ("الإجمالي الكلي:", f"{total_cumulative:.2f} ج.م"),
                ("", ""),
                ("المدفوع الآن:", f"{amount_paid:.2f} ج.م"),
                ("المبلغ المتبقي:", f"{remaining:.2f} ج.م"),
            ]
            
            for label, value in totals_data:
                if not label:
                    y += 10
                    continue
                
                label_ar = ArabicReceiptGenerator.format_arabic_text(label)
                value_ar = ArabicReceiptGenerator.format_arabic_text(value)
                
                draw.text((margin + 40, y), label_ar, fill='#000', font=font_bold)
                
                v_w = draw.textlength(value_ar, font=font_normal)
                draw.text((img_width - margin - v_w - 40, y), value_ar, fill='#333', font=font_normal)
                
                y += small_line
            
            y += 15
            
            # معلومات الدفع
            payment_info = [
                ("طريقة الدفع:", payment_method),
                ("حالة الدفع:", payment_status),
            ]
            
            for label, value in payment_info:
                label_ar = ArabicReceiptGenerator.format_arabic_text(label)
                value_ar = ArabicReceiptGenerator.format_arabic_text(value)
                
                draw.text((margin + 40, y), label_ar, fill='#000', font=font_bold)
                draw.text((margin + 220, y), value_ar, fill='#2c3e50', font=font_normal)
                
                y += small_line
            
            # الملاحظات
            if notes:
                y += 20
                notes_label = ArabicReceiptGenerator.format_arabic_text("ملاحظات:")
                draw.text((margin + 40, y), notes_label, fill='#000', font=font_bold)
                y += small_line
                
                notes_ar = ArabicReceiptGenerator.format_arabic_text(notes)
                draw.text((margin + 40, y), notes_ar, fill='#555', font=font_small)
                y += small_line
            
            y += 25
            draw.line((margin, y, img_width - margin, y), fill='#000', width=3)
            y += 25
            
            # ═══════════════════════════════════════
            # التذييل
            # ═══════════════════════════════════════
            receipt_code = ArabicReceiptGenerator.format_arabic_text(f"كود الفاتورة: INV{receipt_id}")
            w = draw.textlength(receipt_code, font=font_normal)
            draw.text(((img_width - w) // 2, y), receipt_code, fill='#666', font=font_normal)
            y += line_height
            
            thank_you = ArabicReceiptGenerator.format_arabic_text("شكراً لتعاملكم مع شركة مكة المكرمة")
            w = draw.textlength(thank_you, font=font_bold)
            draw.text(((img_width - w) // 2, y), thank_you, fill='#000', font=font_bold)
            
            # حفظ الصورة
            img.save(output_path, 'JPEG', quality=95)
            
            print(f" تم إنشاء فاتورة: {output_path}")
            return output_path
            
        except Exception as e:
            print(f" خطأ في إنشاء الفاتورة: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def get_arabic_font(size=14, bold=False):
        """الحصول على خط عربي"""
        try:
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/tahoma.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/System/Library/Fonts/Arial.ttf",
            ]
            
            for path in font_paths:
                if os.path.exists(path):
                    try:
                        return ImageFont.truetype(path, size + (2 if bold else 0))
                    except:
                        continue
            
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()

def create_arabic_receipt(receipt_data: Dict, output_path: str = None):
    """دالة مبسطة لإنشاء فاتورة"""
    return ArabicReceiptGenerator.generate_receipt(receipt_data, output_path)