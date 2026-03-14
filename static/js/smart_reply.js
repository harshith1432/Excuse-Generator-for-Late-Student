document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('reply-form');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const emptyState = document.getElementById('empty-state');
    const replyContent = document.getElementById('reply-content');
    const copyBtn = document.getElementById('copy-btn');

    let currentReply = "";

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        emptyState.style.display = 'none';
        resultContent.style.display = 'none';
        loader.style.display = 'block';

        const payload = {
            message: document.getElementById('incoming_message').value,
            tone: document.getElementById('tone').value
        };

        try {
            const res = await fetch('/api/letters/smart-reply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok) {
                currentReply = data.reply;
                replyContent.innerHTML = '';
                loader.style.display = 'none';
                resultContent.style.display = 'block';

                // Simple typing effect
                let i = 0;
                const speed = 15;
                function typeWriter() {
                    if (i < currentReply.length) {
                        replyContent.innerHTML += currentReply.charAt(i) === '\n' ? '<br>' : currentReply.charAt(i);
                        i++;
                        setTimeout(typeWriter, speed);
                    }
                }
                typeWriter();

            } else {
                alert(data.error || 'Failed to generate reply');
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
        if (!currentReply) return;
        navigator.clipboard.writeText(currentReply).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
            setTimeout(() => copyBtn.innerHTML = originalText, 2000);
        });
    });
});
