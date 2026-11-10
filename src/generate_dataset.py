"""
SYNTHETIC DATASET GENERATOR FOR INDIAN HOUSE PRICE PREDICTION SYSTEM
=====================================================================

IMPORTANT: This script generates a SYNTHETIC dataset for educational and 
demonstration purposes only. The data does NOT represent actual market prices
or real property listings. All values are algorithmically generated based on
approximate Indian real estate market trends and patterns.

For a real-world application, replace this synthetic dataset with actual 
market data from sources like:
- Kaggle: "Indian House Price Prediction" datasets
- MagicBricks, 99acres, Housing.com data exports
- Government property registration records

Generated Dataset Label: SYNTHETIC / SIMULATED DATA
"""

import pandas as pd
import numpy as np
import os

def generate_indian_house_price_dataset(n_samples=5000, random_state=42):
    """
    Generate a synthetic Indian house price dataset with realistic patterns.
    
    Parameters:
        n_samples (int): Number of property records to generate.
        random_state (int): Seed for reproducibility.
    
    Returns:
        pd.DataFrame: Synthetic dataset with house price features and target.
    """
    np.random.seed(random_state)
    
    # ==========================================
    # Define realistic Indian real estate values
    # ==========================================
    
    # Cities with approximate base price multipliers (per sq ft in INR)
    city_data = {
        'Mumbai': {'base_price': 18000, 'weight': 0.15},
        'Delhi': {'base_price': 14000, 'weight': 0.12},
        'Bangalore': {'base_price': 10000, 'weight': 0.14},
        'Hyderabad': {'base_price': 8000, 'weight': 0.12},
        'Chennai': {'base_price': 9000, 'weight': 0.10},
        'Pune': {'base_price': 8500, 'weight': 0.10},
        'Kolkata': {'base_price': 6500, 'weight': 0.08},
        'Ahmedabad': {'base_price': 5500, 'weight': 0.07},
        'Jaipur': {'base_price': 4500, 'weight': 0.06},
        'Lucknow': {'base_price': 4000, 'weight': 0.06},
    }
    
    # Localities per city with price multipliers
    locality_data = {
        'Mumbai': {
            'Andheri': 1.0, 'Bandra': 1.5, 'Powai': 1.2, 
            'Thane': 0.7, 'Navi Mumbai': 0.6, 'Goregaon': 0.9,
            'Malad': 0.85, 'Borivali': 0.75
        },
        'Delhi': {
            'Dwarka': 0.9, 'Rohini': 0.85, 'Saket': 1.3,
            'Vasant Kunj': 1.2, 'Lajpat Nagar': 1.1, 'Noida': 0.7,
            'Gurgaon': 1.0, 'Greater Noida': 0.5
        },
        'Bangalore': {
            'Whitefield': 1.0, 'Electronic City': 0.8, 'Koramangala': 1.4,
            'HSR Layout': 1.2, 'Marathahalli': 0.9, 'Sarjapur Road': 0.85,
            'Yelahanka': 0.7, 'Bannerghatta Road': 0.95
        },
        'Hyderabad': {
            'Gachibowli': 1.2, 'Kondapur': 1.1, 'Madhapur': 1.15,
            'Kukatpally': 0.8, 'Miyapur': 0.7, 'Secunderabad': 0.9,
            'Begumpet': 1.0, 'LB Nagar': 0.65
        },
        'Chennai': {
            'Adyar': 1.3, 'Velachery': 0.9, 'OMR': 0.85,
            'Anna Nagar': 1.2, 'T Nagar': 1.35, 'Porur': 0.7,
            'Tambaram': 0.6, 'Sholinganallur': 0.8
        },
        'Pune': {
            'Hinjewadi': 0.95, 'Kharadi': 1.0, 'Wakad': 0.85,
            'Baner': 1.1, 'Viman Nagar': 1.05, 'Hadapsar': 0.75,
            'Kothrud': 1.15, 'Pimpri-Chinchwad': 0.65
        },
        'Kolkata': {
            'Salt Lake': 1.1, 'New Town': 0.9, 'Alipore': 1.4,
            'Dum Dum': 0.7, 'Howrah': 0.6, 'Garia': 0.75,
            'Rajarhat': 0.8, 'Behala': 0.65
        },
        'Ahmedabad': {
            'SG Highway': 1.1, 'Prahlad Nagar': 1.2, 'Vastrapur': 1.0,
            'Bopal': 0.8, 'Satellite': 1.15, 'Chandkheda': 0.65,
            'Maninagar': 0.7, 'Navrangpura': 0.95
        },
        'Jaipur': {
            'Vaishali Nagar': 1.0, 'Malviya Nagar': 1.1, 'Mansarovar': 0.85,
            'Jagatpura': 0.7, 'C-Scheme': 1.3, 'Tonk Road': 0.75,
            'Pratap Nagar': 0.65, 'Sirsi Road': 0.6
        },
        'Lucknow': {
            'Gomti Nagar': 1.2, 'Hazratganj': 1.3, 'Aliganj': 0.9,
            'Indira Nagar': 1.0, 'Vikas Nagar': 0.7, 'Jankipuram': 0.65,
            'Mahanagar': 0.85, 'Alambagh': 0.6
        },
    }
    
    property_types = ['Apartment', 'Independent House', 'Villa', 'Builder Floor']
    property_type_weights = [0.55, 0.15, 0.10, 0.20]
    property_type_multipliers = {
        'Apartment': 1.0, 'Independent House': 1.3, 
        'Villa': 1.8, 'Builder Floor': 0.9
    }
    
    furnishing_options = ['Furnished', 'Semi-Furnished', 'Unfurnished']
    furnishing_weights = [0.20, 0.45, 0.35]
    furnishing_multipliers = {'Furnished': 1.15, 'Semi-Furnished': 1.05, 'Unfurnished': 1.0}
    
    # BHK configurations with typical area ranges (sq ft)
    bhk_area_ranges = {
        1: (400, 700),
        2: (650, 1200),
        3: (1000, 1800),
        4: (1500, 2800),
        5: (2200, 4000),
    }
    bhk_weights = [0.15, 0.35, 0.30, 0.15, 0.05]
    
    records = []
    
    # Select cities based on weights
    cities = list(city_data.keys())
    city_weights = [city_data[c]['weight'] for c in cities]
    selected_cities = np.random.choice(cities, size=n_samples, p=city_weights)
    
    for i in range(n_samples):
        city = selected_cities[i]
        base_price = city_data[city]['base_price']
        
        # Select locality
        locs = list(locality_data[city].keys())
        locality = np.random.choice(locs)
        locality_mult = locality_data[city][locality]
        
        # Property type
        prop_type = np.random.choice(property_types, p=property_type_weights)
        prop_mult = property_type_multipliers[prop_type]
        
        # BHK
        bhk = np.random.choice([1, 2, 3, 4, 5], p=bhk_weights)
        
        # Area (super built-up area in sq ft)
        area_min, area_max = bhk_area_ranges[bhk]
        super_builtup_area = int(np.random.uniform(area_min, area_max))
        
        # Carpet area is typically 65-80% of super built-up area
        carpet_ratio = np.random.uniform(0.65, 0.80)
        carpet_area = int(super_builtup_area * carpet_ratio)
        
        # Bathrooms (typically BHK or BHK+1)
        bathrooms = min(bhk + np.random.choice([0, 1], p=[0.6, 0.4]), bhk + 2)
        
        # Property age in years
        property_age = np.random.choice(
            range(0, 31), 
            p=np.array([5 if a < 5 else 3 if a < 10 else 2 if a < 20 else 1 for a in range(31)], dtype=float) / 
              sum([5 if a < 5 else 3 if a < 10 else 2 if a < 20 else 1 for a in range(31)])
        )
        age_mult = max(0.7, 1.0 - property_age * 0.008)  # Older properties slightly cheaper
        
        # Furnishing
        furnishing = np.random.choice(furnishing_options, p=furnishing_weights)
        furn_mult = furnishing_multipliers[furnishing]
        
        # Floor number and total floors
        if prop_type == 'Apartment':
            total_floors = np.random.choice(range(3, 30))
            floor_no = np.random.choice(range(0, total_floors + 1))  # 0 = Ground
        elif prop_type == 'Builder Floor':
            total_floors = np.random.choice(range(2, 6))
            floor_no = np.random.choice(range(0, total_floors + 1))
        elif prop_type == 'Villa':
            total_floors = np.random.choice([1, 2, 3])
            floor_no = 0  # Ground floor for villas
        else:  # Independent House
            total_floors = np.random.choice([1, 2, 3, 4])
            floor_no = 0
        
        # Floor premium (higher floors cost slightly more)
        if total_floors > 0:
            floor_mult = 1.0 + (floor_no / total_floors) * 0.05
        else:
            floor_mult = 1.0
        
        # Parking
        parking = np.random.choice([0, 1, 2, 3], p=[0.15, 0.45, 0.30, 0.10])
        parking_mult = 1.0 + parking * 0.02
        
        # Lift availability
        if prop_type == 'Apartment' and total_floors > 3:
            lift = np.random.choice([1, 0], p=[0.9, 0.1])
        elif prop_type == 'Builder Floor':
            lift = np.random.choice([1, 0], p=[0.3, 0.7])
        else:
            lift = np.random.choice([1, 0], p=[0.1, 0.9])
        lift_mult = 1.02 if lift else 1.0
        
        # Gated community
        if prop_type in ['Apartment', 'Villa']:
            gated_community = np.random.choice([1, 0], p=[0.75, 0.25])
        else:
            gated_community = np.random.choice([1, 0], p=[0.3, 0.7])
        gated_mult = 1.05 if gated_community else 1.0
        
        # ==========================================
        # Calculate price with controlled randomness
        # ==========================================
        price_per_sqft = (
            base_price 
            * locality_mult 
            * prop_mult 
            * furn_mult 
            * age_mult 
            * floor_mult 
            * parking_mult 
            * lift_mult 
            * gated_mult
        )
        
        # Add random noise (±15%)
        noise = np.random.uniform(0.85, 1.15)
        price_per_sqft *= noise
        
        # Total price
        price = price_per_sqft * super_builtup_area
        
        # Round price to nearest lakh (1,00,000)
        price = round(price / 100000) * 100000
        
        # Ensure minimum price
        price = max(price, 500000)
        
        records.append({
            'City': city,
            'Locality': locality,
            'Property_Type': prop_type,
            'BHK': bhk,
            'Bathrooms': bathrooms,
            'Super_Built_Up_Area_sqft': super_builtup_area,
            'Carpet_Area_sqft': carpet_area,
            'Property_Age_years': property_age,
            'Furnishing_Status': furnishing,
            'Floor_No': floor_no,
            'Total_Floors': total_floors,
            'Parking': parking,
            'Lift': lift,
            'Gated_Community': gated_community,
            'Price': int(price),
        })
    
    df = pd.DataFrame(records)
    return df


