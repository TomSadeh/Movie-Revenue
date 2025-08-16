import pandas as pd
import numpy as np
from pathlib import Path

def load_and_process_cpi_data(cpi_file_path):
    """
    Load CPI data from World Bank format and extract world CPI percentages
    """
    # Read the CPI data
    cpi_df = pd.read_csv(cpi_file_path, skiprows=4)
    
    # Look for 'World' in Country Name column
    world_row = cpi_df[cpi_df['Country Name'] == 'World']
    
    if world_row.empty:
        # If 'World' not found, try alternative names
        world_row = cpi_df[cpi_df['Country Name'].str.contains('World', case=False, na=False)]
    
    if world_row.empty:
        raise ValueError("Could not find World CPI data in the file")
    
    # Extract year columns (typically from 1960 onwards)
    year_columns = [col for col in cpi_df.columns if col.isdigit()]
    
    # Get world CPI data for available years
    world_cpi_data = world_row[year_columns].iloc[0]
    
    # Convert to dictionary with years as integers
    cpi_dict = {int(year): value for year, value in world_cpi_data.items() if pd.notna(value)}
    
    return cpi_dict

def create_cpi_index(cpi_percentages, base_year=2024):
    """
    Convert year-over-year CPI percentage changes to an index with base_year = 100
    """
    # Sort years
    years = sorted(cpi_percentages.keys())
    
    # Initialize index dictionary
    cpi_index = {}
    
    # Start with an arbitrary value for the first year
    # We'll rescale everything to base_year = 100 later
    if years:
        cpi_index[years[0]] = 100
        
        # Calculate cumulative index
        for i in range(1, len(years)):
            prev_year = years[i-1]
            curr_year = years[i]
            
            # Apply percentage change
            if pd.notna(cpi_percentages[curr_year]):
                cpi_index[curr_year] = cpi_index[prev_year] * (1 + cpi_percentages[curr_year]/100)
            else:
                # If data is missing, carry forward the previous value
                cpi_index[curr_year] = cpi_index[prev_year]
    
    # Rescale so base_year = 100
    if base_year in cpi_index:
        base_value = cpi_index[base_year]
        cpi_index = {year: (value / base_value) * 100 for year, value in cpi_index.items()}
    else:
        # Use the latest available year as base
        latest_year = max(cpi_index.keys())
        base_value = cpi_index[latest_year]
        cpi_index = {year: (value / base_value) * 100 for year, value in cpi_index.items()}
    
    return cpi_index

def adjust_movie_revenues(movie_file_path, cpi_index, base_year=2024):
    """
    Adjust movie revenues for inflation using CPI index
    """
    # Load movie data
    movies_df = pd.read_csv(movie_file_path)
    
    # Create a copy to avoid modifying original
    adjusted_df = movies_df.copy()
    
    # Add CPI index column
    adjusted_df['CPI_Index'] = adjusted_df['Year'].map(cpi_index)
    
    # Fill missing CPI values with nearest year or interpolation
    if adjusted_df['CPI_Index'].isna().any():
        # For years outside the range, use nearest available CPI
        min_cpi_year = min(cpi_index.keys())
        max_cpi_year = max(cpi_index.keys())
        
        for idx, row in adjusted_df[adjusted_df['CPI_Index'].isna()].iterrows():
            year = row['Year']
            if year < min_cpi_year:
                adjusted_df.at[idx, 'CPI_Index'] = cpi_index[min_cpi_year]
            elif year > max_cpi_year:
                adjusted_df.at[idx, 'CPI_Index'] = cpi_index[max_cpi_year]
    
    # Calculate inflation adjustment factor
    # To convert from year Y to base_year prices: multiply by (100 / CPI_Index_Y)
    adjusted_df['Inflation_Factor'] = 100 / adjusted_df['CPI_Index']
    
    # Adjust worldwide revenue to base_year dollars
    adjusted_df['$Worldwide_Adjusted'] = adjusted_df['$Worldwide'] * adjusted_df['Inflation_Factor']
    
    # Also adjust domestic and foreign revenues
    adjusted_df['$Domestic_Adjusted'] = adjusted_df['$Domestic'] * adjusted_df['Inflation_Factor']
    adjusted_df['$Foreign_Adjusted'] = adjusted_df['$Foreign'] * adjusted_df['Inflation_Factor']
    
    # Calculate the adjustment amount
    adjusted_df['Adjustment_Amount'] = adjusted_df['$Worldwide_Adjusted'] - adjusted_df['$Worldwide']
    
    # Sort by adjusted worldwide revenue
    adjusted_df = adjusted_df.sort_values('$Worldwide_Adjusted', ascending=False)
    
    # Reset rank based on adjusted values
    adjusted_df['Adjusted_Rank'] = range(1, len(adjusted_df) + 1)
    
    return adjusted_df

def main():
    """
    Main function to run the inflation adjustment
    """
    # File paths
    cpi_file = Path('./data/API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_122376.csv')
    movie_file = Path('./data/enhanced_box_office_data(2000-2024)u.csv')
    
    try:
        # Load and process CPI data
        print("Loading CPI data...")
        cpi_percentages = load_and_process_cpi_data(cpi_file)
        print(f"Loaded CPI data for {len(cpi_percentages)} years")
        
        # Create CPI index with 2024 as base year
        print("Creating CPI index with 2024 as base year...")
        cpi_index = create_cpi_index(cpi_percentages, base_year=2024)
        
        # Adjust movie revenues
        print("Adjusting movie revenues for inflation...")
        adjusted_movies = adjust_movie_revenues(movie_file, cpi_index, base_year=2024)
        
        # Save results
        output_file = 'movies_inflation_adjusted_2024.csv'
        adjusted_movies.to_csv(output_file, index=False)
        print(f"Successfully saved adjusted data to {output_file}")
        print(f"Total movies processed: {len(adjusted_movies)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()