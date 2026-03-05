"""
Professional Sankey Visualization with Start/End Year Snapshots
Shows member segment flow with percentages, like sankeyart.com style
"""

import pandas as pd
import plotly.graph_objects as go
import numpy as np


class ProfessionalSankeyBuilder:
    """Build professional Sankey diagrams with percentages and new member tracking"""

    def __init__(self, snapshots_path):
        """Load snapshot data"""
        self.snapshots = pd.read_csv(snapshots_path)
        self.snapshots['Snapshot_Date'] = pd.to_datetime(self.snapshots['Snapshot_Date'])

    def build_transitions(self, year1, year2):
        """
        Build transition data between two years (Start → End → Start → End).

        Creates flows:
        - Year1 Start → Year1 End
        - Year1 End → Year2 Start (accounting for new members)
        - Year2 Start → Year2 End

        Returns:
        --------
        dict with source, target, value, percentage, labels
        """
        # Get snapshots for both years
        year1_start = self.snapshots[
            (self.snapshots['Year'] == year1) &
            (self.snapshots['Snapshot_Type'] == 'Start')
        ][['Member_ID', 'Segment', 'Is_New_Member']].copy()

        year1_end = self.snapshots[
            (self.snapshots['Year'] == year1) &
            (self.snapshots['Snapshot_Type'] == 'End')
        ][['Member_ID', 'Segment', 'Is_New_Member']].copy()

        year2_start = self.snapshots[
            (self.snapshots['Year'] == year2) &
            (self.snapshots['Snapshot_Type'] == 'Start')
        ][['Member_ID', 'Segment', 'Is_New_Member']].copy()

        year2_end = self.snapshots[
            (self.snapshots['Year'] == year2) &
            (self.snapshots['Snapshot_Type'] == 'End')
        ][['Member_ID', 'Segment', 'Is_New_Member']].copy()

        # Rename columns for merging
        year1_start.columns = ['Member_ID', 'Segment_Y1_Start', 'Is_New_Y1_Start']
        year1_end.columns = ['Member_ID', 'Segment_Y1_End', 'Is_New_Y1_End']
        year2_start.columns = ['Member_ID', 'Segment_Y2_Start', 'Is_New_Y2_Start']
        year2_end.columns = ['Member_ID', 'Segment_Y2_End', 'Is_New_Y2_End']

        # Merge all snapshots
        flows = year1_start.merge(year1_end, on='Member_ID', how='outer')
        flows = flows.merge(year2_start, on='Member_ID', how='outer')
        flows = flows.merge(year2_end, on='Member_ID', how='outer')

        # Build transition list
        transitions = []

        # === TRANSITION 1: Year1 Start → Year1 End ===
        trans1 = flows[['Member_ID', 'Segment_Y1_Start', 'Segment_Y1_End']].dropna()
        trans1_counts = trans1.groupby(['Segment_Y1_Start', 'Segment_Y1_End']).size().reset_index(name='Count')

        for _, row in trans1_counts.iterrows():
            source = f"{row['Segment_Y1_Start']} ({year1} Start)"
            target = f"{row['Segment_Y1_End']} ({year1} End)"
            count = row['Count']

            # Calculate percentage of source
            source_total = trans1[trans1['Segment_Y1_Start'] == row['Segment_Y1_Start']].shape[0]
            pct = (count / source_total * 100) if source_total > 0 else 0

            transitions.append({
                'Source': source,
                'Target': target,
                'Count': count,
                'Percentage': pct,
                'Label': f"{count:,} ({pct:.1f}%)"
            })

        # === TRANSITION 2: Year1 End → Year2 Start ===
        # Existing members carry forward, new members appear
        trans2 = flows[['Member_ID', 'Segment_Y1_End', 'Segment_Y2_Start', 'Is_New_Y2_Start']].copy()
        trans2 = trans2.dropna(subset=['Segment_Y2_Start'])

        # Separate existing vs new members
        existing_members = trans2[trans2['Is_New_Y2_Start'] == False]
        new_members = trans2[trans2['Is_New_Y2_Start'] == True]

        # Existing members transition
        if len(existing_members) > 0:
            existing_members = existing_members.dropna(subset=['Segment_Y1_End'])
            trans2_counts = existing_members.groupby(['Segment_Y1_End', 'Segment_Y2_Start']).size().reset_index(name='Count')

            for _, row in trans2_counts.iterrows():
                source = f"{row['Segment_Y1_End']} ({year1} End)"
                target = f"{row['Segment_Y2_Start']} ({year2} Start)"
                count = row['Count']

                # Calculate percentage
                source_total = existing_members[existing_members['Segment_Y1_End'] == row['Segment_Y1_End']].shape[0]
                pct = (count / source_total * 100) if source_total > 0 else 0

                transitions.append({
                    'Source': source,
                    'Target': target,
                    'Count': count,
                    'Percentage': pct,
                    'Label': f"{count:,} ({pct:.1f}%)"
                })

        # New members appear
        if len(new_members) > 0:
            new_counts = new_members.groupby('Segment_Y2_Start').size().reset_index(name='Count')

            for _, row in new_counts.iterrows():
                source = f"New Members ({year2})"
                target = f"{row['Segment_Y2_Start']} ({year2} Start)"
                count = row['Count']

                transitions.append({
                    'Source': source,
                    'Target': target,
                    'Count': count,
                    'Percentage': 100.0,  # All new members
                    'Label': f"{count:,} (100%)"
                })

        # === TRANSITION 3: Year2 Start → Year2 End ===
        trans3 = flows[['Member_ID', 'Segment_Y2_Start', 'Segment_Y2_End']].dropna()
        trans3_counts = trans3.groupby(['Segment_Y2_Start', 'Segment_Y2_End']).size().reset_index(name='Count')

        for _, row in trans3_counts.iterrows():
            source = f"{row['Segment_Y2_Start']} ({year2} Start)"
            target = f"{row['Segment_Y2_End']} ({year2} End)"
            count = row['Count']

            # Calculate percentage
            source_total = trans3[trans3['Segment_Y2_Start'] == row['Segment_Y2_Start']].shape[0]
            pct = (count / source_total * 100) if source_total > 0 else 0

            transitions.append({
                'Source': source,
                'Target': target,
                'Count': count,
                'Percentage': pct,
                'Label': f"{count:,} ({pct:.1f}%)"
            })

        return pd.DataFrame(transitions)

    def create_sankey(self, year1, year2, show_percentages=True):
        """
        Create professional Sankey diagram.

        Parameters:
        -----------
        year1, year2 : int
            Years to compare
        show_percentages : bool
            Show percentage labels on flows

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        # Get transitions
        transitions_df = self.build_transitions(year1, year2)

        # Get unique nodes
        nodes = list(set(transitions_df['Source'].tolist() + transitions_df['Target'].tolist()))
        node_dict = {node: idx for idx, node in enumerate(nodes)}

        # Map to indices
        transitions_df['Source_idx'] = transitions_df['Source'].map(node_dict)
        transitions_df['Target_idx'] = transitions_df['Target'].map(node_dict)

        # Define colors by segment type
        segment_colors = {
            'Active': 'rgba(46, 134, 171, 0.8)',      # Blue
            'At Risk': 'rgba(241, 143, 1, 0.8)',      # Orange
            'Inactive': 'rgba(162, 59, 114, 0.8)',     # Purple
            'Dormant': 'rgba(199, 62, 29, 0.8)',       # Red
            'Never Purchased': 'rgba(108, 117, 125, 0.8)',  # Gray
            'New Members': 'rgba(40, 167, 69, 0.8)'    # Green
        }

        # Assign colors to nodes
        node_colors = []
        for node in nodes:
            # Extract segment name
            if 'New Members' in node:
                segment_name = 'New Members'
            else:
                segment_name = node.split(' (')[0]
            node_colors.append(segment_colors.get(segment_name, 'rgba(128, 128, 128, 0.8)'))

        # Create node labels with counts
        node_labels = []
        for node in nodes:
            # Calculate total count for this node
            incoming = transitions_df[transitions_df['Target'] == node]['Count'].sum()
            outgoing = transitions_df[transitions_df['Source'] == node]['Count'].sum()
            node_count = max(incoming, outgoing)

            # Calculate percentage of total members
            total_members = 2000  # Update based on your data
            node_pct = (node_count / total_members * 100)

            node_labels.append(f"{node}<br>{node_count:,} ({node_pct:.1f}%)")

        # Create link labels with customdata for hover
        link_labels = transitions_df['Label'].tolist() if show_percentages else None

        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            arrangement='snap',
            node=dict(
                pad=20,
                thickness=25,
                line=dict(color='black', width=1.5),
                label=node_labels,
                color=node_colors,
                customdata=nodes,
                hovertemplate='%{customdata}<br>%{value:,} members<extra></extra>'
            ),
            link=dict(
                source=transitions_df['Source_idx'],
                target=transitions_df['Target_idx'],
                value=transitions_df['Count'],
                label=link_labels,
                color='rgba(200, 200, 200, 0.3)',
                customdata=transitions_df[['Source', 'Target', 'Count', 'Percentage']].values,
                hovertemplate='%{customdata[0]} → %{customdata[1]}<br>' +
                             '%{customdata[2]:,} members (%{customdata[3]:.1f}%)<extra></extra>'
            )
        )])

        # Update layout
        fig.update_layout(
            title=dict(
                text=f"Customer Segment Flow Analysis: {year1}-{year2}<br>" +
                     f"<sub>Showing segment transitions from start to end of each year with new member acquisition</sub>",
                font=dict(size=20, family='Arial, sans-serif', color='#333'),
                x=0.5,
                xanchor='center'
            ),
            font=dict(size=11, family='Arial, sans-serif'),
            height=800,
            width=1600,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=50, r=50, t=100, b=50)
        )

        return fig


def main():
    """Generate professional Sankey diagrams"""

    print("="*70)
    print("PROFESSIONAL SANKEY VISUALIZATION")
    print("="*70)

    # Initialize
    builder = ProfessionalSankeyBuilder('../data/snapshots_start_end.csv')

    # Create 2024-2025 Sankey
    print("\nCreating 2024-2025 Sankey with start/end snapshots...")
    fig = builder.create_sankey(2024, 2025, show_percentages=True)

    # Save as HTML
    html_path = '../visualizations/sankey_professional_2024_2025.html'
    fig.write_html(html_path)
    print(f"✓ Saved: {html_path}")

    # Save as PNG
    try:
        png_path = '../visualizations/sankey_professional_2024_2025.png'
        fig.write_image(png_path, width=1600, height=800, scale=2)
        print(f"✓ Saved: {png_path}")
    except Exception as e:
        print(f"⚠ Could not save PNG (kaleido required): {e}")

    # Display transition summary
    print("\n" + "="*70)
    print("TRANSITION SUMMARY")
    print("="*70)

    transitions = builder.build_transitions(2024, 2025)
    print(f"\nTotal flows: {len(transitions)}")
    print("\nTop 10 largest transitions:")
    print(transitions.nlargest(10, 'Count')[['Source', 'Target', 'Count', 'Percentage']])

    print("\n✅ Professional Sankey created! Open the HTML file to view.")


if __name__ == '__main__':
    main()
