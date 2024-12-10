import pandas as pd
from itertools import combinations
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import warnings

warnings.filterwarnings('ignore')  # Suppress warnings for clean output

# Preprocessing Function
def preprocess_data(file_path):
    city_df = pd.read_csv(file_path)
    city_df['avg_citation_sum'] = city_df['citation_sum'] / city_df['p_count']
    city_df = city_df.dropna(subset=['population', 'gdp_per_capita', 'lat', 'lon', 'safety_index', 'primary_language', 'avg_citation_sum'])
    city_df['primary_language'] = city_df['primary_language'].apply(lambda x: 1 if x == 'English' else 0)
    
    # Remove outliers using IQR
    Q1 = city_df['avg_citation_sum'].quantile(0.25)
    Q3 = city_df['avg_citation_sum'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    city_df_filtered = city_df[(city_df['avg_citation_sum'] >= lower_bound) & (city_df['avg_citation_sum'] <= upper_bound)]
    
    return city_df_filtered

# Model Training and Evaluation Function with Stratified Sampling
def evaluate_features_with_stratified_sampling(city_df, all_features):
    best_r2 = float('-inf')
    best_mae = float('inf')
    best_features = None
    best_model = None

    # Create bins for stratified sampling
    city_df['stratify_bins'] = pd.qcut(city_df['avg_citation_sum'], q=5, labels=False)

    for features in [list(comb) for i in range(1, len(all_features) + 1) for comb in combinations(all_features, i)]:
        X = city_df[features]
        y = city_df['avg_citation_sum']
        stratify_bins = city_df['stratify_bins']

        # Stratified train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, stratify=stratify_bins, test_size=0.2, random_state=42
        )

        # Use a pipeline with scaling and RandomForestRegressor
        pipeline = Pipeline([
            ('scaler', StandardScaler()),  # Scale features
            ('model', RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1))
        ])

        # Train the model
        pipeline.fit(X_train, y_train)

        # Evaluate the model
        y_pred = pipeline.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        if r2 > best_r2:
            best_r2 = r2
            best_mae = mae
            best_features = features
            best_model = pipeline

    return best_r2, best_mae, best_features, best_model

# Main Script
if __name__ == "__main__":
    city_df_filtered = preprocess_data('../For_vizml/city_impute_pop_real.csv')
    all_features = ['population', 'gdp_per_capita', 'lat', 'lon', 'safety_index', 'primary_language']

    best_r2, best_mae, best_features, best_model = evaluate_features_with_stratified_sampling(city_df_filtered, all_features)

    print("Best Model Evaluation:")
    print(f"Best R^2 Score: {best_r2:.2f}")
    print(f"Best Mean Absolute Error: {best_mae:.2f}")
    print(f"Best Features: {best_features}")
