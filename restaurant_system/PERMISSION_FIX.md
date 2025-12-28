# Permission Fix for Waiter and Cashier Accounts

## Issue
Waiter and cashier accounts could log into Django admin but showed "You don't have permission to view or edit anything."

## Root Cause
Users had `is_staff=True` (allowing admin login) but no Django model permissions assigned.

## Solution
Updated `seed_data.py` to assign appropriate permissions:

### Waiter Permissions
- **Orders**: add, change, view
- **Order Items**: add, change, view  
- **Tables**: view only
- **Menu Items**: view only

### Cashier Permissions
- **Bills**: add, change, view
- **Orders**: view only
- **Order Items**: view only
- **Tables**: view only

### Manager Permissions
- All permissions (is_superuser=True)

## Changes Made
1. Added imports for ContentType and Permission
2. Created `assign_permissions()` method in Command class
3. Called permission assignment for each user after creation
4. Re-ran `python manage.py seed_data` to apply to existing users

## Testing
After fix, each role can now:
- **Waiter**: See and manage Orders in admin panel
- **Cashier**: See and manage Bills in admin panel
- **Manager**: Full access to everything

## Status
✅ FIXED - All accounts now working correctly
