import re

# So far: remove oxford commas,contract pronouns and verbs, and convert markdown titles into sentence case. 

replacement_rules_contractions = {
    r'\bwe are\b': "we're",
    r'\bI am\b': "I'm",
    r'\byou are\b': "you're",
    r'\bwe will\b': "we'll",
    r'\byou will\b': "you'll",
    r'\byou would\b': "you'd",
    r'\bit is\b': "it's",
}

replacement_rules_commas = {
    r'\b, and\b': " and",
    r'\b, or\b': " or",
    # Add more rules as needed (pattern: replacement)
}

def replace_with_rules(file_path, replacement_rules):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for pattern, replacement in replacement_rules.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def replace_pronoun_verbs(file_path):
    replace_with_rules(file_path, replacement_rules_contractions)

def remove_commas_before_and_or(file_path):
    replace_with_rules(file_path, replacement_rules_commas)

def sentence_case(s):
    return s[:1].upper() + s[1:].lower()

def change_headings_to_sentence_case(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()

    updated_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')  # remove trailing newline
        match = re.match(r"(#+)(\s+)(.*)", line)
        if match:
            hashes, whitespace, heading_text = match.groups()
            updated_line = f"{hashes}{whitespace}{sentence_case(heading_text)}\n"
            updated_lines.append(updated_line)
            # Ensure there's only one blank line after the heading
            if i+1 < len(lines) and lines[i+1].strip() == '':
                i += 1  # skip the blank line
            updated_lines.append('\n')  # Add a blank line after the heading
        elif line.startswith('- ') or re.match(r'\d+\.\s+.*', line):
            # For bullet points and numbered lists, keep the lines as they are
            updated_lines.append(line + '\n')
        else:
            updated_lines.append(line + '\n')
            # Ensure there's only one blank line after non-heading and non-list lines
            if i+1 < len(lines) and lines[i+1].strip() == '':
                i += 1  # skip the blank line
        i += 1

    with open(file_name, "w") as file:
        for line in updated_lines:
            file.write(line)
