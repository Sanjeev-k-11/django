/**
 * StudyMate - Main Client-side JavaScript
 * Handles Theme Toggling, AJAX Operations, Modals, Hotkeys, and Responsive Navigation
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initDropdowns();
  initHotkeys();
  initToasts();
  initAjaxChecklists();
});

// ================= CSRF Token Helper =================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ================= Dark / Light Theme =================
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const themeIcon = document.getElementById('theme-toggle-icon');
  const currentTheme = localStorage.getItem('studymate_theme') || 'light';

  document.documentElement.setAttribute('data-theme', currentTheme);
  updateThemeIcon(currentTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const activeTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('studymate_theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const themeIcon = document.getElementById('theme-toggle-icon');
  if (!themeIcon) return;
  if (theme === 'dark') {
    themeIcon.className = 'fa-solid fa-sun';
  } else {
    themeIcon.className = 'fa-solid fa-moon';
  }
}

// ================= Responsive Sidebar =================
function initSidebar() {
  const menuToggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== menuToggle) {
        sidebar.classList.remove('open');
      }
    });
  }
}

// ================= Dropdowns (Notifications & Profile) =================
function initDropdowns() {
  const notifBtn = document.getElementById('notif-toggle-btn');
  const notifDropdown = document.getElementById('notif-dropdown');

  const profileBtn = document.getElementById('profile-dropdown-btn');
  const profileDropdown = document.getElementById('profile-dropdown');

  if (notifBtn && notifDropdown) {
    notifBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (profileDropdown) profileDropdown.classList.remove('show');
      notifDropdown.classList.toggle('show');
    });
  }

  if (profileBtn && profileDropdown) {
    profileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (notifDropdown) notifDropdown.classList.remove('show');
      profileDropdown.classList.toggle('show');
    });
  }

  document.addEventListener('click', () => {
    if (notifDropdown) notifDropdown.classList.remove('show');
    if (profileDropdown) profileDropdown.classList.remove('show');
  });
}

// ================= Keyboard Shortcuts =================
function initHotkeys() {
  document.addEventListener('keydown', (e) => {
    // Check if key is 'N' or 'n' and user is not inside an input/textarea/select
    if ((e.key === 'n' || e.key === 'N') && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      e.preventDefault();
      openQuickAddModal();
    }
    // Escape closes modals
    if (e.key === 'Escape') {
      closeAllModals();
    }
  });
}

// ================= Modal Functions =================
function openQuickAddModal() {
  const modal = document.getElementById('quick-add-modal');
  if (modal) {
    modal.classList.add('active');
  }
}

function closeAllModals() {
  document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
}

// ================= Toast Auto-Dismiss =================
function initToasts() {
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(toast => {
    setTimeout(() => {
      toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  });
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${message}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ================= AJAX Operations =================
function toggleAssignmentDone(assignmentId, btnElement) {
  const url = `/assignments/${assignmentId}/toggle-status/`;
  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      if (btnElement) {
        if (data.is_completed) {
          btnElement.classList.remove('btn-secondary');
          btnElement.classList.add('btn-success');
          btnElement.innerHTML = '<i class="fa-solid fa-check"></i> Completed';
        } else {
          btnElement.classList.remove('btn-success');
          btnElement.classList.add('btn-secondary');
          btnElement.innerHTML = '<i class="fa-regular fa-circle"></i> Mark as Done';
        }
      }
      showToast(data.is_completed ? 'Assignment marked as completed!' : 'Assignment marked as pending.', 'success');
      
      // Update badge if exists
      const badge = document.getElementById(`assign-badge-${assignmentId}`);
      if (badge) {
        badge.className = `badge ${data.is_completed ? 'badge-completed' : 'badge-not-started'}`;
        badge.innerText = data.is_completed ? 'Completed' : 'Not Started';
      }
    }
  })
  .catch(err => {
    console.error('Error toggling assignment:', err);
    showToast('Failed to update assignment status.', 'danger');
  });
}

function toggleReminder(reminderId, checkboxElement) {
  const url = `/reminders/${reminderId}/toggle/`;
  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const parentLabel = checkboxElement.closest('.reminder-item-label');
      if (parentLabel) {
        if (data.is_done) {
          parentLabel.style.textDecoration = 'line-through';
          parentLabel.style.opacity = '0.6';
        } else {
          parentLabel.style.textDecoration = 'none';
          parentLabel.style.opacity = '1';
        }
      }
      showToast(data.is_done ? 'Reminder marked as done.' : 'Reminder set active.', 'success');
    }
  });
}

function initAjaxChecklists() {
  // Listen for checklist item form submissions
  const subtaskForm = document.getElementById('subtask-create-form');
  if (subtaskForm) {
    subtaskForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = subtaskForm.querySelector('input[name="title"]');
      const title = input.value.trim();
      const actionUrl = subtaskForm.getAttribute('action');

      if (!title) return;

      const formData = new FormData();
      formData.append('title', title);

      fetch(actionUrl, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData,
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          input.value = '';
          const list = document.getElementById('subtasks-list-container');
          const newItem = document.createElement('div');
          newItem.className = 'subtask-item';
          newItem.id = `subtask-row-${data.id}`;
          newItem.style.display = 'flex';
          newItem.style.alignItems = 'center';
          newItem.style.justifyContent = 'space-between';
          newItem.style.padding = '0.5rem 0';
          newItem.style.borderBottom = '1px solid var(--border)';

          newItem.innerHTML = `
            <label style="display:flex; align-items:center; gap:0.5rem; cursor:pointer;">
              <input type="checkbox" class="form-checkbox" onchange="toggleSubtask(${data.id})">
              <span>${data.title}</span>
            </label>
            <button type="button" class="btn btn-sm btn-danger btn-icon" onclick="deleteSubtask(${data.id})">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          `;
          list.appendChild(newItem);
          updateSubtaskProgressUI(data.progress_percent, data.subtasks_done, data.subtasks_total);
          showToast('Subtask added!', 'success');
        }
      });
    });
  }
}

function toggleSubtask(subtaskId) {
  fetch(`/subtasks/${subtaskId}/toggle/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      updateSubtaskProgressUI(data.progress_percent);
    }
  });
}

function deleteSubtask(subtaskId) {
  if (!confirm('Remove this subtask?')) return;
  fetch(`/subtasks/${subtaskId}/delete/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const row = document.getElementById(`subtask-row-${subtaskId}`);
      if (row) row.remove();
      updateSubtaskProgressUI(data.progress_percent);
      showToast('Subtask removed.', 'info');
    }
  });
}

function updateSubtaskProgressUI(percent, doneCount, totalCount) {
  const bar = document.getElementById('subtask-progress-bar');
  const text = document.getElementById('subtask-progress-text');
  if (bar) bar.style.width = `${percent}%`;
  if (text) {
    if (doneCount !== undefined && totalCount !== undefined) {
      text.innerText = `${doneCount}/${totalCount} (${percent}%)`;
    } else {
      text.innerText = `${percent}%`;
    }
  }
}

// ================= Live Goal Progress Slider =================
function updateGoalProgressLive(goalId, progressValue) {
  const displaySpan = document.getElementById(`goal-pct-display-${goalId}`);
  if (displaySpan) {
    displaySpan.innerText = `${progressValue}%`;
  }

  fetch(`/goals/${goalId}/update-progress/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `progress=${progressValue}`
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const statusBadge = document.getElementById(`goal-status-badge-${goalId}`);
      if (statusBadge) {
        statusBadge.innerText = data.status_display;
        if (data.status === 'completed') {
          statusBadge.className = 'badge badge-completed';
        } else if (data.status === 'in_progress') {
          statusBadge.className = 'badge badge-in-progress';
        } else {
          statusBadge.className = 'badge badge-not-started';
        }
      }
    }
  });
}
