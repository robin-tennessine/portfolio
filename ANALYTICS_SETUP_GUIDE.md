# Website Analytics Setup Guide
## Track Visitors & Resume Downloads

## Option 1: Google Analytics 4 (Recommended)

### Step 1: Create Google Analytics Account

1. **Go to Google Analytics:**
   ```
   https://analytics.google.com
   ```

2. **Sign in with Google account**

3. **Create Account:**
   - Click "Start measuring"
   - Account name: "Portfolio"
   - Click "Next"

4. **Create Property:**
   - Property name: "Robin Portfolio Website"
   - Time zone: Your timezone
   - Currency: THB (Thai Baht)
   - Click "Next"

5. **Business Details:**
   - Industry: "Professional Services"
   - Business size: "Small"
   - Click "Next"

6. **Choose "Web" platform**

7. **Set up data stream:**
   - Website URL: `https://robin-tennessine.github.io`
   - Stream name: "Portfolio Website"
   - Click "Create stream"

8. **Copy your Measurement ID** (looks like: G-XXXXXXXXXX)

### Step 2: Add Tracking Code to Website

I'll help you add this automatically, but here's what you'll paste:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Replace `G-XXXXXXXXXX` with your actual Measurement ID.

### Step 3: Track Resume Downloads

Add this event tracking to your resume button:

```javascript
// Track resume download
document.querySelectorAll('a[download]').forEach(button => {
    button.addEventListener('click', function() {
        gtag('event', 'resume_download', {
            'event_category': 'engagement',
            'event_label': 'Resume PDF'
        });
    });
});
```

### Step 4: What You Can Track

**Automatic Metrics:**
- Total page views
- Unique visitors
- Average session duration
- Bounce rate
- Traffic sources (LinkedIn, Google, direct)
- Geographic location
- Device type (mobile, desktop)
- Browser used

**Custom Events You'll Track:**
- Resume downloads
- Contact link clicks
- Project link clicks
- Social media clicks

### Step 5: View Your Data

1. Go to: https://analytics.google.com
2. Navigate to: Reports → Engagement → Events
3. See "resume_download" event count
4. Real-time data: Reports → Realtime

---

## Option 2: Microsoft Clarity (Free Heatmaps)

Great for seeing HOW users interact with your site.

### Setup:

1. **Go to:** https://clarity.microsoft.com
2. **Sign in** with Microsoft account
3. **Create Project:**
   - Name: "Portfolio"
   - Website: `https://robin-tennessine.github.io/portfolio/website/`
4. **Copy tracking code**
5. **Paste in your website `<head>`**

### What You Get:
- Session recordings (watch visitors use your site)
- Heatmaps (see where people click)
- Scroll depth
- Rage clicks (frustrated users)

---

## Option 3: Simple Analytics (Privacy-Focused, Paid)

If you care about visitor privacy and GDPR compliance.

- Cost: $9/month
- No cookies needed
- Privacy-friendly
- Simple dashboard

---

## Quick Setup Script

Once you have your Google Analytics ID, tell me and I'll update your website automatically!

**You'll need:**
1. Your GA4 Measurement ID (G-XXXXXXXXXX)
2. I'll add it to your website
3. Push to GitHub
4. Analytics will start tracking immediately!

---

## What Your Analytics Dashboard Will Show:

### Daily Stats:
```
📊 Today's Traffic:
- Visitors: 15
- Resume Downloads: 3
- Most viewed: Projects section
- Top referrer: LinkedIn

📈 This Week:
- Total visitors: 87
- Resume downloads: 12
- Conversion rate: 13.8%
- Peak day: Tuesday (23 visitors)
```

### Visitor Journey:
```
1. Visitor lands on homepage (from LinkedIn)
2. Scrolls to Projects section
3. Clicks "View Project" link
4. Returns to homepage
5. Downloads resume
6. Clicks LinkedIn contact
```

### Geographic Data:
```
🌍 Visitor Locations:
- Thailand: 45%
- United States: 30%
- Singapore: 15%
- Other: 10%
```

---

## Privacy Note

Add privacy notice to your footer:

```html
<p class="privacy-note">
    This site uses Google Analytics to track anonymous usage data.
</p>
```

---

## Next Steps:

1. ✅ Read this guide
2. ⏳ Create Google Analytics account
3. ⏳ Get your Measurement ID (G-XXXXXXXXXX)
4. ⏳ Tell me your ID, and I'll add it to your website
5. ✅ Start tracking visitors and downloads!

---

## FAQ

**Q: How long before I see data?**
A: Real-time data shows immediately. Full reports take 24-48 hours.

**Q: Can I see who downloaded my resume?**
A: No, Analytics is anonymous. You'll see counts, not names.

**Q: Will this slow down my website?**
A: No, Google Analytics loads asynchronously.

**Q: Is it free forever?**
A: Yes, Google Analytics is 100% free.

**Q: Can I track specific recruiters?**
A: Not by name, but you can see if traffic comes from LinkedIn, company websites, etc.

---

Ready to set this up? Just create your Google Analytics account and give me your Measurement ID!
