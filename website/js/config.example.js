// ============================================
// CONFIGURATION TEMPLATE
// ============================================
// Copy this file to config.js and fill in your actual credentials
// config.js is gitignored and will not be committed to GitHub

const CONFIG = {
    // Your GitHub username
    github: {
        username: 'YOUR_GITHUB_USERNAME',
        // Optional: Personal Access Token for higher API rate limits
        // Leave empty for public repositories (60 requests/hour limit)
        token: ''
    },

    // Your contact information
    contact: {
        email: 'your.email@example.com',
        linkedin: 'https://linkedin.com/in/YOUR_PROFILE',
        github_profile: 'https://github.com/YOUR_USERNAME'
    },

    // Optional: Google Analytics tracking ID
    analytics: {
        trackingId: '' // e.g., 'G-XXXXXXXXXX'
    }
};

// Do not modify below this line
if (typeof window !== 'undefined') {
    window.CONFIG = CONFIG;
}
