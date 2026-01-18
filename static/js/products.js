// Products page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Add to cart animation
    const addToCartForms = document.querySelectorAll('.product-actions form');
    
    addToCartForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const btn = form.querySelector('button');
            const originalText = btn.textContent;
            btn.textContent = 'Adding...';
            btn.disabled = true;
        });
    });

    // Search input focus effect
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.3s';
        });

        searchInput.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    }
});
