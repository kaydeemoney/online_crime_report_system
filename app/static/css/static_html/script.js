// Optional: Add JavaScript for form validation or other interactions
document.getElementById('crime-report-form').addEventListener('submit', function(event) {
    event.preventDefault();
    // You can add form validation and submission logic here
    // For demonstration purposes, we'll just log the form data
    const formData = new FormData(this);
    console.log('Form data:', formData);
    alert('Thank you for your report!');
});
