#!/usr/bin/env python3
import sys
import traceback

try:
    print("Starting game debug...")
    sys.path.append('code')
    
    print("Importing jogo...")
    from jogo import Jogo
    
    print("Creating game instance...")
    jogo = Jogo()
    
    print("Game created successfully!")
    print(f"Initial state: {jogo.estado}")
    
    print("Starting game loop...")
    jogo.run()
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("Full traceback:")
    traceback.print_exc()
    input("Press Enter to exit...")