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
    // EXPORT PORTFOLIO FUNCTION
    // ============================================
    window.exportPortfolio = function() {
        // Create portfolio summary text
        const portfolioData = `
ROBIN PHONPAKDEE - DATA ANALYST PORTFOLIO
========================================

CONTACT INFORMATION
-------------------
Email: robint.phonpakdee@gmail.com
LinkedIn: https://www.linkedin.com/in/robin-phonpakdee-4a4782251
GitHub: https://github.com/robin-tennessine

PROFESSIONAL SUMMARY
--------------------
Junior Data Analyst with one year of experience in retail analytics and business intelligence.
Currently working at Cube Analytics Consulting for Jaymart Holding, specializing in SQL, Python,
and Power BI for data-driven decision making.

TECHNICAL SKILLS
----------------
• SQL (PostgreSQL, MySQL)
• Python (pandas, scikit-learn, matplotlib)
• Power BI (DAX, Power Query)
• Flask API Development
• ETL & Data Pipelines
• RapidMiner
• Excel & Data Visualization

ANALYSIS EXPERTISE
------------------
• Customer Segmentation
• Trend Analysis
• KPI Reporting
• Statistical Analysis
• Machine Learning (K-means)
• Business Intelligence

EXPERIENCE
----------
Junior Data Analyst (2024 — Present)
Cube Analytics Consulting → Jaymart Holding
Bangkok, Thailand

• Design and develop interactive dashboards and reports using Power BI
• Perform customer segmentation analysis to identify high-value segments
• Build ETL pipelines using RapidMiner to automate data processing workflows
• Conduct ad-hoc analysis to support business initiatives
• Collaborate with cross-functional teams to translate business requirements

FEATURED PROJECTS
-----------------
1. Advanced SQL Analytics - PostgreSQL window functions, CTEs, and time-series analysis
2. Python Data Analytics - Machine learning, customer segmentation, and RFM analysis
3. ETL Data Pipeline - Production-ready pipeline with data validation and quality checks
4. Power BI Solutions - 60+ DAX measures and advanced data modeling
5. Flask API Export Service - PDPA-compliant API with data masking and security
6. Customer Segment Flow - Sankey visualization for customer journey analysis

========================================
Generated: ${new Date().toLocaleDateString()}
Visit: https://github.com/robin-tennessine/portfolio
`;

        // Create and download the file
        const blob = new Blob([portfolioData], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Robin_Phonpakdee_Portfolio_Summary.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        console.log('Portfolio exported successfully!');
    };

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
