// Файл: habit_tracker/static/js/script.js

/**
 * Отправляет POST‑запрос к API для отметки привычки как выполненной
 * @param {number} habitId - ID привычки
 */
async function markHabit(habitId) {
    try {
        const response = await fetch(`/api/habits/${habitId}/mark/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            if (response.status === 400) {
                alert('Нельзя отметить привычку дважды за день!');
            } else if (response.status === 404) {
                alert('Привычка не найдена.');
            } else {
                alert(`Ошибка сервера: ${response.statusText}`);
            }
            return;
        }

        const data = await response.json();
        updateHabitUI(habitId, data);

    } catch (error) {
        console.error('Ошибка при отметке привычки:', error);
        alert('Произошла сетевая ошибка. Проверьте подключение и повторите попытку.');
    }
}

/**
 * Обновляет интерфейс привычки после успешной отметки
 * @param {number} habitId - ID привычки
 * @param {Object} data - Ответ API (id, name, streak, last_marked_at)
 */


function updateHabitUI(habitId, data) {
    // Обновляем streak
    const streakElement = document.querySelector(`[data-habit-id="${habitId}"] .streak`);
    if (streakElement) {
        streakElement.textContent = `🔥 ${data.streak}`;
    }

    // Меняем кнопку на "Отмечено!"
    const actionsDiv = document.querySelector(`[data-habit-id="${habitId}"] .habit-actions`);
    if (actionsDiv) {
        actionsDiv.innerHTML = '<span class="marked-today">✅ Отмечено!</span>';
    }
}

/**
 * Отправляет PUT‑запрос для обновления названия привычки
 * @param {number} habitId - ID привычки
 * @param {string} newName - Новое название
 */
function updateHabit(habitId) {
    const form = document.getElementById('update-form');
    const name = form.querySelector('input[name="name"]').value;

    fetch(`/${habitId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => console.log('Успешно:', data))
    .catch(err => console.error('Ошибка:', err));
}

/**
 * Отправляет DELETE‑запрос для удаления привычки
 * @param {number} habitId - ID привычки
 */
async function deleteHabit(habitId) {
    try {
        const response = await fetch(`/api/habits/${habitId}/`, {
            method: 'DELETE'
        });

        if (response.status === 204) {
            const habitItem = document.querySelector(`[data-habit-id="${habitId}"]`);
            if (habitItem) {
                habitItem.remove();
            }
            return;
        }

         if (!response.ok) {
            if (response.status === 404) {
                alert('Привычка не найдена.');
            } else {
                alert(`Ошибка сервера: ${response.statusText}`);
            }
            return;
        }

        // Удаляем элемент из DOM
        const habitItem = document.querySelector(`[data-habit-id="${habitId}"]`);
        if (habitItem) {
            habitItem.remove();
        }

        // Если список пуст, показываем сообщение
        const habitList = document.querySelector('.habit-list');
        if (habitList && !habitList.querySelector('.habit-item')) {
            habitList.innerHTML = '<p>У вас пока нет привычек. Добавьте первую!</p>';
        }

    } catch (error) {
        console.error('Ошибка при удалении привычки:', error);
        alert('Произошла сетевая ошибка. Попробуйте снова.');
    }
}

/**
 * Обработчик кликов по кнопкам в списке привычек
 */
document.addEventListener('click', (event) => {
    const target = event.target;

    // Кнопка "Выполнил сегодня"
    if (target.classList.contains('btn-mark')) {
        const habitId = target.closest('.habit-item').dataset.habitId;
        markHabit(habitId);
    }

    // Кнопка "Удалить привычку" (в детальной странице)
    if (target.classList.contains('btn-danger')) {
        const habitId = target.closest('form').dataset.habitId;
        if (confirm('Вы уверены, что хотите удалить эту привычку?')) {
            deleteHabit(habitId);
        }
    }
});

/**
 * Обработчик отправки формы редактирования названия (в детальной странице)
 */
document.addEventListener('submit', async (event) => {
    if (event.target.classList.contains('edit-form')) {
        event.preventDefault();
        const form = event.target;
        const habitId = form.dataset.habitId;
        const newName = form.querySelector('input[name="name"]').value;

        await updateHabitName(habitId, newName);
    }
});

/**
 * Добавляет data-habit-id к элементам привычек для удобства работы JS
 */
function initHabitItems() {
    document.querySelectorAll('.habit-item').forEach(item => {
        const link = item.querySelector('a');
        const href = link?.getAttribute('href');
        const match = href?.match(/\/habit\/(\d+)\//);
        if (match && match[1]) {
            item.dataset.habitId = match[1];
        }
    });
}

/**
 * Инициализация JS при загрузке страницы
 */
window.addEventListener('load', () => {
    initHabitItems();
    console.log('JavaScript для трекера привычек загружен и готов к работе.');
});
