
import nltk
import random
import json
import os
from datetime import datetime
from nltk.chat.util import Chat, reflections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ConversationSystem:
    def __init__(self):
        # Load or create conversation database
        self.conversation_db = "conversation_db.json"
        self.history_db = "conversation_history.json"
        self.knowledge_base = "knowledge_base.json"
        self.context = {
            'current_topic': None,
            'previous_topics': [],
            'last_response': None
        }
        self.pairs = self.load_conversation_data()
        self.knowledge = self.load_knowledge_base()
        
        # Initialize chatbot
        self.chatbot = Chat(self.pairs, reflections)
        
        # Download NLTK data
        nltk.download('punkt', quiet=True)
        
        # Initialize conversation history
        self.conversation_history = []

    def load_knowledge_base(self):
        """Load the knowledge base from JSON file"""
        try:
            with open(self.knowledge_base, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Knowledge base file {self.knowledge_base} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding knowledge base file {self.knowledge_base}.")
            return {}

    def load_conversation_data(self):
        # Load base conversation patterns
        base_pairs = [
            [
                r"hi|hello|hey",
                ["Hello! How can I help you today?", "Hi there! What can I assist you with?"]
            ],
            [
                r"what does (.*) mean",
                ["Let me explain that for you.", "That phrase means..."]
            ],
            [
                r"I'm feeling (.*)",
                ["I understand. Let's work through this together.", "That sounds challenging. How can I help?"]
            ],
            [
                r"how do I (.*)",
                ["Here's how you might approach that:", "Let me help you with that."]
            ],
            [
                r"what can you do",
                [
                    "Here's what I can do to assist you:\n" +
                    "1. Daily Routine Management - Create and follow schedules\n" +
                    "2. Task Organization - Break down and track tasks\n" +
                    "3. Virtual Garden - Earn plants by completing activities\n" +
                    "4. Social Skills - Practice conversations and interactions\n" +
                    "5. Progress Tracking - Monitor your achievements\n" +
                    "Which feature would you like to know more about?"
                ]
            ],
            [
                r"1|daily routine|routine management|how can you help with routine management|help with routines|how.*routine",
                [
                    "For daily routines, I can help you:\n" +
                    "- Create visual schedules\n" +
                    "- Set reminders for tasks\n" +
                    "- Break down complex tasks\n" +
                    "- Manage transitions between activities\n" +
                    "Would you like to create a new routine or manage an existing one?"
                ]
            ],
            [
                r"transitions|transition management|manage transitions",
                [
                    "I can help with transitions between activities by:\n" +
                    "- Providing visual timers and countdowns\n" +
                    "- Offering transition warnings in advance\n" +
                    "- Breaking down the steps for each transition\n" +
                    "- Using visual schedules to show what's coming next\n" +
                    "Would you like help setting up transition support?"
                ]
            ],
            [
                r"2|task organization|tasks|how can you help with tasks|help with task organization",
                [
                    "For task organization, I can help you:\n" +
                    "- Break down large tasks into smaller steps\n" +
                    "- Set priorities for your tasks\n" +
                    "- Track your progress\n" +
                    "- Create checklists\n" +
                    "What tasks would you like help organizing?"
                ]
            ],
            [
                r"3|virtual garden|plants",
                [
                    "In your virtual garden, you can:\n" +
                    "- Earn plants by completing tasks\n" +
                    "- Watch your garden grow over time\n" +
                    "- Customize your garden layout\n" +
                    "- Track your progress through plant growth\n" +
                    "Would you like to check your garden or learn how to earn new plants?"
                ]
            ],
            [
                r"4|social skills|conversation",
                [
                    "For social skills, I can help you:\n" +
                    "- Practice conversations in different scenarios\n" +
                    "- Understand social cues and norms\n" +
                    "- Role-play social situations\n" +
                    "- Provide feedback on communication\n" +
                    "What specific social skill would you like to work on?"
                ]
            ],
            [
                r"5|progress tracking|achievements",
                [
                    "For progress tracking, I can help you:\n" +
                    "- Monitor your daily achievements\n" +
                    "- Track long-term goals\n" +
                    "- Visualize your progress\n" +
                    "- Celebrate milestones\n" +
                    "What would you like to track today?"
                ]
            ],
            [
                r"help",
                [
                    "Here's how I can assist you:\n" +
                    "1. Daily Routine Management - Create and follow schedules\n" +
                    "2. Task Organization - Break down and track tasks\n" +
                    "3. Virtual Garden - Earn plants by completing activities\n" +
                    "4. Social Skills - Practice conversations and interactions\n" +
                    "5. Progress Tracking - Monitor your achievements\n" +
                    "Which area would you like help with?"
                ]
            ],
            [
                r"routine management|schedule",
                [
                    "I can help you manage your daily routines by:",
                    "1. Creating visual schedules",
                    "2. Setting gentle reminders",
                    "3. Breaking tasks into smaller steps",
                    "4. Helping with transitions between activities",
                    "Would you like to create a new routine or manage an existing one?"
                ]
            ],
            [
                r"virtual garden|plants",
                [
                    "The virtual garden is a reward system where you can:",
                    "1. Earn plants by completing tasks",
                    "2. Watch your garden grow over time",
                    "3. Customize your garden layout",
                    "4. Track your progress through plant growth",
                    "Would you like to check your garden or learn how to earn new plants?"
                ]
            ],
            [
                r"social skills|conversation",
                [
                    "I can help with social skills by:",
                    "1. Practicing conversations in different scenarios",
                    "2. Explaining social cues and norms",
                    "3. Role-playing social situations",
                    "4. Providing feedback on communication",
                    "What specific social skill would you like to work on?"
                ]
            ],
            [
                r"bye|goodbye",
                ["Goodbye! Have a great day!", "Take care!"]
            ],
            [
                r"how are you|how's it going",
                ["I'm here and ready to help! How can I assist you today?"]
            ],
            [
                r"thank you|thanks",
                ["You're welcome! Let me know if there's anything else I can help with."]
            ],
            [
                r"good morning|good afternoon|good evening",
                ["Hello! I hope you're having a great day. How can I assist you?"]
            ],
            [
                r"how's the weather",
                ["I'm not connected to weather services, but I can help you plan your day based on your schedule!"]
            ],
            [
                r"(.*)",
                [
                    "I'm still learning. Could you explain that differently?",
                    "Let me think about that for a moment.",
                    "That's an interesting question. Let me consider it.",
                    "I'm working on understanding that better. Could you rephrase?",
                    "I'm processing that. Could you provide more details?"
                ]
            ]
        ]
        
        # Load learned conversations if they exist
        if os.path.exists(self.conversation_db):
            with open(self.conversation_db, 'r') as f:
                learned_pairs = json.load(f)
                base_pairs.extend(learned_pairs)
        
        return base_pairs

    def save_conversation(self, user_input, response):
        # Save new conversation patterns
        new_pair = [
            [r"(.*)" + user_input.lower() + "(.*)", [response]]
        ]
        
        # Save to conversation database
        if not os.path.exists(self.conversation_db):
            with open(self.conversation_db, 'w') as f:
                json.dump(new_pair, f)
        else:
            with open(self.conversation_db, 'r+') as f:
                data = json.load(f)
                data.extend(new_pair)
                f.seek(0)
                json.dump(data, f)
        
        # Save to conversation history
        self.conversation_history.append({
            'user': user_input,
            'eda': response,
            'timestamp': datetime.now().isoformat()
        })
        
        if not os.path.exists(self.history_db):
            with open(self.history_db, 'w') as f:
                json.dump(self.conversation_history, f)
        else:
            with open(self.history_db, 'r+') as f:
                data = json.load(f)
                data.extend(self.conversation_history)
                f.seek(0)
                json.dump(data, f)

    def learn_from_conversation(self, user_input, response):
        # Enhanced learning mechanism
        if "I'm still learning" not in response:
            # Save the conversation pattern
            self.save_conversation(user_input, response)
            
            # Analyze the conversation for potential new patterns
            words = user_input.lower().split()
            if len(words) > 3:  # Only learn from substantial inputs
                # Create variations of the pattern
                patterns = [
                    r"(.*)" + " ".join(words[-2:]) + "(.*)",  # Last two words
                    r"(.*)" + words[0] + "(.*)",             # First word
                    r"(.*)" + " ".join(words[:2]) + "(.*)"   # First two words
                ]
                
                # Save variations
                for pattern in patterns:
                    new_pair = [[pattern, [response]]]
                    if not os.path.exists(self.conversation_db):
                        with open(self.conversation_db, 'w') as f:
                            json.dump(new_pair, f)
                    else:
                        with open(self.conversation_db, 'r+') as f:
                            data = json.load(f)
                            data.extend(new_pair)
                            f.seek(0)
                            json.dump(data, f)

    def get_response(self, user_input):
        try:
            # First try to find a response in the knowledge base
            knowledge_response = self.query_knowledge_base(user_input)
            if knowledge_response:
                return knowledge_response
            
            # Fall back to the chatbot patterns
            response = self.chatbot.respond(user_input)
            
            # Add empathy for specific complex interactions
            if any(word in user_input.lower() for word in ['feel', 'mean', 'how', 'routine', 'garden', 'social']):
                if random.random() < 0.3:
                    response = self.add_empathy(response)
            return response
        except Exception as e:
            return "I'm having trouble understanding. Could you try again?"

    def query_knowledge_base(self, user_input):
        """Query the knowledge base for relevant information"""
        # Check QA pairs first
        for qa in self.knowledge['qa_pairs']:
            if qa['question'].lower() in user_input.lower():
                return qa['answer']
        
        # Check topics and facts
        for topic, keywords in self.knowledge['topics'].items():
            if any(keyword in user_input.lower() for keyword in keywords):
                if self.knowledge['facts'][topic]:
                    return random.choice(self.knowledge['facts'][topic])
        
        # Check specific categories
        for category in ['daily_living_skills', 'emotional_regulation', 
                        'executive_functioning', 'employment_skills']:
            if category in self.knowledge:
                for item in self.knowledge[category]:
                    if any(keyword in user_input.lower() 
                          for keyword in item.get('keywords', [])):
                        return self.format_knowledge_response(item)
        
        return None

    def format_knowledge_response(self, item):
        """Format knowledge base items into conversational responses"""
        if 'steps' in item:
            response = f"Here's how to {item['skill'].lower()}:\n"
            response += "\n".join(f"- {step}" for step in item['steps'])
            return response
        elif 'strategies' in item:
            response = f"Here are some strategies for {item['skill'].lower()}:\n"
            response += "\n".join(f"- {strategy}" for strategy in item['strategies'])
            return response
        return None

    def add_empathy(self, response):
        empathic_phrases = [
            "I understand.",
            "That sounds challenging.",
            "Let's work through this together.",
            "You're doing great.",
            "I'm here to help."
        ]
        return f"{random.choice(empathic_phrases)} {response}"
        
    def show_progress(self):
        """Display progress metrics"""
        # Count learned patterns
        if os.path.exists(self.conversation_db):
            with open(self.conversation_db, 'r') as f:
                learned_pairs = json.load(f)
                learned_count = len(learned_pairs)
        else:
            learned_count = 0
            
        # Show file locations
        print("\nData Files Location:")
        print(f"- Learned Patterns: {os.path.abspath(self.conversation_db)}")
        print(f"- Conversation History: {os.path.abspath(self.history_db)}")
            
        # Count conversation history
        if os.path.exists(self.history_db):
            with open(self.history_db, 'r') as f:
                history = json.load(f)
                history_count = len(history)
        else:
            history_count = 0
            
        # Calculate response accuracy
        if history_count > 0:
            successful_responses = sum(1 for entry in history 
                                    if "I'm still learning" not in entry['eda'])
            accuracy = (successful_responses / history_count) * 100
        else:
            accuracy = 0
            
        # Display progress report
        print("\n=== Eda's Progress Report ===")
        print(f"Learned Patterns: {learned_count}")
        print(f"Conversation History: {history_count} entries")
        print(f"Response Accuracy: {accuracy:.1f}%")
        print("============================\n")
