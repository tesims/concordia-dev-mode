#!/usr/bin/env python3
"""
Complete guide for setting up a Concordia simulation
Shows each step with detailed explanations
"""

import os
import numpy as np
import sentence_transformers
from dotenv import load_dotenv

# Concordia imports
from concordia.language_model import google_aistudio_model
from concordia.prefabs.simulation import generic as simulation
import concordia.prefabs.entity as entity_prefabs
import concordia.prefabs.game_master as game_master_prefabs
from concordia.typing import prefab as prefab_lib
from concordia.utils import helper_functions

def setup_concordia_simulation():
    """Step-by-step setup of a Concordia simulation"""
    
    print("🎯 CONCORDIA SIMULATION SETUP GUIDE")
    print("="*50)
    
    # STEP 1: ENVIRONMENT SETUP
    print("\n1️⃣ ENVIRONMENT SETUP")
    print("-"*30)
    
    # Load environment variables
    load_dotenv()
    print("✅ Loaded .env file")
    
    # Check for API key
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        print("❌ No API key found! Create a .env file with:")
        print("   GOOGLE_API_KEY=your_api_key_here")
        return
    print(f"✅ Found API key: {GOOGLE_API_KEY[:10]}...")
    
    # STEP 2: INITIALIZE LANGUAGE MODEL
    print("\n2️⃣ LANGUAGE MODEL SETUP")
    print("-"*30)
    
    # Create the LLM that powers agent reasoning
    model = google_aistudio_model.GoogleAIStudioLanguageModel(
        model_name='gemini-1.5-pro-latest',
        api_key=GOOGLE_API_KEY
    )
    print("✅ Initialized Gemini 1.5 Pro model")
    
    # Test the model
    test_response = model.sample_text("Say 'Hello world!' in exactly 2 words")
    print(f"✅ Model test: {test_response}")
    
    # STEP 3: SETUP EMBEDDINGS
    print("\n3️⃣ EMBEDDINGS SETUP")
    print("-"*30)
    
    # Embeddings convert text to vectors for memory search
    st_model = sentence_transformers.SentenceTransformer(
        'sentence-transformers/all-mpnet-base-v2'
    )
    embedder = lambda x: st_model.encode(x, show_progress_bar=False)
    print("✅ Loaded sentence transformer for semantic memory")
    
    # Test embeddings
    test_embedding = embedder("test text")
    print(f"✅ Embedding test: vector shape {test_embedding.shape}")
    
    # STEP 4: LOAD PREFABS
    print("\n4️⃣ PREFAB SYSTEM")
    print("-"*30)
    
    # Prefabs are pre-configured templates for agents and game masters
    prefabs = {
        **helper_functions.get_package_classes(entity_prefabs),
        **helper_functions.get_package_classes(game_master_prefabs),
    }
    print(f"✅ Loaded {len(prefabs)} prefab templates")
    
    # Show available entity types
    print("\nAvailable Entity Prefabs:")
    for name in sorted(prefabs.keys()):
        if name.endswith('__Entity'):
            print(f"   • {name}")
            if name == 'basic__Entity':
                print("     → Uses 'three key questions' reasoning")
            elif name == 'basic_with_plan__Entity':
                print("     → Adds planning capabilities")
            elif name == 'minimal__Entity':
                print("     → Simplified for speed")
    
    # STEP 5: CONFIGURE AGENTS
    print("\n5️⃣ AGENT CONFIGURATION")
    print("-"*30)
    
    # Create instances from prefabs with specific parameters
    instances = [
        # First entity: Alice
        prefab_lib.InstanceConfig(
            prefab='basic__Entity',  # Which template to use
            role=prefab_lib.Role.ENTITY,  # Role in simulation
            params={
                'name': 'Alice',
                'goal': 'have a pleasant conversation and learn about Bob',
                # The prefab will use these to configure the agent's behavior
            },
        ),
        
        # Second entity: Bob  
        prefab_lib.InstanceConfig(
            prefab='basic__Entity',
            role=prefab_lib.Role.ENTITY,
            params={
                'name': 'Bob', 
                'goal': 'share something interesting and make a new friend',
            },
        ),
        
        # Game Master: Controls the environment
        prefab_lib.InstanceConfig(
            prefab='generic__GameMaster',
            role=prefab_lib.Role.GAME_MASTER,
            params={
                'name': 'game master',
                # Game master observes, determines who acts next,
                # and resolves actions into events
            },
        ),
        
        # Initializer: Sets up initial memories
        prefab_lib.InstanceConfig(
            prefab='formative_memories_initializer__GameMaster',
            role=prefab_lib.Role.INITIALIZER,
            params={
                'name': 'setup',
                'next_game_master_name': 'game master',
                'shared_memories': [
                    # These become part of each agent's memory
                    'Alice and Bob are meeting for the first time at a coffee shop.',
                    'The coffee shop is called "The Thinking Bean".',
                    'Today is a beautiful sunny afternoon.',
                ],
                # Each agent also gets unique formative memories
                # (childhood experiences, etc.) generated by the LLM
            },
        ),
    ]
    
    print("✅ Configured 4 instances:")
    for inst in instances:
        print(f"   • {inst.params.get('name', 'unnamed')} ({inst.role.name})")
    
    # STEP 6: CREATE SIMULATION CONFIG
    print("\n6️⃣ SIMULATION CONFIGURATION")
    print("-"*30)
    
    # The config ties everything together
    config = prefab_lib.Config(
        # Overall scenario description
        default_premise="""Alice and Bob meet at "The Thinking Bean" coffee shop.
Alice is curious about people and loves learning new things.
Bob enjoys sharing his knowledge and making connections.""",
        
        # How many turns to simulate
        default_max_steps=5,
        
        # Available prefab templates
        prefabs=prefabs,
        
        # Specific agent instances
        instances=instances,
    )
    
    print("✅ Created simulation config")
    print(f"   • Premise: Coffee shop meeting")
    print(f"   • Max steps: {config.default_max_steps}")
    print(f"   • Entities: {sum(1 for i in instances if i.role == prefab_lib.Role.ENTITY)}")
    
    # STEP 7: CREATE AND RUN SIMULATION
    print("\n7️⃣ SIMULATION CREATION")
    print("-"*30)
    
    # The Simulation class orchestrates everything
    runnable_simulation = simulation.Simulation(
        config=config,
        model=model,      # For agent reasoning
        embedder=embedder,  # For memory search
    )
    
    print("✅ Created simulation object")
    print("\nWhat happens when we run it:")
    print("1. Initializer creates formative memories for agents")
    print("2. Game master sets the scene")
    print("3. Each turn:")
    print("   a. Game master determines who acts next")
    print("   b. Acting entity observes the world")
    print("   c. Entity reasons using 'three key questions':")
    print("      - Who am I?")
    print("      - What happened recently?") 
    print("      - What should I do?")
    print("   d. Entity chooses an action")
    print("   e. Game master resolves action into world event")
    print("   f. All entities observe the event")
    print("   g. Memories are formed")
    print("4. Repeat until max_steps reached")
    
    # STEP 8: RUN THE SIMULATION
    print("\n8️⃣ RUNNING SIMULATION")
    print("-"*30)
    
    try:
        # This is where the magic happens!
        results_html = runnable_simulation.play()
        
        # Save results
        with open('setup_guide_results.html', 'w') as f:
            f.write(results_html)
        
        print("✅ Simulation complete!")
        print("📄 Results saved to setup_guide_results.html")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # STEP 9: UNDERSTANDING THE OUTPUT
    print("\n9️⃣ UNDERSTANDING THE OUTPUT")
    print("-"*30)
    
    print("The HTML file contains:")
    print("• Complete conversation transcript")
    print("• Memory logs for each agent")
    print("• Observation -> Reasoning -> Action cycle")
    print("• How the game master manages the world")
    
    print("\n✨ SIMULATION COMPLETE!")
    
    return runnable_simulation


