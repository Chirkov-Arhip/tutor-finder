const userId = localStorage.getItem('user_id');
const role = localStorage.getItem('role');

// Кнопка кабинета
const dashboardBtn = document.getElementById('dashboardBtn');
if (dashboardBtn) {
    dashboardBtn.href = role === 'student'
        ? '/student/tutors.html'
        : '/tutor/dashboard.html';
}

// Выход
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.clear();
        window.location.href = '/';
    });
}

// Отправка обращения
const supportForm = document.getElementById('supportForm');
if (supportForm) {
    supportForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('error');
        const successDiv = document.getElementById('success');
        errorDiv.classList.add('d-none');
        successDiv.classList.add('d-none');

        const response = await fetch('/api/support', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: parseInt(userId),
                subject: document.getElementById('subject').value,
                description: document.getElementById('description').value
            })
        });

        if (response.ok) {
            successDiv.textContent = 'Обращение отправлено! Мы свяжемся с вами.';
            successDiv.classList.remove('d-none');
            supportForm.reset();
        } else {
            const data = await response.json();
            errorDiv.textContent = data.detail || 'Ошибка отправки';
            errorDiv.classList.remove('d-none');
        }
    });
}