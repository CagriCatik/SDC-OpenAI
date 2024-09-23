import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset

# Set a seed for reproducibility
torch.manual_seed(42)

# Define hyperparameters
LEARNING_RATE = 0.2
EPOCHS = 200
HIDDEN_UNITS = 10
BATCH_SIZE = 32

# Generate data
x = torch.unsqueeze(torch.linspace(-1, 1, 100), dim=1)  # x data (tensor), shape=(100, 1)
y = x.pow(2) + 0.2 * torch.rand(x.size())  # noisy y data (tensor), shape=(100, 1)

# Create dataset and data loader
dataset = TensorDataset(x, y)
data_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)


class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)  # hidden layer
        self.predict = torch.nn.Linear(n_hidden, n_output)  # output layer

    def forward(self, x):
        x = F.relu(self.hidden(x))  # activation function for hidden layer
        x = self.predict(x)  # linear output
        return x


def train(model, optimizer, loss_func, data_loader, epochs):
    plt.ion()  # Turn on interactive mode for live plotting
    for epoch in range(epochs):
        for batch_x, batch_y in data_loader:
            # Forward pass
            prediction = model(batch_x)
            loss = loss_func(prediction, batch_y)

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Plot every 5 epochs
        if epoch % 5 == 0:
            plot_live(x, y, model, loss, epoch)
            print(f"Epoch [{epoch}/{epochs}], Loss: {loss.item():.4f}")

    plt.ioff()  # Turn off interactive mode
    plt.show()


def plot_live(x, y, model, loss, epoch):
    plt.cla()  # Clear the plot
    with torch.no_grad():
        prediction = model(x)
    plt.scatter(x.numpy(), y.numpy())
    plt.plot(x.numpy(), prediction.detach().numpy(), 'r-', lw=5)
    plt.text(0.5, 0, f'Loss={loss:.4f}', fontdict={'size': 20, 'color': 'red'})
    plt.pause(0.1)


def main():
    # Initialize the network
    net = Net(n_feature=1, n_hidden=HIDDEN_UNITS, n_output=1)
    print(net)  # Print the network architecture

    # Define the optimizer and loss function
    optimizer = torch.optim.SGD(net.parameters(), lr=LEARNING_RATE)
    loss_func = torch.nn.MSELoss()

    # Train the network
    train(net, optimizer, loss_func, data_loader, EPOCHS)


if __name__ == '__main__':
    main()
