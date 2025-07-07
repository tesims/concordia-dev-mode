#!/usr/bin/env python3
"""
Verbose test script for Concordia with Gemini API.
Shows more detail about what's happening during the simulation.
"""

import os
import numpy as np
import sentence_transformers
from datetime import datetime

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
    """Run a verbose Concordia simulation with Gemini."""
    
    # Configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    DISABLE_LANGUAGE_MODEL = False  # Set to True to test without API calls
    
    if not GOOGLE_API_KEY and not DISABLE_LANGUAGE_MODEL:
        print("Error: GOOGLE_API_KEY environment variable not set!")
        print("Either set your API key or run with DISABLE_LANGUAGE_MODEL=True")
        print("\nTo set your API key:")
        print("export GOOGLE_API_KEY='your_api_key_here'")
        return
    
    print("🚀 Starting VERBOSE Concordia simulation test...")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Setup language model
    if not DISABLE_LANGUAGE_MODEL:
        print("\n📡 Initializing Gemini model...")
        print("   Model: gemini-1.5-pro-latest")
        print(f"   API Key: {GOOGLE_API_KEY[:10]}...")
        model = google_aistudio_model.GoogleAIStudioLanguageModel(
            model_name='gemini-1.5-pro-latest',
            api_key=GOOGLE_API_KEY
        )
    else:
        print("🔕 Using no-op language model (no API calls)")
        model = no_language_model.NoLanguageModel()
    
    # Setup sentence encoder
    if not DISABLE_LANGUAGE_MODEL:
        print("\n🧠 Loading sentence transformer...")
        print("   Model: sentence-transformers/all-mpnet-base-v2")
        st_model = sentence_transformers.SentenceTransformer(
            'sentence-transformers/all-mpnet-base-v2'
        )
        embedder = lambda x: st_model.encode(x, show_progress_bar=False)
        print("   ✅ Embedder ready")
    else:
        embedder = lambda x: np.ones(5)
    
    # Test the model
    print("\n🧪 Testing language model...")
    test_prompt = "What is the capital of France? (answer in one word)"
    print(f"   Test prompt: {test_prompt}")
    test_response = model.sample_text(test_prompt)
    print(f"   Response: {test_response}")
    print("   ✅ Model test passed")
    
    # Load prefabs
    print("\n🏗️ Loading prefabs...")
    prefabs = {
        **helper_functions.get_package_classes(entity_prefabs),
        **helper_functions.get_package_classes(game_master_prefabs),
    }
    
    print(f"   Total prefabs loaded: {len(prefabs)}")
    print("   Entity prefabs:")
    for name in sorted(prefabs.keys()):
        if name.endswith('__Entity'):
            print(f"      - {name}")
    print("   Game Master prefabs:")
    for name in sorted(prefabs.keys()):
        if name.endswith('__GameMaster'):
            print(f"      - {name}")
    
    # Configure simulation instances
    print("\n⚙️ Configuring simulation...")
    print("   Creating 2 entities and 2 game masters")
    
    instances = [
        prefab_lib.InstanceConfig(
            prefab='basic__Entity',
            role=prefab_lib.Role.ENTITY,
            params={
                'name': 'Alice',
                'goal': 'have a pleasant conversation and learn about Bob',
            },
        ),
        prefab_lib.InstanceConfig(
            prefab='basic__Entity',
            role=prefab_lib.Role.ENTITY,
            params={
                'name': 'Bob',
                'goal': 'share something interesting and make a new friend',
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
                    'The coffee shop is called "The Thinking Bean" and is known for its intellectual atmosphere.',
                    'Today is a beautiful sunny afternoon, perfect for making new connections.',
                ],
            },
        ),
    ]
    
    print("\n   Instance details:")
    for i, instance in enumerate(instances):
        print(f"   {i+1}. {instance.role.name}: {instance.params.get('name', 'unnamed')}")
        if 'goal' in instance.params:
            print(f"      Goal: {instance.params['goal']}")
    
    # Create configuration
    premise = """Alice and Bob meet at "The Thinking Bean" coffee shop on a sunny afternoon.
Alice is curious about people and loves learning new things.
Bob enjoys sharing his knowledge and making meaningful connections."""
    
    config = prefab_lib.Config(
        default_premise=premise,
        default_max_steps=5,  # A bit longer to see more interaction
        prefabs=prefabs,
        instances=instances,
    )
    
    print(f"\n📖 Simulation premise:")
    for line in premise.strip().split('\n'):
        print(f"   {line}")
    print(f"\n   Max steps: {config.default_max_steps}")
    
    # Initialize and run simulation
    print("\n🎭 Creating simulation...")
    runnable_simulation = simulation.Simulation(
        config=config,
        model=model,
        embedder=embedder,
    )
    print("   ✅ Simulation initialized")
    
    print("\n▶️ Running simulation...")
    print("   Watch as Alice and Bob interact:")
    print("="*60)
    
    try:
        # Run the simulation
        results_log = runnable_simulation.play()
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'verbose_simulation_{timestamp}.html'
        
        print("\n="*60)
        print("💾 Saving results...")
        with open(output_file, 'w') as f:
            f.write(results_log)
        
        print(f"\n✅ Simulation completed successfully!")
        print(f"📄 Results saved to: {output_file}")
        print("🌐 Open the HTML file in a browser to see:")
        print("   - Complete conversation transcript")
        print("   - Memory formation and retrieval")
        print("   - Decision-making process")
        print("   - Entity observations and actions")
        
        # Print a summary of what happened
        print("\n📊 Simulation Summary:")
        print(f"   - Duration: {config.default_max_steps} steps")
        print("   - Participants: Alice (curious learner), Bob (knowledge sharer)")
        print("   - Setting: The Thinking Bean coffee shop")
        print("   - Outcome: See HTML file for full conversation")
        
        print("\n💡 What to look for in the HTML results:")
        print("   1. How entities form and use memories")
        print("   2. The 'three key questions' reasoning process")
        print("   3. How the game master manages the scene")
        print("   4. The natural flow of conversation")
        
    except Exception as e:
        print(f"\n❌ Error running simulation: {e}")
        print("This might be due to:")
        print("   - API rate limits")
        print("   - Network connectivity issues")
        print("   - Invalid API key")
        print("   - Configuration problems")
        import traceback
        print("\nFull error:")
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    print("\n🎬 Concordia Verbose Test Script")
    print("This script shows detailed information about the simulation process")
    print("\n")
    
    success = main()
    if success:
        print("\n🎉 Test completed successfully!")
        print("Check the generated HTML file to explore the full simulation")
    else:
        print("\n💥 Test failed!")
        print("Please check the error messages above")