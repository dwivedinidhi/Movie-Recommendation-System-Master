#!/usr/bin/env python3
"""
Train a demo model with 2,000 movies for the Movie Recommendation System
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add the training directory to the path
sys.path.append(str(Path(__file__).parent / 'training'))

from train import MovieRecommenderTrainer

def main():
    """Train a demo model with 2,000 movies"""
    
    # Path to the downloaded dataset
    dataset_path = Path.home() / '.cache' / 'kagglehub' / 'datasets' / 'asaniczka' / 'tmdb-movies-dataset-2023-930k-movies' / 'versions' / '906' / 'TMDB_movie_dataset_v11.csv'
    
    if not dataset_path.exists():
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please run: python -c \"import kagglehub; kagglehub.dataset_download('asaniczka/tmdb-movies-dataset-2023-930k-movies')\"")
        return
    
    print(f"Training demo model with dataset: {dataset_path}")
    
    # Initialize trainer for demo model
    trainer = MovieRecommenderTrainer(
        output_dir='./training/models',
        use_dimensionality_reduction=True,
        n_components=300  # Lower components for smaller model
    )
    
    # Train with only 2,000 movies (demo size)
    print("Training model with 2,000 movies (demo size)...")
    print("This may take a few minutes...")
    
    try:
        df, sim_matrix = trainer.train(
            str(dataset_path),
            quality_threshold='medium',  # Use medium quality (50+ votes)
            max_movies=2000              # Limit to 2,000 movies
        )
        
        print(f"\n✅ Training completed successfully!")
        print(f"📊 Dataset size: {len(df):,} movies")
        print(f"💾 Model saved to: ./training/models/")
        print(f"🎯 Ready to use with the Django application!")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()