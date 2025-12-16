#!/usr/bin/env python3
"""
C.L.A.I.R.E - Conversational Language AI Responsive Entity
Main entry point for the personal AI assistant
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.assistant import ClaireAssistant
from backend.core.config import load_config
from backend.ui.terminal_ui import TerminalUI
from backend.ui.gui import ClaireGUI


def setup_logging(config):
    """Configure logging"""
    log_level = config.get('logging', {}).get('level', 'INFO')
    log_file = config.get('logging', {}).get('file', 'logs/claire.log')
    
    # Create logs directory
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║      ██████╗██╗      █████╗ ██╗██████╗ ███████╗      ║
    ║     ██╔════╝██║     ██╔══██╗██║██╔══██╗██╔════╝      ║
    ║     ██║     ██║     ███████║██║██████╔╝█████╗        ║
    ║     ██║     ██║     ██╔══██║██║██╔══██╗██╔══╝        ║
    ║     ╚██████╗███████╗██║  ██║██║██║  ██║███████╗      ║
    ║      ╚═════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝      ║
    ║                                                       ║
    ║   Conversational Language AI Responsive Entity        ║
    ║            Your Personal AI Assistant                 ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Load configuration
    print("Loading configuration...")
    try:
        config = load_config()
    except FileNotFoundError:
        print("\n❌ Error: config.yaml not found!")
        print("Creating default config.yaml...")
        # Try to create from example
        try:
            import shutil
            example_path = Path(__file__).parent / "config.example.yaml"
            config_path = Path(__file__).parent / "config.yaml"
            if example_path.exists():
                shutil.copy(example_path, config_path)
                print("✅ Created config.yaml from example")
                config = load_config()
            else:
                print("Please copy config.example.yaml to config.yaml and fill in your settings.")
                print("\nRun: copy config.example.yaml config.yaml")
                return 1
        except Exception as e:
            print(f"Could not create config: {e}")
            print("Please copy config.example.yaml to config.yaml manually")
            return 1
    except Exception as e:
        print(f"\n❌ Error loading configuration: {e}")
        return 1
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    logger.info("Starting C.L.A.I.R.E...")
    
    # Initialize assistant
    print("Initializing Claire...")
    try:
        assistant = ClaireAssistant(config)
    except Exception as e:
        print(f"\n❌ Error initializing assistant: {e}")
        logger.error(f"Failed to initialize assistant: {e}", exc_info=True)
        return 1
    
    # Choose UI mode
    print("\nSelect interface mode:")
    print("1. Terminal (Text only)")
    print("2. GUI (Graphical interface)")
    print("3. Voice (Coming soon)")
    
    choice = input("\nEnter choice (1-2) [default: 1]: ").strip() or "1"
    
    try:
        if choice == "1":
            logger.info("Starting terminal UI")
            ui = TerminalUI(assistant)
            ui.run()
        elif choice == "2":
            logger.info("Starting GUI")
            ui = ClaireGUI(assistant)
            ui.run()
        else:
            print("Invalid choice. Starting terminal UI...")
            ui = TerminalUI(assistant)
            ui.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Claire is shutting down...")
        logger.info("User interrupted, shutting down")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Runtime error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
