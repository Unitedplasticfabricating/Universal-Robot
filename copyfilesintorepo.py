# This is a program that takes the programs from the usb drive\programs and copies them into local\programs
# and extracts them into origfilename_extracted.urp files
def main():
    user_input = input('Copy Journal? (Y/N): ')
    if isUserInputYes(user_input):
        copyJournal()
    
def isUserInputYes(input_string):
    # Convert input string to lowercase for case-insensitive comparison
    normalized_input = input_string.lower()
    # List of possible variations of "yes"
    yes_variations = ['yes', 'y']
    # Check if the normalized input is in the list of variations
    ret = normalized_input in yes_variations
    return ret
    
def copyJournal():
    print('now would copy journal')




if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    main()