#!/usr/bin/env python3
"""
Simple test script for Concordia with Gemini API.
Based on the tutorial example but simplified for quick testing.
"""

import os
import numpy as np
import sentence_transformers

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("📁 Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("📁 Using system environment variables")

# Concordia imports
from concordia.language_model import google_aistudio_model
from concordia.language_model import no_language_model
from concordia.prefabs.simulation import generic as simulation
import concordia.prefabs.entity as entity_prefabs
import concordia.prefabs.game_master as game_master_prefabs
from concordia.typing import prefab as prefab_lib
from concordia.utils import helper_functions


def main():
    """Run a simple Concordia simulation with Gemini."""
    
    # Configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    DISABLE_LANGUAGE_MODEL = False  # Set to True to test without API calls
    
    if not GOOGLE_API_KEY and not DISABLE_LANGUAGE_MODEL:
        print("Error: GOOGLE_API_KEY environment variable not set!")
        print("Either set your API key or run with DISABLE_LANGUAGE_MODEL=True")
        print("\nTo set your API key:")
        print("export GOOGLE_API_KEY='your_api_key_here'")
        return
    
    print("🚀 Starting Concordia simulation test...")
    
    # Setup language model
    if not DISABLE_LANGUAGE_MODEL:
        print("📡 Initializing Gemini model...")
        model = google_aistudio_model.GoogleAIStudioLanguageModel(
            model_name='gemini-1.5-pro-latest',
            api_key=GOOGLE_API_KEY
        )
    else:
        print("🔕 Using no-op language model (no API calls)")
        model = no_language_model.NoLanguageModel()
    
    # Setup sentence encoder
    if not DISABLE_LANGUAGE_MODEL:
        print("🧠 Loading sentence transformer...")
        st_model = sentence_transformers.SentenceTransformer(
            'sentence-transformers/all-mpnet-base-v2'
        )
        embedder = lambda x: st_model.encode(x, show_progress_bar=False)
    else:
        embedder = lambda x: np.ones(5)
    
    # Test the model
    print("🧪 Testing language model...")
    test_response = model.sample_text("What is the capital of France?")
    print(f"Model test response: {test_response[:100]}...")
    
    # Load prefabs
    print("🏗️ Loading prefabs...")
    prefabs = {
        **helper_functions.get_package_classes(entity_prefabs),
        **helper_functions.get_package_classes(game_master_prefabs),
    }
    
    print(f"Available prefabs: {list(prefabs.keys())}")
    
    # Configure simulation instances
    print("⚙️ Configuring simulation...")
    instances = [
        prefab_lib.InstanceConfig(
            prefab='basic__Entity',
            role=prefab_lib.Role.ENTITY,
            params={
                'name': 'Alice',
                'goal': 'have a pleasant conversation',
            },
        ),
        prefab_lib.InstanceConfig(
            prefab='basic__Entity',
            role=prefab_lib.Role.ENTITY,
            params={
                'name': 'Bob',
                'goal': 'learn something new',
            },
        ),
        prefab_lib.InstanceConfig(
            prefab='generic__GameMaster',
            role=prefab_lib.Role.GAME_MASTER,
            params={
                'name': 'game master',
            },
        ),
        prefab_lib.InstanceConfig(
            prefab='formative_memories_initializer__GameMaster',
            role=prefab_lib.Role.INITIALIZER,
            params={
                'name': 'setup',
                'next_game_master_name': 'game master',
                'shared_memories': [
                    'Alice and Bob are meeting for the first time at a coffee shop.',
                    'The weather is pleasant and sunny.',
                ],
            },
        ),
    ]
    
    # Create configuration
    config = prefab_lib.Config(
        default_premise='Alice and Bob meet at a cozy coffee shop on a sunny afternoon.',
        default_max_steps=3,  # Keep it short for testing
        prefabs=prefabs,
        instances=instances,
    )
    
    # Initialize and run simulation
    print("🎭 Creating simulation...")
    runnable_simulation = simulation.Simulation(
        config=config,
        model=model,
        embedder=embedder,
    )
    
    print("▶️ Running simulation...")
    try:
        results_log = runnable_simulation.play()
        
        # Save results
        print("💾 Saving results...")
        with open('test_simulation_results.html', 'w') as f:
            f.write(results_log)
        
        print("✅ Simulation completed successfully!")
        print("📄 Results saved to test_simulation_results.html")
        print("🌐 Open the HTML file in a browser to view the full log")
        
        # Print a brief summary
        if not DISABLE_LANGUAGE_MODEL:
            print("\n📊 Brief summary:")
            print("- Language model: Gemini 1.5 Pro")
            print("- Entities: Alice, Bob")
            print("- Scenario: Coffee shop meeting")
            print("- Steps: 3")
        
    except Exception as e:
        print(f"❌ Error running simulation: {e}")
        print("This might be due to API limits, network issues, or configuration problems.")
        return False
    
    return True


if __name__ == '__main__':
    success = main()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")