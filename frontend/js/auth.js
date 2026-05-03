const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('error');

        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                role: document.getElementById('role').value
            })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('user_id', data.id);
            localStorage.setItem('role', data.role);
            if (data.role === 'student') {
                window.location.href = '/student/profile.html';
            } else {
                window.location.href = '/tutor/profile.html';
            }
        } else {
            errorDiv.textContent = data.detail;
            errorDiv.classList.remove('d-none');
        }
    });
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('error');

        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('email').value,
                password: document.getElementById('password').value
            })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('user_id', data.id);
            localStorage.setItem('role', data.role);
            if (data.role === 'student') {
                window.location.href = '/student/tutors.html';
            } else {
                window.location.href = '/tutor/dashboard.html';
            }
        } else {
            errorDiv.textContent = data.detail;
            errorDiv.classList.remove('d-none');
        }
    });
}