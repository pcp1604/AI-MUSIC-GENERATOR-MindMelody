#!/usr/bin/env python3
"""
AI Music Composer - Main Entry Point
A more user-friendly entry point to the AI Music Composer
"""

import sys
import subprocess
import os

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """Display the application header"""
    print("=" * 50)
    print("         AI MUSIC COMPOSER")
    print("         Created with Replit")
    print("=" * 50)
    print()

def show_menu():
    """Display the main menu and get user selection"""
    print("What would you like to do?")
    print()
    print("1. Generate a single composition with AI-suggested parameters")
    print("2. Create a composition with custom parameters")
    print("3. Generate compositions in multiple styles")
    print("4. Analyze an existing MIDI file")
    print("5. Try to play a MIDI file (may not work in Replit)")
    print("6. Exit")
    print()
    
    # In Replit environment, we might encounter EOF errors when reading input
    try:
        while True:
            try:
                choice = int(input("Enter your choice (1-6): "))
                if 1 <= choice <= 6:
                    return choice
                else:
                    print("Please enter a number between 1 and 6.")
            except ValueError:
                print("Please enter a valid number.")
    except EOFError:
        # In non-interactive environments, use option 1 by default
        print("\nNon-interactive environment detected. Using option 1 by default.")
        return 1

def run_command(command):
    """Run a shell command and wait for it to complete"""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    
    try:
        input("\nPress Enter to return to the main menu...")
    except EOFError:
        # In non-interactive environments, we can't wait for input
        print("\nNon-interactive environment detected. Continuing...")
        pass

def handle_generate_ai_suggested():
    """Generate a composition with AI-suggested parameters"""
    clear_screen()
    print("Generating a composition with AI-suggested parameters...")
    run_command("./run_composer.sh")

def handle_generate_custom():
    """Generate a composition with custom parameters"""
    clear_screen()
    print("Create a composition with custom parameters...")
    run_command("python main.py")

def handle_generate_multiple_styles():
    """Generate compositions in multiple styles"""
    clear_screen()
    print("Generating compositions in multiple styles...")
    run_command("./explore_styles.sh")

def handle_analyze_midi():
    """Analyze an existing MIDI file"""
    clear_screen()
    print("Analyze an existing MIDI file...")
    
    # List MIDI files
    print("Available MIDI files:")
    midi_files = []
    for file in os.listdir('.'):
        if file.endswith('.mid'):
            midi_files.append(file)
            print(f"- {file}")
    
    if not midi_files:
        print("No MIDI files found in the current directory.")
        try:
            input("\nPress Enter to return to the main menu...")
        except EOFError:
            pass
        return
    
    # Get file to analyze
    try:
        file_to_analyze = input("\nEnter the name of the file to analyze (or press Enter for ai_composition.mid): ")
    except EOFError:
        # In non-interactive environments, use default file
        print("\nNon-interactive environment detected. Using default file.")
        file_to_analyze = "ai_composition.mid"
        
    if not file_to_analyze:
        file_to_analyze = "ai_composition.mid"
    
    if not os.path.exists(file_to_analyze):
        print(f"File {file_to_analyze} does not exist.")
    else:
        run_command(f"python analyze_midi.py {file_to_analyze}")

def handle_play_midi():
    """Try to play a MIDI file"""
    clear_screen()
    print("Play a MIDI file (note: may not work in Replit environment)...")
    
    # List MIDI files
    print("Available MIDI files:")
    midi_files = []
    for file in os.listdir('.'):
        if file.endswith('.mid'):
            midi_files.append(file)
            print(f"- {file}")
    
    if not midi_files:
        print("No MIDI files found in the current directory.")
        try:
            input("\nPress Enter to return to the main menu...")
        except EOFError:
            pass
        return
    
    # Get file to play
    try:
        file_to_play = input("\nEnter the name of the file to play (or press Enter for ai_composition.mid): ")
    except EOFError:
        # In non-interactive environments, use default file
        print("\nNon-interactive environment detected. Using default file.")
        file_to_play = "ai_composition.mid"
        
    if not file_to_play:
        file_to_play = "ai_composition.mid"
    
    if not os.path.exists(file_to_play):
        print(f"File {file_to_play} does not exist.")
    else:
        run_command(f"python play_music.py {file_to_play}")

def main():
    """Main entry point for the application"""
    try:
        while True:
            clear_screen()
            show_header()
            choice = show_menu()
            
            if choice == 1:
                handle_generate_ai_suggested()
            elif choice == 2:
                handle_generate_custom()
            elif choice == 3:
                handle_generate_multiple_styles()
            elif choice == 4:
                handle_analyze_midi()
            elif choice == 5:
                handle_play_midi()
            elif choice == 6:
                print("Thank you for using AI Music Composer!")
                sys.exit(0)
    except KeyboardInterrupt:
        print("\nThank you for using AI Music Composer!")
        sys.exit(0)

if __name__ == "__main__":
    main()