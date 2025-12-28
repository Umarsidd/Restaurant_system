# 🍽️ Restaurant Live Table Order & Billing System

> **A comprehensive real-time restaurant management system for table management, order processing, and billing operations.**

![Django](https://img.shields.io/badge/Django-5.0.1-green) ![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Status](https://img.shields.io/badge/Status-Production--Ready-success)

**Live Demo:** [https://restaurant-system-jtqy.onrender.com](https://restaurant-system-jtqy.onrender.com)

---

## 🔑 Login Credentials

Access the system with these demo accounts:

| Role | Email | Password | Access Level |
|------|-------|----------|--------------|
| **👨‍💼 Manager** | `manager@restaurant.com` | `manager123` | Complete system access + admin panel + analytics |
| **👨‍🍳 Waiter** | `waiter1@restaurant.com` | `waiter123` | Create & manage orders, view table status |
| **💰 Cashier** | `cashier@restaurant.com` | `cashier123` | Generate bills, process payments, export PDFs |

**Admin Panel Access:** `/admin/` (Manager only)  
**Login Page:** `/login/`

---

## ✨ Key Features

### 🪑 Table Management
- **4 Status Types:** Available, Occupied, Bill Requested, Closed
- **Real-time Status Dashboard** - Live updates showing all tables
- **Auto-Status Transitions** - Status changes automatically based on orders/bills
- **Capacity Tracking** - Seating capacity (2-10 seats) for each table
- **Smart Filtering** - Filter tables by status for quick overview

### 📋 Order Management
- **Create Orders** - Select table, add multiple menu items with quantities
- **Order Lifecycle:** Placed → In Kitchen → Served
- **Real-time Updates** - Track order progress live
- **Order History** - View all orders with timestamps and status
- **Waiter Assignment** - Each order linked to specific waiter
- **Price Snapshots** - Historical pricing preserved for accuracy

### 💰 Billing System
- **Auto-Calculate Bills** - Subtotal + 5% tax = Total
- **PDF Export** - Professional invoice generation with restaurant branding
- **Payment Tracking** - Mark bills as Paid/Pending
- **Revenue Analytics** - Daily/monthly revenue reports
- **Tax Reports** - Automated tax calculations

### 🍕 Menu Management
- **4 Categories:** Starters, Main Course, Drinks, Desserts
- **21 Pre-loaded Items** - Sample menu with images
- **Availability Toggle** - Mark items as available/unavailable
- **Price Management** - Easy price updates (preserves order history)
- **Image Support** - Menu item photos for better UX

### 👥 Role-Based Access Control
- **3 User Roles:** Manager, Waiter, Cashier
- **Permission-Based UI** - Each role sees only relevant features
- **Secure Authentication** - Django's built-in auth system
- **Custom Dashboards** - Role-specific home pages

### 📊 Analytics & Reports (Manager Only)
- **Today's Statistics:**
  - Total orders placed
  - Active orders in kitchen
  - Revenue generated
  - Bills pending payment
- **Table Utilization:** Available vs Occupied ratio
- **Performance Metrics:** Orders per waiter, average bill amount
- **Recent Activity Feed:** Latest orders and payments

### 🔔 Background Tasks (Celery)
- **Kitchen Notifications** - Auto-email when new order placed
- **Auto-Close Tables** - Close abandoned tables after 3 hours
- **Pending Bill Alerts** - Notify manager about unpaid bills >30 min

---

## 🎨 UI/UX Features

### Design Philosophy
- **Clean & Intuitive** - Minimal learning curve for restaurant staff
- **Mobile-Responsive** - Works on tablets and phones
- **Color-Coded Status** - Quick visual identification
  - 🟢 Green - Available
  - 🔵 Blue - Occupied
  - 🟡 Yellow - Bill Requested
  - ⚫ Gray - Closed
- **Icon-Based Navigation** - Emoji icons for better visibility

### Page-by-Page UI Overview

#### 🏠 Login Page (`/login/`)
- Simple email/password form
- Remember me checkbox
- Role-based redirect after login
- Clean, professional design

#### 👨‍🍳 Waiter Dashboard
**Stats Cards:**
- Active Orders count
- Available Tables count
- Today's Orders count

**Quick Actions:**
- ➕ Create New Order
- 📋 View All Orders
- 🪑 Table Status

**Active Orders Table:**
- Table number
- Order status (color-coded)
- Item count
- Total amount
- Creation time
- Quick view button

#### 💰 Cashier Dashboard
**Stats Cards:**
- Pending Bills count
- Today's Bills generated
- Today's Paid Bills
- Today's Revenue (₹)

**Quick Actions:**
- 🧾 Generate Bill
- 💵 View Pending Bills
- 🪑 Table Status

**Pending Bills Table:**
- Table number
- Order total
- Generated time
- Mark as Paid button
- Export PDF option

#### 👨‍💼 Manager Dashboard
**Comprehensive Stats:**
- Total Tables | Available | Occupied
- Today's Orders | Active Orders
- Today's Bills | Paid Bills
- Today's Revenue

**Quick Actions:**
- ➕ Add Table
- 🍕 Manage Menu
- 👥 View Staff
- 📊 Full Reports

**Recent Activity:**
- Latest 5 orders with details
- Latest 5 bills with payment status

#### 🪑 Table Status Dashboard (All Users)
**Visual Grid Display:**
- All tables shown in grid layout
- Color-coded by status
- Shows table number + capacity
- Click to view details
- Real-time status updates

#### 📝 Create Order Page
**Step-by-step Flow:**
1. Select available table from dropdown
2. Browse menu items by category
3. Add items with quantity selector
4. Review order summary
5. Submit (table → Occupied)

**Features:**
- Live total calculation
- Remove items option
- Category filters for menu
- Item availability check

#### 🧾 Bill Generation Page
**Smart Bill Creation:**
- Auto-selects served orders
- Shows order items breakdown
- Calculates subtotal
- Adds 5% tax automatically
- Displays final total
- Generate button → Creates bill

#### 📄 Bill Detail Page
**Professional Invoice View:**
- Restaurant header
- Bill number & timestamp
- Table information
- Complete order breakdown
- Tax calculation details
- Payment status
- Export PDF button
- Mark as Paid button (if pending)

---

## 🏗️ System Architecture

### Technology Stack

```
Frontend:
├── HTML5 + CSS3 (Custom styling)
├── Bootstrap 5 (Responsive grid)
├── JavaScript (Dynamic interactions)
└── Django Templates (Server-side rendering)

Backend:
├── Django 5.0.1 (Web framework)
├── Django REST Framework 3.15.2 (API endpoints)
├── SQLite / PostgreSQL (Database)
├── Celery 5.3.4 (Background tasks)
├── Redis 5.0.1 (Task broker)
└── ReportLab 4.0.9 (PDF generation)

Deployment:
├── Gunicorn (WSGI server)
├── WhiteNoise (Static files)
├── Render.com (Cloud hosting)
└── PostgreSQL (Production DB)
```

### Database Schema

```
┌─────────────┐
│    User     │ (Custom Auth Model)
├─────────────┤
│ id          │
│ email       │ (unique, used for login)
│ role        │ (WAITER/CASHIER/MANAGER)
│ employee_id │
│ phone       │
└─────────────┘
       │
       │ waiter_id (FK)
       ▼
┌─────────────┐      ┌──────────────┐
│   Order     │      │  OrderItem   │
├─────────────┤      ├──────────────┤
│ id          │◄─────┤ order_id     │
│ table_id    │      │ menu_item_id │
│ waiter_id   │      │ quantity     │
│ status      │      │ price_at_order│ (snapshot)
│ created_at  │      └──────────────┘
└─────────────┘
       │
       │ table_id (FK)
       ▼
┌─────────────┐      ┌─────────────┐
│    Table    │      │  MenuItem   │
├─────────────┤      ├─────────────┤
│ id          │      │ id          │
│ table_number│      │ name        │
│ capacity    │      │ category    │
│ status      │      │ price       │
│ last_activity│     │ image       │
└─────────────┘      │ is_available│
       │             └─────────────┘
       │
       │ table_id (FK)
       ▼
┌─────────────┐
│    Bill     │
├─────────────┤
│ id          │
│ order_id    │ (OneToOne)
│ table_id    │
│ cashier_id  │
│ subtotal    │
│ tax_amount  │
│ total_amount│
│ status      │
│ generated_at│
└─────────────┘
```

---

## 🚀 Complete Functionality Guide

### For Waiters 👨‍🍳

**Workflow:**
1. **Login** → Auto-redirect to Waiter Dashboard
2. **View Available Tables** → Check table status dashboard
3. **Create Order:**
   - Click "Create New Order"
   - Select available table
   - Add menu items (category-wise)
   - Set quantities
   - Submit → Table status changes to "Occupied"
4. **Update Order Status:**
   - View order details
   - Mark as "In Kitchen" when sent
   - Mark as "Served" when delivered
5. **Track Performance:** View today's order count in dashboard

### For Cashiers 💰

**Workflow:**
1. **Login** → Auto-redirect to Cashier Dashboard
2. **Identify Tables Needing Bills:**
   - Check "Tables Requesting Bills" section
   - Filter served orders without bills
3. **Generate Bill:**
   - Click "Generate Bill"
   - Select table with served order
   - Review auto-calculated total
   - Confirm → Bill created, table status → "Bill Requested"
4. **Process Payment:**
   - View bill details
   - Verify amount with customer
   - Mark as "Paid" → Table status → "Available"
5. **Export PDF:**
   - Open bill detail page
   - Click "Export PDF"
   - Professional invoice downloads
6. **Track Revenue:** View today's revenue in dashboard

### For Managers 👨‍💼

**Complete System Access:**
1. **Dashboard Analytics:**
   - Monitor real-time stats
   - Track today's performance
   - View revenue trends
2. **Table Management:**
   - Add new tables (number + capacity)
   - Edit table details
   - Delete inactive tables
3. **Menu Management:**
   - Add new menu items with images
   - Update prices
   - Toggle availability
   - Organize by categories
4. **Staff Management:**
   - View all staff members
   - Assign roles
   - Generate performance reports
5. **Order Oversight:**
   - View all orders (any waiter)
   - Track order status
   - Intervene if needed
6. **Financial Reports:**
   - Daily revenue summaries
   - Bill payment tracking
   - Tax calculations
7. **Admin Panel Access:**
   - Full Django admin
   - Database management
   - Advanced configurations

---

## 📦 Installation & Setup

### Quick Start (Development)

```bash
# 1. Clone repository
git clone https://github.com/Umarsidd/Restaurant_system.git
cd Restaurant_system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Load demo data (users, tables, menu)
python manage.py seed_data

# 6. Run development server
python manage.py runserver

# 7. Access system
# http://localhost:8000/login/
```

### Production Deployment (Render.com)

**Environment Variables Required:**
```bash
DJANGO_SETTINGS_MODULE=config.production_settings
DATABASE_URL=<PostgreSQL connection string>
SECRET_KEY=<random secret key>
```

**Deployment Steps:**
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy automatically
5. Run migrations: `python manage.py migrate`
6. Load data: `python manage.py seed_data`

**Current Deployment:** https://restaurant-system-jtqy.onrender.com

---

## 🎯 Sample Workflows

### Complete Order-to-Payment Flow

```
1. WAITER logs in
   ↓
2. Creates order for Table T3
   - 2x Margherita Pizza (₹600)
   - 1x Caesar Salad (₹200)
   - 2x Coca Cola (₹100)
   ↓
3. Table T3 status → OCCUPIED
   ↓
4. Marks order → IN_KITCHEN
   ↓
5. Food prepared, marks → SERVED
   ↓
6. CASHIER logs in
   ↓
7. Generates bill for Table T3
   - Subtotal: ₹900
   - Tax (5%): ₹45
   - Total: ₹945
   ↓
8. Table T3 status → BILL_REQUESTED
   ↓
9. Customer pays, marks bill → PAID
   ↓
10. Table T3 status → AVAILABLE
    ✅ Complete!
```

---

## 📸 Screenshots

*(Add screenshots of your deployed application here)*

- Login Page
- Waiter Dashboard
- Cashier Dashboard
- Manager Dashboard
- Table Status Grid
- Create Order Form
- Bill Generation
- PDF Invoice

---

## 🛠️ Development

### Project Structure

```
Restaurant_system/
├── accounts/           # User authentication & roles
├── tables/             # Table management
├── menu/               # Menu items & categories
├── orders/             # Order processing
├── billing/            # Bill generation & payments
├── notifications/      # Celery background tasks
├── dashboard/          # Role-based dashboards
├── config/             # Django settings & URLs
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── media/              # User uploads (menu images)
├── requirements.txt    # Python dependencies
├── manage.py           # Django CLI
├── build.sh            # Render build script
├── Procfile            # Gunicorn config
└── README.md           # This file
```

### Running Tests

```bash
python manage.py test
```

### Running Background Tasks (Optional)

```bash
# Terminal 1: Redis server
redis-server

# Terminal 2: Celery worker
celery -A config worker -l info

# Terminal 3: Celery beat (scheduled tasks)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## 🔐 Security Features

- ✅ CSRF Protection enabled
- ✅ Password hashing (PBKDF2_SHA256)
- ✅ Role-based access control
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Secure session management
- ✅ HTTPS in production
- ✅ Environment variable secrets

---

## 📞 Support & Contact

**Developer:** Umar Siddiqui  
**GitHub:** [@Umarsidd](https://github.com/Umarsidd)  
**Repository:** [Restaurant_system](https://github.com/Umarsidd/Restaurant_system)

---

## 📄 License

This project is open-source for educational and evaluation purposes.

---

**⭐ If you found this helpful, please star the repository!**

Built with ❤️ using Django | Designed for efficiency in restaurant operations
