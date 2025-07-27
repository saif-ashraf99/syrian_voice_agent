# Demo Scenarios for Syrian Arabic Voice Agent

This document provides test scenarios to demonstrate the capabilities of the Syrian Arabic Voice Agent system. Use these scenarios to showcase the system's functionality during demos and evaluations.

## SIP Call Demo Scenarios

### Scenario 1: Complete Order Flow

**Objective**: Demonstrate end-to-end order processing

**Call Script**:

1. **Customer**: "السلام عليكم"

   - **Expected Response**: "وعليكم السلام وأهلاً وسهلاً بك في مطعم شاركو تشيكن. كيف ممكن ساعدك اليوم؟"
2. **Customer**: "بدي أطلب أكل"

   - **Expected Response**: "أكيد! شو بدك تطلب من عندنا؟ عندنا شاورما دجاج، فروج مشوي، كباب، وكتير أشياء طيبة."
3. **Customer**: "بدي شاورما دجاج وحمص"

   - **Expected Response**: "شاورما دجاج وحمص، اختيار ممتاز! كم قطعة شاورما بدك؟"
4. **Customer**: "قطعتين شاورما"

   - **Expected Response**: "قطعتين شاورما دجاج وحمص. بدك تضيف شي تاني؟ عندنا فتوش وتبولة كتير طيبين."
5. **Customer**: "لا، هيك بس"

   - **Expected Response**: "تمام. اسمك شو لو سمحت؟"
6. **Customer**: "أحمد محمد"

   - **Expected Response**: "شكراً أحمد. طلبك: قطعتين شاورما دجاج وحمص. المجموع 38 دولار. رقم الطلب A1B2C3D4. راح يكون جاهز خلال 25 دقيقة. شكراً إلك!"

### Scenario 2: Menu Inquiry

**Objective**: Show information handling capabilities

**Call Script**:

1. **Customer**: "مرحبا، شو عندكم من الأكل؟"

   - **Expected Response**: "أهلاً فيك! عندنا أطباق سورية أصيلة. من الأطباق الرئيسية: شاورما دجاج، فروج مشوي، وكباب. ومن المقبلات: حمص، فتوش، وتبولة. شو بيعجبك؟"
2. **Customer**: "قديش سعر الشاورما؟"

   - **Expected Response**: "شاورما الدجاج بـ 15 دولار للقطعة. طعمها رائع ومحضرة بالطريقة السورية الأصيلة. بدك تطلب؟"

### Scenario 3: Complaint Handling

**Objective**: Demonstrate empathetic response and problem-solving

**Call Script**:

1. **Customer**: "مرحبا، الأكل اللي طلبته وصل بارد"

   - **Expected Response**: "آسف كتير لهالشي! هاد مش مقبول أبداً. ممكن تعطيني رقم الطلب لأشوف شو صار؟"
2. **Customer**: "رقم الطلب A1B2C3D4"

   - **Expected Response**: "شكراً إلك. راح أتأكد من الموضوع مع المطبخ. بدي أعوضك عن هالتجربة السيئة. راح أبعتلك طلب جديد ساخن، وكمان راح أضيفلك حمص مجاني. موافق؟"
3. **Customer**: "تمام، شكراً"

   - **Expected Response**: "العفو! هاي أقل واجب. الطلب الجديد راح يوصلك خلال 20 دقيقة. وآسف مرة تانية لهالإزعاج."

### Scenario 4: Upselling Demonstration

**Objective**: Show natural sales techniques

**Call Script**:

1. **Customer**: "بدي شاورما دجاج بس"

   - **Expected Response**: "شاورما دجاج، اختيار رائع! بدك تضيفلها حمص؟ بيطلع معها طعم أطيب، وعندنا عرض اليوم: الحمص بنص السعر مع الشاورما."
2. **Customer**: "أوكي، حمص كمان"

   - **Expected Response**: "ممتاز! وبدك تشرب شي؟ عندنا عيران طازج بيروح كتير مع الأكل السوري."

## UI Testing Demo Scenarios

### Voice Testing Interface Demo

1. **Open Streamlit Interface**

   - Navigate to `http://localhost:8501`
   - Show the clean, professional interface
2. **Test Intent Detection**

   **Input**: "مرحبا، بدي أطلب شاورما دجاج وحمص"

   - **Show**: Intent = "order"
   - **Show**: Entities = food_items: ["شاورما دجاج", "حمص"]
   - **Show**: Confidence > 0.9
   - **Show**: Syrian Arabic response
   - **Play**: Generated audio
3. **Test Different Intents**

   **Question Intent**:

   - **Input**: "شو عندكم من الأكل؟"
   - **Show**: Intent = "question", appropriate response

   **Complaint Intent**:

   - **Input**: "الأكل وصل بارد"
   - **Show**: Intent = "complaint", empathetic response

   **Greeting Intent**:

   - **Input**: "السلام عليكم"
   - **Show**: Intent = "greeting", warm welcome
4. **Show Conversation History**

   - Display previous interactions
   - Show conversation flow
   - Demonstrate context awareness

### Order Management Demo

1. **Create New Order**

   - Show menu loading from API
   - Demonstrate order creation
   - Show order confirmation with ETA
2. **View Recent Orders**

   - Display order history
   - Show order details
   - Demonstrate status tracking

### Monitoring Dashboard Demo

1. **Real-time Metrics**

   - Show conversation count
   - Display active calls
   - Show order statistics
2. **Analytics Charts**

   - Intent distribution pie chart
   - Confidence score histogram
   - Timeline of conversations
   - Popular items analysis
