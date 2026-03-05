"""Create percentage breakdown summary table"""

import pandas as pd
import matplotlib.pyplot as plt
from professional_sankey import ProfessionalSankeyBuilder

# Load transitions
builder = ProfessionalSankeyBuilder('../data/snapshots_start_end.csv')
transitions = builder.build_transitions(2024, 2025)

# Create summary figure
fig = plt.figure(figsize=(18, 12))
fig.suptitle('Customer Segment Transition Breakdown - % Movement Analysis\n2024-2025',
             fontsize=20, fontweight='bold')

# Create text summary with proper formatting
summary_text = []

# === 2024 START → 2024 END ===
summary_text.append("="*80)
summary_text.append("2024 START → 2024 END (Within-Year Transitions)")
summary_text.append("="*80)

trans_2024 = transitions[
    transitions['Source'].str.contains('2024 Start') &
    transitions['Target'].str.contains('2024 End')
]

for source in sorted(trans_2024['Source'].unique()):
    source_name = source.replace(' (2024 Start)', '')
    source_flows = trans_2024[trans_2024['Source'] == source]
    total = source_flows['Count'].sum()

    summary_text.append(f"\n{source_name}: {total:,} members")
    for _, flow in source_flows.sort_values('Percentage', ascending=False).iterrows():
        target_name = flow['Target'].replace(' (2024 End)', '')
        pct = flow['Percentage']
        count = flow['Count']
        bar = '█' * int(pct / 5)  # Visual bar
        summary_text.append(f"  → {target_name:20s} {pct:5.1f}% ({count:5,})  {bar}")

# === 2024 END → 2025 START ===
summary_text.append("\n" + "="*80)
summary_text.append("2024 END → 2025 START (Year Transition + New Members)")
summary_text.append("="*80)

trans_year = transitions[
    transitions['Source'].str.contains('2024 End') &
    transitions['Target'].str.contains('2025 Start')
]

for source in sorted(trans_year['Source'].unique()):
    source_name = source.replace(' (2024 End)', '')
    source_flows = trans_year[trans_year['Source'] == source]
    total = source_flows['Count'].sum()

    summary_text.append(f"\n{source_name}: {total:,} members")
    for _, flow in source_flows.sort_values('Percentage', ascending=False).iterrows():
        target_name = flow['Target'].replace(' (2025 Start)', '')
        pct = flow['Percentage']
        count = flow['Count']
        bar = '█' * int(pct / 5)
        summary_text.append(f"  → {target_name:20s} {pct:5.1f}% ({count:5,})  {bar}")

# New members
new_members = transitions[transitions['Source'].str.contains('New Members')]
if len(new_members) > 0:
    total_new = new_members['Count'].sum()
    summary_text.append(f"\nNew Members (2025): {total_new:,} members")
    for _, flow in new_members.iterrows():
        target_name = flow['Target'].replace(' (2025 Start)', '')
        count = flow['Count']
        summary_text.append(f"  → {target_name:20s} ALL NEW  ({count:5,})")

# === 2025 START → 2025 END ===
summary_text.append("\n" + "="*80)
summary_text.append("2025 START → 2025 END (Within-Year Transitions)")
summary_text.append("="*80)

trans_2025 = transitions[
    transitions['Source'].str.contains('2025 Start') &
    transitions['Target'].str.contains('2025 End')
]

for source in sorted(trans_2025['Source'].unique()):
    source_name = source.replace(' (2025 Start)', '')
    source_flows = trans_2025[trans_2025['Source'] == source]
    total = source_flows['Count'].sum()

    summary_text.append(f"\n{source_name}: {total:,} members")
    for _, flow in source_flows.sort_values('Percentage', ascending=False).iterrows():
        target_name = flow['Target'].replace(' (2025 End)', '')
        pct = flow['Percentage']
        count = flow['Count']
        bar = '█' * int(pct / 5)
        summary_text.append(f"  → {target_name:20s} {pct:5.1f}% ({count:5,})  {bar}")

# Display as text on figure
ax = fig.add_subplot(111)
ax.axis('off')

full_text = '\n'.join(summary_text)
ax.text(0.05, 0.95, full_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('../visualizations/segment_transition_percentages.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print('✓ Saved: segment_transition_percentages.png')
print('\nThis shows EXACTLY what % of each segment moved where!')
