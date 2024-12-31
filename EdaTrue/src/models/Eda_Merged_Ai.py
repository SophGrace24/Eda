import pandas as pd
from transformers import pipeline
import torch  # Ensure PyTorch is imported
from sklearn.preprocessing import LabelEncoder
from torch import nn  # Use PyTorch for model architecture
from torch.utils.data import DataLoader, Dataset  # Use PyTorch for data handling

# Load the training data
train_data = pd.read_csv('Eda/train_data.csv')  # Specify the correct path
test_data = pd.read_csv('Eda/test_data.csv')    # Specify the correct path

# Prepare the data for training
X_train = train_data['Message'].dropna().values  # Drop NaN values
X_test = test_data['Message'].dropna().values  # Drop NaN values for test data

# Create a mock response column for demonstration
train_data['Response'] = train_data['Message'].shift(-1)  # Shift messages to create a response
train_data.dropna(inplace=True)  # Drop rows with NaN values

# Ensure y_train is aligned with X_train
y_train = train_data['Response'].dropna().values  # Ensure y_train is aligned
y_test = test_data['Message'].shift(-1).dropna().values  # Create mock responses for test data

# Initialize the Hugging Face Transformers pipeline for text generation
generator = pipeline('text-generation', model='gpt2')  # You can choose a different model if needed

# Example of generating a response
def generate_response(input_text):
    response = generator(input_text, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']

# Function to load Hugging Face dataset
def import_huggingface_dataset():
    # Load the dataset from Hugging Face
    url = "https://huggingface.co/datasets/openai/openai_humaneval/resolve/main/openai_humaneval/test-00000-of-00001.parquet"
    dataset = pd.read_parquet(url)
    print("Hugging Face dataset loaded successfully.")
    print(dataset.head())  # Display the first few rows of the dataset

# Example usage
for message in X_train[:5]:  # Generate responses for the first 5 messages
    print(f"Input: {message}")
    print(f"Response: {generate_response(message)}")
    print("-" * 50)

print("Training complete.")

# Tokenization
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(X_train)
X_train_sequences = tokenizer.texts_to_sequences(X_train)
X_train_padded = pad_sequences(X_train_sequences, padding='post')

# Encode the labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train.tolist())  # Convert to list

# Define the model architecture using PyTorch
class TextModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(TextModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x = self.fc(x[:, -1, :])  # Get the last time step
        return x

# Initialize the model
model = TextModel(vocab_size=10000, embedding_dim=64, hidden_dim=128, output_dim=len(np.unique(y_train_encoded)))

# Define loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train_padded, dtype=torch.long)
y_train_tensor = torch.tensor(y_train_encoded, dtype=torch.long)

# Train the model
model.train()
for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# Evaluate the model
model.eval()
with torch.no_grad():
    outputs = model(X_train_tensor)
    _, predicted = torch.max(outputs, 1)
    accuracy = (predicted == y_train_tensor).float().mean()
    print(f'Model Accuracy: {accuracy.item()}')

print("Training complete.")
