import pandas as pd
import os


# Configuration parameters - defined outside functions
NETWORK_FILES = [
    'normalized_eco_network.xlsx',
    'normalized_econ_network.xlsx',
    'normalized_soc_network.xlsx'
]

DEFAULT_WEIGHTS = [1, 1, 1]
DEFAULT_THRESHOLD = 0.01

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def combine_networks(result_dir, weights=None):
    """Combine three network tables by weighted summing normalized_value
    for the same (from_id, to_id) pairs.

    Args:
        result_dir (str): Relative path to the result directory
        weights (list, optional): Weight list for each file. 
            Defaults to DEFAULT_WEIGHTS.

    Returns:
        pd.DataFrame: Combined result DataFrame
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    # Convert relative path to absolute path
    abs_result_dir = os.path.join(SCRIPT_DIR, result_dir)

    # Read and combine data
    combined_df = None
    for i, file in enumerate(NETWORK_FILES):
        path = os.path.join(abs_result_dir, file)
        df = pd.read_excel(path)

        # Apply weight
        df['weighted_value'] = df['normalized_value'] * weights[i]

        if combined_df is None:
            combined_df = df[['from_id', 'to_id', 'weighted_value']]
        else:
            # Concatenate data
            combined_df = pd.concat([
                combined_df,
                df[['from_id', 'to_id', 'weighted_value']]
            ])

    # Sum weighted values for the same (from_id, to_id) pairs
    result = combined_df.groupby(['from_id', 'to_id'])[
        'weighted_value'
    ].sum().reset_index()
    result.rename(columns={'weighted_value': 'combined_value'}, inplace=True)

    return result


def filter_by_threshold(input_path, output_path, threshold):
    """Filter network data by threshold and rename columns.

    Args:
        input_path (str): Relative input file path (combined network data)
        output_path (str): Relative output file path
        threshold (float): Threshold value (required)

    Returns:
        pd.DataFrame: Filtered result DataFrame with renamed columns
    """
    # Convert relative paths to absolute paths
    abs_input_path = os.path.join(SCRIPT_DIR, input_path)
    abs_output_path = os.path.join(SCRIPT_DIR, output_path)

    df = pd.read_excel(abs_input_path)

    # Filter rows where combined_value > threshold
    filtered_df = df[df['combined_value'] > threshold]

    # Rename columns to source, target, weight
    filtered_df = filtered_df.rename(columns={
        'from_id': 'source',
        'to_id': 'target',
        'combined_value': 'weight'
    })

    # Save result
    filtered_df.to_excel(abs_output_path, index=False)

    return filtered_df


if __name__ == '__main__':
    # Configuration parameters (relative paths)
    result_dir = 'result'
    weights = DEFAULT_WEIGHTS
    threshold = DEFAULT_THRESHOLD

    # Combine networks
    result_df = combine_networks(result_dir, weights)

    # Save combined result
    combined_path = 'result/combined_network.xlsx'
    abs_combined_path = os.path.join(SCRIPT_DIR, combined_path)
    result_df.to_excel(abs_combined_path, index=False)

    print(f"Combined! Result saved to {abs_combined_path}")
    print(f"Weights: {weights}")
    print(f"Combined edges: {len(result_df)}")

    # Filter by threshold
    edges_path = 'result/edges.xlsx'
    filtered_df = filter_by_threshold(combined_path, edges_path, threshold)

    abs_edges_path = os.path.join(SCRIPT_DIR, edges_path)
    print(f"\nFiltered! Result saved to {abs_edges_path}")
    print(f"Threshold: {threshold}")
    print(f"Filtered edges: {len(filtered_df)}")
    print(f"Filter ratio: {len(filtered_df)/len(result_df)*100:.2f}%")

    print("\nTop 10 rows after filtering:")
    print(filtered_df.head(10))
