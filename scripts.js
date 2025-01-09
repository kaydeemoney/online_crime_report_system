document.getElementById('crime-report-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Simulating form submission process
    alert('Your report has been submitted successfully!');
  
    // Reset the form
    this.reset();
  });
  