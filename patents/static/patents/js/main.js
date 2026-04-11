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

// ===== Table Sorting =====
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('.sortable-table');
    console.log('Found', tables.length, 'sortable tables');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('th.sortable');
        console.log('Found', headers.length, 'sortable headers in table');
        
        headers.forEach(header => {
            header.style.cursor = 'pointer'; // Ensure cursor shows it's clickable
            header.addEventListener('click', function() {
                console.log('Sorting column:', this.getAttribute('data-field'));
                const field = this.getAttribute('data-field');
                const type = this.getAttribute('data-type');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                // Determine sort order
                let ascending = true;
                if (this.classList.contains('sorted-asc')) {
                    ascending = false;
                    this.classList.remove('sorted-asc');
                    this.classList.add('sorted-desc');
                } else {
                    // Remove sorting from all headers
                    headers.forEach(h => {
                        h.classList.remove('sorted-asc', 'sorted-desc');
                    });
                    this.classList.add('sorted-asc');
                }
                
                // Get column index
                const columnIndex = Array.from(this.parentElement.children).indexOf(this);
                
                // Sort rows
                rows.sort((a, b) => {
                    const aCell = a.children[columnIndex];
                    const bCell = b.children[columnIndex];
                    
                    // Get text from truncate-cell if it exists, otherwise from cell
                    let aValue = '';
                    let bValue = '';
                    
                    const aTruncateCell = aCell.querySelector('.truncate-cell');
                    const bTruncateCell = bCell.querySelector('.truncate-cell');
                    
                    if (aTruncateCell) {
                        // Use data-full-text for accurate sorting
                        aValue = aTruncateCell.getAttribute('data-full-text') || '';
                    } else {
                        aValue = aCell.textContent.trim();
                    }
                    
                    if (bTruncateCell) {
                        // Use data-full-text for accurate sorting
                        bValue = bTruncateCell.getAttribute('data-full-text') || '';
                    } else {
                        bValue = bCell.textContent.trim();
                    }
                    
                    // Handle empty values
                    if (aValue === '-' || aValue === '—' || aValue === '') aValue = '';
                    if (bValue === '-' || bValue === '—' || bValue === '') bValue = '';
                    
                    // Sort based on type
                    if (type === 'number') {
                        aValue = parseFloat(aValue) || 0;
                        bValue = parseFloat(bValue) || 0;
                        return ascending ? aValue - bValue : bValue - aValue;
                    } else if (type === 'date') {
                        // Parse dates in dd/mm/yyyy format
                        aValue = parseDateString(aValue);
                        bValue = parseDateString(bValue);
                        return ascending ? aValue - bValue : bValue - aValue;
                    } else {
                        // Text comparison
                        if (ascending) {
                            return aValue.localeCompare(bValue);
                        } else {
                            return bValue.localeCompare(aValue);
                        }
                    }
                });
                
                // Re-append rows in sorted order
                rows.forEach(row => tbody.appendChild(row));
            });
        });
    });
});

// Helper function to parse date strings
function parseDateString(dateStr) {
    if (!dateStr || dateStr === '-' || dateStr === '—') {
        return 0;
    }
    
    // Handle dd/mm/yyyy or dd.mm.yyyy or dd-mm-yyyy formats
    const parts = dateStr.split(/[\/\.\-]/);
    if (parts.length === 3) {
        // Assume dd/mm/yyyy format
        const day = parseInt(parts[0]) || 0;
        const month = parseInt(parts[1]) || 0;
        const year = parseInt(parts[2]) || 0;
        return new Date(year, month - 1, day).getTime();
    }
    
    // Try to parse as regular date
    const date = new Date(dateStr);
    return isNaN(date.getTime()) ? 0 : date.getTime();
}

// ===== Show More / Show Less Toggle =====
// Make function globally accessible for inline onclick handlers
window.toggleShowMore = function(button) {
    console.log('toggleShowMore called');
    const cell = button.closest('.truncate-cell');
    const textSpan = cell.querySelector('.truncated-text');
    const fullText = cell.getAttribute('data-full-text');
    
    if (button.classList.contains('expanded')) {
        // Collapse: show truncated text
        const truncatedText = fullText.length > 100 ? fullText.substring(0, 100) + '...' : fullText;
        textSpan.textContent = truncatedText;
        button.textContent = 'Show More';
        button.classList.remove('expanded');
        cell.classList.remove('expanded');
    } else {
        // Expand: show full text
        textSpan.textContent = fullText;
        button.textContent = 'Show Less';
        button.classList.add('expanded');
        cell.classList.add('expanded');
    }
};

