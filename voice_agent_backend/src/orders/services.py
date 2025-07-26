import uuid
import random
import logging
from datetime import datetime, timedelta
from .storage import orders_storage
from .config import ORDER_ID_LENGTH, MIN_ETA_MINUTES, MAX_ETA_MINUTES, VALID_ORDER_STATUSES

logger = logging.getLogger(__name__)

class OrderService:
    @staticmethod
    def validate_order_data(data):
        """Validate order submission data"""
        errors = []
        
        if not data:
            errors.append('No data provided')
            return errors
        
        # Validate required fields
        if 'name' not in data or not data['name'].strip():
            errors.append('Name is required and cannot be empty')
        
        if 'order_list' not in data:
            errors.append('Order list is required')
        elif not isinstance(data['order_list'], list) or not data['order_list']:
            errors.append('Order list must be a non-empty array')
        
        return errors
    
    @staticmethod
    def validate_order_items(order_list):
        """Validate and process order items"""
        validated_items = []
        total_price = 0.0
        
        for item in order_list:
            if not isinstance(item, dict):
                raise ValueError('Each order item must be an object')
            
            item_name = item.get('item', '').strip()
            quantity = item.get('quantity', 1)
            price = item.get('price', 0.0)
            
            if not item_name:
                raise ValueError('Item name cannot be empty')
            
            try:
                quantity = int(quantity)
                price = float(price)
                if quantity <= 0 or price < 0:
                    raise ValueError()
            except (ValueError, TypeError):
                raise ValueError('Invalid quantity or price values')
            
            item_total = quantity * price
            total_price += item_total
            
            validated_items.append({
                'item': item_name,
                'quantity': quantity,
                'unit_price': price,
                'total_price': item_total
            })
        
        return validated_items, round(total_price, 2)
    
    @staticmethod
    def generate_order_id():
        """Generate unique order ID"""
        return str(uuid.uuid4())[:ORDER_ID_LENGTH].upper()
    
    @staticmethod
    def calculate_eta():
        """Calculate estimated time of arrival"""
        eta_minutes = random.randint(MIN_ETA_MINUTES, MAX_ETA_MINUTES)
        eta_time = datetime.now() + timedelta(minutes=eta_minutes)
        return eta_time, eta_minutes
    
    @staticmethod
    def create_order(data):
        """Create a new order"""
        # Validate basic data
        validation_errors = OrderService.validate_order_data(data)
        if validation_errors:
            raise ValueError('; '.join(validation_errors))
        
        name = data['name'].strip()
        order_list = data['order_list']
        phone = data.get('phone', '')
        notes = data.get('notes', '')
        
        # Validate and process order items
        validated_items, total_price = OrderService.validate_order_items(order_list)
        
        # Generate order details
        order_id = OrderService.generate_order_id()
        eta_time, eta_minutes = OrderService.calculate_eta()
        
        # Create order object
        order = {
            'order_id': order_id,
            'customer_name': name,
            'phone': phone,
            'order_items': validated_items,
            'total_price': total_price,
            'notes': notes,
            'order_time': datetime.now().isoformat(),
            'eta': eta_time.isoformat(),
            'eta_minutes': eta_minutes,
            'status': 'confirmed'
        }
        
        # Store the order
        orders_storage.append(order)
        
        logger.info(f"New order created: {order_id} for {name}")
        
        return order
    
    @staticmethod
    def get_orders(status=None, customer_name=None, limit=None):
        """Get filtered orders"""
        filtered_orders = orders_storage.copy()
        
        if status:
            filtered_orders = [order for order in filtered_orders if order['status'] == status]
        
        if customer_name:
            filtered_orders = [
                order for order in filtered_orders 
                if customer_name.lower() in order['customer_name'].lower()
            ]
        
        # Sort by order time (newest first)
        filtered_orders.sort(key=lambda x: x['order_time'], reverse=True)
        
        # Apply limit
        if limit and limit > 0:
            filtered_orders = filtered_orders[:limit]
        
        return filtered_orders
    
    @staticmethod
    def get_order_by_id(order_id):
        """Get order by ID"""
        return next((order for order in orders_storage if order['order_id'] == order_id), None)
    
    @staticmethod
    def update_order_status(order_id, new_status):
        """Update order status"""
        if new_status not in VALID_ORDER_STATUSES:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(VALID_ORDER_STATUSES)}')
        
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError('Order not found')
        
        old_status = order['status']
        order['status'] = new_status
        order['status_updated'] = datetime.now().isoformat()
        
        logger.info(f"Order {order_id} status updated from {old_status} to {new_status}")
        
        return {
            'order_id': order_id,
            'old_status': old_status,
            'new_status': new_status,
            'updated_at': order['status_updated']
        }
    
    @staticmethod
    def get_order_statistics():
        """Calculate order statistics"""
        total_orders = len(orders_storage)
        
        if total_orders == 0:
            return {
                'total_orders': 0,
                'total_revenue': 0.0,
                'average_order_value': 0.0,
                'orders_by_status': {},
                'popular_items': []
            }
        
        # Calculate statistics
        total_revenue = sum(order['total_price'] for order in orders_storage)
        average_order_value = total_revenue / total_orders
        
        # Orders by status
        orders_by_status = {}
        for order in orders_storage:
            status = order['status']
            orders_by_status[status] = orders_by_status.get(status, 0) + 1
        
        # Popular items
        item_counts = {}
        for order in orders_storage:
            for item in order['order_items']:
                item_name = item['item']
                item_counts[item_name] = item_counts.get(item_name, 0) + item['quantity']
        
        popular_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'average_order_value': round(average_order_value, 2),
            'orders_by_status': orders_by_status,
            'popular_items': [{'item': item, 'count': count} for item, count in popular_items]
        }