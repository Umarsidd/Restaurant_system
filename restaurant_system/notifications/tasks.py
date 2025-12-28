"""
Celery tasks for notifications and background jobs
"""
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


@shared_task
def send_kitchen_notification(order_id):
    """Send email notification to kitchen when new order is placed"""
    from orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        subject = f'New Order #{order.id} - Table {order.table.table_number}'
        message = f"""
        New order received!
        
        Table: {order.table.table_number}
        Waiter: {order.waiter.get_full_name() or order.waiter.username}
        Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Items:
        """
        
        for item in order.items.all():
            message += f"\n- {item.quantity}x {item.menu_item.name}"
        
        if order.notes:
            message += f"\n\nNotes: {order.notes}"
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['kitchen@restaurant.com'],  # Replace with actual kitchen email
            fail_silently=False,
        )
        return f"Kitchen notified for order #{order.id}"
    except Exception as e:
        return f"Error sending kitchen notification: {str(e)}"


@shared_task
def auto_close_abandoned_tables():
    """Auto-close tables that have been inactive for more than 3 hours"""
    from tables.models import Table
    
    threshold = timezone.now() - timedelta(hours=3)
    abandoned_tables = Table.objects.filter(
        status__in=['OCCUPIED', 'BILL_REQUESTED'],
        last_activity__lt=threshold
    )
    
    count = 0
    for table in abandoned_tables:
        table.status = Table.Status.CLOSED
        table.save()
        count += 1
    
    return f"Closed {count} abandoned tables"


@shared_task
def alert_pending_bills():
    """Alert manager about bills pending payment for more than 30 minutes"""
    from billing.models import Bill
    
    threshold = timezone.now() - timedelta(minutes=30)
    pending_bills = Bill.objects.filter(
        status='PENDING_PAYMENT',
        generated_at__lt=threshold
    )
    
    if pending_bills.exists():
        bill_list = "\n".join([
            f"- Bill #{bill.id} (Table {bill.table.table_number}): ₹{bill.total_amount}"
            for bill in pending_bills
        ])
        
        subject = f'Alert: {pending_bills.count()} Pending Bills'
        message = f"""
        The following bills have been pending payment for more than 30 minutes:
        
        {bill_list}
        
        Please follow up with the cashier.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['manager@restaurant.com'],  # Replace with actual manager email
            fail_silently=False,
        )
        return f"Alert sent for {pending_bills.count()} pending bills"
    
    return "No pending bills to alert"
