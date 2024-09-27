document.getElementById('report-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get selected batch
    const batch = document.getElementById('batch').value;

    try {
        // Make a request to backend to generate the report
        const response = await fetch(`http://localhost:8000/generate-report/${batch}`, {
            method: 'GET'
        });

        if (response.ok) {
            const reportUrl = await response.text();
            document.getElementById('report-message').innerHTML = `Report generated successfully! <a href="${reportUrl}" target="_blank">Download Report</a>`;
        } else {
            document.getElementById('report-message').textContent = "Failed to generate the report.";
        }
    } catch (error) {
        console.error('Error generating report:', error);
        document.getElementById('report-message').textContent = "An error occurred while generating the report.";
    }
});
