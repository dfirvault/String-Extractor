import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)
    print()

def select_folder_with_picker(prompt):
    """Open a folder picker dialog for Windows"""
    print(f"\n{prompt}")
    print("A folder picker window will open. Please select a folder.")
    print("(The folder picker may appear behind this window)")
    input("\nPress Enter to open folder picker...")
    
    # Initialize Tkinter root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring to front
    
    # Open folder picker dialog
    folder_path = filedialog.askdirectory(
        title=prompt,
        mustexist=True
    )
    
    root.destroy()  # Close Tkinter
    
    if folder_path:
        print(f"Selected folder: {folder_path}")
        return folder_path
    else:
        print("No folder selected.")
        return None

def extract_ascii_text(file_path):
    """Extract ASCII characters from a file"""
    try:
        # Try to read with different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                    content = file.read()
                break
            except (UnicodeDecodeError, LookupError):
                continue
        else:
            # If all encodings fail, use binary mode
            with open(file_path, 'rb') as file:
                content = file.read().decode('ascii', errors='ignore')
        
        # Filter to keep only ASCII characters (0-127)
        ascii_content = ''.join(char for char in content if ord(char) < 128)
        
        # Remove control characters (except newline, tab, carriage return, form feed)
        cleaned_content = ''.join(
            char for char in ascii_content 
            if ord(char) >= 32 or char in '\n\t\r\f'
        )
        
        return cleaned_content.strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def process_files(source_folder, output_folder):
    """Process all files in the source folder and its subfolders"""
    print(f"\n{'='*60}")
    print("PROCESSING FILES")
    print("=" * 60)
    print(f"Source: {source_folder}")
    print(f"Output: {output_folder}")
    print("-" * 60)
    
    processed_count = 0
    error_count = 0
    skipped_count = 0
    
    # Walk through all files in source folder
    for root, dirs, files in os.walk(source_folder):
        # Calculate relative path for output
        rel_path = os.path.relpath(root, source_folder)
        if rel_path == ".":
            rel_path = ""
        
        # Create corresponding output directory
        output_dir = os.path.join(output_folder, rel_path)
        os.makedirs(output_dir, exist_ok=True)
        
        for file in files:
            source_file_path = os.path.join(root, file)
            
            # Generate output filename (original_name + .txt)
            output_filename = f"{file}.txt"
            output_file_path = os.path.join(output_dir, output_filename)
            
            # Skip if output file already exists (avoid overwriting)
            if os.path.exists(output_file_path):
                print(f"⚠ Skipping (already exists): {file} -> {output_filename}")
                skipped_count += 1
                continue
            
            # Extract ASCII text
            ascii_text = extract_ascii_text(source_file_path)
            
            if ascii_text:
                try:
                    with open(output_file_path, 'w', encoding='ascii') as output_file:
                        output_file.write(ascii_text)
                    
                    # Show file size info
                    original_size = os.path.getsize(source_file_path)
                    new_size = len(ascii_text.encode('ascii'))
                    
                    print(f"✓ Processed: {file} -> {output_filename}")
                    print(f"  Size: {original_size:,} bytes → {new_size:,} bytes")
                    processed_count += 1
                    
                except Exception as e:
                    print(f"✗ Error saving {file}: {e}")
                    error_count += 1
            else:
                # Create empty file if no ASCII content
                try:
                    with open(output_file_path, 'w', encoding='ascii') as output_file:
                        pass
                    print(f"⚠ Empty ASCII: {file} -> {output_filename} (created empty file)")
                    processed_count += 1
                except Exception as e:
                    print(f"✗ Error creating empty file for {file}: {e}")
                    error_count += 1
    
    return processed_count, error_count, skipped_count

def main_menu():
    """Display the main menu"""
    clear_screen()
    print_header("ASCII Text Extractor")
    
    print("1. Select source folder and extract ASCII text")
    print("2. Show detailed instructions")
    print("3. Exit program")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        extract_ascii_menu()
    elif choice == '2':
        show_instructions()
    elif choice == '3':
        print("\nThank you for using ASCII Text Extractor!")
        sys.exit(0)
    else:
        print("\nInvalid choice. Please try again.")
        input("\nPress Enter to continue...")
        main_menu()

