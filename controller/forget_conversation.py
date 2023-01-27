import logging
from datetime import datetime

# configure logging
logging.basicConfig(filename='forgotten_memories.log', level=logging.INFO,
                    format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def forget_conversation(
        conversation_file_path: str = "conversation.txt",
        forgotten_file_path: str = "conversation_forgotten.txt") -> None:
    """Moves the first half of the conversation.txt contents into conversation_forgotten.txt"""
    # Open the conversation.txt file
    with open(conversation_file_path, "r", encoding='utf-8') as file:
        # Read all the lines in the file
        lines = file.readlines()
        # Calculate the number of lines in the file
        num_lines = len(lines)
        logging.info("Number of lines in the file: %s", num_lines)

        # Get the first half of the lines
        first_half = lines[:num_lines//2]

        # Open a new file called conversation_forgotten.txt
        with open(forgotten_file_path, "a", encoding='utf-8') as new_file:
            # Write the first half of the lines to the new file
            for line in first_half:
                new_file.write(line)

        # Remove the first half of the lines from the original file
        with open(conversation_file_path, "w", encoding='utf-8') as file:
            for line in lines[num_lines//2:]:
                file.write(line)

    logging.info(
        "The first half of the lines have been moved and removed from conversation.txt")


if __name__ == '__main__':
    forget_conversation()