def main():
    """Generate and save the synthetic dataset."""
    print("=" * 60)
    print("SYNTHETIC DATASET GENERATOR")
    print("Indian House Price Prediction System")
    print("=" * 60)
    print()
    print("⚠️  NOTE: This dataset is SYNTHETIC (algorithmically generated)")
    print("   for educational/demonstration purposes only.")
    print("   It does NOT represent actual real estate market data.")
    print()
    
    # Generate dataset
    df = generate_indian_house_price_dataset(n_samples=5000, random_state=42)
    
    # Save to data folder
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, 'house_prices.csv')
    df.to_csv(filepath, index=False)
    
    print(f"✅ Dataset generated successfully!")
    print(f"📁 Saved to: {filepath}")
    print(f"\n📊 Dataset Summary:")
    print(f"   - Shape: {df.shape}")
    print(f"   - Columns: {list(df.columns)}")
    print(f"\n📈 Price Statistics:")
    print(f"   - Min Price: ₹{df['Price'].min():,.0f}")
    print(f"   - Max Price: ₹{df['Price'].max():,.0f}")
    print(f"   - Mean Price: ₹{df['Price'].mean():,.0f}")
    print(f"   - Median Price: ₹{df['Price'].median():,.0f}")
    print(f"\n🏙️  Cities: {df['City'].nunique()} ({', '.join(df['City'].unique())})")
    print(f"🏘️  Property Types: {df['Property_Type'].nunique()} ({', '.join(df['Property_Type'].unique())})")
    print(f"\n📋 First 5 records:")
    print(df.head().to_string(index=False))
    print()
    
    return df


if __name__ == '__main__':
    main()

