def format_time(seconds):
    # Convert seconds to hours, minutes, seconds, and milliseconds
    millis = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    # Format the time string for subtitles
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03d}"

#def chunk_text(text):
#    # Split the text by newline characters
#    lines = text.split('\n')
#
#    # Filter out blank lines
#    non_blank_lines = [line for line in lines if line.strip() != '']
#
#    return non_blank_lines

def remove_empty_lines(input_string):
    return "\n".join(line for line in input_string.splitlines() if line.strip())