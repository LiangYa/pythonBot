def chatbot(user_input):
    print("Hi, I'm your AI assistant. How can I help you today?")
    while True:
        # user_input = input().lower()
        if "yes" in user_input:
            print("Great!")
        elif "no" in user_input:
            print("I'm sorry to hear that. Is there anything else I can help you with?")
        else:
            print("I'm sorry, I didn't understand. Can you please rephrase?")


def test_chatbot():
    expected_responses = {
        "yes": "Great!",
        "no": "I'm sorry to hear that. Is there anything else I can help you with?",
        "hello": "I'm sorry, I didn't understand. Can you please rephrase?",
        "": "I'm sorry, I didn't understand. Can you please rephrase?",
    }
    for user_input, expected_response in expected_responses.items():
        print(f"User: {user_input}")
        response = chatbot(user_input)
        assert response == expected_response
        print(f"Bot: {response}")
    print("All tests passed!")


if __name__ == '__main__':
    test_chatbot()
    pass
