
// Global UI Functions
function showTool(tool) {
    if(window.location.pathname !== '/') {
        // If not on dashboard, redirect or handle.
        // For simplicity: Redirect to dashboard with a hash or query param?
        // Or just redirect to dashboard and let user click again.
        // Better: Redirect to / and open tool.
        window.location.href = '/?tool=' + tool;
        return;
    }

    document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
    
    if (tool === 'jobs') {
        const m = document.getElementById('jobs-modal');
        if(m) m.style.display = 'flex';
    }
    if (tool === 'products') {
        const m = document.getElementById('products-modal');
        if(m) m.style.display = 'flex';
    } 
    // Chat is default view on index
}

function showSettings() {
    // If settings modal exists on this page (it is currently only in index.html)
    const m = document.getElementById('settings-modal');
    if(m) {
        m.style.display = 'flex';
    } else {
        // If on research page, we might not have the modal. 
        // Ideally include settings modal in base.html or sidebar.
        // For now, alert or redirect.
        alert("Settings are available on the Dashboard.");
        window.location.href = '/';
    }
}

function closeSettings() {
    const m = document.getElementById('settings-modal');
    if(m) m.style.display = 'none';
}

function startNewChat() {
     if(window.location.pathname !== '/') {
        window.location.href = '/';
     } else {
         // Existing logic on index page
         if(typeof currentConversationId !== 'undefined') {
             currentConversationId = null;
             document.getElementById('chat-messages').innerHTML = '<div class="ai-message message">Hello! How can I help you today?</div>';
             showTool('chat');
         }
     }
}

function clearCurrentChat() {
    if(confirm('Clear the current chat? This cannot be undone.')) {
        // Clear chat messages
        const chatMessages = document.getElementById('chat-messages');
        if(chatMessages) {
            chatMessages.innerHTML = '<div class="message ai"><div class="message-avatar"><i class="fas fa-robot"></i></div><div class="message-content">Hello! How can I help you today?</div></div>';
        }
        
        // Reset conversation ID
        if(typeof currentConversationId !== 'undefined') {
            currentConversationId = null;
        }
        
        console.log('Chat cleared successfully');
    }
}

function clearHistory() {
    if(confirm('Clear ALL chat history? This will delete all your conversations and cannot be undone.')) {
        // Clear from localStorage
        const keysToRemove = [];
        for(let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if(key && (key.startsWith('chat_') || key.startsWith('conversation_'))) {
                keysToRemove.push(key);
            }
        }
        keysToRemove.forEach(key => localStorage.removeItem(key));
        
        // Clear history nav
        const historyNav = document.getElementById('history-nav');
        if(historyNav) {
            const newChatBtn = historyNav.querySelector('a[onclick="startNewChat()"]');
            historyNav.innerHTML = '';
            if(newChatBtn) historyNav.appendChild(newChatBtn);
        }
        
        // Clear current chat without confirmation
        const chatMessages = document.getElementById('chat-messages');
        if(chatMessages) {
            chatMessages.innerHTML = '<div class="message ai"><div class="message-avatar"><i class="fas fa-robot"></i></div><div class="message-content">Hello! How can I help you today?</div></div>';
        }
        
        if(typeof currentConversationId !== 'undefined') {
            currentConversationId = null;
        }
        
        console.log('All history cleared successfully');
        alert('All history cleared!');
    }
}

function logout() {
    // Clear any stored auth tokens or session data
    localStorage.clear();
    sessionStorage.clear();
    
    // Redirect to login page
    window.location.href = '/login';
}

// Check for URL params to open tools automatically (e.g. redirect from Research page)
window.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const tool = params.get('tool');
    if(tool && window.location.pathname === '/') {
        showTool(tool);
    }
    
    // Add logout button event listener
    const logoutBtn = document.getElementById('logout-btn');
    if(logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});
