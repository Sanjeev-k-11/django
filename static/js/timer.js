/**
 * StudyMate - Luxury Pomodoro Focus Timer
 * - Circular SVG Progress Ring with smooth animated arc
 * - Built-in Web Audio Ambient Noise Synthesizer (Rain, Deep Waves, Clock, Mute)
 * - Auto-logging of completed study sessions via AJAX to Django backend
 * - Streak & Daily Study Milestone Badges
 */

let timerInterval = null;
let currentMode = 'focus'; // 'focus', 'short_break', 'long_break'
let totalSessionSeconds = 25 * 60;
let timeRemaining = 25 * 60;
let isRunning = false;
let sessionWorkMinutes = 25;
const CIRCUMFERENCE = 880; // 2 * PI * 140

// Ambient Sound Variables
let ambientCtx = null;
let ambientSource = null;
let ambientGain = null;
let currentSound = 'none';

document.addEventListener('DOMContentLoaded', () => {
  initTimer();
});

function initTimer() {
  const display = document.getElementById('timer-time-text');
  const startBtn = document.getElementById('timer-start-btn');
  const pauseBtn = document.getElementById('timer-pause-btn');
  const resetBtn = document.getElementById('timer-reset-btn');
  const logBtn = document.getElementById('timer-log-manual-btn');
  const circleProgress = document.getElementById('timer-progress-circle');
  const statusHint = document.getElementById('timer-status-hint');

  const focusTab = document.getElementById('timer-tab-focus');
  const shortBreakTab = document.getElementById('timer-tab-short');
  const longBreakTab = document.getElementById('timer-tab-long');

  if (!display) return;

  function updateDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const formatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    display.innerText = formatted;
    document.title = `${formatted} (${currentMode === 'focus' ? 'Focus' : 'Break'}) - StudyMate`;

    // Update Circular Arc
    if (circleProgress) {
      const progressFraction = (totalSessionSeconds - timeRemaining) / totalSessionSeconds;
      const offset = CIRCUMFERENCE * (1 - progressFraction);
      circleProgress.style.strokeDashoffset = offset;
    }
  }

  function setMode(mode, minutes) {
    currentMode = mode;
    sessionWorkMinutes = minutes;
    totalSessionSeconds = minutes * 60;
    timeRemaining = totalSessionSeconds;
    isRunning = false;
    clearInterval(timerInterval);

    // Update Mode Pills
    [focusTab, shortBreakTab, longBreakTab].forEach(t => t && t.classList.remove('active'));

    const modeLabel = document.getElementById('timer-mode-label');

    if (mode === 'focus') {
      if (focusTab) focusTab.classList.add('active');
      if (modeLabel) {
        modeLabel.innerText = 'FOCUS CYCLE';
        modeLabel.style.color = 'var(--luxury-rose)';
      }
      if (circleProgress) circleProgress.style.stroke = 'url(#timerGradFocus)';
      if (statusHint) statusHint.innerText = 'Ready to focus';
    } else if (mode === 'short_break') {
      if (shortBreakTab) shortBreakTab.classList.add('active');
      if (modeLabel) {
        modeLabel.innerText = 'SHORT BREAK';
        modeLabel.style.color = '#0D9488';
      }
      if (circleProgress) circleProgress.style.stroke = 'url(#timerGradBreak)';
      if (statusHint) statusHint.innerText = 'Rest your eyes & stretch';
    } else if (mode === 'long_break') {
      if (longBreakTab) longBreakTab.classList.add('active');
      if (modeLabel) {
        modeLabel.innerText = 'LONG BREAK';
        modeLabel.style.color = '#7C3AED';
      }
      if (circleProgress) circleProgress.style.stroke = '#7C3AED';
      if (statusHint) statusHint.innerText = 'Recharge & take a walk';
    }

    if (startBtn) startBtn.style.display = 'inline-flex';
    if (pauseBtn) pauseBtn.style.display = 'none';

    updateDisplay();
  }

  window.applyPreset = function(minutes) {
    document.querySelectorAll('.preset-chip').forEach(c => c.classList.remove('active'));
    if (event && event.target) event.target.classList.add('active');
    setMode('focus', minutes);
  };

  if (focusTab) focusTab.addEventListener('click', () => setMode('focus', getCustomMinutes('focus', 25)));
  if (shortBreakTab) shortBreakTab.addEventListener('click', () => setMode('short_break', getCustomMinutes('short', 5)));
  if (longBreakTab) longBreakTab.addEventListener('click', () => setMode('long_break', getCustomMinutes('long', 15)));

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      if (isRunning) return;
      isRunning = true;
      startBtn.style.display = 'none';
      if (pauseBtn) pauseBtn.style.display = 'inline-flex';
      if (statusHint) statusHint.innerText = currentMode === 'focus' ? 'Focusing in flow...' : 'Taking a rest...';

      timerInterval = setInterval(() => {
        if (timeRemaining > 0) {
          timeRemaining--;
          updateDisplay();
        } else {
          // Finished Interval
          clearInterval(timerInterval);
          isRunning = false;
          startBtn.style.display = 'inline-flex';
          if (pauseBtn) pauseBtn.style.display = 'none';

          playAlertSound();

          if (currentMode === 'focus') {
            logCompletedSession(sessionWorkMinutes);
            alert(`🎉 Outstanding work! You completed a ${sessionWorkMinutes}-minute focus block.`);
            setMode('short_break', 5);
          } else {
            alert('Break complete! Ready to begin your next focus cycle?');
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
      if (statusHint) statusHint.innerText = 'Paused';
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      setMode(currentMode, sessionWorkMinutes);
    });
  }

  if (logBtn) {
    logBtn.addEventListener('click', () => {
      const manualMins = prompt("How many study minutes would you like to record?", "25");
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

/* Synthesized Ambient Audio Focus Generators */
window.setAmbientSound = function(type) {
  document.querySelectorAll('.sound-chip').forEach(b => b.classList.remove('active'));
  const activeBtn = document.querySelector(`.sound-chip[data-sound="${type}"]`);
  if (activeBtn) activeBtn.classList.add('active');

  stopAmbientSound();
  if (type === 'none') return;

  try {
    ambientCtx = new (window.AudioContext || window.webkitAudioContext)();
    currentSound = type;

    if (type === 'rain' || type === 'brown') {
      const bufferSize = ambientCtx.sampleRate * 2;
      const buffer = ambientCtx.createBuffer(1, bufferSize, ambientCtx.sampleRate);
      const data = buffer.getChannelData(0);

      let lastOut = 0.0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        if (type === 'brown') {
          lastOut = (lastOut + (0.02 * white)) / 1.02;
          data[i] = lastOut * 3.5;
        } else {
          // Rain pinkish
          data[i] = (white * 0.4) + (Math.random() * 0.1);
        }
      }

      ambientSource = ambientCtx.createBufferSource();
      ambientSource.buffer = buffer;
      ambientSource.loop = true;

      ambientGain = ambientCtx.createGain();
      ambientGain.gain.setValueAtTime(0.08, ambientCtx.currentTime);

      ambientSource.connect(ambientGain);
      ambientGain.connect(ambientCtx.destination);
      ambientSource.start();
    } else if (type === 'tick') {
      playClockTickLoop();
    }
  } catch (e) {
    console.log('Web audio ambient not supported in this browser:', e);
  }
};

let tickInterval = null;
function playClockTickLoop() {
  tickInterval = setInterval(() => {
    if (!ambientCtx || currentSound !== 'tick') {
      clearInterval(tickInterval);
      return;
    }
    const osc = ambientCtx.createOscillator();
    const g = ambientCtx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(1000, ambientCtx.currentTime);
    g.gain.setValueAtTime(0.03, ambientCtx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ambientCtx.currentTime + 0.04);
    osc.connect(g);
    g.connect(ambientCtx.destination);
    osc.start();
    osc.stop(ambientCtx.currentTime + 0.05);
  }, 1000);
}

function stopAmbientSound() {
  if (tickInterval) { clearInterval(tickInterval); tickInterval = null; }
  if (ambientSource) {
    try { ambientSource.stop(); } catch (e) {}
    ambientSource = null;
  }
  if (ambientCtx) {
    ambientCtx.close().catch(() => {});
    ambientCtx = null;
  }
  currentSound = 'none';
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
    osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.2); // A5
    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.7);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.7);
  } catch (e) {}
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

      // Update counters
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
