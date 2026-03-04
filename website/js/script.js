// ============================================
// PROFESSIONAL PORTFOLIO - MINIMAL JAVASCRIPT
// ============================================

(function() {
    'use strict';

    // ============================================
    // SMOOTH SCROLL FOR NAVIGATION
    // ============================================
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const target = document.querySelector(targetId);

                if (target) {
                    // Make section visible immediately before scrolling
                    target.classList.add('visible');

                    // Scroll to target
                    const offsetTop = target.offsetTop - 80; // Account for fixed nav
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // ============================================
    // SCROLL ANIMATIONS REMOVED FOR RELIABILITY
    // ============================================
    // All content is visible by default for maximum reliability
    // and professional presentation

    // ============================================
    // NAVIGATION SCROLL BEHAVIOR
    // ============================================
    function initNavigationScroll() {
        const nav = document.querySelector('.nav');

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            // Add shadow on scroll
            if (currentScroll > 50) {
                nav.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
            } else {
                nav.style.boxShadow = 'none';
            }
        });
    }

    // ============================================
    // GITHUB API INTEGRATION (Optional)
    // ============================================
    async function fetchGitHubStats() {
        // Check if config is loaded
        if (typeof CONFIG === 'undefined' || !CONFIG.github.username) {
            console.log('GitHub config not found. Skipping GitHub API integration.');
            return;
        }

        const username = CONFIG.github.username;

        // Skip if placeholder value
        if (username === 'YOUR_GITHUB_USERNAME') {
            console.log('Please update your GitHub username in js/config.js');
            return;
        }

        try {
            const headers = {
                'Accept': 'application/vnd.github.v3+json'
            };

            // Add token if provided (higher rate limits)
            if (CONFIG.github.token) {
                headers['Authorization'] = `token ${CONFIG.github.token}`;
            }

            // Fetch user info
            const userResponse = await fetch(`https://api.github.com/users/${username}`, { headers });

            if (!userResponse.ok) {
                throw new Error('Failed to fetch GitHub data');
            }

            const userData = await userResponse.json();

            // Display stats in footer or create a stats section
            displayGitHubStats(userData);

        } catch (error) {
            console.error('Error fetching GitHub stats:', error);
        }
    }

    function displayGitHubStats(userData) {
        // Create or update GitHub stats display
        const footer = document.querySelector('.footer .container');

        if (!footer) return;

        const statsHTML = `
            <div class="github-stats" style="margin-bottom: 1.5rem; padding: 1rem; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; display: inline-block;">
                <p style="font-size: 0.875rem; margin: 0; color: rgba(255,255,255,0.9);">
                    <strong>${userData.public_repos}</strong> public repos •
                    <strong>${userData.followers}</strong> followers
                </p>
            </div>
        `;

        footer.insertAdjacentHTML('afterbegin', statsHTML);
    }

    // ============================================
    // UPDATE CONTACT LINKS FROM CONFIG
    // ============================================
    function updateContactLinks() {
        if (typeof CONFIG === 'undefined') return;

        const { email, linkedin, github_profile } = CONFIG.contact;

        // Update email link
        const emailLink = document.querySelector('a[href^="mailto:"]');
        if (emailLink && email) {
            emailLink.href = `mailto:${email}`;
        }

        // Update LinkedIn link
        const linkedinLink = document.querySelector('a[href*="linkedin"]');
        if (linkedinLink && linkedin) {
            linkedinLink.href = linkedin;
        }

        // Update GitHub profile links
        const githubLinks = document.querySelectorAll('a[href*="github.com/YOUR_USERNAME"]');
        if (github_profile) {
            githubLinks.forEach(link => {
                // Replace YOUR_USERNAME with actual username in all GitHub links
                link.href = link.href.replace('YOUR_USERNAME', CONFIG.github.username);
            });
        }
    }

    // ============================================
    // ANALYTICS (Optional)
    // ============================================
    function initAnalytics() {
        if (typeof CONFIG === 'undefined' || !CONFIG.analytics.trackingId) {
            return;
        }

        const trackingId = CONFIG.analytics.trackingId;

        if (trackingId && trackingId !== 'G-XXXXXXXXXX') {
            // Load Google Analytics
            const script = document.createElement('script');
            script.async = true;
            script.src = `https://www.googletagmanager.com/gtag/js?id=${trackingId}`;
            document.head.appendChild(script);

            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', trackingId);
        }
    }

    // ============================================
    // INITIALIZE ALL
    // ============================================
    function init() {
        console.log('Portfolio initialized');

        // Core functionality
        initSmoothScroll();
        initNavigationScroll();

        // Optional features (require config.js)
        updateContactLinks();
        fetchGitHubStats();
        initAnalytics();
    }

    // Wait for DOM and config to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
