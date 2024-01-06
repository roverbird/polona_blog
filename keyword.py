import re
import os
import yaml

def tag_keywords_in_md_files(directory_path, keywords_file_path):
    # Load keywords from the file
    with open(keywords_file_path, 'r', encoding='utf-8') as keywords_file:
        keywords = [line.strip() for line in keywords_file]

    # Iterate through MD files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".md"):
            file_path = os.path.join(directory_path, filename)

            with open(file_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            # Split YAML frontmatter and content
            yaml_match = re.match(r'---\n(.*?\n)---\n\n(.*)', md_content, re.DOTALL)
            if yaml_match:
                yaml_frontmatter = yaml_match.group(1)
                md_text = yaml_match.group(2)

                # Load existing YAML data
                existing_data = yaml.safe_load(yaml_frontmatter) or {}

                # Check for keywords in the main text
                tags = []
                for keyword in keywords:
                    if re.search(rf'\b{re.escape(keyword)}\b', md_text, flags=re.IGNORECASE):
                        tags.append(keyword)

                # Add Tags field to existing data
                existing_data['Tags'] = tags

                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as updated_md_file:
                    updated_md_file.write("---\n\n")
                    updated_md_file.write(yaml.dump(existing_data, default_style="'", allow_unicode=True))
                    updated_md_file.write("---\n\n")
                    updated_md_file.write(md_text)

if __name__ == "__main__":
    out_directory = "OUT"
    keywords_file_path = "keywords.txt"  # Specify the path to your keywords file
    tag_keywords_in_md_files(out_directory, keywords_file_path)
