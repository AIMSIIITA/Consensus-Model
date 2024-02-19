import pygame
import random
import math
import matplotlib.pyplot as plt

# Constants
WIDTH = 900
HEIGHT = 500
AGENT_SIZE = 5
NUM_AGENTS = 70
AGENT_SPEED = 1.0
NEIGHBOR_RADIUS = 25
REPULSION_RADIUS = 2 * NEIGHBOR_RADIUS
REPULSION_STRENGTH = 0.2
ALIGNMENT_STRENGTH = 0.9
ATTRACT_STRENGTH = 0.8
LATENT_AGENT_COLOR = (255, 0, 0)  # Red color for latent agents
NON_LATENT_AGENT_COLOR = (0, 0, 255)  # Blue color for non-latent agents
INTERACTION_RADIUS = 120  # Interaction radius between agents
CONSENSUS_PERIOD = 100  # Consensus phase occurs every 200 frames


# Constants for objects
NUM_TARGET = 2
TARGET_SIZE = 40
STARTING_AREA_WIDTH = 100
TARGET_AREA_WIDTH = 100

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swarm Robotics - Majority Rule")
clock = pygame.time.Clock()


class Object:
    def __init__(self, a, b, targe_x, targe_y):
        self.x = a
        self.y = b
        self.target_x = targe_x
        self.target_y = targe_y
        self.is_carried = False


class Agent:
    def __init__(self, is_latent, start_x, start_y, start_direction):
        self.x = start_x
        self.y = start_y
        self.direction = start_direction
        self.is_latent = is_latent
        self.has_consensus = False
        self.reached_goal = False

    def move(self):
        if not self.reached_goal:
            self.x += math.cos(self.direction) * AGENT_SPEED
            self.y += math.sin(self.direction) * AGENT_SPEED

    def update_direction(self, neighbors, obstacles):
        if neighbors:
            # Compute forces acting on the agent from its neighbors
            repulsion_x, repulsion_y = 0, 0
            alignment_x, alignment_y = 0, 0
            attract_x, attract_y = 0, 0

            for neighbor in neighbors:
                dx = neighbor.x - self.x
                dy = neighbor.y - self.y
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < NEIGHBOR_RADIUS:
                    repulsion_x += dx
                    repulsion_y += dy
                    alignment_x += math.cos(neighbor.direction)
                    alignment_y += math.sin(neighbor.direction)
                    attract_x += WIDTH / 2 - self.x
                    attract_y += HEIGHT / 2 - self.y

            # Compute the new direction based on the forces
            self.direction += REPULSION_STRENGTH * math.atan2(repulsion_y, repulsion_x)
            self.direction += ALIGNMENT_STRENGTH * math.atan2(alignment_y, alignment_x)
            self.direction += ATTRACT_STRENGTH * math.atan2(HEIGHT / 2 - self.y, WIDTH / 2 - self.x)

        # Apply collision avoidance with hurdles
        for obstacles in obstacles:
            obstacles_x, obstacles_y, amp, oscillation_frq = obstacles
            dx = obstacles_x - self.x
            dy = obstacles_y - self.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist < REPULSION_RADIUS:
                repulsion_force = (REPULSION_RADIUS - dist) / dist
                self.x -= repulsion_force * dx
                self.y -= repulsion_force * dy

    def wrap_around_screen(self):
        # Restrict the agent's position within the platform boundaries
        if self.x < STARTING_AREA_WIDTH:
            self.x = STARTING_AREA_WIDTH
        elif self.x > WIDTH - STARTING_AREA_WIDTH:
            self.x = WIDTH - STARTING_AREA_WIDTH
        if self.y < 0:
            self.y = 0
        elif self.y >= HEIGHT:
            self.y = HEIGHT

    def find_nearest_goal(self, targets):
        # Find the nearest goal to the agent
        nearest_goal_distance = float('inf')
        nearest_goal = None
        for object in targets:
            if not object.is_carried:
                distance_to_goal = math.hypot(object.x - self.x, object.y - self.y)
                if distance_to_goal < nearest_goal_distance:
                    nearest_goal_distance = distance_to_goal
                    nearest_goal = object
        return nearest_goal

    def move_to_goal(self, goal):
        # Move the agent towards the goal
        if goal:
            dx = goal.x - self.x
            dy = goal.y - self.y
            distance_to_goal = math.hypot(dx, dy)
            if distance_to_goal > 0:
                self.x += dx / distance_to_goal * AGENT_SPEED
                self.y += dy / distance_to_goal * AGENT_SPEED
            else:
                self.reached_goal = True

    def update(self, targets, obstacles):
        # Perform agent's update based on consensus and move towards the goal if it has one
        neighbors = get_neighbors(self)
        # Apply Majority Rule
        if frame_count % CONSENSUS_PERIOD == 0:  # Perform consensus phase every CONSENSUS_PERIOD frames
            consensus_direction = calculate_average_direction(neighbors)
            if consensus_direction is not None:
                self.direction = consensus_direction
                self.has_consensus = True

        if self.has_consensus:
            nearest_goal = self.find_nearest_goal(targets)
            self.move_to_goal(nearest_goal)

        self.update_direction(neighbors, obstacles)
        self.move()
        self.wrap_around_screen()


