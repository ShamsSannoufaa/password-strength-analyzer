import os

def merge_files(input_folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        for line in infile:
                            outfile.write(line)
                except:
                    continue

merge_files("data/strong", "data/strong.txt")