def extract_ascii_menu():
    """Menu for extracting ASCII text"""
    clear_screen()
    print_header("Extract ASCII Text")
    
    # Get source folder using picker
    source_folder = select_folder_with_picker("Select SOURCE folder containing files to process")
    
    if not source_folder:
        print("\nNo source folder selected. Returning to main menu.")
        input("\nPress Enter to continue...")
        main_menu()
        return
    
    # Create default output folder name
    folder_name = os.path.basename(source_folder)
    default_output = os.path.join(os.path.dirname(source_folder), f"{folder_name}_ascii")
    
    print(f"\nDefault output folder will be: {default_output}")
    
    # Ask if user wants to select output folder or use default
    print("\nOutput folder options:")
    print("1. Use default folder")
    print("2. Select custom folder")
    print()
    
    output_choice = input("Choose option (1 or 2): ").strip()
    
    if output_choice == '2':
        output_folder = select_folder_with_picker("Select OUTPUT folder for ASCII text files")
        if not output_folder:
            print("\nNo output folder selected. Using default.")
            output_folder = default_output
    else:
        output_folder = default_output
    
    # Ask about overwriting existing files
    print("\n" + "="*60)
    print("PROCESSING OPTIONS")
    print("=" * 60)
    print("If output files already exist:")
    print("1. Skip existing files (recommended)")
    print("2. Overwrite existing files")
    print()
    
    overwrite_choice = input("Choose option (1 or 2): ").strip()
    skip_existing = (overwrite_choice != '2')
    
    if skip_existing:
        print("\n✓ Will skip existing files")
    else:
        print("\n⚠ WARNING: Will overwrite existing files")
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Final confirmation
    print(f"\n{'='*60}")
    print("CONFIRM PROCESSING")
    print("=" * 60)
    print(f"Source folder: {source_folder}")
    print(f"Output folder: {output_folder}")
    print(f"Skip existing: {'Yes' if skip_existing else 'No (overwrite)'}")
    print(f"Files will be renamed: filename.ext → filename.ext.txt")
    print()
    
    confirm = input("Start processing? (Y/n): ").strip().lower()
    
    if confirm != 'n':
        # Process the files
        processed, errors, skipped = process_files(source_folder, output_folder)
        
        print(f"\n{'='*60}")
        print("PROCESSING COMPLETE")
        print("=" * 60)
        print(f"✓ Files processed successfully: {processed}")
        if skipped > 0:
            print(f"⏭ Files skipped (already existed): {skipped}")
        if errors > 0:
            print(f"✗ Files with errors: {errors}")
        print(f"📁 Output location: {output_folder}")
        print(f"📁 Output naming: original_name.ext → original_name.ext.txt")
    
    input("\nPress Enter to return to main menu...")
    main_menu()

def show_instructions():
    """Display program instructions"""
    clear_screen()
    print_header("INSTRUCTIONS")
    
    print("📁 ASCII TEXT EXTRACTOR")
    print()
    print("WHAT THIS PROGRAM DOES:")
    print("• Scans through ALL files in selected folder and subfolders")
    print("• Extracts only ASCII text (characters 0-127)")
    print("• Saves ASCII text to new .txt files")
    print("• Replicates original folder structure")
    print("• Preserves original filenames (adds .txt extension)")
    print()
    print("📝 NAMING CONVENTION:")
    print("  Original:  document.pdf")
    print("  Output:    document.pdf.txt")
    print()
    print("  Original:  data.xml")
    print("  Output:    data.xml.txt")
    print()
    print("  Original:  script.py")
    print("  Output:    script.py.txt")
    print()
    print("🎯 KEY FEATURES:")
    print("• Windows folder picker interface")
    print("• Multiple encoding support (UTF-8, Latin-1, etc.)")
    print("• Option to skip or overwrite existing files")
    print("• Shows file size before/after conversion")
    print("• Original files are NEVER modified")
    print()
    print("⚠ NOTES:")
    print("• Non-ASCII characters are removed (é, ñ, 汉字, emojis, etc.)")
    print("• Some binary files may produce empty or garbled output")
    print("• The folder picker may appear behind other windows")
    print()
    print("💡 TIPS:")
    print("• You can process any folder with text-based files")
    print("• Default output is '[original_folder]_ascii'")
    print("• Empty .txt files are created for files with no ASCII content")
    
    input("\nPress Enter to return to main menu...")
    main_menu()

def check_dependencies():
    """Check if required modules are available"""
    try:
        import tkinter
        return True
    except ImportError:
        print("ERROR: Tkinter is not installed.")
        print("This program requires Tkinter for the folder picker.")
        print("\nTo install Tkinter:")
        print("1. Windows: It should be included with Python")
        print("2. If not, reinstall Python and check 'tcl/tk' option")
        return False

if __name__ == "__main__":
    # Check for Tkinter dependency
    if not check_dependencies():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
