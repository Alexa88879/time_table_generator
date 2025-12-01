// Main JavaScript - Core Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS (Animate on Scroll)
    AOS.init({
        duration: 600,
        easing: 'ease-out-cubic',
        once: true,
        offset: 50
    });

    // Initialize Components
    initSidebar();
    initThemeToggle();
    initLoadingOverlay();
    initQuickStats();
    initDataTables();
    initFormValidation();
    initTooltips();
});

// Sidebar Toggle
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const openBtn = document.getElementById('openSidebar');
    const closeBtn = document.getElementById('toggleSidebar');
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    if (openBtn) {
        openBtn.addEventListener('click', () => {
            sidebar.classList.add('show');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            sidebar.classList.remove('show');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    overlay.addEventListener('click', () => {
        sidebar.classList.remove('show');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    });

    // Add CSS for overlay
    const style = document.createElement('style');
    style.textContent = `
        .sidebar-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 999;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        .sidebar-overlay.active {
            opacity: 1;
            visibility: visible;
        }
    `;
    document.head.appendChild(style);
}

// Theme Toggle
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');

    // Set initial theme
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
        updateThemeButton(savedTheme === 'dark');
    } else if (prefersDark) {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        updateThemeButton(true);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeButton(newTheme === 'dark');
        });
    }

    function updateThemeButton(isDark) {
        if (themeToggle) {
            themeToggle.innerHTML = isDark 
                ? '<i class="bi bi-sun-fill"></i><span>Light Mode</span>'
                : '<i class="bi bi-moon-stars-fill"></i><span>Dark Mode</span>';
        }
    }
}

// Loading Overlay
function initLoadingOverlay() {
    window.showLoading = function(text = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        const loaderText = overlay.querySelector('.loader-text');
        if (loaderText) loaderText.textContent = text;
        overlay.classList.add('active');
    };

    window.hideLoading = function() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.remove('active');
    };
}

// Quick Stats (Header)
function initQuickStats() {
    // Update quick stats from dashboard data if available
    const sectionsEl = document.getElementById('statSections');
    const facultyEl = document.getElementById('statFaculty');
    
    if (sectionsEl && document.getElementById('quickStatSections')) {
        document.getElementById('quickStatSections').textContent = sectionsEl.textContent;
    }
    if (facultyEl && document.getElementById('quickStatFaculty')) {
        document.getElementById('quickStatFaculty').textContent = facultyEl.textContent;
    }
}

// DataTables Initialization
function initDataTables() {
    const tables = document.querySelectorAll('.data-table');
    tables.forEach(table => {
        if (!$.fn.DataTable.isDataTable(table)) {
            $(table).DataTable({
                pageLength: 10,
                responsive: true,
                dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
                     '<"row"<"col-sm-12"tr>>' +
                     '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
                language: {
                    search: '',
                    searchPlaceholder: 'Search...',
                    lengthMenu: 'Show _MENU_ entries',
                    info: 'Showing _START_ to _END_ of _TOTAL_ entries',
                    paginate: {
                        first: '<i class="bi bi-chevron-double-left"></i>',
                        previous: '<i class="bi bi-chevron-left"></i>',
                        next: '<i class="bi bi-chevron-right"></i>',
                        last: '<i class="bi bi-chevron-double-right"></i>'
                    }
                },
                drawCallback: function() {
                    // Reinitialize tooltips after table redraw
                    initTooltips();
                }
            });
        }
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Tooltips
function initTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => {
        new bootstrap.Tooltip(el);
    });
}

// SweetAlert2 Helpers
window.showSuccess = function(title, text) {
    return Swal.fire({
        icon: 'success',
        title: title,
        text: text,
        confirmButtonColor: 'var(--primary)',
        background: 'var(--bg-card)',
        color: 'var(--text-primary)'
    });
};

window.showError = function(title, text) {
    return Swal.fire({
        icon: 'error',
        title: title,
        text: text,
        confirmButtonColor: 'var(--danger)',
        background: 'var(--bg-card)',
        color: 'var(--text-primary)'
    });
};

window.showConfirm = function(title, text, confirmText = 'Yes, proceed') {
    return Swal.fire({
        icon: 'warning',
        title: title,
        text: text,
        showCancelButton: true,
        confirmButtonColor: 'var(--primary)',
        cancelButtonColor: 'var(--danger)',
        confirmButtonText: confirmText,
        cancelButtonText: 'Cancel',
        background: 'var(--bg-card)',
        color: 'var(--text-primary)'
    });
};

window.showToast = function(icon, title) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        background: 'var(--bg-card)',
        color: 'var(--text-primary)',
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer);
            toast.addEventListener('mouseleave', Swal.resumeTimer);
        }
    });
    return Toast.fire({ icon, title });
};

