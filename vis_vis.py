from zipfile import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_palette("husl")
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

def load_adjusted_data(file_path='movies_inflation_adjusted_2024.csv'):
    """Load the inflation-adjusted movie data"""
    df = pd.read_csv(file_path)
    
    # Define franchise keywords
    marvel_keywords = ['Marvel', 'Avengers', 'Iron Man', 'Thor', 'Captain America', 'Spider-Man', 
                      'Guardians of the Galaxy', 'Black Panther', 'Doctor Strange', 'Ant-Man', 
                      'Captain Marvel', 'Hulk', 'X-Men', 'Wolverine', 'Deadpool', 'Fantastic Four',
                      'Blade', 'Daredevil', 'Punisher', 'Ghost Rider', 'Venom', 'Morbius', 
                      'Eternals', 'Shang-Chi', 'Black Widow']
    
    dc_keywords = ['DC', 'Batman', 'Superman', 'Wonder Woman', 'Justice League', 'Aquaman', 
                   'Flash', 'Green Lantern', 'Suicide Squad', 'Joker', 'Harley Quinn', 
                   'Shazam', 'Birds of Prey', 'Man of Steel', 'Dark Knight', 'Catwoman',
                   'Watchmen', 'V for Vendetta', 'Constantine', 'Swamp Thing', 'Blue Beetle',
                   'Black Adam', 'Peacemaker']
    
    star_wars_keywords = ['Star Wars', 'Rogue One', 'Solo: A Star Wars', 'The Force Awakens',
                         'The Last Jedi', 'Rise of Skywalker', 'Phantom Menace', 'Attack of the Clones',
                         'Revenge of the Sith', 'A New Hope', 'Empire Strikes Back', 'Return of the Jedi']
    
    harry_potter_keywords = ['Harry Potter', 'Fantastic Beasts', 'Secrets of Dumbledore',
                            'Crimes of Grindelwald', 'Philosopher\'s Stone', 'Chamber of Secrets',
                            'Prisoner of Azkaban', 'Goblet of Fire', 'Order of the Phoenix',
                            'Half-Blood Prince', 'Deathly Hallows']
    
    lotr_hobbit_keywords = ['Lord of the Rings', 'The Hobbit', 'Fellowship of the Ring',
                           'Two Towers', 'Return of the King', 'Unexpected Journey',
                           'Desolation of Smaug', 'Battle of the Five Armies']
    
    pixar_keywords = ['Toy Story', 'Cars', 'Finding Nemo', 'Finding Dory', 'The Incredibles',
                     'Monsters, Inc', 'Monsters University', 'WALL-E', 'Up', 'Brave', 'Inside Out',
                     'Coco', 'Soul', 'Luca', 'Turning Red', 'Lightyear', 'Elemental', 'Ratatouille',
                     'A Bug\'s Life', 'The Good Dinosaur', 'Onward']
    
    disney_keywords = ['Frozen', 'Moana', 'Tangled', 'Encanto', 'Raya and the Last Dragon',
                      'Wreck-It Ralph', 'Zootopia', 'Big Hero 6', 'The Lion King', 'Aladdin',
                      'Beauty and the Beast', 'The Little Mermaid', 'Mulan', 'Pocahontas',
                      'Sleeping Beauty', 'Snow White', 'Cinderella', 'The Princess and the Frog',
                      'Wish', 'Strange World', 'Caribbean', 'Pirates of the Caribbean']
    
    fast_furious_keywords = ['Fast & Furious', 'Fast and Furious', 'The Fast and the Furious',
                            '2 Fast 2 Furious', 'Tokyo Drift', 'Fast Five', 'Fast & Furious 6',
                            'Furious 7', 'Fate of the Furious', 'F9', 'Fast X', 'Hobbs & Shaw']
    
    james_bond_keywords = ['James Bond', '007', 'Casino Royale', 'Quantum of Solace', 'Skyfall',
                          'Spectre', 'No Time to Die', 'Die Another Day', 'The World Is Not Enough',
                          'Tomorrow Never Dies', 'GoldenEye']
    
    transformers_keywords = ['Transformers', 'Bumblebee', 'Rise of the Beasts', 'The Last Knight',
                            'Age of Extinction', 'Dark of the Moon', 'Revenge of the Fallen']
    
    jurassic_keywords = ['Jurassic Park', 'Jurassic World', 'The Lost World', 'Dominion',
                        'Fallen Kingdom', 'Jurassic Park III']
    
    mission_impossible_keywords = ['Mission: Impossible', 'Mission Impossible', 'M:I', 
                                  'Ghost Protocol', 'Rogue Nation', 'Fallout', 'Dead Reckoning']
    
    # Create patterns
    marvel_pattern = '|'.join(marvel_keywords)
    dc_pattern = '|'.join(dc_keywords)
    star_wars_pattern = '|'.join(star_wars_keywords)
    harry_potter_pattern = '|'.join(harry_potter_keywords)
    lotr_hobbit_pattern = '|'.join(lotr_hobbit_keywords)
    pixar_pattern = '|'.join(pixar_keywords)
    disney_pattern = '|'.join(disney_keywords)
    fast_furious_pattern = '|'.join(fast_furious_keywords)
    james_bond_pattern = '|'.join(james_bond_keywords)
    transformers_pattern = '|'.join(transformers_keywords)
    jurassic_pattern = '|'.join(jurassic_keywords)
    mission_impossible_pattern = '|'.join(mission_impossible_keywords)
    
    # Create franchise column with priority order
    df['Franchise'] = 'Other'
    
    # Apply patterns in order of priority (more specific first)
    df.loc[df['Release Group'].str.contains(pixar_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Pixar'
    df.loc[df['Release Group'].str.contains(disney_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Disney'
    df.loc[df['Release Group'].str.contains(star_wars_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Star Wars'
    df.loc[df['Release Group'].str.contains(harry_potter_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Harry Potter'
    df.loc[df['Release Group'].str.contains(lotr_hobbit_pattern, case=False, na=False, regex=True), 'Franchise'] = 'LOTR/Hobbit'
    df.loc[df['Release Group'].str.contains(fast_furious_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Fast & Furious'
    df.loc[df['Release Group'].str.contains(james_bond_pattern, case=False, na=False, regex=True), 'Franchise'] = 'James Bond'
    df.loc[df['Release Group'].str.contains(transformers_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Transformers'
    df.loc[df['Release Group'].str.contains(jurassic_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Jurassic'
    df.loc[df['Release Group'].str.contains(mission_impossible_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Mission Impossible'
    df.loc[df['Release Group'].str.contains(marvel_pattern, case=False, na=False, regex=True), 'Franchise'] = 'Marvel'
    df.loc[df['Release Group'].str.contains(dc_pattern, case=False, na=False, regex=True), 'Franchise'] = 'DC'
    
    # Keep backward compatibility
    df['Is_Marvel'] = df['Franchise'] == 'Marvel'
    df['Is_DC'] = df['Franchise'] == 'DC'
    
    return df

def create_top_movies_chart(df, n=50):
   """Create a horizontal bar chart of top N movies"""
   fig, ax = plt.subplots(figsize=(14, 20))  # Increased height for 50 movies
   
   top_movies = df.nlargest(n, '$Worldwide_Adjusted')
   
   # Define franchise colors - expanded palette
   franchise_colors = {
       'Marvel': '#ED1D24',        # Marvel Red
       'DC': '#0476F2',            # DC Blue
       'Star Wars': '#FFE81F',     # Star Wars Yellow
       'Harry Potter': '#740001',  # Gryffindor Scarlet
       'LOTR/Hobbit': '#228B22',   # Forest Green
       'Pixar': '#00A8E1',         # Pixar Blue
       'Disney': '#7C4DFF',        # Disney Purple
       'Fast & Furious': '#FF6B35', # Orange/Red
       'James Bond': '#2C3E50',    # Dark Blue-Gray
       'Transformers': '#8B4513',  # Robot Bronze
       'Jurassic': '#006400',      # Dark Green
       'Mission Impossible': '#FF4500', # Red-Orange
       'Other': '#808080'          # Gray
   }
   
   # Create color map based on franchise using the dictionary
   colors = [franchise_colors.get(franchise, '#808080') for franchise in top_movies['Franchise']]
   
   # Create horizontal bar chart
   bars = ax.barh(range(n), top_movies['$Worldwide_Adjusted'].values/1e9, color=colors, alpha=0.8)
   
   # Add movie names and years (shortened for better readability with 50 movies)
   y_labels = [f"{i+1}. {row['Release Group'][:]} ({int(row['Year'])})" 
               for i, (_, row) in enumerate(top_movies.iterrows())]
   ax.set_yticks(range(n))
   ax.set_yticklabels(y_labels, fontsize=8)  # Smaller font for 50 movies
   
   # Add value labels on bars
   for i, (bar, value) in enumerate(zip(bars, top_movies['$Worldwide_Adjusted'].values/1e9)):
       ax.text(value + 0.02, bar.get_y() + bar.get_height()/2, 
               f'${value:.2f}B', va='center', fontsize=7)  # Smaller font for values
   
   ax.set_xlabel('Revenue (Billions USD, 2024 dollars)', fontsize=12)
   ax.set_title(f'Top {n} Movies by Inflation-Adjusted Revenue', fontsize=14, fontweight='bold', pad=10)
   ax.invert_yaxis()
   
   # Adjust y-axis limits to reduce top and bottom gaps
   ax.set_ylim(n - 0.5, -0.5)  # This reduces the gap at top and bottom
   
   ax.grid(True, alpha=0.3, axis='x')
   
   # Add expanded legend with all franchises present in top movies
   from matplotlib.patches import Patch
   
   # Get unique franchises in the top movies
   unique_franchises = top_movies['Franchise'].unique()
   # Sort franchises for consistent legend order
   sorted_franchises = sorted(unique_franchises, key=lambda x: (x == 'Other', x))
   
   legend_elements = []
   for franchise in sorted_franchises:
       if franchise in franchise_colors:
           legend_elements.append(
               Patch(facecolor=franchise_colors[franchise], alpha=0.8, label=franchise)
           )
   
   # Create legend with multiple columns if there are many franchises
   n_franchises = len(legend_elements)
   n_cols = 3 if n_franchises > 6 else 2 if n_franchises > 3 else 1
   
   ax.legend(handles=legend_elements, loc='lower right', ncol=n_cols, 
             fontsize=8, framealpha=0.9)

   source_text = "Data Sources: Box Office Mojo (2000-2024) | World Bank CPI Data\nAnalysis & Visualization: @tom_sadeh | github.com/TomSadeh/Movie-Revenue"

   # Add to the bottom of the figure
   fig.text(0.01, -0.01, source_text, 
               ha='left', va='bottom',
               fontsize=7, style='italic',
               color='#666666',
               transform=fig.transFigure,
               wrap=True)

   # Use tight_layout with adjusted padding
   plt.subplots_adjust(top=0.97, bottom=0.03, left=0.15, right=0.98)
   plt.savefig('top_movies_inflation_adjusted.png', dpi=300, bbox_inches='tight')
   plt.show()

def main():
    """Main function to generate all visualizations"""
    print("Loading inflation-adjusted movie data...")
    df = load_adjusted_data(Path(r'./output/movies_inflation_adjusted_2024.csv'))
    
    print(f"Loaded {len(df)} movies")
    print(f"Years covered: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Marvel movies: {df['Is_Marvel'].sum()}")
    print(f"DC movies: {df['Is_DC'].sum()}")
    
    print("\nGenerating visualizations...")
    
    
    print("Creating top movies chart...")
    create_top_movies_chart(df, n=50)
    

if __name__ == "__main__":
    main()