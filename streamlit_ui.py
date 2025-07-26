import streamlit as st
import requests
import json
import base64
import io
import tempfile
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Syrian Arabic Voice Agent - Testing Interface",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for RTL support and Arabic text
st.markdown("""
<style>
    .arabic-text {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', 'Tahoma', sans-serif;
    }
    .conversation-bubble {
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #e3f2fd;
        margin-left: auto;
        text-align: right;
    }
    .agent-bubble {
        background-color: #f3e5f5;
        margin-right: auto;
        text-align: left;
    }
    .intent-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
    .intent-order { background-color: #4caf50; color: white; }
    .intent-complaint { background-color: #f44336; color: white; }
    .intent-question { background-color: #2196f3; color: white; }
    .intent-greeting { background-color: #ff9800; color: white; }
    .intent-goodbye { background-color: #9c27b0; color: white; }
    .intent-unknown { background-color: #757575; color: white; }
</style>
""", unsafe_allow_html=True)

# Backend URL configuration
BACKEND_URL = st.sidebar.text_input(
    "Backend URL", 
    value="http://localhost:5000",
    help="URL of the Flask backend server"
)

# Sidebar navigation
st.sidebar.title("🎤 Syrian Voice Agent")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Voice Testing", "Order Management", "Conversation Logs", "Monitoring Dashboard"]
)

