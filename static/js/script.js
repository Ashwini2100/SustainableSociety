document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const symptomsForm = document.getElementById('symptomsForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsSection = document.getElementById('resultsSection');
    const conditionsList = document.getElementById('conditionsList');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    const disclaimerElement = document.getElementById('disclaimer');
    const generalAdviceElement = document.getElementById('generalAdvice');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    // Handle form submission
    symptomsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading indicator
        loadingIndicator.classList.remove('d-none');
        
        // Hide results and error sections
        resultsSection.classList.add('d-none');
        errorAlert.classList.add('d-none');
        
        // Disable submit button
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing...';
        
        // Get form data
        const formData = new FormData(symptomsForm);
        
        // Send request to backend
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading indicator
            loadingIndicator.classList.add('d-none');
            
            // Enable submit button
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-search me-2"></i>Analyze Symptoms';
            
            if (data.success) {
                // Display results
                displayResults(data.result);
                resultsSection.classList.remove('d-none');
                
                // Scroll to results
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                // Show error message
                errorMessage.textContent = data.error || 'An unexpected error occurred. Please try again.';
                errorAlert.classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Hide loading indicator
            loadingIndicator.classList.add('d-none');
            
            // Enable submit button
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-search me-2"></i>Analyze Symptoms';
            
            // Show error message
            errorMessage.textContent = 'Network error. Please check your connection and try again.';
            errorAlert.classList.remove('d-none');
        });
    });
    
    // Function to display analysis results
    function displayResults(result) {
        // Clear previous results
        conditionsList.innerHTML = '';
        
        // Set disclaimer and general advice
        if (result.disclaimer) {
            disclaimerElement.textContent = result.disclaimer;
        }
        
        if (result.general_advice) {
            generalAdviceElement.textContent = result.general_advice;
        }
        
        // If we have raw response instead of structured data
        if (result.raw_response) {
            const rawResponseItem = document.createElement('div');
            rawResponseItem.className = 'list-group-item';
            rawResponseItem.innerHTML = `<p>${result.raw_response.replace(/\n/g, '<br>')}</p>`;
            conditionsList.appendChild(rawResponseItem);
            return;
        }
        
        // Handle case where there are no conditions returned
        if (!result.possible_conditions || result.possible_conditions.length === 0) {
            const noResultsItem = document.createElement('div');
            noResultsItem.className = 'list-group-item text-center';
            noResultsItem.innerHTML = `
                <p class="mb-0">No specific conditions could be identified based on the provided symptoms. 
                Please consult with a healthcare professional for a proper evaluation.</p>
            `;
            conditionsList.appendChild(noResultsItem);
            return;
        }
        
        // Create card for each condition
        result.possible_conditions.forEach((condition, index) => {
            // Determine urgency class
            let urgencyClass = '';
            let urgencyBadge = '';
            
            if (condition.urgency_level === 'immediate_attention') {
                urgencyClass = 'urgency-immediate';
                urgencyBadge = '<span class="badge bg-danger me-2">Seek immediate medical attention</span>';
            } else if (condition.urgency_level === 'doctor_visit') {
                urgencyClass = 'urgency-doctor';
                urgencyBadge = '<span class="badge bg-warning text-dark me-2">Consult a doctor soon</span>';
            } else if (condition.urgency_level === 'self_care') {
                urgencyClass = 'urgency-self';
                urgencyBadge = '<span class="badge bg-success me-2">May resolve with self-care</span>';
            }
            
            // Create condition card
            const conditionItem = document.createElement('div');
            conditionItem.className = `list-group-item mb-3 ${urgencyClass}`;
            
            // Generate symptoms badges HTML
            let symptomsHTML = '';
            if (condition.common_symptoms && condition.common_symptoms.length > 0) {
                symptomsHTML = '<div class="mt-3 mb-2"><strong>Common symptoms:</strong></div><div>';
                
                condition.common_symptoms.forEach(symptom => {
                    symptomsHTML += `<span class="badge bg-info text-dark symptom-badge">${symptom}</span> `;
                });
                
                symptomsHTML += '</div>';
            }
            
            // Set HTML content for condition card
            conditionItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <h5 class="mb-1">${condition.name || 'Unknown Condition'}</h5>
                    ${urgencyBadge}
                </div>
                <p class="mb-1">${condition.description || 'No description available.'}</p>
                ${symptomsHTML}
            `;
            
            conditionsList.appendChild(conditionItem);
        });
    }
});
