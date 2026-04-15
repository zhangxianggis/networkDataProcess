import os
from excel_processor import process_excel

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    # Input and output directories (relative paths)
    input_dir = 'input'
    output_dir = 'result'
    
    # Convert to absolute paths
    abs_input_dir = os.path.join(SCRIPT_DIR, input_dir)
    abs_output_dir = os.path.join(SCRIPT_DIR, output_dir)
    
    # Create output directory if it doesn't exist
    os.makedirs(abs_output_dir, exist_ok=True)
    
    # Get all Excel files
    excel_files = [f for f in os.listdir(abs_input_dir) if f.endswith('.xlsx')]
    
    if not excel_files:
        print("No Excel files found")
        return
    
    print(f"Found {len(excel_files)} Excel files, starting processing...\n")
    
    # Process each file
    for file_name in excel_files:
        input_path = os.path.join(abs_input_dir, file_name)
        output_file_name = 'normalized_' + file_name
        output_path = os.path.join(abs_output_dir, output_file_name)
        
        print(f"Processing file: {file_name}")
        try:
            original_count, filtered_count, min_val, max_val = process_excel(input_path, output_path)
            print(f"  Original rows: {original_count}")
            print(f"  Filtered rows: {filtered_count}")
            print(f"  Result saved to: {output_path}")
        except Exception as e:
            print(f"  Processing failed: {str(e)}")
        print()
    
    print("All files processed!")


if __name__ == '__main__':
    main()
