// Sample data for the batches
const batchData = [
    { name: 'Java Batch', mcq: 85, project: 90, completion: 80 },
    { name: '.NET Batch', mcq: 88, project: 85, completion: 75 },
    { name: 'Data Engineering Batch', mcq: 90, project: 92, completion: 88 }
];

// Chart.js to visualize batch performance
const ctx = document.getElementById('batch-comparison-chart').getContext('2d');
const batchComparisonChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: batchData.map(batch => batch.name),
        datasets: [
            {
                label: 'MCQ Score (%)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                data: batchData.map(batch => batch.mcq)
            },
            {
                label: 'Project Score (%)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1,
                data: batchData.map(batch => batch.project)
            },
            {
                label: 'Completion (%)',
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1,
                data: batchData.map(batch => batch.completion)
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Export comparison report functionality
document.getElementById('export-report-btn').addEventListener('click', () => {
    alert('This functionality will export a PDF report with the batch comparison data.');
    // Implement PDF generation and export logic here
});
