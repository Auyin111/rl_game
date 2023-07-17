class RlCarRacingCfg:
    """
    if test_mode == True, only use low computation setting to debug the code
    """

    def __init__(self, test_mode, dir_data):
        self.test_mode = test_mode
        self.dir_data = dir_data

        # Define
        self._define_hyper()
        self._define_constant()
        self._define_wandb()

    def _define_hyper(self):
        """define hyperparameters"""
        self.LR = 5e-4

    def _define_constant(self):
        # discount factor
        self.GAMMA = 0.99

        # number of transitions sampled from the replay buffer
        self.BATCH_SIZE = 10 if self.test_mode else 48

        self.NUM_EPISODES = 3 if self.test_mode else 1000
        # memory capacity
        self.MEMORY_CAP = 10 if self.test_mode else 18000

        ### epsilon
        # starting value
        self.EPS_START = 1
        # final value
        self.EPS_END = 0.05
        # rate of expoential decay of epsilon, higher means a slower decay
        self.EPS_DECAY = 9000

        # update rate of the target network
        self.TAU = 0.02

        # display
        self.EPISODE_PRINT = 20
        self.SF = 5

    def _define_wandb(self):
        self.project = 'rl_CarRacing'
        self.user = 'Kyle'
        self.version = 'v_2_2_7'
        self.model = 'DQN'
        self.entity = 'kaggle_winner'
        self.md_name = f'{self.project}_{self.version}_test.pth' if self.test_mode else f'{self.project}_{self.version}.pth'
