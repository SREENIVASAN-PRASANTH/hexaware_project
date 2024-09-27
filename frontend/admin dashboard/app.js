// Fetch candidate data from the backend and populate the table
async function loadCandidates() {
    try {
        const response = await fetch('http://localhost:8000/candidates/');
        const candidates = await response.json();

        const candidateTable = document.getElementById('candidate-table');
        candidateTable.innerHTML = ''; // Clear any existing content

        candidates.forEach(candidate => {
            const row = `<tr>
                <td>${candidate.name}</td>
                <td>${candidate.email}</td>
                <td>${candidate.degree}</td>
                <td>${candidate.batch}</td>
                <td>${candidate.progress}%</td>
            </tr>`;
            candidateTable.innerHTML += row;
        });
    } catch (error) {
        console.error('Error loading candidates:', error);
    }
}

// Load candidates when the page loads
document.addEventListener('DOMContentLoaded', loadCandidates);

// Generate reports when the button is clicked
document.getElementById('generate-reports').addEventListener('click', async function() {
    try {
        const response = await fetch('http://localhost:8000/reports/generate', { method: 'POST' });
        if (response.ok) {
            alert('Reports generated successfully!');
        } else {
            alert('Failed to generate reports.');
        }
    } catch (error) {
        console.error('Error generating reports:', error);
        alert('Something went wrong.');
    }
});
