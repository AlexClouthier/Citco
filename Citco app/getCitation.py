import pandas as pd
from scholarly import scholarly

def main():
    input_file = "Name3.csv"
    output_file = "scholar_citations.csv"

    try:
        # Load names from the CSV file
        df = pd.read_csv(input_file, encoding="latin1")
        names = df['Name'].unique().tolist()  # Assuming the column is named "Name"
    except Exception as e:
        print(f"Failed to read input file: {e}")
        return

    results = []

    for name in names:
        try:
            search_query = scholarly.search_author(name)
            author = next(search_query, None)
            if author:
                scholarly.fill(author)
                citations = author.get('citedby', 0)
                print(f"{name}: {citations} citations")
                results.append([name, citations])
            else:
                print(f"No author found for: {name}")
        except Exception as e:
            print(f"Error processing {name}: {e}")

    try:
        # Save the results to a new CSV file
        output_df = pd.DataFrame(results, columns=["Name", "CitationsCounts"])
        output_df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Failed to write output file: {e}")

if __name__ == "__main__":
    main()
