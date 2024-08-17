import gamelib
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        self.agent = DQNAgent(state_size=4, action_size=10)  # Adjusted action size
        self.batch_size = 32
        self.previous_state = None
        self.previous_action = None
        self.previous_health = 30

    def on_game_start(self, config):
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        self.scored_on_locations = []

    def get_state(self, game_state):
        return np.array([
            game_state.get_resource(SP),
            game_state.get_resource(MP),
            game_state.my_health,
            game_state.turn_number
        ]).reshape(1, 4)

    def perform_action(self, game_state, action):
        actions = [
            self.build_defences,
            self.build_supports,
            self.send_scouts,
            self.send_demolishers,
            self.send_interceptors,
            self.upgrade_defences,
            self.build_reactive_defense,
            self.demolisher_line_strategy,
            self.stall_with_interceptors,
            self.do_nothing
        ]
        actions[action](game_state)

    def get_reward(self, game_state):
        current_health = game_state.my_health
        enemy_health = game_state.enemy_health
        health_change = current_health - self.previous_health
        self.previous_health = current_health
        return health_change + (30 - enemy_health) * 0.5

    def on_turn(self, turn_state):
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)

        current_state = self.get_state(game_state)
        action = self.agent.act(current_state)
        self.perform_action(game_state, action)

        reward = self.get_reward(game_state)

        if self.previous_state is not None:
            self.agent.remember(self.previous_state, self.previous_action, reward, current_state, False)

        if len(self.agent.memory) > self.batch_size:
            self.agent.replay(self.batch_size)

        self.previous_state = current_state
        self.previous_action = action

        game_state.submit_turn()

    def build_defences(self, game_state):
        turret_locations = [[0, 13], [27, 13], [8, 11], [19, 11], [13, 11], [14, 11]]
        game_state.attempt_spawn(TURRET, turret_locations)
        wall_locations = [[8, 12], [19, 12]]
        game_state.attempt_spawn(WALL, wall_locations)

    def build_supports(self, game_state):
        support_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
        game_state.attempt_spawn(SUPPORT, support_locations)

    def send_scouts(self, game_state):
        scout_spawn_location_options = [[13, 0], [14, 0]]
        best_location = self.least_damage_spawn_location(game_state, scout_spawn_location_options)
        game_state.attempt_spawn(SCOUT, best_location, 1000)

    def send_demolishers(self, game_state):
        game_state.attempt_spawn(DEMOLISHER, [24, 10], 3)

    def send_interceptors(self, game_state):
        game_state.attempt_spawn(INTERCEPTOR, [13, 0], 1000)

    def upgrade_defences(self, game_state):
        upgrade_locations = [[8, 11], [19, 11], [13, 11], [14, 11]]
        game_state.attempt_upgrade(upgrade_locations)

    def build_reactive_defense(self, game_state):
        for location in self.scored_on_locations:
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(TURRET, build_location)

    def demolisher_line_strategy(self, game_state):
        for x in range(27, 5, -1):
            game_state.attempt_spawn(WALL, [x, 11])
        game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)

    def stall_with_interceptors(self, game_state):
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            game_state.attempt_spawn(INTERCEPTOR, deploy_location)

    def do_nothing(self, game_state):
        pass

    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path from the location to the enemy and sums up the damage taken.
        The location that takes the least damage is returned.
        """
        damages = []
        # Get the damage taken for each path
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy turrets that can attack the final location
                damage += len(game_state.get_attackers(path_location, 0))
            damages.append(damage)
        
        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()