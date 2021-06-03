import pygame
from pygame.math import Vector2

import random
import math

class Agent:
    def __init__(self, width, height):
        """Initialize agent parameters

        Args:
            width (int): width of the game screen
            height (int): height of the game screen
        """
        self.position = Vector2(random.randint(0, width), random.randint(0, height))
        self.velocity = Vector2(random.randint(-100, 100), random.randint(-100, 100))
        self.acceleration = Vector2(0.0, 0.0)
        self.max_force = 100
        self.max_mag = 300
        self.max_velocity = 5
    
    def update(self, dt):
        """Update the agent position

        Args:
            dt (float): delta time 
        """
        self.position += self.velocity * dt
        self.velocity += self.acceleration * dt
        self.acceleration = Vector2(0.0, 0.0)

    
    def align(self, agents):
        """ Generate the alignment behavior

        Args:
            agents (List[Agent]): list of all agents

        Returns:
            Vector2: global direction to take in order for the agent to be align with the others
        """
        fov = 1000
        average = Vector2(0.0, 0.0)
        total = 0
        
        for agent in agents:
            distance = self.position.distance_to(agent.position)
            if distance < fov and self.position != agent.position:
                average += agent.velocity
                total += 1

        if total > 0 :
            average = average / total
            
            # Setting magnitude to max to avoid standing still
            average = Vector2( average.x * self.max_mag / average.magnitude(), average.y * self.max_mag / average.magnitude())

            average -= self.velocity
            average = self.limit(average, self.max_force)
        
        return average
    
    def cohesion(self, agents):
        """Generate the cohesion behavior

        Args:
            agents (List[Agent]): list of all agents

        Returns:
            Vector2: global direction to take in order for the agent to join the others
        """
        fov = 200
        average = Vector2(0.0, 0.0)
        total = 0
        
        for agent in agents:
            distance = self.position.distance_to(agent.position)
            if distance < fov and self.position != agent.position:
                average += agent.position
                total += 1

        if total > 0 :

            average = average / total

            # Steering
            average -= self.position
            
            # Setting magnitude to max to avoid standing still
            average = Vector2( average.x * self.max_mag / average.magnitude(), average.y * self.max_mag / average.magnitude())
            
            average -= self.velocity
            average = self.limit(average, self.max_force)
        
        return average
    
    
    
    def follow(self, group):
        """Concatenation of all different behaviours

        Args:
            group (List[Agent]): [description]
        """
        align_vector = self.align(group)   
        cohesion_vector = self.cohesion(group)
        self.acceleration += align_vector
        self.acceleration += cohesion_vector
        
        
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

    def limit(self, vector: Vector2, n_max: int):
        """[summary]

        Args:
            vector (Vector2): [description]
            n_max (int): [description]

        Returns:
            Vector2: [description]
        """
        vx = vector.x
        vy = vector.y
        n = math.sqrt(vx**2 + vy**2)
        f = min(n, n_max) / n
        return Vector2(f*vx, f*vy)