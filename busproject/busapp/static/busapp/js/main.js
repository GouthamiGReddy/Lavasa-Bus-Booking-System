/* ── Bus Booking System — Main JS ── */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss alerts ──
  setTimeout(() => {
    document.querySelectorAll('.alert-dismissible').forEach(el => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert && bsAlert.close();
    });
  }, 5000);

  // ── Journey type toggle (booking forms) ──
  const journeySelect = document.getElementById('id_journey_type');
  const onewayFields = document.getElementById('oneway-fields');
  const serviceType = document.body.dataset.serviceType;

  function toggleOnewayFields() {
    if (!journeySelect || !onewayFields) return;
    const val = journeySelect.value;
    const isVacation = serviceType === 'vacation';
    if (isVacation || val === 'bothway') {
      onewayFields.style.display = 'none';
      // Clear required on hidden fields
      document.querySelectorAll('#oneway-fields [required]').forEach(el => el.removeAttribute('required'));
    } else {
      onewayFields.style.display = 'block';
      if (!isVacation) {
        const reasonEl = document.getElementById('id_reason');
        if (reasonEl) reasonEl.setAttribute('required', '');
      }
    }
  }

  if (journeySelect) {
    journeySelect.addEventListener('change', toggleOnewayFields);
    toggleOnewayFields(); // run on load
  }

  // ── Admin: return slot toggle ──
  const hasReturnCheck = document.getElementById('hasReturnCheck');
  const returnFields = document.getElementById('return-slot-fields');
  const serviceTypeSelect = document.getElementById('id_service_type');

  function toggleReturnFields() {
    if (!returnFields) return;
    const isWeekend = !serviceTypeSelect || serviceTypeSelect.value === 'weekend';
    const checked = hasReturnCheck && hasReturnCheck.checked;
    returnFields.style.display = (isWeekend && checked) ? 'block' : 'none';
  }

  function handleServiceTypeChange() {
    if (!hasReturnCheck || !returnFields) return;
    const isVacation = serviceTypeSelect && serviceTypeSelect.value === 'vacation';
    const hasReturnRow = hasReturnCheck.closest('.mb-3') || hasReturnCheck.closest('.row');
    if (hasReturnRow) hasReturnRow.style.display = isVacation ? 'none' : 'block';
    if (isVacation) {
      hasReturnCheck.checked = false;
      returnFields.style.display = 'none';
    } else {
      toggleReturnFields();
    }
  }

  if (hasReturnCheck) {
    hasReturnCheck.addEventListener('change', toggleReturnFields);
    toggleReturnFields();
  }
  if (serviceTypeSelect) {
    serviceTypeSelect.addEventListener('change', handleServiceTypeChange);
    handleServiceTypeChange();
  }

  // ── Seat bar animations ──
  document.querySelectorAll('.seat-bar-fill').forEach(el => {
    const pct = parseFloat(el.dataset.pct || 0);
    el.style.width = '0%';
    setTimeout(() => { el.style.width = pct + '%'; }, 200);
    if (pct > 70) el.classList.add('low');
  });

  // ── Confirm delete ──
  document.querySelectorAll('.confirm-delete').forEach(btn => {
    btn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to permanently delete this slot? This cannot be undone.')) {
        e.preventDefault();
      }
    });
  });

  // ── Confirm cancel booking ──
  document.querySelectorAll('.confirm-cancel').forEach(btn => {
    btn.addEventListener('click', function (e) {
      if (!confirm('Withdraw your booking? This action cannot be undone.')) {
        e.preventDefault();
      }
    });
  });

  // ── Admin booking action modal ──
  const bookingActionModal = document.getElementById('bookingActionModal');
  if (bookingActionModal) {
    bookingActionModal.addEventListener('show.bs.modal', function (e) {
      const btn = e.relatedTarget;
      const action = btn.dataset.action;
      const name = btn.dataset.name;
      const url = btn.dataset.url;

      this.querySelector('#modal-action-name').textContent = name || '';
      this.querySelector('#modal-action-verb').textContent =
        action === 'approve' ? 'Approve' : action === 'cancel' ? 'Cancel' : 'Revert';
      this.querySelector('#modal-action-input').value = action;
      this.querySelector('#modal-form').action = url;
    });
  }

  // ── Tooltip init ──
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el, { trigger: 'hover' });
  });

  // ── Year of study visibility (signup) ──
  const roleSelect = document.getElementById('id_role');
  const yearRow = document.getElementById('year-of-study-row');
  function toggleYearRow() {
    if (!roleSelect || !yearRow) return;
    yearRow.style.display = roleSelect.value === 'student' ? 'block' : 'none';
  }
  if (roleSelect) {
    roleSelect.addEventListener('change', toggleYearRow);
    toggleYearRow();
  }

});
