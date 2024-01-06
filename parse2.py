import os
import yaml
import re

from datetime import datetime

from bs4 import BeautifulSoup

def parse_source_date(source):
    match = re.match(r'([^\d]+), (\d{1,2})\.(\d{1,2})\.(\d{4})', source)
    if match:
        source_name, day, month, year = match.groups()
        date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}T01:00:00"
        leto = int(year)  # Extract the year as an integer
        return source_name.strip(), date_str, leto
    else:
        return source, "", None

def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title_element = soup.find('div', class_='naslov')
    main_text_element = soup.find('div', class_='besedilo')
    intro_element = soup.find('div', class_='uvod')

    # Check if the elements exist before accessing their text attributes
    title = title_element.text.strip() if title_element else ""
    main_text = main_text_element.text.strip() if main_text_element else ""
    intro = intro_element.text.strip() if intro_element else ""

    metadata = {}
    metadata_table = soup.find('table', bgcolor='#dae6ff')
    if metadata_table:
        rows = metadata_table.find_all('tr')
        for row in rows:
            key_element = row.find('td')
            value_element = row.find('td', class_='kategorizacija')

            if key_element and value_element:
                key = key_element.text.strip()
                value = value_element.text.strip()
                metadata[key] = value

    # Extracting values from nested tables
    nested_tables = soup.find_all('table', bgcolor='#dae6ff')[1:]  # Skip the first table
    for table in nested_tables:
        rows = table.find_all('tr')
        for row in rows:
            key_element = row.find('td')
            value_element = row.find('td', class_='kategorizacija')

            if key_element and value_element:
                key = key_element.text.strip()
                value = value_element.text.strip()
                metadata[key] = value

    # Extracting author from metadata
    author = metadata.get('Avtor', '')

    
    # Add slug field
    slug = re.sub(r'\W+', '-', title.lower())

    return {
        'title': title,
        'main_text': main_text,
        'author': author,
        'intro': intro,
        'metadata': metadata,
        'slug': slug
    }

def write_to_md(output_directory, file_name, data):
    md_content = "---\n\n"
    md_content += "Slug: \"{}\"\n\n".format(re.sub(r"^\W+|\W+$", "", data['slug']))
    md_content += "Title: \"{}\"\n\n".format(data['title'])
    md_content += "Description: \"{}\"\n\n".format(re.sub(r'\s+', ' ', data['intro']))

    # Parse source and date
    source, date, leto = parse_source_date(data['metadata'].get('Vir', ''))
    md_content += "Source:\n - {}\n\n".format(source)
    md_content += "Date: \"{}\"\n\n".format(date)
    md_content += "Leto:\n - '{}'\n\n".format(str(leto))

    md_content += "Author:\n - {}\n\n".format(data['author'])
    #md_content += "Section: \"{}\"\n\n".format(data['metadata'].get('Sekcija', ''))
    #md_content += "Edition: \"{}\"\n\n".format(data['metadata'].get('Izdaja', ''))
    #md_content += "Section: \"{}\"\n\n".format(re.sub(r'[\\n\\r"]', ' ', data['metadata'].get('Sekcija', '')))
    #md_content += "Edition: \"{}\"\n\n".format(re.sub(r'[\\n\\r"]', ' ', data['metadata'].get('Izdaja', '')))
    #md_content += "Page: \"{}\"\n\n".format(data['metadata'].get('Stran', ''))
    #md_content += "Udk: \"{}\"\n\n".format(data['metadata'].get('Udk', ''))
    #md_content += "People: \"{}\"\n\n".format(data['metadata'].get('Osebe', ''))

    # Write multi-value fields as lists
    for field in ['Osebe', 'Sekcija', 'Izdaja', 'Geo']:
        values = data['metadata'].get(field, '').split(',')
        if any(values):
            md_content += "{}:\n".format(field)
            for value in values:
                md_content += "  - {}\n".format(value.strip())

    # Format main_text to remove repeating whitespace
    main_text = re.sub(r'[^\S\n]+', ' ', data['main_text'])
    md_content += "---\n\n{}\n".format(main_text)

    output_file_path = os.path.join(output_directory, "{}.md".format(file_name))
    with open(output_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

def convert_html_files_to_md(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.html'):
            file_path = os.path.join(input_directory, file_name)
            
            # Read the content of the HTML file
            with open(file_path, 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()

            extracted_data = extract_data(html_content)
            write_to_md(output_directory, os.path.splitext(file_name)[0], extracted_data)

# Example usage
input_directory = 'DIR'
output_directory = 'OUT'
convert_html_files_to_md(input_directory, output_directory)


