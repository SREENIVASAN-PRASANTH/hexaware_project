document.getElementById('feedback-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Collect form data
    const feedbackData = {
        topic: document.getElementById('topic').value,
        rating: document.getElementById('rating').value,
        comments: document.getElementById('comments').value
    };

    // Post feedback to server
    try {
        const response = await fetch('http://localhost:8000/submit-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(feedbackData)
        });

        if (response.ok) {
            document.getElementById('feedback-message').textContent = "Feedback submitted successfully!";
        } else {
            document.getElementById('feedback-message').textContent = "Failed to submit feedback. Try again.";
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        document.getElementById('feedback-message').textContent = "An error occurred. Please try again.";
    }
});
