import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
dataset_path = r'C:\Users\19856\.vscode\extensions\ms-dotnettools.dotnet-interactive-vscode-1.0.5568010\resources\Resources\Eda\kagglehub\datasets\projjal1\human-conversation-training-data\versions\1\human_chat.txt'
data = pd.read_csv(dataset_path, delimiter="\t", header=None, names=["Conversation"])

# Split the conversations into two columns
# Split the conversations into two columns, handling cases where the delimiter might not be present
data[['Speaker', 'Message']] = data['Conversation'].str.split(': ', n=1, expand=True)

# Clean the data
data['Message'] = data['Message'].str.lower().str.replace('[^\\w\\s]', '', regex=True)  # Remove punctuation and convert to lowercase

# Create input-output pairs (example)
input_output_pairs = data[['Message']].copy()  # Adjust as necessary for your model

# Train-test split
train_data, test_data = train_test_split(input_output_pairs, test_size=0.2)

# Save the processed data
train_data.to_csv('train_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)

print("Preprocessing complete. Train and test data saved.")
