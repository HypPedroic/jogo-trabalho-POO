!/usr/bin/env python3

print("Starting test...")

try:
    print("Importing pygame...")
    import pygame

    print("Pygame imported successfully")

    print("Initializing pygame...")
    pygame.init()
    print("Pygame initialized successfully")

    print("Creating screen...")
    screen = pygame.display.set_mode((832, 640))
    print("Screen created successfully")

    print("Importing menu...")
    from code.menu.menu import Menu

    print("Menu imported successfully")

    print("Creating menu...")
    menu = Menu(screen)
    print("Menu created successfully")

    print("All imports and initializations successful!")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()

finally:
    print("Test completed.")
