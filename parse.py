from bs4 import BeautifulSoup
import os

def process_html_file(input_path, results_file):
    with open(input_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Convert HTML to TXT (UTF-8)
        text_content = soup.get_text()

        # Remove line returns and newlines
        text_content = text_content.replace('\n', '').replace('\r', '')

        # Replace specific text
        text_content = text_content.replace('FRELIH Polona', ' placeholder1 ')
        text_content = text_content.replace('Polona Frelih', ' placeholder2 ')

        # Find the positions of the placeholders
        placeholder1_pos = text_content.find('placeholder1')
        placeholder2_pos = text_content.find('placeholder2')

        # Remove anything before the first placeholder
        text_content = text_content[placeholder1_pos:]

        # Remove anything after the second placeholder
        text_content = text_content[:placeholder2_pos + len('placeholder2')]

        # Remove any newlines
        text_content = text_content.replace('\n', '')

        # Write the resulting content to the results file
        with open(results_file, 'a', encoding='utf-8') as output_file:
            output_file.write(text_content + '\n')

# Input and output directories
input_dir = 'DIR'
output_file = 'results.txt'

# Create results file or clear existing content
with open(output_file, 'w', encoding='utf-8'):
    pass

# Iterate through each HTML file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".html"):
        input_path = os.path.join(input_dir, filename)

        process_html_file(input_path, output_file)

print("HTML to TXT conversion and text processing completed. Results written to results.txt.")

