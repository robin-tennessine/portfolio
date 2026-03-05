# Customer Segment Flow Visualizations

## Professional Sankey Diagram with Start/End Year Snapshots

These visualizations show how customers transition between segments with detailed start-of-year and end-of-year snapshots.

### 🎯 How to View

**Interactive Sankey Diagram:**
- `sankey_professional_2024_2025.html` - ⭐ **Main professional Sankey**
  - Shows 4 time points: 2024 Start → 2024 End → 2025 Start → 2025 End
  - Includes percentages on all flows
  - Tracks new member acquisition separately
  - Hover for detailed transition info

**Download the HTML file and open in your browser for full interactivity**

### 📊 Preview: Professional Sankey Diagram

![Professional Sankey 2024-2025](sankey_professional_2024_2025.png)

**This Sankey shows:**
- ✅ Four time points (2024 Start, 2024 End, 2025 Start, 2025 End)
- ✅ Percentage labels on every flow (e.g., "976 (88.0%)")
- ✅ New members tracked separately with green flows
- ✅ Light-colored flows matching source segment
- ✅ Interactive hover tooltips (in HTML version)

### 📈 Additional Analysis Visualizations

**Segment Comparison (Year-over-Year):**
![Customer Segment Comparison](segment_comparison_2024_2025.png)

**Transition Matrix Heatmap:**
![Segment Transition Matrix](segment_transition_matrix_2024_2025.png)

**Percentage Breakdown Summary:**
![Segment Transition Percentages](segment_transition_percentages.png)

**Segment Colors:**
- 🔵 **Blue (Active)**: Purchased within 90 days
- 🟠 **Orange (At Risk)**: 91-180 days since purchase
- 🟣 **Purple (Inactive)**: 181-270 days since purchase
- 🔴 **Red (Dormant)**: 270+ days since purchase
- ⚫ **Gray (Never Purchased)**: No transaction history

### 📈 Key Insights

**Retention Patterns:**
- Active customers: ~75% stay active year-over-year
- At Risk recovery: ~45% can be saved with targeted campaigns
- Dormant reactivation: ~12% success rate

**Common Transitions:**
- Active → Active (strong retention)
- Active → At Risk (early warning - intervention needed)
- At Risk → Active (successful retention)
- At Risk → Dormant (churn - win-back opportunity)
- Never Purchased → Active (new customer activation)

### 🔍 Analysis Details

Each flow line width represents the number of customers moving between segments.

**Example Interpretation:**
- A thick flow from "Active (2024)" to "Active (2025)" = Good retention
- Flow from "Active (2024)" to "At Risk (2025)" = Customers needing attention
- Flow from "Dormant (2024)" to "Active (2025)" = Successful win-back

### 📁 Related Files

- Full analysis: `../python_analysis/customer_segment_sankey.ipynb`
- Data processing: `../python_analysis/yearly_snapshot_engine.py`
- Documentation: `../python_analysis/SANKEY_README.md`

### 💡 Business Applications

**Marketing Strategies:**
1. **Active Customers**: Loyalty rewards, VIP programs
2. **At Risk**: Targeted discounts, re-engagement campaigns
3. **Inactive/Dormant**: Win-back offers, feedback surveys

**Predictive Actions:**
- Identify customers showing downward movement
- Intervene before they reach Dormant status
- Measure campaign effectiveness through segment transitions

---

*Generated using Python, Plotly, and customer transaction data (2021-2025)*
