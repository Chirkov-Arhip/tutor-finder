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

// Загрузка профиля
async function loadProfile() {
    const url = role === 'student'
        ? `/api/students/profile/full/${userId}`
        : `/api/tutors/profile/full/${userId}`;

    const response = await fetch(url);
    if (!response.ok) {
        window.location.href = '/';
        return;
    }

    const profile = await response.json();

    document.getElementById('last_name').value = profile.last_name;
    document.getElementById('first_name').value = profile.first_name;
    document.getElementById('middle_name').value = profile.middle_name || '';
    document.getElementById('age').value = profile.age;
    document.getElementById('about').value = profile.about || '';

    if (role === 'tutor') {
        document.getElementById('experienceDiv').classList.remove('d-none');
        document.getElementById('subjectsDiv').classList.remove('d-none');
        document.getElementById('experience').value = profile.experience;

        const subjectsResponse = await fetch('/api/students/subjects');
        const allSubjects = await subjectsResponse.json();
        const currentSubjectIds = profile.subjects.map(s => s.id);

        const container = document.getElementById('subjectsList');
        container.innerHTML = allSubjects.map(s => `
            <div class="col-md-4">
                <div class="form-check">
                    <input class="form-check-input subject-checkbox"
                           type="checkbox" value="${s.id}" id="subject_${s.id}"
                           ${currentSubjectIds.includes(s.id) ? 'checked' : ''}>
                    <label class="form-check-label" for="subject_${s.id}">${s.name}</label>
                </div>
            </div>
        `).join('');
    }
}

// Сохранение профиля
const profileForm = document.getElementById('profileForm');
if (profileForm) {
    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('error');
        const successDiv = document.getElementById('success');
        errorDiv.classList.add('d-none');
        successDiv.classList.add('d-none');

        const currentPassword = document.getElementById('current_password').value;
        const newPassword = document.getElementById('new_password').value;

        const checkResponse = await fetch('/api/auth/password', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: parseInt(userId),
                old_password: currentPassword,
                new_password: newPassword || currentPassword
            })
        });

        if (!checkResponse.ok) {
            const data = await checkResponse.json();
            errorDiv.textContent = data.detail;
            errorDiv.classList.remove('d-none');
            return;
        }

        const profileData = {
            last_name: document.getElementById('last_name').value,
            first_name: document.getElementById('first_name').value,
            middle_name: document.getElementById('middle_name').value,
            age: parseInt(document.getElementById('age').value),
            about: document.getElementById('about').value
        };

        if (role === 'tutor') {
            profileData.experience = parseInt(document.getElementById('experience').value);
            profileData.subjects = [...document.querySelectorAll('.subject-checkbox:checked')]
                .map(cb => parseInt(cb.value));
            profileData.custom_subject = document.getElementById('custom_subject').value || null;
        }

        const url = role === 'student'
            ? `/api/students/profile/${userId}`
            : `/api/tutors/profile/${userId}`;

        const updateResponse = await fetch(url, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profileData)
        });

        if (!updateResponse.ok) {
            errorDiv.textContent = 'Ошибка при обновлении профиля';
            errorDiv.classList.remove('d-none');
            return;
        }

        successDiv.textContent = 'Изменения сохранены!';
        successDiv.classList.remove('d-none');
        document.getElementById('current_password').value = '';
        document.getElementById('new_password').value = '';
    });
}

loadProfile();