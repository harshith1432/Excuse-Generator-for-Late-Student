document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('letter-form');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const emptyState = document.getElementById('empty-state');
    const letterContent = document.getElementById('letter-content');
    const copyBtn = document.getElementById('copy-btn');
    const exportPdf = document.getElementById('export-pdf');
    const exportDocx = document.getElementById('export-docx');

    let currentLetter = "";

    // Pre-fill user data if available
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        document.getElementById('user_name').value = user.name || '';
        document.getElementById('email').value = user.email || '';
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        emptyState.style.display = 'none';
        resultContent.style.display = 'none';
        loader.style.display = 'block';

        const payload = {
            type: document.getElementById('letter_type').value,
            recipient_name: document.getElementById('recipient_name').value,
            subject: document.getElementById('subject').value,
            reason: document.getElementById('reason').value,
            name: document.getElementById('user_name').value,
            class_dept: document.getElementById('class_dept').value,
            contact: document.getElementById('contact').value,
            email: document.getElementById('email').value,
            college_company: document.getElementById('college_company').value
        };

        try {
            const res = await fetch('/api/letters/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok) {
                currentLetter = data.generated_letter;

                // Typing animation effect
                letterContent.innerHTML = '';
                loader.style.display = 'none';
                resultContent.style.display = 'block';

                let i = 0;
                const speed = 10;
                function typeWriter() {
                    if (i < currentLetter.length) {
                        letterContent.innerHTML += currentLetter.charAt(i) === '\n' ? '<br>' : currentLetter.charAt(i);
                        i++;
                        setTimeout(typeWriter, speed);
                    }
                }
                typeWriter();

            } else {
                alert(data.error || 'Failed to generate letter');
                loader.style.display = 'none';
                emptyState.style.display = 'block';
            }
        } catch (err) {
            console.error('Error:', err);
            loader.style.display = 'none';
            emptyState.style.display = 'block';
        }
    });

    copyBtn.addEventListener('click', () => {
        if (!currentLetter) return;
        navigator.clipboard.writeText(currentLetter).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
            setTimeout(() => copyBtn.innerHTML = originalText, 2000);
        });
    });

    async function handleExport(endpoint, filename) {
        if (!currentLetter) return;

        try {
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: currentLetter })
            });

            if (res.ok) {
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
            } else {
                alert(`Export failed.`);
            }
        } catch (err) {
            console.error('Export error:', err);
        }
    }

    exportPdf.addEventListener('click', () => handleExport('/api/export/pdf', 'letter.pdf'));
    exportDocx.addEventListener('click', () => handleExport('/api/export/docx', 'letter.docx'));
});
