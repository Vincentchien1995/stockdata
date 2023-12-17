import os
from urllib.request import urlopen

# stock list
symbols = ['GOOG', 'TSLA', 'AAPL']

# Folders for data download and output
download_folder = 'data'
output_folder = 'output'

# Create folders
os.makedirs(download_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Download symbols
for symbol in symbols:
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=1587042293&period2=1618578293&interval=1d&events=history&includeAdjustedClose=true'
    local_path = os.path.join(download_folder, f'{symbol}.csv')
    with urlopen(url) as response, open(local_path, 'wb') as file:
        file.write(response.read())

# read csv and add new columns for calculating the percentage change between Close and Open price
    output_lines = []
    with open(local_path, 'r') as file:
        header = file.readline().strip() + ',Change\n'
        output_lines.append(header)

        for line in file:
            columns = line.strip().split(',')
            try:
                open_price = float(columns[1])
                close_price = float(columns[4])
                change = (close_price - open_price) / open_price
                output_lines.append(line.strip() + f',{change:.4f}\n')
            except ValueError:
                print(f"error：{line}")

    # save new data to output file
    output_file_path = os.path.join(output_folder, f'{symbol}_processed.csv')
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(output_lines)
