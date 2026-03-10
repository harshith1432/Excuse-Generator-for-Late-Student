document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Check local storage for theme
    const currentTheme = localStorage.getItem('theme') || 'light-mode';
    body.className = currentTheme;
    updateThemeIcon(currentTheme);

    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('light-mode')) {
            body.className = 'dark-mode';
            localStorage.setItem('theme', 'dark-mode');
            updateThemeIcon('dark-mode');
        } else {
            body.className = 'light-mode';
            localStorage.setItem('theme', 'light-mode');
            updateThemeIcon('light-mode');
        }
    });

    function updateThemeIcon(theme) {
        if (theme === 'dark-mode') {
            themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
        } else {
            themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
        }
    }

    // Auth Modal Logic
    const authBtn = document.getElementById('auth-btn');
    const authModal = document.getElementById('auth-modal');
    const closeModal = document.querySelector('.close-modal');
    const toggleAuthMode = document.getElementById('toggle-auth-mode');
    const nameGroup = document.getElementById('name-group');
    const modalTitle = document.getElementById('modal-title');
    const authSubmitBtn = document.getElementById('auth-submit');
    const authForm = document.getElementById('auth-form');

    let isLogin = true;

    // Check if user is logged in
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        authBtn.innerHTML = `<i class="fa-solid fa-user"></i> ${user.name}`;
    }

    authBtn.addEventListener('click', () => {
        if (localStorage.getItem('user')) {
            // Logout
            fetch('/auth/logout', { method: 'POST' })
            .then(() => {
                localStorage.removeItem('user');
                window.location.reload();
            });
        } else {
            authModal.classList.add('show');
        }
    });

    closeModal.addEventListener('click', () => {
        authModal.classList.remove('show');
    });

    window.addEventListener('click', (e) => {
        if (e.target === authModal) {
            authModal.classList.remove('show');
        }
    });

    toggleAuthMode.addEventListener('click', (e) => {
        e.preventDefault();
        isLogin = !isLogin;
        if (isLogin) {
            modalTitle.innerText = 'Sign In';
            authSubmitBtn.innerText = 'Login';
            nameGroup.style.display = 'none';
            toggleAuthMode.innerHTML = 'Sign Up';
        } else {
            modalTitle.innerText = 'Create Account';
            authSubmitBtn.innerText = 'Register';
            nameGroup.style.display = 'block';
            toggleAuthMode.innerHTML = 'Sign In';
        }
    });

    authForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('auth-email').value;
        const password = document.getElementById('auth-password').value;
        const name = document.getElementById('auth-name').value;

        const endpoint = isLogin ? '/auth/login' : '/auth/register';
        const payload = isLogin ? { email, password } : { name, email, password };

        try {
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            if (res.ok) {
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.reload();
            } else {
                alert(data.error || 'Authentication failed');
            }
        } catch (err) {
            console.error('Auth error:', err);
        }
    });
});
