// Restaurant Management System - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Order item quantity calculations
    const quantityInputs = document.querySelectorAll('.item-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', updateOrderTotal);
    });

    // Table search/filter
    const tableSearch = document.getElementById('table-search');
    if (tableSearch) {
        tableSearch.addEventListener('input', filterTables);
    }

    // Menu category filter
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterMenuItems);
    }

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', confirmDelete);
    });

    // Dynamic form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', validateForm);
    });
});

function updateOrderTotal() {
    let total = 0;
    const items = document.querySelectorAll('.order-item');
    
    items.forEach(item => {
        const price = parseFloat(item.dataset.price || 0);
        const quantity = parseInt(item.querySelector('.item-quantity').value || 0);
        const subtotal = price * quantity;
        
        const subtotalEl = item.querySelector('.item-subtotal');
        if (subtotalEl) {
            subtotalEl.textContent = '₹' + subtotal.toFixed(2);
        }
        
        total += subtotal;
    });
    
    const totalEl = document.getElementById('order-total');
    if (totalEl) {
        totalEl.textContent = '₹' + total.toFixed(2);
    }
    
    // Calculate tax if present
    const taxRate = parseFloat(document.getElementById('tax-rate')?.value || 5);
    const taxAmount = (total * taxRate) / 100;
    const grandTotal = total + taxAmount;
    
    const taxEl = document.getElementById('tax-amount');
    if (taxEl) {
        taxEl.textContent = '₹' + taxAmount.toFixed(2);
    }
    
    const grandTotalEl = document.getElementById('grand-total');
    if (grandTotalEl) {
        grandTotalEl.textContent = '₹' + grandTotal.toFixed(2);
    }
}

function filterTables() {
    const searchTerm = this.value.toLowerCase();
    const tables = document.querySelectorAll('.table-status-card');
    
    tables.forEach(table => {
        const tableNumber = table.querySelector('.table-number').textContent.toLowerCase();
        const tableStatus = table.querySelector('.table-status-badge').textContent.toLowerCase();
        
        if (tableNumber.includes(searchTerm) || tableStatus.includes(searchTerm)) {
            table.style.display = '';
        } else {
            table.style.display = 'none';
        }
    });
}

function filterMenuItems() {
    const category = this.value;
    const items = document.querySelectorAll('.menu-item');
    
    items.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

function confirmDelete(e) {
    if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
        e.preventDefault();
        return false;
    }
}

function validateForm(e) {
    const requiredFields = this.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = 'var(--danger-color)';
        } else {
            field.style.borderColor = 'var(--border-color)';
        }
    });
    
    if (!isValid) {
        e.preventDefault();
        alert('Please fill in all required fields.');
        return false;
    }
}

// Add item to order (dynamic)
function addOrderItem(menuItemId, menuItemName, menuItemPrice) {
    const orderItems = document.getElementById('order-items');
    if (!orderItems) return;
    
    const itemHtml = `
        <div class="order-item card" data-price="${menuItemPrice}">
            <div class="flex justify-between items-center">
                <div>
                    <strong>${menuItemName}</strong>
                    <span class="text-muted">₹${menuItemPrice}</span>
                </div>
                <div class="flex items-center gap-2">
                    <input type="number" class="form-control item-quantity" 
                           name="items[${menuItemId}]" min="1" value="1" 
                           style="width: 80px;">
                    <span class="item-subtotal">₹${menuItemPrice}</span>
                    <button type="button" class="btn btn-danger btn-sm" onclick="removeOrderItem(this)">
                        Remove
                    </button>
                </div>
            </div>
        </div>
    `;
    
    orderItems.insertAdjacentHTML('beforeend', itemHtml);
    updateOrderTotal();
}

function removeOrderItem(button) {
    button.closest('.order-item').remove();
    updateOrderTotal();
}

// Refresh table status (for dashboard)
function refreshTableStatus() {
    // This would typically make an AJAX call to get updated table statuses
    // For now, just reload the page
    location.reload();
}

// Set auto-refresh for dashboard (every 30 seconds)
if (document.querySelector('.table-grid')) {
    setInterval(refreshTableStatus, 30000);
}
