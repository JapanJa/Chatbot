import json

def load_data(file_path):
    """Load conversation data from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data.get("conversations", [])

def save_data(file_path, conversations):
    """Save conversation data to a JSON file."""
    data = {"conversations": conversations}
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_response(question, conversations):
    """Get response from the chatbot."""
    max_similarity = 0
    best_response = ""
    for conv in conversations:
        similarity = similar(question.lower(), conv["question"].lower())
        if similarity >= max_similarity:
            max_similarity = similarity
            best_response = conv["answer"]
    if max_similarity < 0.9:  # Adjust threshold as needed
        return None
    return best_response

def similar(a, b):
    """Calculate similarity between two strings."""
    return sum(1 for x, y in zip(a, b) if x == y) / max(len(a), len(b))

def main():
    file_path = "conversation_data.json"
    conversations = load_data(file_path)

    print("Welcome! Ask me anything or type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            save_data(file_path, conversations)
            print("Goodbye!")
            break

        if user_input.lower() == 'skip':
            print("ChatBot: I'm not sure about that. Moving to the next question.")
            continue

        response = get_response(user_input, conversations)
        if response is None:
            new_response = input("ChatBot: I'm not sure about that. What should I respond? ")
            if new_response.lower() != 'skip':
                conversations.append({"question": user_input, "answer": new_response})
                print("ChatBot: Thanks for teaching me!")
            else:
                print("ChatBot: Skipping...")
        else:
            print("ChatBot:", response)

if __name__ == "__main__":
    main()
