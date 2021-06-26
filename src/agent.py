import random

import pygame
from pygame.math import Vector2


class Agent:
    def __init__(self, width, height):
        """Initialize agent parameters

        Args:
            width (int): width of the game screen
            height (int): height of the game screen
        """
        self.position = Vector2(random.randint(0, width), random.randint(0, height))
        self.velocity = Vector2(random.randint(-100, 100), random.randint(-100, 100))
        self.acceleration = Vector2()
        self.max_mag = 100
        self.max_force = 50

    def update(self, dt):
        """Update the agent position

        Args:
            dt (float): delta time
        """
        self.position += self.velocity * dt
        self.velocity += self.acceleration * dt

    def align(self, agents):
        """Generate the alignment behavior

        Args:
            agents (List[Agent]): list of all agents

        Returns:
            Vector2: global direction to take in order for the agent to be align with the others
        """
        fov = 100
        average = Vector2()
        total = 0

        for agent in agents:
            distance = self.position.distance_to(agent.position)
            if distance < fov and self.position != agent.position:
                average += agent.velocity
                total += 1

        if total > 0:
            average = average / len(agents)

            # Setting magnitude to max to avoid standing still
            average = Vector2(
                average.x * self.max_mag / average.magnitude(),
                average.y * self.max_mag / average.magnitude(),
            )

            average -= self.velocity

        return average

    def cohesion(self, agents):
        """Generate the cohesion behavior

        Args:
            agents (List[Agent]): list of all agents

        Returns:
            Vector2: global direction to take in order for the agent to join the others
        """
        fov = 100
        average = Vector2()
        total = 0

        for agent in agents:
            distance = self.position.distance_to(agent.position)
            if distance < fov and self.position != agent.position:
                average += agent.position
                total += 1

        if total > 0:
            average = average / total

            average -= self.position

            # Setting magnitude to max to avoid standing still
            average = Vector2(
                average.x * self.max_mag / average.magnitude(),
                average.y * self.max_mag / average.magnitude(),
            )

            average -= self.velocity

            # if average.magnitude() > self.max_force:
            #     average = (average / average.magnitude()) * self.max_force

        return average

    def separation(self, agents):
        """Generate the separation behavior

        Args:
            agents (List[Agent]): list of all agents

        Returns:
            Vector2: global direction to take in order for the agent to join the others
        """
        fov = 100
        average = Vector2()
        total = 0

        for agent in agents:
            distance = self.position.distance_to(agent.position)
            if distance < fov and self.position != agent.position:
                intersection = self.position - agent.position
                intersection /= distance
                average += intersection
                total += 1

        if total > 0:
            average = average / len(agents)

            # Setting magnitude to max to avoid standing still
            average = Vector2(
                average.x * self.max_mag / average.magnitude(),
                average.y * self.max_mag / average.magnitude(),
            )

            average -= self.velocity
            if average.magnitude() > self.max_force:
                average = (average / average.magnitude()) * self.max_force

        return average

    def follow(self, group):
        """Concatenation of all different behaviours

        Args:
            group (List[Agent]): [description]
        """
        align_vector = self.align(group)
        cohesion_vector = self.cohesion(group)
        separation_vector = self.separation(group)
        self.acceleration = Vector2(0.0, 0.0)
        self.acceleration += align_vector
        self.acceleration += cohesion_vector / 2
        self.acceleration += separation_vector

    def out_of_bounds(self, width, height):
        """Make a out of bounds agent reappear on the other side of the screen

        Args:
            width (int): width of the game screen
            height (int): height of the game screen
        """
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width

        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height
