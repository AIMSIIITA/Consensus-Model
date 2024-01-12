import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

#  dimensions of the simulation window
window_width = 1300
window_height = 575

# simulation window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Voter Model of Swarm Robotics")

#  background color
background_color = (255, 255, 255)

# target site color
target_color = (255, 0, 0)

#  size of the target sites
target_width = 50
target_height = 50

#  agent color
agent_color = (0, 0, 255)

# consensus color
consensus_color = (255, 255, 0)  # Yellow color

# radius of the agents
agent_radius = 4

# position of the starting point for the agents
start_x = agent_radius
start_y = window_height // 2

#  positions of the target sites
target_y1 = random.randint(0, start_y - target_height)
target_y2 = random.randint(0, window_height - target_height)

# positions of the agents at the starting point
agents = [(start_x, start_y)] * 20

# Initialize the opinion of agents
opinions = [0] * len(agents)

# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

hurdles = [
    (200, 300, 120, 0.1),   # Hurdle 1: x=200, y=300, amplitude=120, oscillation frequency=0.1
    (400, 400, 60, 0.3),   # Hurdle 2: x=400, y=400, amplitude=60, oscillation frequency=0.3
    (600, 500, 100, 0.1),  # Hurdle 3: x=600, y=500, amplitude=100, oscillation frequency=0.1
    (800, 250, 120, 0.1),   # Hurdle 4: x=800, y=250, amplitude=120, oscillation frequency=0.1
    (1000, 350, 70, 0.2)    # Hurdle 5: x=1000, y=350, amplitude=70, oscillation frequency=0.2
]


#  repulsion radius for hurdle avoidance
repulsion_radius_hurdles = 85

# Function to move the agents towards a given target while avoiding collisions
def move_agents(target_x=None, target_y=None):
    for i, agent in enumerate(agents):
        agent_x, agent_y = agent

        if target_x is None or target_y is None:
            # Calculate the distance traveled to each target
            distance_to_target1 = calculate_distance(agent_x, agent_y, window_width - target_width, target_y1)
            distance_to_target2 = calculate_distance(agent_x, agent_y, window_width - target_width, target_y2)

            # Move towards the nearest target while avoiding collisions
            if distance_to_target1 < distance_to_target2:
                target_x = window_width - target_width
                target_y = target_y1
            else:
                target_x = window_width - target_width
                target_y = target_y2

        # Calculate the vector towards the target
        dx = target_x - agent_x
        dy = target_y - agent_y

        #  unit vector
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance

        # Check for collisions with other agents and adjust the direction
        for j, other_agent in enumerate(agents):
            if i != j:
                other_agent_x, other_agent_y = other_agent
                distance_to_other_agent = calculate_distance(agent_x, agent_y, other_agent_x, other_agent_y)
                if distance_to_other_agent < agent_radius * 2:
                    if distance_to_other_agent != 0:
                        dx -= (other_agent_x - agent_x) / distance_to_other_agent
                        dy -= (other_agent_y - agent_y) / distance_to_other_agent

        #  repulsion force from the hurdles and adjust the direction
        repulsion_force_x = 0
        repulsion_force_y = 0
        for hurdle in hurdles:
            hurdle_x, hurdle_y, amplitude, oscillation_frequency = hurdle
            # Calculate the current vertical position of the hurdle based on elapsed time
            angle = elapsed_time * 2 * math.pi * oscillation_frequency
            hurdle_current_y = hurdle_y + amplitude * math.sin(angle)

            dx_hurdle = hurdle_x - agent_x
            dy_hurdle = hurdle_current_y - agent_y  # Calculate distance to the current vertical position of the hurdle
            distance_to_hurdle = math.sqrt(dx_hurdle ** 2 + dy_hurdle ** 2)
            if distance_to_hurdle < repulsion_radius_hurdles:
                if distance_to_hurdle != 0:
                    # Calculate the repulsion force based on the distance to the current position of the hurdle
                    repulsion_force_x -= (hurdle_x - agent_x) / distance_to_hurdle
                    repulsion_force_y -= (hurdle_current_y - agent_y) / distance_to_hurdle

        # Combine the target direction and repulsion force
        dx += repulsion_force_x
        dy += repulsion_force_y

        # Normalize the direction vector
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance

        #  speed or distance the agent should move
        speed = 1

        # Update the agent's position
        new_agent_x = agent_x + dx * speed
        new_agent_y = agent_y + dy * speed

        agents[i] = (new_agent_x, new_agent_y)


# Function to calculate the time taken during motion 1 to reach target A
def calculate_motion1_time():
    total_time = 0
    target_x = window_width - target_width
    target_y = target_y1

    for agent in agents:
        agent_x, agent_y = agent
        distance = calculate_distance(agent_x, agent_y, target_x, target_y)
        time = distance / 1  # Assuming a constant speed of 1 unit per iteration

        # time increment based on agent's speed
        speed = 1  
        time_increment = 1 / speed

        for hurdle in hurdles:
            hurdle_x, hurdle_y, amplitude, oscillation_frequency = hurdle
            distance_to_hurdle = calculate_distance(agent_x, agent_y, hurdle_x, hurdle_y)

            if distance_to_hurdle < repulsion_radius_hurdles:
                # Calculate the number of iterations spent within the repulsion radius
                num_iterations_within_radius = int(repulsion_radius_hurdles / speed)

                # Increment the time for each iteration within the repulsion radius
                time += time_increment * num_iterations_within_radius

        total_time += time

    return total_time

