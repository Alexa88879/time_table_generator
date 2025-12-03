document.addEventListener('DOMContentLoaded', function(){
  // Theme toggle
  const themeToggle = document.getElementById('theme-toggle');
  if(themeToggle){
    themeToggle.addEventListener('click', function(){
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const newTheme = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('site-theme', newTheme);
      
      // Update button text
      themeToggle.innerHTML = newTheme === 'dark' 
        ? '<i class="bi bi-sun-fill"></i> Light Mode' 
        : '<i class="bi bi-moon-stars-fill"></i> Dark Mode';
    });

    // Restore saved theme
    const saved = localStorage.getItem('site-theme');
    if(saved){
      document.documentElement.setAttribute('data-theme', saved);
      themeToggle.innerHTML = saved === 'dark' 
        ? '<i class="bi bi-sun-fill"></i> Light Mode' 
        : '<i class="bi bi-moon-stars-fill"></i> Dark Mode';
    } else {
      // Check system preference
      if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i> Light Mode';
      }
    }
  }

  // Sidebar toggle for mobile
  const sidebarOpen = document.getElementById('sidebar-open');
  const sidebarClose = document.getElementById('sidebar-close');
  const sidebar = document.getElementById('sidebar');
  
  if(sidebar){
    function toggleSidebar(){
      sidebar.classList.toggle('open');
    }
    
    if(sidebarOpen) sidebarOpen.addEventListener('click', toggleSidebar);
    if(sidebarClose) sidebarClose.addEventListener('click', toggleSidebar);

    // Close sidebar when clicking outside
    document.addEventListener('click', function(e){
      if(sidebar.classList.contains('open') && 
         !sidebar.contains(e.target) && 
         (!sidebarOpen || !sidebarOpen.contains(e.target)) &&
         (!sidebarClose || !sidebarClose.contains(e.target))){
        sidebar.classList.remove('open');
      }
    });
  }

  // Active nav link highlighting
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    if(link.getAttribute('href') === currentPath){
      link.classList.add('active');
    }
  });

  // Timetable class click handler
  document.querySelectorAll('.tclass').forEach(function(el){
    el.addEventListener('click', function(e){
      const title = this.querySelector('.tclass-title')?.innerText || 'Class';
      const meta = this.querySelector('.tclass-meta')?.innerText || '';
      
      const modalBody = document.getElementById('modalBody');
      if(modalBody){
        modalBody.innerHTML = `<p><strong>${title}</strong></p><p class="text-muted">${meta}</p>`;
        const modal = document.getElementById('classModal');
        if(modal && typeof bootstrap !== 'undefined'){
          new bootstrap.Modal(modal).show();
        }
      }
    });
  });

  // Initialize tooltips if Bootstrap is loaded
  if(typeof bootstrap !== 'undefined' && bootstrap.Tooltip){
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(tooltipTriggerEl => {
      new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }

  // Initialize popovers if Bootstrap is loaded
  if(typeof bootstrap !== 'undefined' && bootstrap.Popover){
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    popoverTriggerList.forEach(popoverTriggerEl => {
      new bootstrap.Popover(popoverTriggerEl);
    });
  }

  // Loading overlay functionality
  window.showLoading = function(message = 'Loading...'){
    let overlay = document.getElementById('loadingOverlay');
    if(!overlay){
      overlay = document.createElement('div');
      overlay.id = 'loadingOverlay';
      overlay.innerHTML = `
        <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;">
          <div style="background:white;padding:2rem;border-radius:12px;text-align:center;">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3 mb-0">${message}</p>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);
    }
    overlay.style.display = 'block';
  };

  window.hideLoading = function(){
    const overlay = document.getElementById('loadingOverlay');
    if(overlay){
      overlay.style.display = 'none';
    }
  };

  // SweetAlert2 helpers (if available)
  if(typeof Swal !== 'undefined'){
    window.showSuccess = function(title, text){
      return Swal.fire({
        icon: 'success',
        title: title,
        text: text,
        confirmButtonColor: '#6366f1'
      });
    };

    window.showError = function(title, text){
      return Swal.fire({
        icon: 'error',
        title: title,
        text: text,
        confirmButtonColor: '#ef4444'
      });
    };

    window.confirmDelete = function(url, itemName = 'this item'){
      return Swal.fire({
        title: 'Are you sure?',
        text: `You are about to delete ${itemName}. This action cannot be undone.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#6b7280',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if(result.isConfirmed){
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
            if(data.success){
              showSuccess('Deleted!', data.message || 'Item has been deleted.').then(() => {
                location.reload();
              });
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
  }

  // DataTables initialization (if available)
  if(typeof jQuery !== 'undefined' && jQuery.fn.DataTable){
    jQuery('.data-table').DataTable({
      pageLength: 10,
      responsive: true,
      language: {
        search: '',
        searchPlaceholder: 'Search...'
      }
    });
  }

  // Responsive timetable grid
  const grid = document.getElementById('timetableGrid');
  if(grid && window.innerWidth < 768){
    grid.style.overflowX = 'auto';
  }

  // Animate counters on dashboard
  const counters = document.querySelectorAll('.stat-card h3, .stat-info h3');
  counters.forEach(counter => {
    const target = parseInt(counter.textContent) || 0;
    if (target > 0) {
      counter.textContent = '0';
      setTimeout(() => animateCounter(counter, target), 300);
    }
  });

  // Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.card, .stat-card').forEach(el => {
    observer.observe(el);
  });
});

// Helper Functions

// Animate Counter
function animateCounter(element, target, duration = 1000) {
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
}

// Copy to Clipboard
window.copyToClipboard = function(text) {
  if(navigator.clipboard){
    navigator.clipboard.writeText(text).then(() => {
      if(typeof Swal !== 'undefined'){
        Swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'success',
          title: 'Copied to clipboard!',
          showConfirmButton: false,
          timer: 2000
        });
      } else {
        alert('Copied to clipboard!');
      }
    }).catch(() => {
      alert('Failed to copy.');
    });
  }
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
      if(typeof showSuccess === 'function'){
        showSuccess('Success!', data.message || 'Operation completed successfully.')
          .then(() => {
            if (successCallback) successCallback(data);
            else if (data.redirect) window.location.href = data.redirect;
          });
      } else {
        if (successCallback) successCallback(data);
        else if (data.redirect) window.location.href = data.redirect;
      }
    } else {
      if(typeof showError === 'function'){
        showError('Error', data.message || 'An error occurred.');
      } else {
        alert(data.message || 'An error occurred.');
      }
    }
  })
  .catch(error => {
    hideLoading();
    if(typeof showError === 'function'){
      showError('Error', 'An error occurred. Please try again.');
    } else {
      alert('An error occurred. Please try again.');
    }
  });
};

// Download file helper
window.downloadFile = function(url, filename) {
  showLoading('Generating file...');
  
  fetch(url)
    .then(response => response.blob())
    .then(blob => {
      hideLoading();
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename || 'download.xlsx';
      link.click();
      URL.revokeObjectURL(link.href);
      if(typeof Swal !== 'undefined'){
        Swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'success',
          title: 'File downloaded successfully!',
          showConfirmButton: false,
          timer: 2000
        });
      }
    })
    .catch(error => {
      hideLoading();
      if(typeof showError === 'function'){
        showError('Error', 'Failed to download file.');
      } else {
        alert('Failed to download file.');
      }
    });
};