def test_backend_connection():
    """Test if backend is accessible"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/menu", timeout=5)
        return response.status_code == 200
    except:
        return False

def display_intent_badge(intent):
    """Display intent as a colored badge"""
    return f'<span class="intent-badge intent-{intent}">{intent.upper()}</span>'

def format_arabic_text(text):
    """Format Arabic text with RTL support"""
    return f'<div class="arabic-text">{text}</div>'

# Main content based on selected page
if page == "Voice Testing":
    st.title("🎤 Voice Agent Testing Interface")
    st.markdown("Test the Syrian Arabic voice agent with text input or audio upload")
    
    # Check backend connection
    if not test_backend_connection():
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}. Please check if the server is running.")
        st.stop()
    
    st.success(f"✅ Connected to backend at {BACKEND_URL}")
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Methods")
        
        # Text input tab
        input_method = st.radio(
            "Choose input method:",
            ["Text Input", "Audio Upload (Future Feature)"]
        )
        
        if input_method == "Text Input":
            st.markdown("### Text Input (Arabic)")
            
            # Predefined examples
            examples = {
                "Order Example": "مرحبا، بدي أطلب شاورما دجاج وحمص",
                "Question Example": "شو عندكم من الأكل؟",
                "Complaint Example": "الأكل وصل بارد",
                "Greeting Example": "السلام عليكم"
            }
            
            selected_example = st.selectbox("Quick Examples:", ["Custom"] + list(examples.keys()))
            
            if selected_example != "Custom":
                default_text = examples[selected_example]
            else:
                default_text = ""
            
            user_input = st.text_area(
                "Enter your message in Syrian Arabic:",
                value=default_text,
                height=100,
                help="Type your message in Arabic. The agent will detect intent and respond."
            )
            
            if st.button("🎯 Test Voice Agent", type="primary"):
                if user_input.strip():
                    with st.spinner("Processing..."):
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/api/voice_agent/test_voice",
                                json={"text": user_input},
                                timeout=30
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                # Store in session state for conversation history
                                if 'conversation_history' not in st.session_state:
                                    st.session_state.conversation_history = []
                                
                                st.session_state.conversation_history.append({
                                    'timestamp': datetime.now(),
                                    'user_input': user_input,
                                    'result': result
                                })
                                
                                st.success("✅ Response generated successfully!")
                                
                            else:
                                st.error(f"❌ Error: {response.status_code} - {response.text}")
                                
                        except requests.exceptions.Timeout:
                            st.error("❌ Request timed out. The backend might be processing a complex request.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("Please enter some text to test.")
        
        else:
            st.info("🚧 Audio upload feature will be implemented in the next version.")
            st.markdown("For now, please use text input to test the voice agent.")
    
    with col2:
        st.subheader("Latest Response")
        
        if 'conversation_history' in st.session_state and st.session_state.conversation_history:
            latest = st.session_state.conversation_history[-1]
            result = latest['result']
            
            # Display results
            st.markdown("**Transcribed Input:**")
            st.markdown(format_arabic_text(result['transcribed_input']), unsafe_allow_html=True)
            
            st.markdown("**Detected Intent:**")
            st.markdown(display_intent_badge(result['detected_intent']), unsafe_allow_html=True)
            
            st.markdown(f"**Confidence:** {result['confidence']:.2f}")
            
            if result['entities']:
                st.markdown("**Entities:**")
                for entity_type, entities in result['entities'].items():
                    if entities:
                        st.write(f"- {entity_type}: {', '.join(entities)}")
            
            st.markdown("**Agent Response:**")
            st.markdown(format_arabic_text(result['agent_response']), unsafe_allow_html=True)
            
            # Audio player (if available)
            if result.get('audio_base64'):
                st.markdown("**Generated Audio:**")
                try:
                    audio_bytes = base64.b64decode(result['audio_base64'])
                    st.audio(audio_bytes, format='audio/wav')
                except Exception as e:
                    st.warning(f"Could not play audio: {str(e)}")
        else:
            st.info("No responses yet. Test the voice agent to see results here.")
    
    # Conversation History
    if 'conversation_history' in st.session_state and st.session_state.conversation_history:
        st.subheader("💬 Conversation History")
        
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5
            with st.expander(f"Conversation {len(st.session_state.conversation_history) - i} - {conv['timestamp'].strftime('%H:%M:%S')}"):
                result = conv['result']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**User Input:**")
                    st.markdown(format_arabic_text(conv['user_input']), unsafe_allow_html=True)
                    
                    st.markdown("**Intent & Confidence:**")
                    st.markdown(f"{display_intent_badge(result['detected_intent'])} ({result['confidence']:.2f})", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Agent Response:**")
                    st.markdown(format_arabic_text(result['agent_response']), unsafe_allow_html=True)

elif page == "Order Management":
    st.title("📋 Order Management")
    
    if not test_backend_connection():
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}")
        st.stop()
    
    # Create new order section
    st.subheader("🆕 Create New Order")
    
    with st.form("new_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name *", placeholder="أحمد محمد")
            phone = st.text_input("Phone Number", placeholder="+963123456789")
        
        with col2:
            notes = st.text_area("Order Notes", placeholder="Extra sauce, no onions...")
        
        st.markdown("**Order Items:**")
        
        # Get menu from backend
        try:
            menu_response = requests.get(f"{BACKEND_URL}/api/menu")
            if menu_response.status_code == 200:
                menu = menu_response.json()
                
                order_items = []
                for category in menu['categories']:
                    st.markdown(f"**{category['name']} ({category['name_en']})**")
                    
                    for item in category['items']:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.write(f"{item['name']} ({item['name_en']}) - ${item['price']:.2f}")
                        
                        with col2:
                            quantity = st.number_input(
                                f"Qty", 
                                min_value=0, 
                                max_value=10, 
                                value=0, 
                                key=f"qty_{item['id']}"
                            )
                        
                        with col3:
                            if quantity > 0:
                                order_items.append({
                                    "item": item['name'],
                                    "quantity": quantity,
                                    "price": item['price']
                                })
                                st.write(f"${quantity * item['price']:.2f}")
            else:
                st.error("Could not load menu")
                order_items = []
                
        except Exception as e:
            st.error(f"Error loading menu: {str(e)}")
            order_items = []
        
        submitted = st.form_submit_button("📤 Submit Order", type="primary")
        
        if submitted:
            if customer_name and order_items:
                try:
                    order_data = {
                        "name": customer_name,
                        "order_list": order_items,
                        "phone": phone,
                        "notes": notes
                    }
                    
                    response = requests.post(
                        f"{BACKEND_URL}/api/submit-order",
                        json=order_data
                    )
                    
                    if response.status_code == 201:
                        result = response.json()
                        st.success(f"✅ Order submitted successfully!")
                        st.info(f"Order ID: {result['order_id']}")
                        st.info(f"ETA: {result['eta_minutes']} minutes")
                        st.markdown(format_arabic_text(result['message']), unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error submitting order: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please fill in customer name and select at least one item.")
    
    # Recent orders
    st.subheader("📋 Recent Orders")
    
    try:
        orders_response = requests.get(f"{BACKEND_URL}/api/orders?limit=10")
        if orders_response.status_code == 200:
            orders_data = orders_response.json()
            orders = orders_data['orders']
            
            if orders:
                for order in orders:
                    with st.expander(f"Order {order['order_id']} - {order['customer_name']} ({order['status']})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Customer:** {order['customer_name']}")
                            st.write(f"**Phone:** {order.get('phone', 'N/A')}")
                            st.write(f"**Total:** ${order['total_price']:.2f}")
                            st.write(f"**Status:** {order['status']}")
                        
                        with col2:
                            st.write(f"**Order Time:** {order['order_time'][:19]}")
                            st.write(f"**ETA:** {order['eta_minutes']} minutes")
                            if order.get('notes'):
                                st.write(f"**Notes:** {order['notes']}")
                        
                        st.write("**Items:**")
                        for item in order['order_items']:
                            st.write(f"- {item['item']} x{item['quantity']} = ${item['total_price']:.2f}")
            else:
                st.info("No orders found.")
        else:
            st.error("Could not load orders")
            
    except Exception as e:
        st.error(f"Error loading orders: {str(e)}")

elif page == "Conversation Logs":
    st.title("💬 Conversation Logs")
    
    if not test_backend_connection():
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}")
        st.stop()
    
    try:
        logs_response = requests.get(f"{BACKEND_URL}/api/voice_agent/conversation_logs")
        if logs_response.status_code == 200:
            logs_data = logs_response.json()
            logs = logs_data['logs']
            
            st.metric("Total Conversations", logs_data['total_conversations'])
            st.metric("Active Calls", logs_data['active_calls'])
            
            if logs:
                # Filter options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    intent_filter = st.selectbox(
                        "Filter by Intent:",
                        ["All"] + list(set([log['intent'] for log in logs]))
                    )
                
                with col2:
                    test_mode_filter = st.selectbox(
                        "Filter by Mode:",
                        ["All", "Test Mode", "Live Calls"]
                    )
                
                with col3:
                    limit = st.number_input("Show last N conversations:", min_value=1, max_value=100, value=20)
                
                # Apply filters
                filtered_logs = logs
                
                if intent_filter != "All":
                    filtered_logs = [log for log in filtered_logs if log['intent'] == intent_filter]
                
                if test_mode_filter == "Test Mode":
                    filtered_logs = [log for log in filtered_logs if log.get('test_mode', False)]
                elif test_mode_filter == "Live Calls":
                    filtered_logs = [log for log in filtered_logs if not log.get('test_mode', False)]
                
                # Sort and limit
                filtered_logs = sorted(filtered_logs, key=lambda x: x['timestamp'], reverse=True)[:limit]
                
                st.subheader(f"Showing {len(filtered_logs)} conversations")
                
                for i, log in enumerate(filtered_logs):
                    with st.expander(f"Conversation {i+1} - {log['timestamp'][:19]} - {display_intent_badge(log['intent'])}", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Customer Input:**")
                            st.markdown(format_arabic_text(log['customer_text']), unsafe_allow_html=True)
                            
                            st.markdown("**Intent & Confidence:**")
                            st.markdown(f"{display_intent_badge(log['intent'])} ({log['confidence']:.2f})", unsafe_allow_html=True)
                            
                            if log.get('entities'):
                                st.markdown("**Entities:**")
                                for entity_type, entities in log['entities'].items():
                                    if entities:
                                        st.write(f"- {entity_type}: {', '.join(entities)}")
                        
                        with col2:
                            st.markdown("**Agent Response:**")
                            st.markdown(format_arabic_text(log['agent_response']), unsafe_allow_html=True)
                            
                            if log.get('call_sid'):
                                st.write(f"**Call ID:** {log['call_sid']}")
                            
                            if log.get('test_mode'):
                                st.info("🧪 Test Mode")
                            else:
                                st.info("📞 Live Call")
            else:
                st.info("No conversation logs found.")
        else:
            st.error("Could not load conversation logs")
            
    except Exception as e:
        st.error(f"Error loading logs: {str(e)}")

elif page == "Monitoring Dashboard":
    st.title("📊 Monitoring Dashboard")
    
    if not test_backend_connection():
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}")
        st.stop()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Get conversation logs
        logs_response = requests.get(f"{BACKEND_URL}/api/voice_agent/conversation_logs")
        orders_response = requests.get(f"{BACKEND_URL}/api/stats")
        
        if logs_response.status_code == 200:
            logs_data = logs_response.json()
            
            with col1:
                st.metric("Total Conversations", logs_data['total_conversations'])
            
            with col2:
                st.metric("Active Calls", logs_data['active_calls'])
        
        if orders_response.status_code == 200:
            stats_data = orders_response.json()
            
            with col3:
                st.metric("Total Orders", stats_data['total_orders'])
            
            with col4:
                st.metric("Total Revenue", f"${stats_data['total_revenue']:.2f}")
        
        # Charts
        if logs_response.status_code == 200 and logs_data['logs']:
            logs = logs_data['logs']
            
            # Intent distribution
            st.subheader("📈 Intent Distribution")
            intent_counts = {}
            for log in logs:
                intent = log['intent']
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            if intent_counts:
                fig_intent = px.pie(
                    values=list(intent_counts.values()),
                    names=list(intent_counts.keys()),
                    title="Distribution of Customer Intents"
                )
                st.plotly_chart(fig_intent, use_container_width=True)
            
            # Confidence distribution
            st.subheader("🎯 Confidence Score Distribution")
            confidences = [log['confidence'] for log in logs if 'confidence' in log]
            
            if confidences:
                fig_conf = px.histogram(
                    x=confidences,
                    nbins=20,
                    title="Distribution of Intent Detection Confidence",
                    labels={'x': 'Confidence Score', 'y': 'Count'}
                )
                st.plotly_chart(fig_conf, use_container_width=True)
            
            # Timeline
            st.subheader("⏰ Conversation Timeline")
            
            # Convert timestamps and create hourly counts
            from datetime import datetime
            import pandas as pd
            
            timestamps = []
            for log in logs:
                try:
                    ts = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
                    timestamps.append(ts)
                except:
                    continue
            
            if timestamps:
                df = pd.DataFrame({'timestamp': timestamps})
                df['hour'] = df['timestamp'].dt.floor('H')
                hourly_counts = df.groupby('hour').size().reset_index(name='count')
                
                fig_timeline = px.line(
                    hourly_counts,
                    x='hour',
                    y='count',
                    title="Conversations per Hour",
                    labels={'hour': 'Time', 'count': 'Number of Conversations'}
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Order statistics
        if orders_response.status_code == 200 and stats_data['total_orders'] > 0:
            st.subheader("🍽️ Order Statistics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Orders by status
                if stats_data['orders_by_status']:
                    fig_status = px.pie(
                        values=list(stats_data['orders_by_status'].values()),
                        names=list(stats_data['orders_by_status'].keys()),
                        title="Orders by Status"
                    )
                    st.plotly_chart(fig_status, use_container_width=True)
            
            with col2:
                # Popular items
                if stats_data['popular_items']:
                    items_df = pd.DataFrame(stats_data['popular_items'])
                    fig_items = px.bar(
                        items_df,
                        x='count',
                        y='item',
                        orientation='h',
                        title="Most Popular Items"
                    )
                    st.plotly_chart(fig_items, use_container_width=True)
            
            # Key metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Average Order Value", f"${stats_data['average_order_value']:.2f}")
            
            with col2:
                st.metric("Total Revenue", f"${stats_data['total_revenue']:.2f}")
    
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Syrian Arabic Voice Agent**")
st.sidebar.markdown("Built for Charco Chicken Restaurant")
st.sidebar.markdown("🎤 Real-time SIP Integration")
st.sidebar.markdown("🧠 AI-Powered Intent Detection")
st.sidebar.markdown("🗣️ Flawless Syrian Arabic TTS")

