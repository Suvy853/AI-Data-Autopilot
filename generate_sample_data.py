import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(filename="sample_data/subscription_data.csv"):
    """
    Generate sample SaaS subscription data for testing.
    Creates one CSV file with 18,250 rows of realistic data.
    """
    
    # Set random seed (same data every time for consistency)
    np.random.seed(42)
    
    # Parameters
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    n_accounts = 50
    
    segments = ['Enterprise', 'Mid-Market', 'SMB']
    industries = ['Tech', 'Finance', 'Healthcare', 'Retail']
    statuses = ['Active', 'Churned', 'Paused']
    
    # Create data
    data = []
    
    for date in dates:
        for account_id in range(1, n_accounts + 1):
            # Deterministic: same account always has same properties
            np.random.seed(account_id * 100 + date.toordinal())
            
            segment = np.random.choice(segments, p=[0.2, 0.3, 0.5])
            industry = np.random.choice(industries)
            
            # MRR varies by segment
            if segment == 'Enterprise':
                mrr = np.random.uniform(10000, 25000)
            elif segment == 'Mid-Market':
                mrr = np.random.uniform(3000, 10000)
            else:  # SMB
                mrr = np.random.uniform(500, 3000)
            
            # Churn rate by segment
            churn_rate = {'Enterprise': 0.02, 'Mid-Market': 0.05, 'SMB': 0.12}[segment]
            
            if np.random.random() < churn_rate:
                status = 'Churned'
            elif np.random.random() < 0.05:
                status = 'Paused'
            else:
                status = 'Active'
            
            # Expansion revenue
            expansion = mrr * np.random.uniform(0, 0.3) if status == 'Active' else 0
            
            # Feature adoption
            if status == 'Churned':
                adoption = np.random.uniform(20, 60)
            else:
                adoption = np.random.uniform(60, 100)
            
            # Create record
            record = {
                'Date': date,
                'Account_ID': f'ACC{account_id:05d}',
                'Customer_Segment': segment,
                'Industry': industry,
                'Subscription_Status': status,
                'Monthly_Recurring_Revenue': round(mrr, 2),
                'Expansion_Revenue': round(expansion, 2),
                'Support_Tickets_Last_30d': np.random.randint(0, 10),
                'Feature_Adoption_Score': round(adoption, 1),
            }
            
            data.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    print(f"✓ Sample data created: {filename}")
    print(f"  - {len(df)} rows")
    print(f"  - {len(df.columns)} columns")
    print(f"  - Ready for testing!")

if __name__ == "__main__":
    generate_sample_data()