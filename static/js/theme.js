// Theme initialization - apply on all pages
(function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    window.applyTheme = function(theme) {
        if(theme === 'light') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
        updateThemeUI(theme);
    }
    
    function updateThemeUI(theme) {
        const checkbox = document.getElementById('theme-toggle-checkbox');
        if(checkbox) {
            checkbox.checked = (theme === 'light');
        }
    }
    
    window.toggleTheme = function() {
        const currentTheme = localStorage.getItem('theme') || 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
        
        // Update settings if on settings page
        const prefTheme = document.getElementById('pref-theme');
        if(prefTheme) {
            prefTheme.value = newTheme;
        }
    }
    
    // Apply immediately to prevent flash
    applyTheme(savedTheme);
    
    // Update UI when DOM is ready
    if(document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => updateThemeUI(savedTheme));
    } else {
        updateThemeUI(savedTheme);
    }
})();
