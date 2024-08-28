def str_diff(str1, str2):
     # Ensure the keys have the same length
     if len(str1) != len(str2):
         return False
     # Count the number of differing characters
     differences = sum(1 for a, b in zip(str1, str2) if a != b)
     return differences
