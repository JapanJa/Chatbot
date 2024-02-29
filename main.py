import json
from fuzzywuzzy import fuzz

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
        similarity = fuzz.partial_ratio(question.lower(), conv["question"].lower())
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = conv["answer"]
    if max_similarity < 70:  # Adjust threshold as needed
        return None
    return best_response

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

        response = get_response(user_input, conversations)
        if response is None:
            new_response = input("ChatBot: I'm not sure about that. What should I respond? ")
            conversations.append({"question": user_input, "answer": new_response})
            print("ChatBot: Thanks for teaching me!")
        else:
            print("ChatBot:", response)

if __name__ == "__main__":
    main()
