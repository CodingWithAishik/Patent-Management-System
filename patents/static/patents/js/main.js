// ===== Theme Toggle =====
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    
    // Load saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-theme', savedTheme);
    updateThemeButton(savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeButton(newTheme);
        });
    }
    
    function updateThemeButton(theme) {
        if (themeToggle) {
            themeToggle.textContent = theme === 'light' ? '🌙 Dark' : '☀️ Light';
        }
    }
});

// ===== Dynamic Search Fields =====
document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.search-param-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const fieldId = this.getAttribute('data-field');
            const field = document.getElementById(fieldId);
            
            if (field) {
                if (this.checked) {
                    field.classList.add('active');
                    const input = field.querySelector('input');
                    if (input) {
                        input.setAttribute('required', 'required');
                    }
                } else {
                    field.classList.remove('active');
                    const input = field.querySelector('input');
                    if (input) {
                        input.removeAttribute('required');
                        input.value = '';
                    }
                }
            }
        });
        
        // Initialize on page load
        if (checkbox.checked) {
            const fieldId = checkbox.getAttribute('data-field');
            const field = document.getElementById(fieldId);
            if (field) {
                field.classList.add('active');
            }
        }
    });
});

// ===== Form Validation =====
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = 'var(--danger)';
                } else {
                    field.style.borderColor = 'var(--border-color)';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
});

// ===== Confirm Delete =====
function confirmDelete(itemName) {
    return confirm(`Are you sure you want to delete "${itemName}"?`);
}

// ===== Table Sorting (Optional Enhancement) =====
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            if (!header.classList.contains('no-sort')) {
                header.style.cursor = 'pointer';
                header.title = 'Click to sort';
            }
        });
    });
});
