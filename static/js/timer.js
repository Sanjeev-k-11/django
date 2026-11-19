/**
 * StudyMate - Pomodoro Study Timer
 * Provides Focus (25m), Short Break (5m), and Long Break (15m) sessions
 * Logs completed study sessions automatically via AJAX to Django backend
 */

let timerInterval = null;
let currentMode = 'focus'; // 'focus', 'short_break', 'long_break'
let timeRemaining = 25 * 60; // in seconds
let isRunning = false;
let sessionWorkMinutes = 25;

document.addEventListener('DOMContentLoaded', () => {
  initTimer();
});

function initTimer() {
  const display = document.getElementById('timer-time-text');
  const startBtn = document.getElementById('timer-start-btn');
  const pauseBtn = document.getElementById('timer-pause-btn');
  const resetBtn = document.getElementById('timer-reset-btn');
  const logBtn = document.getElementById('timer-log-manual-btn');

  const focusTab = document.getElementById('timer-tab-focus');
  const shortBreakTab = document.getElementById('timer-tab-short');
  const longBreakTab = document.getElementById('timer-tab-long');

  if (!display) return;

  function updateDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const formatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    display.innerText = formatted;
    document.title = `${formatted} - StudyMate Pomodoro`;
  }

  function setMode(mode, minutes) {
    currentMode = mode;
    sessionWorkMinutes = minutes;
    timeRemaining = minutes * 60;
    isRunning = false;
    clearInterval(timerInterval);

    // Update UI tabs
    [focusTab, shortBreakTab, longBreakTab].forEach(t => t && t.classList.remove('btn-primary'));
    [focusTab, shortBreakTab, longBreakTab].forEach(t => t && t.classList.add('btn-secondary'));

    const modeLabel = document.getElementById('timer-mode-label');
    const circle = document.getElementById('timer-circle');

    if (mode === 'focus') {
      if (focusTab) { focusTab.classList.remove('btn-secondary'); focusTab.classList.add('btn-primary'); }
      if (modeLabel) modeLabel.innerText = 'Focus Session';
      if (circle) circle.style.borderTopColor = 'var(--primary)';
    } else if (mode === 'short_break') {
      if (shortBreakTab) { shortBreakTab.classList.remove('btn-secondary'); shortBreakTab.classList.add('btn-primary'); }
      if (modeLabel) modeLabel.innerText = 'Short Break';
      if (circle) circle.style.borderTopColor = 'var(--accent-teal)';
    } else if (mode === 'long_break') {
      if (longBreakTab) { longBreakTab.classList.remove('btn-secondary'); longBreakTab.classList.add('btn-primary'); }
      if (modeLabel) modeLabel.innerText = 'Long Break';
      if (circle) circle.style.borderTopColor = 'var(--purple)';
    }

    if (startBtn) startBtn.style.display = 'inline-flex';
    if (pauseBtn) pauseBtn.style.display = 'none';

    updateDisplay();
  }

  if (focusTab) focusTab.addEventListener('click', () => setMode('focus', getCustomMinutes('focus', 25)));
  if (shortBreakTab) shortBreakTab.addEventListener('click', () => setMode('short_break', getCustomMinutes('short', 5)));
  if (longBreakTab) longBreakTab.addEventListener('click', () => setMode('long_break', getCustomMinutes('long', 15)));

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      if (isRunning) return;
      isRunning = true;
      startBtn.style.display = 'none';
      if (pauseBtn) pauseBtn.style.display = 'inline-flex';

      timerInterval = setInterval(() => {
        if (timeRemaining > 0) {
          timeRemaining--;
          updateDisplay();
        } else {
          // Timer finished
          clearInterval(timerInterval);
          isRunning = false;
          startBtn.style.display = 'inline-flex';
          if (pauseBtn) pauseBtn.style.display = 'none';

          playAlertSound();

          if (currentMode === 'focus') {
            logCompletedSession(sessionWorkMinutes);
            alert(`Great work! You completed a ${sessionWorkMinutes}-minute focus session.`);
            setMode('short_break', 5);
          } else {
            alert('Break ended! Ready to focus again?');
            setMode('focus', 25);
          }
        }
      }, 1000);
    });
  }

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      isRunning = false;
      clearInterval(timerInterval);
      pauseBtn.style.display = 'none';
      if (startBtn) startBtn.style.display = 'inline-flex';
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      setMode(currentMode, sessionWorkMinutes);
    });
  }

  if (logBtn) {
    logBtn.addEventListener('click', () => {
      const manualMins = prompt("How many minutes did you study?", "25");
      if (manualMins && !isNaN(manualMins) && parseInt(manualMins) > 0) {
        logCompletedSession(parseInt(manualMins));
      }
    });
  }

  updateDisplay();
}

function getCustomMinutes(type, defaultVal) {
  const customInput = document.getElementById(`custom-${type}-min`);
  if (customInput && customInput.value && !isNaN(customInput.value)) {
    return Math.max(1, parseInt(customInput.value));
  }
  return defaultVal;
}

function playAlertSound() {
  try {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
    osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.15); // A5
    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.6);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.6);
  } catch (e) {
    console.log('Audio notification fallback');
  }
}

function logCompletedSession(durationMinutes) {
  const subjectSelect = document.getElementById('timer-subject-select');
  const subjectId = subjectSelect ? subjectSelect.value : null;
  const notesInput = document.getElementById('timer-notes-input');
  const notes = notesInput ? notesInput.value : '';

  fetch('/timer/log/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      subject_id: subjectId,
      duration_minutes: durationMinutes,
      notes: notes,
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      if (notesInput) notesInput.value = '';
      showToast(`Logged ${durationMinutes} minutes for ${data.subject_name}!`, 'success');

      // Update today's and week's hours on the page
      const todayEl = document.getElementById('timer-today-hours');
      const weekEl = document.getElementById('timer-week-hours');
      const streakEl = document.getElementById('timer-streak-val');

      if (todayEl) todayEl.innerText = `${data.today_hours} hrs`;
      if (weekEl) weekEl.innerText = `${data.week_hours} hrs`;
      if (streakEl) streakEl.innerText = `${data.streak} Days`;
    }
  })
  .catch(err => {
    console.error('Failed to log study session:', err);
  });
}
