// Function to handle save candidate details
document.getElementById('save-candidate-btn').addEventListener('click', async () => {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const degree = document.getElementById('degree').value;
    const specialization = document.getElementById('specialization').value;
    const batch = document.getElementById('batch').value;
    const completion = document.getElementById('completion').value;
    const mcq = document.getElementById('mcq').value;
    const project = document.getElementById('project').value;

    // Collect form data and make an API request to update the candidate details
    const formData = {
        name, email, degree, specialization, batch, completion, mcq, project
    };

    try {
        const response = await fetch('http://localhost:8000/update-candidate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            alert('Candidate details updated successfully!');
        } else {
            alert('Failed to update candidate details.');
        }
    } catch (error) {
        console.error('Error updating candidate details:', error);
        alert('An error occurred while updating candidate details.');
    }
});

// Handle certificate removal
document.querySelectorAll('.remove-cert').forEach(button => {
    button.addEventListener('click', (e) => {
        e.target.parentElement.remove(); // Remove the certificate from the list
        // You can also make an API call to delete the certificate from the backend
    });
});
