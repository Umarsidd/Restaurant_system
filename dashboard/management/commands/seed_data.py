"""
Management command to seed database with demo data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tables.models import Table
from menu.models import MenuItem
from orders.models import Order, OrderItem
from billing.models import Bill
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with demo data for restaurant system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create users with different roles
        self.stdout.write('Creating users...')
        
        # Manager
        manager, _ = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@restaurant.com',
                'first_name': 'John',
                'last_name': 'Manager',
                'role': 'MANAGER',
                'employee_id': 'M001',
                'phone_number': '+1234567890',
            }
        )
        if _:
            manager.set_password('manager123')
            manager.is_staff = True
            manager.is_superuser = True
            manager.save()
        
        # Waiters
        waiter1, _ = User.objects.get_or_create(
            username='waiter1',
            defaults={
                'email': 'waiter1@restaurant.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'role': 'WAITER',
                'employee_id': 'W001',
                'phone_number': '+1234567891',
            }
        )
        if _:
            waiter1.set_password('waiter123')
            waiter1.is_staff = True
            waiter1.save()
        
        waiter2, _ = User.objects.get_or_create(
            username='waiter2',
            defaults={
                'email': 'waiter2@restaurant.com',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'role': 'WAITER',
                'employee_id': 'W002',
                'phone_number': '+1234567892',
            }
        )
        if _:
            waiter2.set_password('waiter123')
            waiter2.is_staff = True
            waiter2.save()
        
        # Cashier
        cashier, _ = User.objects.get_or_create(
            username='cashier',
            defaults={
                'email': 'cashier@restaurant.com',
                'first_name': 'Carol',
                'last_name': 'Davis',
                'role': 'CASHIER',
                'employee_id': 'C001',
                'phone_number': '+1234567893',
            }
        )
        if _:
            cashier.set_password('cashier123')
            cashier.is_staff = True
            cashier.save()
        
        self.stdout.write(self.style.SUCCESS('[OK] Users created'))
        
        # Create tables
        self.stdout.write('Creating tables...')
        tables_data = [
            ('T1', 2), ('T2', 2), ('T3', 4), ('T4', 4),
            ('T5', 4), ('T6', 6), ('T7', 6), ('T8', 8),
            ('T9', 8), ('T10', 10),
        ]
        
        for table_num, capacity in tables_data:
            Table.objects.get_or_create(
                table_number=table_num,
                defaults={'seating_capacity': capacity}
            )
        
        self.stdout.write(self.style.SUCCESS('[OK] Tables created'))
        
        # Create menu items
        self.stdout.write('Creating menu items...')
        menu_items = [
            # Starters
            ('Garlic Bread', 'STARTER', Decimal('4.99'), 'Crispy bread with garlic butter'),
            ('Spring Rolls', 'STARTER', Decimal('5.99'), 'Crispy vegetable spring rolls'),
            ('Caesar Salad', 'STARTER', Decimal('6.99'), 'Fresh romaine with caesar dressing'),
            ('Soup of the Day', 'STARTER', Decimal('4.49'), 'Chef\'s special soup'),
            
            # Main Course
            ('Margherita Pizza', 'MAIN', Decimal('12.99'), 'Classic tomato and mozzarella'),
            ('Pepperoni Pizza', 'MAIN', Decimal('14.99'), 'Loaded with pepperoni'),
            ('Pasta Carbonara', 'MAIN', Decimal('13.99'), 'Creamy bacon pasta'),
            ('Grilled Chicken', 'MAIN', Decimal('15.99'), 'Herb-marinated grilled chicken'),
            ('Fish and Chips', 'MAIN', Decimal('14.49'), 'Crispy battered fish'),
            ('Beef Burger', 'MAIN', Decimal('11.99'), 'Juicy beef patty with cheese'),
            ('Vegetable Stir Fry', 'MAIN', Decimal('10.99'), 'Mixed veggies in sauce'),
            ('Steak', 'MAIN', Decimal('24.99'), 'Premium ribeye steak'),
            
            # Drinks
            ('Coca Cola', 'DRINKS', Decimal('2.99'), 'Chilled soft drink'),
            ('Fresh Orange Juice', 'DRINKS', Decimal('3.99'), 'Freshly squeezed'),
            ('Iced Tea', 'DRINKS', Decimal('2.49'), 'Lemon iced tea'),
            ('Coffee', 'DRINKS', Decimal('2.99'), 'Freshly brewed'),
            ('Mineral Water', 'DRINKS', Decimal('1.99'), 'Still or sparkling'),
            
            # Desserts
            ('Chocolate Cake', 'DESSERT', Decimal('5.99'), 'Rich chocolate layer cake'),
            ('Ice Cream Sundae', 'DESSERT', Decimal('4.99'), 'Three scoops with toppings'),
            ('Tiramisu', 'DESSERT', Decimal('6.49'), 'Italian coffee dessert'),
            ('Apple Pie', 'DESSERT', Decimal('5.49'), 'Warm apple pie with ice cream'),
        ]
        
        for name, category, price, description in menu_items:
            MenuItem.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'price': price,
                    'description': description,
                    'is_available': True
                }
            )
        
        self.stdout.write(self.style.SUCCESS('[OK] Menu items created'))
        
        # Create some sample orders
        self.stdout.write('Creating sample orders...')
        
        table3 = Table.objects.get(table_number='T3')
        table6 = Table.objects.get(table_number='T6')
        
        # Order 1 - In Kitchen
        if not table3.current_order:
            order1 = Order.objects.create(
                table=table3,
                waiter=waiter1,
                status='IN_KITCHEN',
                notes='Customer allergic to nuts'
            )
            
            pizza = MenuItem.objects.get(name='Margherita Pizza')
            salad = MenuItem.objects.get(name='Caesar Salad')
            coke = MenuItem.objects.get(name='Coca Cola')
            
            OrderItem.objects.create(order=order1, menu_item=pizza, quantity=2, price_at_order=pizza.price)
            OrderItem.objects.create(order=order1, menu_item=salad, quantity=1, price_at_order=salad.price)
            OrderItem.objects.create(order=order1, menu_item=coke, quantity=2, price_at_order=coke.price)
        
        # Order 2 - Placed
        if not table6.current_order:
            order2 = Order.objects.create(
                table=table6,
                waiter=waiter2,
                status='PLACED'
            )
            
            steak = MenuItem.objects.get(name='Steak')
            burger = MenuItem.objects.get(name='Beef Burger')
            juice = MenuItem.objects.get(name='Fresh Orange Juice')
            
            OrderItem.objects.create(order=order2, menu_item=steak, quantity=1, price_at_order=steak.price)
            OrderItem.objects.create(order=order2, menu_item=burger, quantity=2, price_at_order=burger.price)
            OrderItem.objects.create(order=order2, menu_item=juice, quantity=3, price_at_order=juice.price)
        
        self.stdout.write(self.style.SUCCESS('[OK] Sample orders created'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))
        self.stdout.write('Demo Credentials:')
        self.stdout.write('Manager:  username=manager  password=manager123')
        self.stdout.write('Waiter 1: username=waiter1  password=waiter123')
        self.stdout.write('Waiter 2: username=waiter2  password=waiter123')
        self.stdout.write('Cashier:  username=cashier  password=cashier123')
