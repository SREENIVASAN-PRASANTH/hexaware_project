// Mock data for the candidate
const candidateData = {
    name: "John Doe",
    email: "john.doe@example.com",
    degree: "B.Tech Computer Science",
    batch: "Java Batch",
    linkedin: "https://www.linkedin.com/in/johndoe",
    progress: 75,
    recommendations: "Focus more on project work and Java-based courses for improvement."
};

// Populate candidate data on page load
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('candidate-name').textContent = candidateData.name;
    document.getElementById('candidate-name-display').textContent = candidateData.name;
    document.getElementById('candidate-email').textContent = candidateData.email;
    document.getElementById('candidate-degree').textContent = candidateData.degree;
    document.getElementById('candidate-batch').textContent = candidateData.batch;
    document.getElementById('candidate-linkedin').innerHTML = `<a href="${candidateData.linkedin}">${candidateData.linkedin}</a>`;
    document.getElementById('progress').value = candidateData.progress;
    document.getElementById('progress-value').textContent = `${candidateData.progress}%`;
    document.getElementById('ai-recommendations').textContent = candidateData.recommendations;
});

// Handle certificate upload
document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('certificate');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append('certificate', file);

    try {
        const response = await fetch('http://localhost:8000/upload-certificate', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            document.getElementById('upload-message').textContent = "Certificate uploaded successfully!";
        } else {
            document.getElementById('upload-message').textContent = "Failed to upload certificate.";
        }
    } catch (error) {
        console.error('Error uploading certificate:', error);
        document.getElementById('upload-message').textContent = "An error occurred during upload.";
    }
});
