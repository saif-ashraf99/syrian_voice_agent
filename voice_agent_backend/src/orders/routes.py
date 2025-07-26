import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from .services import OrderService
from .menu import get_menu_data

logger = logging.getLogger(__name__)

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/submit-order', methods=['POST'])
@cross_origin()
def submit_order():
    """
    Submit a new order
    Expected JSON payload:
    {
        "name": "Customer Name",
        "order_list": [
            {"item": "شاورما دجاج", "quantity": 2, "price": 15.00},
            {"item": "حمص", "quantity": 1, "price": 8.00}
        ],
        "phone": "+963123456789",  # Optional
        "notes": "Extra sauce"      # Optional
    }
    """
    try:
        data = request.get_json()
        order = OrderService.create_order(data)
        
        # Return response
        return jsonify({
            'order_id': order['order_id'],
            'eta': order['eta'][:5],  # Format HH:MM
            'eta_minutes': order['eta_minutes'],
            'total_price': order['total_price'],
            'status': order['status'],
            'message': f'شكراً {order["customer_name"]}! تم تأكيد طلبك. رقم الطلب: {order["order_id"]}. سيكون جاهز خلال {order["eta_minutes"]} دقيقة.'
        }), 201
        
    except ValueError as e:
        logger.warning(f"Order validation error: {e}")
        return jsonify({
            'error': str(e),
            'message': 'حدث خطأ في بيانات الطلب. يرجى التحقق من البيانات المدخلة.'
        }), 400
        
    except Exception as e:
        logger.error(f"Order submission error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'حدث خطأ في معالجة الطلب. يرجى المحاولة مرة أخرى.'
        }), 500

@orders_bp.route('/orders', methods=['GET'])
@cross_origin()
def get_orders():
    """Get all orders with optional filtering"""
    try:
        # Get query parameters
        status = request.args.get('status')
        customer_name = request.args.get('customer_name')
        limit = request.args.get('limit', type=int)
        
        # Get filtered orders
        filtered_orders = OrderService.get_orders(status, customer_name, limit)
        
        return jsonify({
            'orders': filtered_orders,
            'total_count': len(OrderService.get_orders()),
            'filtered_count': len(filtered_orders)
        })
        
    except Exception as e:
        logger.error(f"Get orders error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@orders_bp.route('/orders/<order_id>', methods=['GET'])
@cross_origin()
def get_order(order_id):
    """Get a specific order by ID"""
    try:
        order = OrderService.get_order_by_id(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify(order)
        
    except Exception as e:
        logger.error(f"Get order error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@orders_bp.route('/orders/<order_id>/status', methods=['PUT'])
@cross_origin()
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        result = OrderService.update_order_status(order_id, new_status)
        return jsonify(result)
        
    except ValueError as e:
        logger.warning(f"Order status update validation error: {e}")
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        logger.error(f"Update order status error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@orders_bp.route('/menu', methods=['GET'])
@cross_origin()
def get_menu():
    """Get restaurant menu"""
    try:
        menu = get_menu_data()
        return jsonify(menu)
        
    except Exception as e:
        logger.error(f"Get menu error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@orders_bp.route('/stats', methods=['GET'])
@cross_origin()
def get_order_stats():
    """Get order statistics"""
    try:
        stats = OrderService.get_order_statistics()
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Get stats error: {e}")
        return jsonify({'error': 'Internal server error'}), 500