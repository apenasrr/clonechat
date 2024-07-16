def sanitize_string(string_input):
    """
    Sanitizes a given string by special characters, and
    spaces.

    Args:
        string_input (str): The original string to be sanitized.

    Returns:
        str: The sanitized string with special characters replaced by
            underscores, and excess spaces trimmed.
    """
    # Encode the string to utf-8 and decode it to handle special characters
    # properly
    str_encode_clean = string_input.encode("utf-8", errors="ignore").decode()

    # Iterate through each special character and replace it with an underscore
    str_removed_special_carac = str_encode_clean
    for c in r"!@#$%^&*()[]{};:,./<>?\|`'/\\~-=_+»":
        str_removed_special_carac = str_removed_special_carac.translate(
            {ord(c): "_"}
        )

    # Replace multiple consecutive spaces with a single underscore,
    # remove excess underscores at the beginning and end
    string_output = (
        str_removed_special_carac.replace(" ", "_")
        .replace("___", "_")
        .replace("__", "_")
        .strip("_")
        .replace("_-_", "-")
        .replace("_-", "-")
        .replace("-_", "-")
    )
    return string_output
