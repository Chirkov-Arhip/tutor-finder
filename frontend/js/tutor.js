const userId = localStorage.getItem('user_id');

// Загрузка предметов
async function loadSubjects() {
    const container = document.getElementById('subjectsList');
    if (!container) return;

    const response = await fetch('/api/students/subjects');
    const subjects = await response.json();

    container.innerHTML = subjects.map(s => `
        <div class="col-md-4">
            <div class="form-check">
                <input class="form-check-input subject-checkbox"
                       type="checkbox" value="${s.id}" id="subject_${s.id}">
                <label class="form-check-label" for="subject_${s.id}">${s.name}</label>
            </div>
        </div>
    `).join('');
}

// Сохранение профиля
const tutorProfileForm = document.getElementById('tutorProfileForm');
if (tutorProfileForm) {
    tutorProfileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('error');

        const selectedSubjects = [...document.querySelectorAll('.subject-checkbox:checked')]
            .map(cb => parseInt(cb.value));

        const response = await fetch('/api/tutors/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: parseInt(userId),
                last_name: document.getElementById('last_name').value,
                first_name: document.getElementById('first_name').value,
                middle_name: document.getElementById('middle_name').value,
                age: parseInt(document.getElementById('age').value),
                experience: parseInt(document.getElementById('experience').value),
                phone: document.getElementById('phone').value,
                about: document.getElementById('about').value,
                subjects: selectedSubjects
            })
        });

        const data = await response.json();
        if (response.ok) {
            window.location.href = '/tutor/dashboard.html';
        } else {
            errorDiv.textContent = data.detail;
            errorDiv.classList.remove('d-none');
        }
    });
}

// Загрузка заявок
async function loadApplications() {
    const container = document.getElementById('applicationsList');
    if (!container) return;

    // Сначала получаем id профиля репетитора
    const profileResponse = await fetch(`/api/tutors/profile/full/${userId}`);
    if (!profileResponse.ok) {
        container.innerHTML = '<p class="text-muted">Профиль не найден</p>';
        return;
    }
    const profile = await profileResponse.json();
    const tutorProfileId = profile.id;

    const response = await fetch(`/api/tutors/applications/${tutorProfileId}`);
    if (!response.ok) {
        container.innerHTML = '<p class="text-muted">Ошибка загрузки заявок</p>';
        return;
    }

    const apps = await response.json();
    if (apps.length === 0) {
        container.innerHTML = '<p class="text-muted">Заявок пока нет</p>';
        return;
    }

    container.innerHTML = apps.map(a => `
        <div class="card mb-3">
            <div class="card-body">
                <h5>${a.student.full_name}</h5>
                <p>Возраст: ${a.student.age}</p>
                <p>Предмет: ${a.subject}</p>
                <p>О себе: ${a.student.about || '—'}</p>
                <p>Телефон: ${a.student.phone || 'Доступен после принятия заявки'}</p>
                <p>Статус: ${getStatusBadge(a.status)}</p>
                ${a.status === 'pending' ? `
                    <button onclick="respond(${a.id}, 'accepted')"
                            class="btn btn-success btn-sm me-2">Принять</button>
                    <button onclick="respond(${a.id}, 'rejected')"
                            class="btn btn-danger btn-sm">Отклонить</button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function getStatusBadge(status) {
    const badges = {
        'pending': '<span class="badge bg-warning">Ожидает</span>',
        'accepted': '<span class="badge bg-success">Принята</span>',
        'rejected': '<span class="badge bg-danger">Отклонена</span>'
    };
    return badges[status] || status;
}

async function respond(appId, status) {
    await fetch(`/api/tutors/applications/${appId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
    });
    loadApplications();
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

loadSubjects();
loadApplications();