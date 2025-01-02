from conversation import ConversationSystem
import time

def run_conversation_tests():
    eda = ConversationSystem()
    
    # Define test conversations with varied phrasing and follow-ups
    test_conversations = [
        # Greetings
        ("Hello there!", None),
        ("Good morning Eda", None),
        ("Hey, how's it going?", None),
        
        # Capabilities
        ("What are your features?", None),
        ("Tell me about what you can do", None),
        ("What services do you offer?", None),
        
        # Routine Management
        ("I need help with my daily schedule", None),
        ("How do I create a routine?", None),
        ("Can you remind me about my tasks?", None),
        ("What's the best way to manage my day?", None),
        
        # Task Organization
        ("I'm overwhelmed with my tasks", None),
        ("How do I prioritize my work?", None),
        ("Can you help me break down this project?", None),
        ("What's the best way to organize my tasks?", None),
        
        # Social Skills
        ("I struggle with conversations", None),
        ("How do I make small talk?", None),
        ("Can you help me practice social interactions?", None),
        ("What should I do in social situations?", None),
        
        # Progress Tracking
        ("How can I track my achievements?", None),
        ("I want to see my progress", None),
        ("Can you show me how I'm doing?", None),
        ("How do I know if I'm improving?", None),
        
        # Transitions
        ("I have trouble switching tasks", None),
        ("How do I handle transitions better?", None),
        ("Can you help me move between activities?", None),
        ("What's the best way to change tasks?", None),
        
        # General Help
        ("I need some assistance", None),
        ("Can you help me with something?", None),
        ("What support can you provide?", None),
        
        # Closing
        ("Thanks for your help", None),
        ("Appreciate your assistance", None),
        ("Goodbye for now", None),
        ("See you later", None)
    ]
    
    # Run test conversations
    for i, (user_input, expected_response) in enumerate(test_conversations):
        print(f"\nTest {i+1}:")
        print(f"You: {user_input}")
        response = eda.get_response(user_input)
        print(f"Eda: {response}")
        
        # Pause briefly between conversations
        time.sleep(1)
        
        # Learn from the conversation
        eda.learn_from_conversation(user_input, response)
    
    print("\nTest conversations completed. Eda's knowledge has been updated.")
    eda.show_progress()

if __name__ == "__main__":
    # Run multiple iterations to rapidly develop Eda
    for i in range(5):  # Run 5 iterations
        print(f"\n=== Running conversation iteration {i+1} ===")
        run_conversation_tests()
        time.sleep(2)  # Brief pause between iterations
