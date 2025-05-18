import pandas as pd

# Load the Data CSV file into a DataFrame
df = pd.read_csv('owid-covid-data.csv.zip')  

# Check Columns
print("Columns in the DataFrame:")
print(df.columns)

# Preview Rows
print("\nPreview of the first few rows:")
print(df.head())

# Identify Missing Values
print("\nMissing values in each column:")
print(df.isnull().sum())

# Filter countries of interest
countries_of_interest = ['Kenya', 'USA', 'India']
filtered_df = df[df['location'].isin(countries_of_interest)]

# Drop rows with missing dates or critical values
# Assuming 'date', 'total_cases', and 'total_deaths' are critical values
cleaned_df = filtered_df.dropna(subset=['date', 'total_cases', 'total_deaths'])

# Convert date column to datetime
cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])

# Handle missing numeric values
# Fill missing numeric values with the mean of the column
cleaned_df['total_cases'].fillna(cleaned_df['total_cases'].mean(), inplace=True)
cleaned_df['total_deaths'].fillna(cleaned_df['total_deaths'].mean(), inplace=True)
cleaned_df['new_cases'].fillna(cleaned_df['new_cases'].mean(), inplace=True)
cleaned_df['new_deaths'].fillna(cleaned_df['new_deaths'].mean(), inplace=True)
cleaned_df['total_vaccinations'].fillna(cleaned_df['total_vaccinations'].mean(), inplace=True)

# Display the cleaned DataFrame
print("Cleaned DataFrame:")
print(cleaned_df.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Calculate the death rate
filtered_df['death_rate'] = filtered_df['total_deaths'] / filtered_df['total_cases']

#Plot total cases over time for selected countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], marker='o', label=country)

plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Plot total deaths over time
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], marker='o', label=country)

plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Compare daily new cases between countries
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['new_cases'], marker='o', label=country)

plt.title('Daily New COVID-19 Cases Comparison')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Bar chart for top countries by total cases
top_countries = df.groupby('location')['total_cases'].sum().nlargest(10).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='total_cases', y='location', data=top_countries, palette='viridis')
plt.title('Top 10 Countries by Total COVID-19 Cases')
plt.xlabel('Total Cases')
plt.ylabel('Country')
plt.show()

# Heatmap for correlation analysis
plt.figure(figsize=(10, 6))
correlation_matrix = filtered_df[['total_cases', 'total_deaths', 'new_cases', 'death_rate']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

plt.xlabel('Date')
plt.ylabel('Cumulative Vaccinations')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

#  Filter countries of interest
countries_of_interest = ['USA', 'India', 'Brazil', 'UK']
filtered_df = df[df['country'].isin(countries_of_interest)]

# Convert date to datetime format
filtered_df['date'] = pd.to_datetime(filtered_df['date'])

# Calculate cumulative vaccinations
filtered_df['cumulative_vaccinations'] = filtered_df.groupby('country')['total_vaccinations'].cumsum()

# Plot cumulative vaccinations over time
plt.figure(figsize=(12, 6))
for country in countries_of_interest:
    country_data = filtered_df[filtered_df['country'] == country]
    plt.plot(country_data['date'], country_data['cumulative_vaccinations'], marker='o', label=country)

plt.title('Cumulative COVID-19 Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Vaccinations')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Compare % vaccinated population
filtered_df['vaccination_percentage'] = (filtered_df['total_vaccinations'] / filtered_df['population']) * 100

# Plot vaccination percentage
plt.figure(figsize=(12, 6))
sns.barplot(x='country', y='vaccination_percentage', data=filtered_df.groupby('country')['vaccination_percentage'].max().reset_index(), palette='viridis')
plt.title('Vaccination Percentage by Country')
plt.xlabel('Country')
plt.ylabel('Vaccination Percentage (%)')
plt.show()

# Pie chart for vaccinated vs. unvaccinated
total_vaccinated = df['total_vaccinations'].sum()
total_population = df['population'].sum()
unvaccinated = total_population - total_vaccinated

plt.figure(figsize=(8, 8))
plt.pie([total_vaccinated, unvaccinated], labels=['Vaccinated', 'Unvaccinated'], autopct='%1.1f%%', startangle=140)
plt.title('Vaccinated vs. Unvaccinated Population')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