// Delete Confirmation
window.confirmDelete = function(url, itemName = 'this item') {
    showConfirm(
        'Are you sure?',
        `You are about to delete ${itemName}. This action cannot be undone.`,
        'Yes, delete it'
    ).then((result) => {
        if (result.isConfirmed) {
            showLoading('Deleting...');
            
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                if (data.success) {
                    showSuccess('Deleted!', data.message || 'Item has been deleted.')
                        .then(() => location.reload());
                } else {
                    showError('Error', data.message || 'Failed to delete item.');
                }
            })
            .catch(error => {
                hideLoading();
                showError('Error', 'An error occurred while deleting.');
            });
        }
    });
};

// Form Submit with AJAX
window.submitFormAjax = function(form, successCallback) {
    const formData = new FormData(form);
    const url = form.action;
    const method = form.method || 'POST';

    showLoading('Saving...');

    fetch(url, {
        method: method,
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            showSuccess('Success!', data.message || 'Operation completed successfully.')
                .then(() => {
                    if (successCallback) successCallback(data);
                    else if (data.redirect) window.location.href = data.redirect;
                });
        } else {
            showError('Error', data.message || 'An error occurred.');
        }
    })
    .catch(error => {
        hideLoading();
        showError('Error', 'An error occurred. Please try again.');
    });
};

// Debounce Function
window.debounce = function(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Format Date
window.formatDate = function(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
};

// Copy to Clipboard
window.copyToClipboard = function(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('success', 'Copied to clipboard!');
    }).catch(() => {
        showToast('error', 'Failed to copy.');
    });
};

// Excel Download Helper
window.downloadExcel = function(url, filename) {
    showLoading('Generating Excel file...');
    
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            hideLoading();
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename || 'download.xlsx';
            link.click();
            URL.revokeObjectURL(link.href);
            showToast('success', 'File downloaded successfully!');
        })
        .catch(error => {
            hideLoading();
            showError('Error', 'Failed to download file.');
        });
};

// PDF Download Helper
window.downloadPDF = function(url, filename) {
    showLoading('Generating PDF file...');
    
    fetch(url)
        .then(response => response.blob())
        .then(blob => {
            hideLoading();
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename || 'download.pdf';
            link.click();
            URL.revokeObjectURL(link.href);
            showToast('success', 'File downloaded successfully!');
        })
        .catch(error => {
            hideLoading();
            showError('Error', 'Failed to download file.');
        });
};

// Animate Counter
window.animateCounter = function(element, target, duration = 1000) {
    const start = parseInt(element.textContent) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
};

// Smooth Scroll to Element
window.scrollToElement = function(selector, offset = 100) {
    const element = document.querySelector(selector);
    if (element) {
        const top = element.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top, behavior: 'smooth' });
    }
};

// Local Storage Helpers
window.storage = {
    set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
    get: (key) => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    },
    remove: (key) => localStorage.removeItem(key)
};

// Event Delegation Helper
window.delegate = function(parent, eventType, selector, handler) {
    parent.addEventListener(eventType, function(event) {
        const targetElement = event.target.closest(selector);
        if (targetElement && parent.contains(targetElement)) {
            handler.call(targetElement, event);
        }
    });
};
