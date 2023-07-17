import torch
import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):
    """
    A convolutional network.
    Architecture as outlined in the methods section of
    "Human-level control through deep reinforcement learning" - Mnih et. al
    There is nothing about this architecture which is specific to Deep-q-learning - in fact,
    the algorithm's performance should be fairly robust to the number and sizes of layers.
    """

    def __init__(self, state_dim, input_size, output_size):
        """
        Initialise the layers of the DQN
        :param state_dim
        :param input_size: width/height of the input image (we assume it's square)
        :param output_size: number out elements in the output vector
        """
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(state_dim, 32, kernel_size=(4, 4), stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=(4, 4), stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=(3, 3), stride=1)

        # Calculate the size of the image when squashed to a linear vector
        # We assume here that the input image is square
        conv_length = self._conv_shape(
            self._conv_shape(self._conv_shape(input_size, 4, 4), 4, 2), 3, 1
        )
        conv_shape = conv_length ** 2 * 64
        self.linear1 = nn.Linear(conv_shape, 256)
        self.linear2 = nn.Linear(256, output_size)

        nn.init.xavier_normal_(self.conv1.weight)
        nn.init.zeros_(self.conv1.bias)
        nn.init.xavier_normal_(self.conv2.weight)
        nn.init.zeros_(self.conv2.bias)
        nn.init.xavier_normal_(self.conv3.weight)
        nn.init.zeros_(self.conv3.bias)

        nn.init.xavier_normal_(self.linear1.weight)
        nn.init.zeros_(self.linear1.bias)
        nn.init.xavier_normal_(self.linear2.weight)
        nn.init.zeros_(self.linear2.bias)

    @staticmethod
    def _conv_shape(input_size, filter_size, stride, padding=0):
        return 1 + (input_size - filter_size + 2 * padding) // stride

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = torch.flatten(x, 1)

        x = F.relu(self.linear1(x))
        return self.linear2(x)
