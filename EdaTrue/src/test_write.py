try:
    with open('Eda/Eda_personality.py', 'a') as file:
        file.write("\n# Test write operation successful.")
        print("Write operation completed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
