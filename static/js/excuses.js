document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('excuse-form');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const emptyState = document.getElementById('empty-state');
    const variationsContainer = document.getElementById('variations-container');
    const badge = document.getElementById('believability-badge');
    const copyBtn = document.getElementById('copy-btn');
    const exportPdf = document.getElementById('export-pdf');

    let selectedExcuse = "";

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loader
        emptyState.style.display = 'none';
        resultContent.style.display = 'none';
        badge.style.display = 'none';
        loader.style.display = 'block';

        const payload = {
            situation: document.getElementById('situation').value,
            delay_time: document.getElementById('delay_time').value,
            reason_category: document.getElementById('reason_category').value
        };

        try {
            const res = await fetch('/api/excuses/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok) {
                renderVariations(data.variations, data.believability_score);
            } else {
                alert(data.error || 'Failed to generate excuse');
                loader.style.display = 'none';
                emptyState.style.display = 'block';
            }
        } catch (err) {
            console.error('Error:', err);
            loader.style.display = 'none';
            emptyState.style.display = 'block';
        }
    });

    function renderVariations(variations, score) {
        variationsContainer.innerHTML = '';
        selectedExcuse = variations[0]; // Default selection

        variations.forEach((text, i) => {
            const card = document.createElement('div');
            card.className = `variation-card ${i === 0 ? 'selected' : ''}`;
            card.innerHTML = `<p>${text}</p>`;

            card.addEventListener('click', () => {
                document.querySelectorAll('.variation-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedExcuse = text;
            });

            variationsContainer.appendChild(card);
        });

        // Setup badge
        badge.className = 'score-badge';
        if (score >= 8) badge.classList.add('score-high');
        else if (score >= 5) badge.classList.add('score-medium');
        else badge.classList.add('score-low');

        badge.innerHTML = `<i class="fa-solid fa-shield-halved"></i> Believability: ${score}/10`;
        badge.style.display = 'inline-flex';

        // Show content
        loader.style.display = 'none';
        resultContent.style.display = 'block';
    }

    copyBtn.addEventListener('click', () => {
        if (!selectedExcuse) return;
        navigator.clipboard.writeText(selectedExcuse).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
            setTimeout(() => copyBtn.innerHTML = originalText, 2000);
        });
    });

    exportPdf.addEventListener('click', async () => {
        if (!selectedExcuse) return;

        try {
            const res = await fetch('/api/export/pdf', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: selectedExcuse })
            });

            if (res.ok) {
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'excuse.pdf';
                document.body.appendChild(a);
                a.click();
                a.remove();
            } else {
                alert('Export failed. Ensure wkhtmltopdf is installed on server.');
            }
        } catch (err) {
            console.error('Export error:', err);
        }
    });
});
