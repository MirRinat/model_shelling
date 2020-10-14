import matplotlib.pyplot as plt
import itertools
import random
import copy


class Schelling:
    def __init__(self, n, similarity_threshold, n_iterations, races = 2):
        self.width = n
        self.height = n
        self.races = races#количество цветов
        self.empty_ratio = 0.1#доля пустых
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        self.empty_houses = []
        self.agents = {}

    def populate(self):
        self.all_houses = list(itertools.product(range(self.width), range(self.height)))
        random.shuffle(self.all_houses)#создаем случайный список всех точек

        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_houses = self.all_houses[:self.n_empty]#список пустых

        self.remaining_houses = self.all_houses[self.n_empty:]#все непустые
        houses_by_race = [self.remaining_houses[i::self.races] for i in range(self.races)]
        for i in range(self.races):
            # create agents for each race
            self.agents = dict(
                list(self.agents.items()) +
                list(dict(zip(houses_by_race[i], [i + 1] * len(houses_by_race[i]))).items())
            )

    def is_unhappy(self, x, y):#проверка на счастье

        race = self.agents[(x, y)]
        count_similar = 0
        # count_different = 0

        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_houses:
            if self.agents[(x - 1, y - 1)] == race:
                count_similar += 1
            # else:
            #     count_different += 1
        if y > 0 and (x, y - 1) not in self.empty_houses:
            if self.agents[(x, y - 1)] == race:
                count_similar += 1
            # else:
            #     count_different += 1
        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_houses:
            if self.agents[(x + 1, y - 1)] == race:
                count_similar += 1
            # else:
            #     count_different += 1
        if x > 0 and (x - 1, y) not in self.empty_houses:
            if self.agents[(x - 1, y)] == race:
                count_similar += 1
            # else:
            #     count_different += 1
        if x < (self.width - 1) and (x + 1, y) not in self.empty_houses:
            if self.agents[(x + 1, y)] == race:
                count_similar += 1
            # else:
            #     count_different += 1
        if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_houses:
            if self.agents[(x - 1, y + 1)] == race:
                count_similar += 1
            # else:
            #     count_different += 1
        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_houses:
            if self.agents[(x, y + 1)] == race:
                count_similar += 1
            # else:
            #     count_different += 1
        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_houses:
            if self.agents[(x + 1, y + 1)] == race:
                count_similar += 1
            # else:
            #     count_different += 1

        if (count_similar) >= 2:
            return False#возвращает false если он счастлив
        else:
            return True #float(count_similar) / (count_similar + count_different) < self.happy_threshold

    def update(self):
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            n_changes = 0
            for agent in self.old_agents:
                if self.is_unhappy(agent[0], agent[1]):
                    agent_race = self.agents[agent]
                    empty_house = random.choice(self.empty_houses)
                    self.agents[empty_house] = agent_race
                    del self.agents[agent]
                    self.empty_houses.remove(empty_house)
                    self.empty_houses.append(agent)
                    n_changes += 1
            print(n_changes)
            if n_changes == 0:
                break

    def move_to_empty(self, x, y):
        race = self.agents[(x, y)]
        empty_house = random.choice(self.empty_houses)
        self.updated_agents[empty_house] = race
        del self.updated_agents[(x, y)]
        self.empty_houses.remove(empty_house)
        self.empty_houses.append((x, y))

    def plot(self, file_name):
        fig, ax = plt.subplots()
        # If you want to run the simulation with more than 7 colors, you should set agent_colors accordingly
        agent_colors = {1: 'b', 2: 'r'}
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, color=agent_colors[self.agents[agent]])

        # ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

schelling_1 = Schelling(10, 0.1, 5, 2)
schelling_1.populate()
schelling_1.plot('schelling_1.png')
schelling_1.update()
schelling_1.plot('schelling_2.png')