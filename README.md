# Consensus-Model

[![Owner](https://avatars.githubusercontent.com/u/000000?v=4)](https://github.com/AIMSIIITA)

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [Branch Information](#branch-information)
    - [Main (Consensus Model)](#main-consensus-model)
    - [Branch 1: HK Model](#branch-1-hk-model)
    - [Branch 2: Swarm Majority Rule](#branch-2-swarm-majority-rule)
    - [Branch 3: Voter Model](#branch-3-voter-model)
4. [Technologies Used](#technologies-used)
5. [Installation Instructions](#installation-instructions)
6. [Usage Instructions](#usage-instructions)
7. [Example/Preview](#examplepreview)
8. [Contributing Guidelines](#contributing-guidelines)
9. [License](#license)
10. [Contact Information](#contact-information)

## Project Description

This project focuses on consensus and obstacle avoidance in swarm robotics using various models, including the voter model, HK model, and majority rule model. The objective is to simulate and analyze how different decision-making strategies can be applied to swarms to achieve efficient navigation and obstacle avoidance.

## Features

- Implementation of consensus algorithms for swarm robotics.
- Simulation of obstacle avoidance.
- Analysis and comparison of different decision-making models.
- Detailed reports and presentations for each model.
- Simulation videos showcasing model performance.

## Branch Information

### Main (Consensus Model)

**Description**: This is the main branch containing the comprehensive consensus model implementation. The main branch serves as the backbone of the project, integrating various decision-making models for swarm robotics and their respective obstacle avoidance techniques. The models were developed using Python, with simulations built from scratch using libraries such as Pygame for visual representation, Matplotlib for data plotting, and in some cases, deep reinforcement learning facilitated by OpenAI Gymnasium. 

In this branch, extensive work has been done to ensure that the simulations are robust and scalable. Each model was meticulously tested to handle various swarm sizes and dynamic obstacle environments. The codebase is well-documented, making it easy for new contributors to understand the implementation details.

**Key Files/Directories**:
- [README.md](README.md): Project overview and instructions.
- [CONSENSUS AND OBSTACLE AVOIDANCE USING VOTER MODEL.py](branches/main/CONSENSUS%20AND%20OBSTACLE%20AVOIDANCE%20USING%20VOTER%20MODEL.py): Implementation of the voter model for consensus and obstacle avoidance.
- [Democratic Swarms Navigating Collision Avoidance through Consensus Decision Making with the voter model.pptx](branches/main/Democratic%20Swarms%20Navigating%20Collision%20Avoidance%20through%20Consensus%20Decision%20Making%20with%20the%20voter%20model.pptx): Presentation on the voter model.
- [obstacles_avoidance_simulation.mov](branches/main/obstacles_avoidance_simulation.mov): Simulation video.
- [votermodelresearchpaper.pdf](branches/main/votermodelresearchpaper.pdf): Research paper on the voter model.

### Branch 1: HK Model

**Description**: The Hegselmann-Krause (HK) model branch focuses on implementing the HK consensus model for swarm robotics. This model is essential for understanding how agents in a swarm can reach consensus over time while avoiding obstacles. The simulations were meticulously developed from scratch using Pygame for rendering the agent movements, Matplotlib for plotting the data, and incorporating deep reinforcement learning techniques using OpenAI Gymnasium to enhance the decision-making process of the agents. This approach allows for a robust simulation environment where swarms can adapt to dynamic obstacles and changing conditions.

In this branch, the HK model was extended to include obstacle avoidance, making it a comprehensive tool for studying real-world swarm behaviors. Detailed presentations and reports were created to document the methodology and findings, providing valuable insights for further research.

**Key Files/Directories**:
- [HKModel.py](branches/HK-model/HKModel.py): HK model implementation.
- [HKModelwithObstacles.py](branches/HK-model/HKModelwithObstacles.py): HK model with obstacle avoidance.
- [HK_Model_PPT.pptx](branches/HK-model/HK_Model_PPT.pptx): Presentation on the HK model.
- [Report_HKModel.pdf](branches/HK-model/Report_HKModel.pdf): Detailed report on the HK model.
- [output_video.mov](branches/HK-model/output_video.mov): Simulation video.

### Branch 2: Swarm Majority Rule

**Description**: This branch implements the swarm majority rule model, a decision-making process where the majority vote determines the action of the swarm. The simulations in this branch are crafted from scratch, utilizing Pygame for the visualization of agent movements and interactions, and Matplotlib for analyzing the simulation results. Deep reinforcement learning is integrated through OpenAI Gymnasium to refine the agents' ability to navigate and avoid obstacles based on the majority rule consensus. This model demonstrates how simple majority voting mechanisms can lead to efficient and robust swarm behaviors in complex environments.

In this branch, the focus was on optimizing the majority rule decision-making process to handle real-time dynamic changes in the environment. Comprehensive presentations and detailed reports were created to capture the essence of the model and its effectiveness in various scenarios.

**Key Files/Directories**:
- [.idea/](branches/Swarm-majority-rule/.idea/): IDE configuration files.
- [Consensus and Obstacle Avoidance using Majority Rule.py](branches/Swarm-majority-rule/Consensus%20and%20Obstacle%20Avoidance%20using%20Majority%20Rule.py): Implementation of the majority rule model.
- [Empowering Consensus A Majority Model Approach to Collision Avoidance in Swarm Systems.pptx](branches/Swarm-majority-rule/Empowering%20Consensus%20A%20Majority%20Model%20Approach%20to%20Collision%20Avoidance%20in%20Swarm%20Systems.pptx): Presentation on the majority rule model.
- [Empowering Consensus_ A Majority Model Approach to Collision Avoidance in Swarm Systems.pdf](branches/Swarm-majority-rule/Empowering%20Consensus_%20A%20Majority%20Model%20Approach%20to%20Collision%20Avoidance%20in%20Swarm%20Systems.pdf): Research paper on the majority rule model.
- [VID-20230728-WA0006.mp4](branches/Swarm-majority-rule/VID-20230728-WA0006.mp4): Simulation video.

### Branch 3: Voter Model

**Description**: The voter model branch is dedicated to implementing the voter model for consensus and obstacle avoidance in swarm robotics. This model explores how individual agents, acting based on the state of their neighbors, can achieve consensus and navigate through environments with obstacles. The simulation is developed using Pygame for dynamic visualization, Matplotlib for detailed data analysis, and incorporates deep reinforcement learning via OpenAI Gymnasium to optimize the agents' decision-making processes. The voter model is particularly effective in demonstrating decentralized decision-making and its impact on swarm behavior.

This branch involved extensive experimentation to refine the voter model, ensuring it performs efficiently in various scenarios. Detailed documentation, including research papers and presentations, was created to provide a thorough understanding of the model and its applications.

**Key Files/Directories**:
- [CONSENSUS AND OBSTACLE AVOIDANCE USING VOTER MODEL.py](branches/Voter-model/CONSENSUS%20AND%20OBSTACLE%20AVOIDANCE%20USING%20VOTER%20MODEL.py): Voter model implementation.
- [Democratic Swarms Navigating Collision Avoidance through Consensus Decision Making with the voter model.pptx](branches/Voter-model/Democratic%20Swarms%20Navigating%20Collision%20Avoidance%20through%20Consensus%20Decision%20Making%20with%20the%20voter%20model.pptx): Presentation on the voter model.
- [obstacles_avoidance_simulation.mov](branches/Voter-model/obstacles_avoidance_simulation.mov): Simulation video.
- [votermodelresearchpaper.pdf](branches/Voter-model/votermodelresearchpaper.pdf): Research paper on the voter model.

## Technologies Used

- Python
- Pygame
- Matplotlib
- Deep Reinforcement Learning
- OpenAI Gymnasium

## Installation Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/AIMSIIITA/Consensus-Model.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Consensus-Model
    ```
3. Install necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage Instructions

### Running the Simulations

1. For the HK model:
    ```bash
    python HKModel.py
    ```
2. For the Voter model:
    ```bash
    python CONSENSUS_AND_OBSTACLE_AVOIDANCE_USING_VOTER_MODEL.py
    ```
3. For the Swarm Majority Rule model:
    ```bash
    python Consensus_and_Obstacle_Avoidance_using_Majority_Rule.py
    ```

## Example/Preview

![Obstacle Avoidance Simulation](branches/main/obstacles_avoidance_simulation.mov)

## Contributing Guidelines

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature
