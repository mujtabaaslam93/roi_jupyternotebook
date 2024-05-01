import pandas as pd

class PropertyInvestment:
    def __init__(self, df):
        self.df = df
        self.monthly_savings = 0
        self.cash_at_hand = 0
        self.bought_properties = pd.DataFrame(columns=['Type', 'Size', 'Price', 'Rent', 'ROI', 'Bought Month'])
        self.calculateROI()

    def getProperties(self):
        return self.df
        
    def calculateROI(self):
        self.df['ROI'] = (self.df['rent'] * 12) / self.df['price'] * 100

    def sort_properties(self, strategy):
        """Sort properties based on the chosen strategy using DataFrame sorting."""
        if strategy == "high_roi":
            self.df = self.df.sort_values(by=['ROI', 'price'], ascending=[False, True])
        elif strategy == "low_investment":
            self.df = self.df.sort_values(by='price')

    def execute_strategy(self, strategy, monthly_savings, max_years):
        """Execute the buying strategy using DataFrame."""
        self.sort_properties(strategy)
        self.monthly_savings = monthly_savings
        self.cash_at_hand = 0  # Starting with zero cash at hand

        max_months = max_years * 12
        month = 0

        while month < max_months and not self.df.empty:
            month += 1
            self.cash_at_hand += self.monthly_savings
            self.cash_at_hand += self.get_total_monthly_rent()  # Assuming this is defined elsewhere

            affordable = self.df[self.df['price'] <= self.cash_at_hand]
            for idx, row in affordable.iterrows():
                bought_property = pd.DataFrame({
                    'Type': [row['type']],
                    'City': [row['city']],  # Assuming 'Area' is equivalent to 'Size'
                    'Size': [row['size']],  # Assuming 'Area' is equivalent to 'Size'
                    'Price': [row['price']],
                    'Rent': [row['rent']],
                    'ROI': [row['ROI']],
                    'Bought Month': [month]
                })
                self.bought_properties = pd.concat([self.bought_properties, bought_property], ignore_index=True)
                self.cash_at_hand -= row['price']
                self.df.drop(idx, inplace=True)

    def get_total_monthly_rent(self):
        """Calculate total monthly rent from bought properties."""
        return self.bought_properties['Rent'].sum()