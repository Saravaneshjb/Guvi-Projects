import re

def convert_duration(duration_str):
    if not isinstance(duration_str, str):
        return None  # Return None if duration_str is not a string

    # Regular expression to extract minutes and seconds from the duration string
    duration_regex = r'PT(\d+)M(\d+)S'
    match = re.match(duration_regex, duration_str)
    
    if match:
        # Extract minutes and seconds from the match object
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        
        # Calculate total duration in minutes
        total_minutes = minutes + seconds / 60
        
        # Round off to two decimal points
        total_minutes_rounded = round(total_minutes, 2)
        
        return total_minutes_rounded
    else:
        return None

# Example usage
# duration_str = 'PT2M10S'
# total_minutes_rounded = convert_duration(duration_str)
# print(total_minutes_rounded)  # Output: 2.17