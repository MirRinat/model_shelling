import matplotlib.pyplot as plt
import random
import copy
import imageio
import glob, os


class Schelling:
    def __init__(self, n, n_iterations, count_colors = 2):
        self.width = n
        self.height = n
        self.colors = count_colors
        self.empty_ratio = 0.1#доля пустых
        self.n_iterations = n_iterations
        self.empty_house = []
        self.agents = {}#словарь из координат точек и цвета

    def create_map(self):
        self.all_houses = []

        for i in range(self.height):
            for j in range(self.width):
                self.all_houses.append((i, j))
        random.shuffle(self.all_houses)#создаем случайный список всех точек

        self.n_empty = int(self.empty_ratio * len(self.all_houses))
        self.empty_house = self.all_houses[:self.n_empty]#список пустых

        self.remaining_houses = self.all_houses[self.n_empty:]#все непустые

        dots_by_color = [self.remaining_houses[i::self.colors] for i in range(self.colors)]

        # создаем словарь из координат и цвета(цифры 1-голубой или 2-красный)
        for i in range(self.colors):
            for k in dots_by_color[i]:
                self.agents[k] = i + 1

    def is_unhappy(self, x, y):#проверка на счастье
        race = self.agents[(x, y)]
        count_similar = 0#счетчик "своих"

        if x > 0 and y > 0 and (x - 1, y - 1) not in self.empty_house:
            if self.agents[(x - 1, y - 1)] == race:
                count_similar += 1

        if y > 0 and (x, y - 1) not in self.empty_house:
            if self.agents[(x, y - 1)] == race:
                count_similar += 1

        if x < (self.width - 1) and y > 0 and (x + 1, y - 1) not in self.empty_house:
            if self.agents[(x + 1, y - 1)] == race:
                count_similar += 1

        if x > 0 and (x - 1, y) not in self.empty_house:
            if self.agents[(x - 1, y)] == race:
                count_similar += 1

        if x < (self.width - 1) and (x + 1, y) not in self.empty_house:
            if self.agents[(x + 1, y)] == race:
                count_similar += 1

        if x > 0 and y < (self.height - 1) and (x - 1, y + 1) not in self.empty_house:
            if self.agents[(x - 1, y + 1)] == race:
                count_similar += 1

        if x > 0 and y < (self.height - 1) and (x, y + 1) not in self.empty_house:
            if self.agents[(x, y + 1)] == race:
                count_similar += 1

        if x < (self.width - 1) and y < (self.height - 1) and (x + 1, y + 1) not in self.empty_house:
            if self.agents[(x + 1, y + 1)] == race:
                count_similar += 1

        if (count_similar) >= 2:
            return False#возвращает false если он счастлив
        else:
            return True#возвращает true если несчастлив, то что нужно

    def plot(self, file_name):
        fig, ax = plt.subplots()

        agent_colors = {1: 'b', 2: 'r'}
        for agent in self.agents:
            ax.scatter(agent[0] + 0.5, agent[1] + 0.5, color=agent_colors[self.agents[agent]])

        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(file_name)

    def update(self, filename):
        for i in range(self.n_iterations):
            self.old_agents = copy.deepcopy(self.agents)
            count_unhappy = 0
            for agent in self.old_agents:
                if self.is_unhappy(agent[0], agent[1]):
                    #перенос несчстливой точки в рандомную пустую ячейку
                    unhappy_agent = self.agents[agent]
                    empty_house = random.choice(self.empty_house)
                    self.agents[empty_house] = unhappy_agent
                    del self.agents[agent]
                    self.empty_house.remove(empty_house)
                    self.empty_house.append(agent)
                    count_unhappy += 1
            if count_unhappy != 0:
                self.plot(filename+"{}.png".format(i))
            if count_unhappy == 0:
                break

    def create_gif(self):
        images = []
        filenames = ['img/schelling_{}.png'.format(f) for f in range(0, len(glob.glob('img/*.png')))]
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('img/movie.gif', images, fps=2)

for f in glob.glob('img/*'):
    os.remove(f)

schelling_1 = Schelling(20,100, 2)
schelling_1.create_map()
schelling_1.update("img/schelling_")
schelling_1.create_gif()
