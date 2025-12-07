document.addEventListener('DOMContentLoaded', function() {
    // Create Widget HTML
    const widgetHTML = `
    <div id="accessibility-widget">
        <div id="accessibility-menu">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="mb-0 fw-bold">Εργαλεία Προσβασιμότητας</h6>
                <button class="btn-close btn-sm" id="acc-close-btn"></button>
            </div>
            
            <div class="acc-option">
                <span class="acc-option-title">Μέγεθος Κειμένου</span>
                <div class="acc-btn-group">
                    <button class="acc-btn" onclick="setAccessFont('normal')">A</button>
                    <button class="acc-btn" onclick="setAccessFont('large')">A+</button>
                    <button class="acc-btn" onclick="setAccessFont('xlarge')">A++</button>
                </div>
            </div>

            <div class="acc-option">
                <span class="acc-option-title">Αντίθεση</span>
                <div class="acc-btn-group">
                    <button class="acc-btn" onclick="setAccessContrast('normal')">Κανονική</button>
                    <button class="acc-btn" onclick="setAccessContrast('high')">Υψηλή</button>
                </div>
            </div>

            <div class="acc-option">
                <span class="acc-option-title">Σύνδεσμοι</span>
                <div class="acc-btn-group">
                    <button class="acc-btn" onclick="toggleLinksHighlight(this)">Υπογράμμιση</button>
                </div>
            </div>
            
            <div class="mt-3 text-center">
                <button class="btn btn-sm btn-outline-secondary w-100" onclick="resetAccessibility()">Επαναφορά</button>
            </div>
        </div>
        <button id="accessibility-btn" aria-label="Accessibility Options">
            <i class="fas fa-universal-access"></i>
        </button>
    </div>
    `;

    document.body.insertAdjacentHTML('beforeend', widgetHTML);

    // Logic
    const btn = document.getElementById('accessibility-btn');
    const menu = document.getElementById('accessibility-menu');
    const closeBtn = document.getElementById('acc-close-btn');

    btn.addEventListener('click', () => {
        menu.classList.toggle('show');
    });

    closeBtn.addEventListener('click', () => {
        menu.classList.remove('show');
    });
});

// Helper Functions (Global)
window.setAccessFont = function(size) {
    document.documentElement.classList.remove('acc-font-large', 'acc-font-xlarge');
    if (size === 'large') document.documentElement.classList.add('acc-font-large');
    if (size === 'xlarge') document.documentElement.classList.add('acc-font-xlarge');
    saveAccessState();
};

window.setAccessContrast = function(mode) {
    document.body.classList.remove('acc-high-contrast');
    if (mode === 'high') document.body.classList.add('acc-high-contrast');
    saveAccessState();
};

window.toggleLinksHighlight = function(btn) {
    document.body.classList.toggle('acc-links-highlight');
    btn.classList.toggle('active');
    saveAccessState();
};

window.resetAccessibility = function() {
    document.documentElement.classList.remove('acc-font-large', 'acc-font-xlarge');
    document.body.classList.remove('acc-high-contrast', 'acc-links-highlight');
    
    // Reset buttons
    const btns = document.querySelectorAll('.acc-btn');
    btns.forEach(b => b.classList.remove('active'));
    
    saveAccessState();
};

function saveAccessState() {
    const state = {
        fontLarge: document.documentElement.classList.contains('acc-font-large'),
        fontXLarge: document.documentElement.classList.contains('acc-font-xlarge'),
        highContrast: document.body.classList.contains('acc-high-contrast'),
        linksHighlight: document.body.classList.contains('acc-links-highlight')
    };
    localStorage.setItem('healthAppAccessState', JSON.stringify(state));
}

function loadAccessState() {
    const saved = localStorage.getItem('healthAppAccessState');
    if (saved) {
        const state = JSON.parse(saved);
        if (state.fontLarge) document.documentElement.classList.add('acc-font-large');
        if (state.fontXLarge) document.documentElement.classList.add('acc-font-xlarge');
        if (state.highContrast) document.body.classList.add('acc-high-contrast');
        if (state.linksHighlight) {
            document.body.classList.add('acc-links-highlight');
            // Locate the button to toggle active state visually if we wanted perfectly, but functionally this is enough
        }
    }
}

// Load state on start
loadAccessState();

