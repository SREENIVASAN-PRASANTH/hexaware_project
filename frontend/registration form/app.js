document.getElementById('candidate-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent page reload

    const form = document.getElementById('candidate-form');
    const formData = new FormData(form);

    const candidateData = {
        name: formData.get('name'),
        email: formData.get('email'),
        degree: formData.get('degree'),
        specialization: formData.get('specialization'),
        phone_number: formData.get('phone_number'),
        certifications: formData.get('certifications'),
        internships: formData.get('internships'),
        courses: formData.get('courses'),
        linkedin_profile: formData.get('linkedin_profile'),
        github_profile: formData.get('github_profile'),
        programming_languages: formData.get('programming_languages'),
    };

    try {
        const response = await fetch('http://localhost:8000/candidates/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(candidateData),
        });

        if (response.ok) {
            document.getElementById('message').innerHTML = "<p>Registration successful!</p>";
            form.reset();
        } else {
            document.getElementById('message').innerHTML = "<p>Registration failed. Please try again.</p>";
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').innerHTML = "<p>Something went wrong. Please try again.</p>";
    }
});
