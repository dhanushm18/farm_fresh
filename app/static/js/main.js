// Main JavaScript file for FarmFresh

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Flash messages auto-close
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Handle delete product form submission
    console.log('Setting up delete product handlers');
    var deleteForms = document.querySelectorAll('.delete-product-form');
    console.log('Found ' + deleteForms.length + ' delete forms');

    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            // Prevent the default form submission
            event.preventDefault();
            console.log('Delete form submitted');

            // Get the product name from the data attribute
            var productName = this.getAttribute('data-product-name');
            console.log('Deleting product: ' + productName);

            // Confirm deletion
            if (confirm('Are you sure you want to delete "' + productName + '"?')) {
                console.log('Deletion confirmed, submitting form');
                // If confirmed, submit the form
                this.submit();
            } else {
                console.log('Deletion cancelled');
            }
        });
    });
});
