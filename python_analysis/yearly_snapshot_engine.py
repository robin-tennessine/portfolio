"""
Yearly Snapshot Engine - Python implementation of Power BI DAX YearlySnapshot
Replicates the DAX ADDCOLUMNS logic for customer segment analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class YearlySnapshotEngine:
    """
    Engine to create yearly customer snapshots with RFM metrics and segmentation.
    Replicates Power BI DAX YearlySnapshot calculation.
    """

    def __init__(self, member_master_path, member_yearly_path):
        """
        Initialize the engine with data paths

        Parameters:
        -----------
        member_master_path : str
            Path to member master data CSV
        member_yearly_path : str
            Path to member yearly transaction data CSV
        """
        self.member_master = pd.read_csv(member_master_path)
        self.member_yearly = pd.read_csv(member_yearly_path)

        # Convert date columns
        self.member_yearly['MaxSaleDate'] = pd.to_datetime(self.member_yearly['MaxSaleDate'])
        self.member_master['FirstPurchaseDate'] = pd.to_datetime(self.member_master['FirstPurchaseDate'])

        # Get max date across all data
        self.max_date = self.member_yearly['MaxSaleDate'].max()
        self.max_year = self.max_date.year

    def create_year_table(self):
        """
        Create YearTable - all combinations of members and years they could be active

        Returns:
        --------
        pd.DataFrame
            DataFrame with Member_ID and YEAR combinations
        """
        # Get unique members
        members = self.member_master['Member_ID'].unique()

        # Get year range
        years = sorted(self.member_yearly['YEAR'].unique())

        # Create all combinations
        year_table = pd.DataFrame([
            {'Member_ID': member, 'YEAR': year}
            for member in members
            for year in years
        ])

        return year_table

    def calculate_year_end_date(self, year):
        """
        Calculate Year_End date (Dec 31 or max_date for current year)

        Parameters:
        -----------
        year : int or str
            Year to calculate end date for

        Returns:
        --------
        datetime
            Year end date
        """
        year = int(year) if isinstance(year, str) else year

        if year == self.max_year:
            return self.max_date
        else:
            return datetime(year, 12, 31)

    def calculate_point_range(self, points):
        """
        Categorize total points into ranges

        Parameters:
        -----------
        points : float
            Total loyalty points

        Returns:
        --------
        str
            Point range category
        """
        if pd.isna(points):
            return "No Points"
        elif points == 0:
            return "0 Points"
        elif points <= 50:
            return "1-50"
        elif points <= 100:
            return "51-100"
        elif points <= 200:
            return "101-200"
        elif points <= 500:
            return "201-500"
        elif points <= 1000:
            return "501-1,000"
        elif points <= 2000:
            return "1,001-2,000"
        elif points <= 5000:
            return "2,001-5,000"
        else:
            return "5,001+"

    def calculate_lap_days(self, year_end, cumulative_last_txn):
        """
        Calculate Last Activity Period (LAP) in days

        Parameters:
        -----------
        year_end : datetime
            End date of the year
        cumulative_last_txn : datetime
            Date of last transaction up to this year

        Returns:
        --------
        int
            Days since last activity
        """
        if pd.isna(cumulative_last_txn):
            return np.nan

        return (year_end - cumulative_last_txn).days

    def calculate_recency_text(self, lap_days):
        """
        Categorize recency into text segments

        Parameters:
        -----------
        lap_days : float
            Days since last activity

        Returns:
        --------
        str
            Recency segment
        """
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

    def build_yearly_snapshot(self):
        """
        Build the complete yearly snapshot with all metrics.
        Replicates Power BI DAX YearlySnapshot calculation.

        Returns:
        --------
        pd.DataFrame
            Complete yearly snapshot with all calculated columns
        """
        print("Building Yearly Snapshot...")

        # Step 1: Create Year Table
        year_table = self.create_year_table()
        print(f"Created year table: {len(year_table):,} rows")

        # Step 2: Add columns from member_yearly (ADDCOLUMNS logic)
        print("Adding transaction metrics...")

        # Merge with yearly transaction data
        snapshot = year_table.merge(
            self.member_yearly,
            on=['Member_ID', 'YEAR'],
            how='left'
        )

        # Fill missing transaction data with 0
        snapshot['TotalTxn'] = snapshot['TotalTxn'].fillna(0)
        snapshot['TotalSpend'] = snapshot['TotalSpend'].fillna(0)
        snapshot['TotalQty'] = snapshot['TotalQty'].fillna(0)

        # Step 3: Add member master data (demographics)
        print("Adding member demographics...")
        snapshot = snapshot.merge(
            self.member_master[[
                'Member_ID', 'FIRST_NAME', 'LAST_NAME', 'GENDER',
                'Age_Range', 'Generation', 'UUID', 'MOBILE_NO',
                'Total_point', 'FirstPurchaseDate', 'BIRTHDATE'
            ]],
            on='Member_ID',
            how='left'
        )

        # Step 4: Calculate Year_End
        print("Calculating year end dates...")
        snapshot['Year_End'] = snapshot['YEAR'].apply(self.calculate_year_end_date)

        # Step 5: Calculate Cumulative metrics
        print("Calculating cumulative metrics...")

        # Sort by Member and Year for cumulative calculations
        snapshot = snapshot.sort_values(['Member_ID', 'YEAR'])

        # Cumulative_TotalTxn: Sum of all transactions up to year end
        cumulative_txn = []
        for member_id in snapshot['Member_ID'].unique():
            member_data = self.member_yearly[self.member_yearly['Member_ID'] == member_id].copy()

            for year in snapshot[snapshot['Member_ID'] == member_id]['YEAR'].values:
                year_end = self.calculate_year_end_date(year)

                # Sum all transactions up to year end
                cum_txn = member_data[
                    member_data['MaxSaleDate'] <= year_end
                ]['TotalTxn'].sum()

                cumulative_txn.append({
                    'Member_ID': member_id,
                    'YEAR': year,
                    'Cumulative_TotalTxn': cum_txn
                })

        cumulative_df = pd.DataFrame(cumulative_txn)
        snapshot = snapshot.merge(cumulative_df, on=['Member_ID', 'YEAR'], how='left')

        # Active_Years_Count: Count of distinct years with transactions up to year end
        active_years = []
        for member_id in snapshot['Member_ID'].unique():
            member_data = self.member_yearly[self.member_yearly['Member_ID'] == member_id].copy()

            for year in snapshot[snapshot['Member_ID'] == member_id]['YEAR'].values:
                year_end = self.calculate_year_end_date(year)

                # Count distinct years up to year end
                years_count = member_data[
                    member_data['MaxSaleDate'] <= year_end
                ]['YEAR'].nunique()

                active_years.append({
                    'Member_ID': member_id,
                    'YEAR': year,
                    'Active_Years_Count': years_count
                })

        active_years_df = pd.DataFrame(active_years)
        snapshot = snapshot.merge(active_years_df, on=['Member_ID', 'YEAR'], how='left')

        # Cumulative_Last_Txn: Most recent transaction date up to year end
        last_txn = []
        for member_id in snapshot['Member_ID'].unique():
            member_data = self.member_yearly[self.member_yearly['Member_ID'] == member_id].copy()

            for year in snapshot[snapshot['Member_ID'] == member_id]['YEAR'].values:
                year_end = self.calculate_year_end_date(year)

                # Get max date up to year end
                eligible_txns = member_data[member_data['MaxSaleDate'] <= year_end]

                if len(eligible_txns) > 0:
                    last_date = eligible_txns['MaxSaleDate'].max()
                else:
                    last_date = pd.NaT

                last_txn.append({
                    'Member_ID': member_id,
                    'YEAR': year,
                    'Cumulative_Last_Txn': last_date
                })

        last_txn_df = pd.DataFrame(last_txn)
        snapshot = snapshot.merge(last_txn_df, on=['Member_ID', 'YEAR'], how='left')

        # Step 6: Calculate Point_Range
        print("Calculating point ranges...")
        snapshot['Point_Range'] = snapshot['Total_point'].apply(self.calculate_point_range)

        # Step 7: Calculate LAP_Days (Last Activity Period)
        print("Calculating LAP days...")
        snapshot['LAP_Days'] = snapshot.apply(
            lambda row: self.calculate_lap_days(row['Year_End'], row['Cumulative_Last_Txn']),
            axis=1
        )

        # Step 8: Calculate Recency_Text (Segment)
        print("Calculating recency segments...")
        snapshot['Recency_Text'] = snapshot['LAP_Days'].apply(self.calculate_recency_text)

        # Step 9: Add YEAR_SORT for proper ordering
        snapshot['YEAR_SORT'] = snapshot['YEAR'].astype(int)

        # Reorder columns to match Power BI output
        column_order = [
            'Member_ID', 'YEAR', 'YEAR_SORT', 'TotalSpend', 'TotalQty', 'TotalTxn',
            'MaxSaleDate', 'FirstPurchaseDate', 'Point_Range', 'Total_point',
            'GENDER', 'Generation', 'MOBILE_NO', 'FIRST_NAME', 'LAST_NAME',
            'BIRTHDATE', 'UUID', 'Age_Range', 'Year_End', 'Mode_ProductCategory',
            'Cumulative_TotalTxn', 'Active_Years_Count', 'Cumulative_Last_Txn',
            'LAP_Days', 'Recency_Text'
        ]

        # Only include columns that exist
        column_order = [col for col in column_order if col in snapshot.columns]
        snapshot = snapshot[column_order]

        print(f"\nYearly Snapshot complete: {len(snapshot):,} rows")

        return snapshot


def main():
    """Example usage"""

    # Initialize engine
    engine = YearlySnapshotEngine(
        member_master_path='../data/member_master.csv',
        member_yearly_path='../data/member_segment_yearly.csv'
    )

    # Build yearly snapshot
    snapshot = engine.build_yearly_snapshot()

    # Save results
    output_path = '../data/yearly_snapshot.csv'
    snapshot.to_csv(output_path, index=False)
    print(f"\nSnapshot saved to: {output_path}")

    # Display summary
    print("\n=== Yearly Snapshot Summary ===")
    print(f"Total records: {len(snapshot):,}")
    print(f"Unique members: {snapshot['Member_ID'].nunique():,}")
    print(f"Year range: {snapshot['YEAR'].min()} - {snapshot['YEAR'].max()}")

    print("\n=== Recency Segment Distribution ===")
    print(snapshot.groupby('Recency_Text').size().sort_values(ascending=False))

    print("\n=== Segment Distribution by Year ===")
    segment_by_year = snapshot.groupby(['YEAR', 'Recency_Text']).size().unstack(fill_value=0)
    print(segment_by_year)

    print("\n=== Sample Records ===")
    print(snapshot.head(10))


if __name__ == '__main__':
    main()
