import re

def split_assembly_line(line):
    pattern = r'([^\s"\']+)|(["\'])(.*?)(\2)'
    tokens = [match[0] if match[0] else match[2] for match in re.findall(pattern, line)]
    return tokens

# Example usage:
line = "times 31 db \"$\""
tokens = split_assembly_line(line)
print(tokens)