#  calculate the time taken during motion 3 to reach target B
def calculate_motion3_time():
    total_time = 0
    target_x = window_width - target_width
    target_y = target_y2

    for agent in agents:
        agent_x, agent_y = agent
        distance = calculate_distance(agent_x, agent_y, target_x, target_y)
        time = distance / 1  # Assuming a constant speed of 1 unit per iteration

        #  time increment based on agent's speed
        speed = 1 
        time_increment = 1 / speed

        for hurdle in hurdles:
            hurdle_x, hurdle_y, amplitude, oscillation_frequency = hurdle
            distance_to_hurdle = calculate_distance(agent_x, agent_y, hurdle_x, hurdle_y)

            if distance_to_hurdle < repulsion_radius_hurdles:
                # Calculate the number of iterations spent within the repulsion radius
                num_iterations_within_radius = int(repulsion_radius_hurdles / speed)

                # Increment the time for each iteration within the repulsion radius
                time += time_increment * num_iterations_within_radius

        total_time += time

    return total_time# Function to calculate the target with the shorter time taken during motions 1 and 3
def calculate_less_time_target():
    target_time1 = calculate_motion1_time()
    target_time3 = calculate_motion3_time()

    if target_time1 < target_time3:
        return window_width - target_width, target_y1
    else:
        return window_width - target_width, target_y2

# Function to update agent opinions based on the time taken to reach each target
def update_opinions(target_x1, target_y1, target_x2, target_y2):
    for i, agent in enumerate(agents):
        agent_x, agent_y = agent

        time_to_target1 = calculate_motion1_time()
        time_to_target2 = calculate_motion3_time()
        if time_to_target1 < time_to_target2:
            opinions[i] = 0  # Agent's opinion is for target A
        else:
            opinions[i] = 1  # Agent's opinion is for target B
            
# Function to calculate the target decided by consensus opinion
def calculate_consensus_target():
    target_x, target_y = None, None
    if opinions.count(0) > opinions.count(1):
        # Consensus is in favor of target A (upper target)
        target_x = window_width - target_width
        target_y = target_y1
    else:
        # Consensus is in favor of target B (lower target)
        target_x = window_width - target_width
        target_y = target_y2

    return target_x, target_y


# Game loop
motion_counter = 0
motion_1 = True
motion_2 = False
motion_3 = False
motion_4 = False
motion_5 = False
running = True


start_time = time.time()  # Get the initial start time

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill(background_color)

    # Draw the target sites
    pygame.draw.rect(window, target_color, (window_width - target_width, target_y1, target_width, target_height))
    pygame.draw.rect(window, target_color, (window_width - target_width, target_y2, target_width, target_height))

    # Draw hurdles
    current_time = time.time()  # Get the current time
    elapsed_time = current_time - start_time  #  elapsed time
    for hurdle in hurdles:
        hurdle_x, hurdle_y, amplitude, oscillation_frequency = hurdle
        # Convert elapsed time to radians for smooth oscillation
        angle = elapsed_time * 2 * math.pi * oscillation_frequency
        hurdle_y += amplitude * math.sin(angle)

        hurdle_width = 20
        hurdle_height = 30
        pygame.draw.rect(window, (0, 0, 0), (hurdle_x, hurdle_y, hurdle_width, hurdle_height))


    # Perform different motions based on boolean flags
    if motion_1:
        # Motion 1: Move agents to target A (upper target)
        move_agents(window_width - target_width, target_y1)
        if agents[-1][0] >= window_width - target_width:
            motion_1 = False
            motion_2 = True
            

            update_opinions(window_width - target_width, target_y1, window_width - target_width, target_y2)

    
    elif motion_2:
        # Motion 2: Return agents to the origin point
        move_agents(start_x, start_y)
        if agents[-1][0] <= start_x:
            motion_2 = False
            motion_3 = True
            

    elif motion_3:
        # Motion 3: Move agents to target B (lower target)
        move_agents(window_width - target_width, target_y2)
        if agents[-1][0] >= window_width - target_width:
            motion_3 = False
            motion_4 = True
            

            update_opinions(window_width - target_width, target_y1, window_width - target_width, target_y2)
    elif motion_4:
        # Motion 4: Return agents to the origin point
        move_agents(start_x, start_y)
        if agents[-1][0] <= start_x:
            motion_4 = False
            motion_5 = True
            

            # Change the color of agents to consensus color before entering motion 5
            agent_color = consensus_color
            # Perform opinion exchange and consensus
            opinions_set = set(opinions)
            if len(opinions_set) == 1:
                # All agents have the same opinion, so consensus is reached
                target_x, target_y = calculate_less_time_target()
                update_opinions(target_x, target_y, target_x, target_y)
            else:
                # Not all agents have the same opinion, so exchange opinions with neighbors
                for i in range(len(agents)):
                    neighbor_indices = [j for j in range(len(agents)) if j != i]
                    random_neighbor_index = random.choice(neighbor_indices)
                    opinions[i] = opinions[random_neighbor_index]

    elif motion_5:
    # Motion 5: Move agents to the target decided by consensus opinion
     target_x, target_y = calculate_consensus_target()
     move_agents(target_x, target_y)
     if all(agent[0] >= target_x for agent in agents):
        motion_5 = False
        motion_1 = True
        # Reset the color of agents to the original color after completing motion 5
        agent_color = (0, 0, 255)


    # Draw the agents
    for agent in agents:
        agent_x, agent_y = agent
        pygame.draw.circle(window, agent_color, (int(agent_x), int(agent_y)), agent_radius)

    # Update the window
    pygame.display.update()

# Quit the game
pygame.quit()

