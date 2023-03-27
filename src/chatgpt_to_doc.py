import os
import openai
import docx


from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from termcolor import colored
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()


def save_to_doc_file(filename, title, content):
    doc = docx.Document()

    # Add title
    title_paragraph = doc.add_paragraph()
    title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    title_run = title_paragraph.add_run(title)
    title_run.bold = True
    title_run.font.size = Pt(14)
    doc.add_paragraph()

    # Add bullet points
    for line in content.split('\n'):
        bullet_paragraph = doc.add_paragraph(style='ListBullet')
        bullet_run = bullet_paragraph.add_run(line)
        bullet_run.font.size = Pt(12)

    doc.save(filename)


if __name__ == "__main__":
    # Get user input
    topic = input("Enter a topic: ")
    adjective = input("Enter an adjective (e.g., intriguing, funny, sad): ")
    num_facts = input("Enter the number of facts (e.g., 5, 10, 20): ")
    format_ = input(
        "Enter the format (e.g., list, paragraph, bullet points): ")
    importance = input(
        "Enter the importance (e.g., most important, least important, random): ")
    category = input(
        "Enter the category (e.g., history, nutrition, sports, uses, etc.): ")
    simplify = input("Simplify the text? (y/n): ")

    # Generate text
    prompt = f"Write {num_facts} {adjective} {importance} facts about {topic} in the {category} category in {format_} format:\n\n"
    if simplify == "y":
        prompt += "\nSimplify the text."

    generated_text = generate_text(prompt)

    # Remove blank lines
    lines = [line for line in generated_text.splitlines() if line.strip()
             ]  # filter out blank lines
    result = "\n".join(lines)

    # Save to doc file
    output_filename = "chatgpt_output.docx"
    save_to_doc_file(
        output_filename, f"{num_facts} {adjective.title()} {importance.title()} Facts About {topic.title()} ({category.title()})", result)

    # Print results
    print(colored(f"Generated text saved to {output_filename}\n", "green"))
    print("Generated content:\n")
    print(colored(generated_text, "cyan"))
