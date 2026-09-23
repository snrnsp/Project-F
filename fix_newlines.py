path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Fix: join broken string literals caused by literal newlines inside C# strings
# We need to find lines where a string is opened but not closed, and the next line continues it
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Check if this is a speechStyle or profileText line with a broken string
    # Pattern: the line has an odd number of unescaped quotes (string not closed)
    stripped = line.rstrip('\r\n')
    
    # Count quotes (simple heuristic: if line ends mid-string)
    # Look for pattern like: speechStyle = "text\n  (actual newline breaks the string)
    if i + 1 < len(lines):
        # Check if current line has an unclosed string by looking for specific field patterns
        for field in ['speechStyle = "', 'profileText.text =']:
            if field in stripped:
                # Check if the string constant is properly terminated
                # Count double quotes after the field assignment
                pass
        
        # More direct approach: if current line's last non-whitespace char suggests broken string
        # and next line looks like continuation
        next_stripped = lines[i+1].rstrip('\r\n').strip() if i+1 < len(lines) else ''
        
        # Detect broken C# string: line with unclosed " that continues on next line
        # Count quotes in the line (excluding escaped ones)
        temp = stripped.replace('\\"', '')
        quote_count = temp.count('"')
        
        if quote_count % 2 == 1 and not stripped.rstrip().endswith(';') and not stripped.rstrip().endswith('{') and not stripped.rstrip().endswith('}'):
            # This line has an unclosed string - merge with next line using \n
            merged = stripped + '\\n' + lines[i+1].rstrip('\r\n').strip()
            fixed_lines.append(merged + '\n')
            i += 2
            continue
    
    fixed_lines.append(line)
    i += 1

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(fixed_lines)

print(f'Fixed {len(lines) - len(fixed_lines)} broken lines')
