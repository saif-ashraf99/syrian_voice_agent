from datetime import datetime
from .config import DEFAULT_CURRENCY

def get_menu_data():
    """Get restaurant menu data"""
    return {
        'categories': [
            {
                'name': 'الأطباق الرئيسية',
                'name_en': 'Main Dishes',
                'items': [
                    {
                        'id': 'shawarma_chicken',
                        'name': 'شاورما دجاج',
                        'name_en': 'Chicken Shawarma',
                        'description': 'شاورما دجاج طازجة مع الخضار والصوص',
                        'price': 15.00,
                        'available': True
                    },
                    {
                        'id': 'grilled_chicken',
                        'name': 'فروج مشوي',
                        'name_en': 'Grilled Chicken',
                        'description': 'فروج مشوي كامل مع البهارات السورية',
                        'price': 25.00,
                        'available': True
                    },
                    {
                        'id': 'kebab',
                        'name': 'كباب',
                        'name_en': 'Kebab',
                        'description': 'كباب لحم مشوي مع الأرز',
                        'price': 20.00,
                        'available': True
                    }
                ]
            },
            {
                'name': 'المقبلات',
                'name_en': 'Appetizers',
                'items': [
                    {
                        'id': 'hummus',
                        'name': 'حمص',
                        'name_en': 'Hummus',
                        'description': 'حمص طازج مع زيت الزيتون',
                        'price': 8.00,
                        'available': True
                    },
                    {
                        'id': 'fattoush',
                        'name': 'فتوش',
                        'name_en': 'Fattoush',
                        'description': 'سلطة فتوش بالخضار الطازجة',
                        'price': 10.00,
                        'available': True
                    },
                    {
                        'id': 'tabbouleh',
                        'name': 'تبولة',
                        'name_en': 'Tabbouleh',
                        'description': 'تبولة بالبقدونس والطماطم',
                        'price': 9.00,
                        'available': True
                    }
                ]
            },
            {
                'name': 'المشروبات',
                'name_en': 'Beverages',
                'items': [
                    {
                        'id': 'ayran',
                        'name': 'عيران',
                        'name_en': 'Ayran',
                        'description': 'عيران طازج',
                        'price': 3.00,
                        'available': True
                    },
                    {
                        'id': 'tea',
                        'name': 'شاي',
                        'name_en': 'Tea',
                        'description': 'شاي أحمر',
                        'price': 2.00,
                        'available': True
                    },
                    {
                        'id': 'coffee',
                        'name': 'قهوة',
                        'name_en': 'Coffee',
                        'description': 'قهوة عربية',
                        'price': 4.00,
                        'available': True
                    }
                ]
            }
        ],
        'currency': DEFAULT_CURRENCY,
        'last_updated': datetime.now().isoformat()
    }