def get_neighbors(agent):
    neighbors = []
    for neighbour_agent in agents:
        if neighbour_agent != agent:
            dist = math.sqrt((neighbour_agent.x - agent.x) ** 2 + (neighbour_agent.y - agent.y) ** 2)
            if dist <= INTERACTION_RADIUS:
                neighbors.append(neighbour_agent)
    return neighbors


def calculate_average_direction(neighbors):
    if not neighbors:
        return None

    total_direction_x, total_direction_y = 0, 0
    for neighbor in neighbors:
        total_direction_x += math.cos(neighbor.direction)
        total_direction_y += math.sin(neighbor.direction)

    average_direction = math.atan2(total_direction_y, total_direction_x)
    return average_direction


# Lists to store collision information
collision_frames = []
collision_count = []

# Initialize agents and objects
agents = []
for _ in range(NUM_AGENTS):
    initial_x = random.uniform(0, STARTING_AREA_WIDTH)
    initial_y = random.uniform(0, HEIGHT)
    initial_direction = random.uniform(0, 2 * math.pi)
    agents.append(Agent(random.choice([True, False]), initial_x, initial_y, initial_direction))

objects = []
for _ in range(NUM_TARGET):
    x = WIDTH - STARTING_AREA_WIDTH - TARGET_SIZE / 2
    y = random.uniform(0, HEIGHT)
    target_x = WIDTH - TARGET_AREA_WIDTH + TARGET_SIZE / 2
    target_y = random.uniform(0, HEIGHT)
    objects.append(Object(x, y, target_x, target_y))

# Define the hurdles with individual coordinates, amplitude, and oscillation frequency
hurdles = [
    (200, 200, 2, 0.05),   # Hurdle 1: x=200, y=200, amplitude=2, oscillation frequency=0.05
    (400, 300, 1, 0.06),   # Hurdle 2: x=400, y=300, amplitude=1, oscillation frequency=0.06
    (300, 150, 1, 0.03),   # Hurdle 3: x=300, y=150, amplitude=1, oscillation frequency=0.03
    (500, 250, 2, 0.04),   # Hurdle 4: x=500, y=250, amplitude=2, oscillation frequency=0.04
    (600, 100, 1.5, 0.07)  # Hurdle 5: x=600, y=100, amplitude=1.5, oscillation frequency=0.07
]

# Main game loop
running = True
frame_count = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    all_agents_reached_goal = all(agent.reached_goal for agent in agents)

    for i, hurdle in enumerate(hurdles):
        hurdle_x, hurdle_y, amplitude, oscillation_frequency = hurdle
        hurdle_y += math.sin(frame_count * oscillation_frequency) * amplitude

        hurdles[i] = (hurdle_x, hurdle_y, amplitude, oscillation_frequency)
        # Lists to store agent indices involved in collisions
        collisions = set()

    for agent in agents:
        agent.update(objects, hurdles)

        if agent.is_latent and agent.has_consensus:
            color = NON_LATENT_AGENT_COLOR
        else:
            color = LATENT_AGENT_COLOR

        pygame.draw.circle(screen, color, (int(agent.x), int(agent.y)), AGENT_SIZE)
        # Check for collisions
        for other_agent in agents:
            if agent != other_agent:
                distance = math.sqrt((other_agent.x - agent.x) ** 2 + (other_agent.y - agent.y) ** 2)
                if distance <= 2 * AGENT_SIZE:
                    collisions.add(agents.index(agent))
                    collisions.add(agents.index(other_agent))

    # Save collision information
    collision_frames.append(frame_count)
    collision_count.append(len(collisions))

    for obj in objects:
        TARGET_SIZE = 30
        pygame.draw.circle(screen, (0, 0, 0), (int(obj.x), int(obj.y)), TARGET_SIZE)

    for hurdle in hurdles:
        hurdle_x, hurdle_y, _, _ = hurdle
        hurdle_width = 20
        hurdle_height = 30
        pygame.draw.rect(screen, (0, 0, 0), (hurdle_x, hurdle_y, hurdle_width, hurdle_height))

    pygame.display.flip()
    frame_count += 1

    clock.tick(60)

    if all_agents_reached_goal:
        running = False


# After the simulation ends, plot the collision graph using matplotlib
plt.plot(collision_frames, collision_count)
plt.xlabel("Frame Number")
plt.ylabel("Collision Count")
plt.title("Agent Collision Graph")
plt.show()

pygame.quit()
