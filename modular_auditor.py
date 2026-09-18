def get_valid_input():
    """
    Handles the prompt AND input validation.
 
    Takes: nothing.
    Returns:
        - an int, if the user entered a valid non-negative whole number
        - the string "quit", if the user wants to stop
        - None, if the entry was invalid (not a number, or negative)
          -- the caller decides what to do with an invalid entry.
    """