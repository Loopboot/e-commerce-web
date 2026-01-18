// Cart page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Update cart item quantity
    const quantityForms = document.querySelectorAll('.quantity-form');
    
    quantityForms.forEach(function(form) {
        const input = form.querySelector('input[name="quantity"]');
        
        input.addEventListener('change', function() {
            if (this.value < 1) {
                if (confirm('Remove this item from cart?')) {
                    this.value = 0;
                    form.submit();
                } else {
                    this.value = 1;
                }
            }
        });
    });

    // Confirm before removing item
    const removeForms = document.querySelectorAll('form[action*="remove"]');
    removeForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to remove this item?')) {
                e.preventDefault();
            }
        });
    });

    // Calculate and display real-time totals
    function updateTotals() {
        let total = 0;
        const rows = document.querySelectorAll('.cart-table tbody tr');
        
        rows.forEach(function(row) {
            const priceText = row.querySelector('td:nth-child(2)').textContent;
            const quantityInput = row.querySelector('input[name="quantity"]');
            const totalCell = row.querySelector('td:nth-child(4)');
            
            if (priceText && quantityInput) {
                const price = parseFloat(priceText.replace('$', ''));
                const quantity = parseInt(quantityInput.value);
                const itemTotal = price * quantity;
                
                totalCell.textContent = '$' + itemTotal.toFixed(2);
                total += itemTotal;
            }
        });
    }

    // Listen for quantity changes
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('input', updateTotals);
    });
});
