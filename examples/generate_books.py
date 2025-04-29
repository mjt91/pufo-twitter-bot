"""Example script to demonstrate the ChatGPT generator usage."""

from pufo_twitter_bot.chatgpt_generator import ChatGPTGenerator


def main():
    # Initialize the generator
    generator = ChatGPTGenerator()

    # Generate 5 random book-author pairs
    books = generator.generate_pairs(count=5)

    # Print the results
    print("\nGenerated Books:")
    print("-" * 50)
    for book in books:
        print(f"{book.title} - {book.author.name}")

    # Save to file
    generator.save_to_file(books, "generated_books.json")
    print("\nResults saved to 'generated_books.json'")


if __name__ == "__main__":
    main()
