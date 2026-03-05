"""
Enhanced Yearly Snapshot Engine - Start & End of Year
Creates snapshots at both start and end of each year for Sankey visualization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class EnhancedSnapshotEngine:
    """
    Create start-of-year and end-of-year snapshots for customer segmentation.
    Tracks new member acquisition and segment transitions within years.
    """

    def __init__(self, member_master_path, member_yearly_path):
        """Initialize with data paths"""
        self.member_master = pd.read_csv(member_master_path)
        self.member_yearly = pd.read_csv(member_yearly_path)

        # Convert dates
        self.member_yearly['MaxSaleDate'] = pd.to_datetime(self.member_yearly['MaxSaleDate'])
        self.member_master['FirstPurchaseDate'] = pd.to_datetime(self.member_master['FirstPurchaseDate'])

        # Get max date and year
        self.max_date = self.member_yearly['MaxSaleDate'].max()
        self.max_year = self.max_date.year

    def calculate_recency_segment(self, lap_days):
        """Categorize LAP into segment"""
        if pd.isna(lap_days):
            return "Never Purchased"
        elif lap_days <= 90:
            return "Active"
        elif lap_days <= 180:
            return "At Risk"
        elif lap_days <= 270:
            return "Inactive"
        else:
            return "Dormant"

    def get_member_status_at_date(self, member_id, reference_date):
        """
        Get member's recency status at a specific date.

        Parameters:
        -----------
        member_id : str
            Member ID
        reference_date : datetime
            Date to check status

        Returns:
        --------
        dict with segment, LAP_days, last_txn_date
        """
        # Get all transactions up to reference date
        member_txns = self.member_yearly[
            (self.member_yearly['Member_ID'] == member_id) &
            (self.member_yearly['MaxSaleDate'] <= reference_date)
        ]

        if len(member_txns) == 0:
            # No purchase before reference date
            return {
                'Segment': 'Never Purchased',
                'LAP_Days': np.nan,
                'Last_Txn_Date': pd.NaT,
                'Total_Txns': 0,
                'Total_Spend': 0
            }
        else:
            # Calculate LAP from last transaction to reference date
            last_txn_date = member_txns['MaxSaleDate'].max()
            lap_days = (reference_date - last_txn_date).days
            segment = self.calculate_recency_segment(lap_days)

            return {
                'Segment': segment,
                'LAP_Days': lap_days,
                'Last_Txn_Date': last_txn_date,
                'Total_Txns': member_txns['TotalTxn'].sum(),
                'Total_Spend': member_txns['TotalSpend'].sum()
            }

    def create_start_end_snapshots(self):
        """
        Create snapshots at start and end of each year.

        Returns:
        --------
        pd.DataFrame with columns:
            - Member_ID
            - Year
            - Snapshot_Type (Start/End)
            - Snapshot_Date
            - Segment
            - LAP_Days
            - Is_New_Member (True if first purchase in this year)
        """
        years = sorted([int(y) for y in self.member_yearly['YEAR'].unique()])
        all_members = self.member_master['Member_ID'].unique()

        snapshots = []

        for year in years:
            print(f"Processing year {year}...")

            # Start of year date (Jan 1)
            start_date = datetime(year, 1, 1)

            # End of year date (Dec 31 or max_date if current year)
            if year == self.max_year:
                end_date = self.max_date
            else:
                end_date = datetime(year, 12, 31)

            # For each member, calculate status at start and end
            for member_id in all_members:
                # Get first purchase date for this member
                first_purchase = self.member_master[
                    self.member_master['Member_ID'] == member_id
                ]['FirstPurchaseDate'].iloc[0]

                # === START OF YEAR SNAPSHOT ===
                start_status = self.get_member_status_at_date(member_id, start_date)

                # Check if this is a new member (first purchase in this year)
                is_new_at_start = (first_purchase.year == year) and (first_purchase < start_date)

                snapshots.append({
                    'Member_ID': member_id,
                    'Year': year,
                    'Snapshot_Type': 'Start',
                    'Snapshot_Date': start_date,
                    'Segment': start_status['Segment'],
                    'LAP_Days': start_status['LAP_Days'],
                    'Total_Txns': start_status['Total_Txns'],
                    'Total_Spend': start_status['Total_Spend'],
                    'Is_New_Member': is_new_at_start
                })

                # === END OF YEAR SNAPSHOT ===
                end_status = self.get_member_status_at_date(member_id, end_date)

                # Check if member joined during the year
                is_new_at_end = (first_purchase.year == year) and (first_purchase <= end_date)

                snapshots.append({
                    'Member_ID': member_id,
                    'Year': year,
                    'Snapshot_Type': 'End',
                    'Snapshot_Date': end_date,
                    'Segment': end_status['Segment'],
                    'LAP_Days': end_status['LAP_Days'],
                    'Total_Txns': end_status['Total_Txns'],
                    'Total_Spend': end_status['Total_Spend'],
                    'Is_New_Member': is_new_at_end and not is_new_at_start
                })

        snapshot_df = pd.DataFrame(snapshots)

        # Add demographics
        snapshot_df = snapshot_df.merge(
            self.member_master[['Member_ID', 'FIRST_NAME', 'LAST_NAME',
                               'GENDER', 'Age_Range', 'Generation']],
            on='Member_ID',
            how='left'
        )

        return snapshot_df


def main():
    """Generate start/end snapshots"""

    print("="*70)
    print("ENHANCED SNAPSHOT ENGINE - START & END OF YEAR")
    print("="*70)

    # Initialize
    engine = EnhancedSnapshotEngine(
        member_master_path='../data/member_master.csv',
        member_yearly_path='../data/member_segment_yearly.csv'
    )

    # Create snapshots
    snapshots = engine.create_start_end_snapshots()

    # Save
    output_path = '../data/snapshots_start_end.csv'
    snapshots.to_csv(output_path, index=False)
    print(f"\n✓ Saved: {output_path}")

    # Display summary
    print("\n" + "="*70)
    print("SNAPSHOT SUMMARY")
    print("="*70)

    print(f"\nTotal records: {len(snapshots):,}")
    print(f"Unique members: {snapshots['Member_ID'].nunique():,}")
    print(f"Years covered: {sorted(snapshots['Year'].unique())}")

    print("\n" + "-"*70)
    print("SEGMENT DISTRIBUTION BY SNAPSHOT TYPE")
    print("-"*70)

    summary = snapshots.groupby(['Year', 'Snapshot_Type', 'Segment']).size().unstack(fill_value=0)
    print(summary)

    print("\n" + "-"*70)
    print("NEW MEMBER ACQUISITION")
    print("-"*70)

    new_members = snapshots[snapshots['Is_New_Member'] == True].groupby(['Year', 'Snapshot_Type']).size()
    print(new_members)

    print("\n" + "-"*70)
    print("SAMPLE RECORDS")
    print("-"*70)
    print(snapshots[snapshots['Year'] == 2024].head(10))

    return snapshots


if __name__ == '__main__':
    main()
