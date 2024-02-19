import pygame
import random
import math
import sys
import matplotlib.pyplot as plt
import numpy as np

# Constants
WIDTH = 800
HEIGHT = 800
NUM_AGENTS = 15
BOUNDED_CONFIDENCE = 0.2
G_RADIUS = 100
R_RADIUS = 80
NUM_STEPS = 1000
MAX_VELOCITY = 2
FLOCK_CENTERING_FACTOR = 0.02
VELOCITY_MATCHING_FACTOR = 0.05
COLLISION_AVOIDANCE_FACTOR = 0.8
SEPARATION_DISTANCE = 30
SEPARATION_FACTOR = 0.7

class Agent:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.velocity = random.uniform(0, MAX_VELOCITY)
        self.angle = random.uniform(0, 2 * math.pi)
        self.opinion = random.uniform(0, 1)

    def update(self, agents, obstacles, target_x, target_y):
        # Update the agent's position, velocity, and opinion based on neighbors and target position
        neighbors = self.find_neighbors(agents)
        if neighbors:
            self.flock_centering(neighbors)
            self.velocity_matching(neighbors)
            self.collision_avoidance(neighbors, obstacles)
            self.separation(neighbors)
        self.move(target_x, target_y)
        self.update_opinion(neighbors)

    def find_neighbors(self, agents):
        # Find neighboring agents based on eyeshot distance
        neighbors = []
        for agent in agents:
            if agent != self:
                distance = math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
                if distance <= G_RADIUS:
                    neighbors.append(agent)
        return neighbors

    def flock_centering(self, neighbors):
        # Adjust the agent's angle towards the center of the flock
        center_x = sum(agent.x for agent in neighbors) / len(neighbors)
        center_y = sum(agent.y for agent in neighbors) / len(neighbors)
        angle_to_center = math.atan2(center_y - self.y, center_x - self.x)
        self.angle = (self.angle + FLOCK_CENTERING_FACTOR * (angle_to_center - self.angle)) % (2 * math.pi)

    def velocity_matching(self, neighbors):
        # Adjust the agent's velocity to match the average velocity of neighbors
        avg_velocity = sum(agent.velocity for agent in neighbors) / len(neighbors)
        self.velocity = self.velocity + VELOCITY_MATCHING_FACTOR * (avg_velocity - self.velocity)

    def collision_avoidance(self, neighbors, obstacles):
        # Adjust the agent's angle to avoid collisions with neighbors and obstacles
        for agent in neighbors:
            distance = math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
            if distance <= SEPARATION_DISTANCE:
                angle_to_avoid = math.atan2(self.y - agent.y, self.x - agent.x)
                self.angle = (self.angle + COLLISION_AVOIDANCE_FACTOR * (angle_to_avoid - self.angle)) % (2 * math.pi)

        for obstacle in obstacles:
            distance_x = abs(self.x - obstacle.x) - obstacle.width / 2
            distance_y = abs(self.y - obstacle.y) - obstacle.height / 2
            if distance_x <= SEPARATION_DISTANCE and distance_y <= SEPARATION_DISTANCE:
                angle_to_avoid = math.atan2(self.y - obstacle.y, self.x - obstacle.x)
                self.angle = (self.angle + COLLISION_AVOIDANCE_FACTOR * (angle_to_avoid - self.angle)) % (2 * math.pi)

    def separation(self, neighbors):
        # Adjust the agent's angle to maintain a minimum separation distance from neighbors
        for agent in neighbors:
            distance = math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
            if distance <= SEPARATION_DISTANCE:
                angle_to_separate = math.atan2(self.y - agent.y, self.x - agent.x)
                self.angle = (self.angle + SEPARATION_FACTOR * (angle_to_separate - self.angle)) % (2 * math.pi)

    def move(self, target_x, target_y):
        # Calculate the angle towards the target position
        angle_to_target = math.atan2(target_y - self.y, target_x - self.x)

        # Adjust the agent's angle smoothly towards the target angle
        angle_diff = (angle_to_target - self.angle + math.pi) % (2 * math.pi) - math.pi
        max_turn = 0.1
        if abs(angle_diff) > max_turn:
            angle_diff = math.copysign(max_turn, angle_diff)
        self.angle = (self.angle + angle_diff) % (2 * math.pi)

        # Move the agent based on its angle and velocity
        new_x = self.x + self.velocity * math.cos(self.angle)
        new_y = self.y + self.velocity * math.sin(self.angle)

        # Check if the new position is within the boundaries
        if 0 <= new_x <= WIDTH and 0 <= new_y <= HEIGHT:
            self.x = new_x
            self.y = new_y
        else:
            # If the new position is outside the boundaries, hit the boundary and change direction
            self.angle = (self.angle + math.pi) % (2 * math.pi)

    def update_opinion(self, neighbors):
        # Update the agent's opinion based on Hegselmann and Krause model
        similar_opinions = [agent.opinion for agent in neighbors if abs(agent.opinion - self.opinion) <= BOUNDED_CONFIDENCE]
        if similar_opinions:
            self.opinion = sum(similar_opinions) / len(similar_opinions)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flocking Simulation on Opinion Dynamics")

    agents = [Agent() for _ in range(NUM_AGENTS)]

    obstacles = [
        Obstacle(random.uniform(100, WIDTH - 100), random.uniform(100, HEIGHT - 100), random.uniform(60, 180), random.uniform(60, 180))
        for _ in range(4)
    ]
    
    collision_count = []
    agent_collision_count = []

    clock = pygame.time.Clock()

    target_x, target_y = WIDTH / 2, HEIGHT / 2  # Initialize target position
    
    for step in range(NUM_STEPS):
        collisions = 0  # Count of collisions at the current step
        agent_collisions = np.zeros(NUM_AGENTS)  # Count of collisions between agents
        
        for agent in agents:
            agent.update(agents, obstacles, target_x, target_y)

            # Check for collisions with other agents
            for i, other_agent in enumerate(agents):
                if agent != other_agent:
                    distance = math.sqrt((agent.x - other_agent.x) ** 2 + (agent.y - other_agent.y) ** 2)
                    if distance <= 2 * R_RADIUS:
                        collisions += 1
                        agent_collisions[i] += 1

           # Check for collisions with obstacles
            for obstacle in obstacles:
                distance_x = abs(agent.x - obstacle.x) - obstacle.width / 2
                distance_y = abs(agent.y - obstacle.y) - obstacle.height / 2
                if distance_x <= SEPARATION_DISTANCE and distance_y <= SEPARATION_DISTANCE:
                    collisions += 1

        collision_count.append(collisions)
        agent_collision_count.append(agent_collisions)


    

        screen.fill((255, 255, 255))  # Set background color to white

        for agent in agents:
            agent.update(agents, obstacles, target_x, target_y)

            # Calculate the points of the arrow shape based on agent's position and angle
            arrow_length = 35
            arrow_tip_x = agent.x + arrow_length * math.cos(agent.angle)
            arrow_tip_y = agent.y + arrow_length * math.sin(agent.angle)
            arrow_base1_x = agent.x + 0.5 * arrow_length * math.cos(agent.angle + math.pi / 6)
            arrow_base1_y = agent.y + 0.5 * arrow_length * math.sin(agent.angle + math.pi / 6)
            arrow_base2_x = agent.x + 0.5 * arrow_length * math.cos(agent.angle - math.pi / 6)
            arrow_base2_y = agent.y + 0.5 * arrow_length * math.sin(agent.angle - math.pi / 6)

            # Draw the agent as an arrow based on the calculated points
            color = (0, 0, 255)  # Set arrow color to blue
            pygame.draw.polygon(screen, color, [(arrow_tip_x, arrow_tip_y), (arrow_base1_x, arrow_base1_y), (arrow_base2_x, arrow_base2_y)])

        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 0, 0), (obstacle.x - obstacle.width / 2, obstacle.y - obstacle.height / 2, obstacle.width, obstacle.height))


        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                target_x, target_y = event.pos

    pygame.quit()
        
    plot_collision_count(collision_count)
    plot_agent_collision_count(agent_collision_count)

def plot_collision_count(collision_count):
    plt.plot(range(NUM_STEPS), collision_count)
    plt.xlabel("Time Step")
    plt.ylabel("Collision Count")
    plt.title("Collision Count over Time")
    plt.show()
    
def plot_agent_collision_count(agent_collision_count):
    agent_collision_count = np.array(agent_collision_count)
    for i in range(NUM_AGENTS):
        plt.plot(range(NUM_STEPS), agent_collision_count[:, i], label=f"Agent {i+1}")
    plt.xlabel("Time Step")
    plt.ylabel("Collision Count")
    plt.title("Agent Collision Count over Time")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    run_simulation()
