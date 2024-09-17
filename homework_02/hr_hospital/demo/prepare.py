import os
import pandas as pd


def process_csv_file(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Add quotes around each data entry
    df = df.map(lambda x: f"'{x}'")
    # print(df)
    # df = df.applymap(lambda x: f'"{x}"')

    # Define the new file name
    new_file_path = file_path.replace('.csv', 'New.csv')

    # Save the DataFrame to the new CSV file
    df.to_csv(file_path, index=False)

    print(f"Processed file saved as: {file_path}")


def main(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is a CSV
        if os.path.isfile(file_path) and file_name.lower().endswith('.csv'):
            print(f"Processing file: {file_path}")
            process_csv_file(file_path)
        else:
            print(f"Skipping file: {file_path}")


if __name__ == "__main__":
    # Specify the folder path where CSV files are located
    folder_path = '/home/user/newproject/repositories/lisivka/odoo_lsm/homework_02/hr_hospital/demo'  # Update this with your folder path
    main(folder_path)
