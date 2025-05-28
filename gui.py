import os
from component.TypeMyWord import TypeMyWord


def list_csv_files(directory):
    """List all CSV files in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith(".csv")]


def main():
    words_dir = os.path.join(os.getcwd(), "words")
    if not os.path.exists(words_dir):
        print(f"Error: Directory '{words_dir}' does not exist.")
        return

    csv_files = list_csv_files(words_dir)

    if not csv_files:
        print(f"No CSV files found in '{words_dir}'.")
        return

    if len(csv_files) == 1:
        selected_csv = os.path.join(words_dir, csv_files[0])
        print(f"Automatically selected the only CSV file: {csv_files[0]}")
    else:
        print("Available CSV files:")
        for idx, file in enumerate(csv_files, start=1):
            print(f"{idx}. {file}")
        try:
            choice = int(input("Select a file by number: ")) - 1
            if choice < 0 or choice >= len(csv_files):
                print("Invalid selection.")
                return
            selected_csv = os.path.join(words_dir, csv_files[choice])
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

    # Run the application with the selected CSV file
    TypeMyWord(selected_csv=selected_csv).run()


if __name__ == "__main__":
    main()
