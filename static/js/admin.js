// Admin page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Confirm before deleting product
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this product?')) {
                e.preventDefault();
            }
        });
    });

    // Status change confirmation
    const statusSelects = document.querySelectorAll('select[name="status"]');
    statusSelects.forEach(function(select) {
        const originalValue = select.value;
        
        select.addEventListener('change', function() {
            if (!confirm('Are you sure you want to change the order status?')) {
                this.value = originalValue;
            }
        });
    });

    // Image preview on file select
    const imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.getElementById('image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'image-preview';
                        preview.style.maxWidth = '200px';
                        preview.style.marginTop = '10px';
                        preview.style.display = 'block';
                        input.parentElement.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Form validation
    const adminForms = document.querySelectorAll('.admin-form');
    adminForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const priceInput = form.querySelector('input[name="price"]');
            const stockInput = form.querySelector('input[name="stock"]');
            
            if (priceInput && parseFloat(priceInput.value) < 0) {
                alert('Price cannot be negative');
                e.preventDefault();
                return;
            }
            
            if (stockInput && parseInt(stockInput.value) < 0) {
                alert('Stock cannot be negative');
                e.preventDefault();
                return;
            }
        });
    });
});
