import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from torch.utils.data import DataLoader, TensorDataset

# Set random seed for reproducibility
torch.manual_seed(42)

# Generate synthetic binary classification data (two classes shaped like moons)
n_samples = 500
x_data, y_data = make_moons(n_samples=n_samples, noise=0.2, random_state=42)

# Convert to PyTorch tensors
x = torch.tensor(x_data, dtype=torch.float32)
y = torch.tensor(y_data, dtype=torch.float32).unsqueeze(1)  # Make y shape (n_samples, 1)

# Create a dataset and data loader
dataset = TensorDataset(x, y)
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)


# Define a simple neural network for binary classification
class BinaryClassifier(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BinaryClassifier, self).__init__()
        self.hidden = torch.nn.Linear(input_size, hidden_size)  # Hidden layer
        self.output = torch.nn.Linear(hidden_size, output_size)  # Output layer

    def forward(self, x):
        x = F.relu(self.hidden(x))  # Activation function for the hidden layer
        x = torch.sigmoid(self.output(x))  # Sigmoid activation for binary classification
        return x


# Function to train the network
def train(model, optimizer, loss_func, data_loader, epochs):
    plt.ion()  # Enable interactive plotting
    for epoch in range(epochs):
        for batch_x, batch_y in data_loader:
            # Forward pass: compute predictions
            prediction = model(batch_x)
            loss = loss_func(prediction, batch_y)

            # Backpropagation and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Plot every 10 epochs
        if epoch % 10 == 0:
            plot_decision_boundary(x, y, model, loss, epoch)
            print(f"Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}")

    plt.ioff()  # Disable interactive plotting
    plt.show()


# Plot decision boundary and data points
def plot_decision_boundary(x, y, model, loss, epoch):
    plt.cla()
    
    # Generate a grid of points to plot the decision boundary
    x_min, x_max = x[:, 0].min() - 0.5, x[:, 0].max() + 0.5
    y_min, y_max = x[:, 1].min() - 0.5, x[:, 1].max() + 0.5
    xx, yy = torch.meshgrid(torch.linspace(x_min, x_max, 100), torch.linspace(y_min, y_max, 100))
    grid = torch.cat([xx.reshape(-1, 1), yy.reshape(-1, 1)], dim=1)

    # Make predictions on the grid to determine the decision boundary
    with torch.no_grad():
        zz = model(grid).reshape(xx.shape)
    
    # Plot decision boundary
    plt.contourf(xx, yy, zz, levels=[0, 0.5, 1], cmap="coolwarm", alpha=0.6)
    
    # Plot the actual data points
    plt.scatter(x[:, 0], x[:, 1], c=y.reshape(-1), cmap="coolwarm", edgecolor='k')
    plt.text(0.5, -1.2, f'Loss: {loss:.4f}', fontdict={'size': 20, 'color': 'red'})
    plt.pause(0.1)


# Main function to initialize and train the model
def main():
    # Define the model
    input_size = 2  # Each data point has 2 features (x1, x2)
    hidden_size = 10  # Number of hidden neurons
    output_size = 1  # Binary output (0 or 1)
    
    model = BinaryClassifier(input_size, hidden_size, output_size)
    print(model)  # Print model architecture

    # Define optimizer and loss function
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_func = torch.nn.BCELoss()  # Binary Cross-Entropy Loss

    # Train the model
    train(model, optimizer, loss_func, data_loader, epochs=200)


if __name__ == '__main__':
    main()
