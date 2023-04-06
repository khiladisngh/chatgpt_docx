import random
import logging
from termcolor import colored
import pyperclip

# Prompt database
prompts = [
    "Write {num_facts} {adjective} {importance} facts about {topic}",
    "Give me {num_facts} {adjective} {importance} facts about {topic}",
    "Tell me {num_facts} {adjective} {importance} facts about {topic}",
    "What are {num_facts} {adjective} {importance} facts about {topic}",
    "Share {num_facts} {adjective} {importance} facts about {topic}",
    "Enlighten me with {num_facts} {adjective} {importance} facts about {topic}",
]

# Default values
default_topic = "Cars"
default_adjective = "interesting"
default_num_facts = 10
default_format = "list"
default_importance = "random"
default_category = None
default_simplify = False

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger()


def generate_prompt(topic, num_facts, adjective=default_adjective, format_=default_format, importance=default_importance, category=default_category, simplify=default_simplify):
    try:
        # Choose a random prompt from the database
        prompt = random.choice(prompts)

        # Fill in the variables
        prompt = prompt.format(
            topic=topic,
            num_facts=num_facts,
            adjective=adjective,
            importance=importance,
            category=category,
        )

        # Add optional parts
        if format_:
            prompt += f" in the format: {format_}"
        if simplify:
            prompt += "\nSimplify the text."
        else:
            prompt += "\nDon't simplify the text."

        return prompt
    except Exception as e:
        logger.error(colored(f"Error generating prompt: {str(e)}", "red"))
        raise


def main():
    try:
        # Get user input
        topic = input(
            f"Enter a topic (default: '{default_topic}'): ") or default_topic
        adjective = input(
            f"Enter an adjective (default: '{default_adjective}'): ") or default_adjective
        num_facts = input(
            f"Enter the number of facts (default: {default_num_facts}): ") or default_num_facts
        format_ = input(
            f"Enter the format (default: '{default_format}'): ") or default_format
        importance = input(
            f"Enter the importance (default: '{default_importance}'): ") or default_importance
        category = input(
            f"Enter the category (default: '{default_category}'): ") or default_category
        simplify = input(
            f"Simplify the text? (y/n) (default: {'y' if default_simplify else 'n'}): ").lower() == 'y'

        # Generate prompt
        prompt = generate_prompt(
            topic, num_facts, adjective, format_, importance, category, simplify)

        # Copy prompt to clipboard
        pyperclip.copy(prompt)

        # Print prompt
        logger.info(colored(f"\nGenerated prompt:\n{prompt}", "green"))
        logger.info(
            colored("The prompt has been copied to the clipboard.", "green"))
    except KeyboardInterrupt:
        # Handle user interrupt (Ctrl+C)
        logger.warning(colored("\nUser interrupt.", "yellow"))
    except Exception as e:
        logger.error(colored(f"\nError: {str(e)}", "red"))


if __name__ == "__main__":
    main()