# Additional helper to show how agents work internally
def explain_agent_architecture():
    """Explain how Concordia agents are built"""
    
    print("\n📚 HOW CONCORDIA AGENTS WORK")
    print("="*50)
    
    print("\n1. COMPONENT-BASED ARCHITECTURE")
    print("-"*30)
    print("Agents are built from modular components:")
    print("• Instructions: Define role and behavior")
    print("• Memory: Store and retrieve experiences")
    print("• Observation: Process incoming information")
    print("• Plan: Strategic thinking (optional)")
    print("• Question components: Contextual reasoning")
    print("• Act component: Generate responses")
    
    print("\n2. THE THREE KEY QUESTIONS")
    print("-"*30)
    print("Basic agents answer three questions:")
    print("• 'Who am I?' → Identity and goals")
    print("• 'What happened recently?' → Recent observations")
    print("• 'What should I do?' → Action selection")
    
    print("\n3. MEMORY SYSTEM")
    print("-"*30)
    print("• Semantic search using embeddings")
    print("• Importance scoring for memories")
    print("• Formative memories shape personality")
    print("• Recent memories guide current actions")
    
    print("\n4. OBSERVATION → ACTION CYCLE")
    print("-"*30)
    print("1. Receive observation from game master")
    print("2. Store observation in memory")
    print("3. Retrieve relevant memories")
    print("4. Answer contextual questions")
    print("5. Generate action based on context")
    print("6. Game master resolves action")
    
    print("\n5. GAME MASTER ROLE")
    print("-"*30)
    print("• Maintains world state")
    print("• Determines action order")
    print("• Resolves actions into events")
    print("• Broadcasts events to all agents")
    print("• Decides when simulation ends")


if __name__ == '__main__':
    # Run the setup guide
    setup_concordia_simulation()
    
    # Explain the architecture
    explain_agent_architecture()