import pygame
import random
import math
from config import *

class Particle:
    def __init__(self, x, y, color, velocity, lifetime, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity[0]
        self.velocity_y = velocity[1]
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.alpha = 255
    
    def update(self):
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Apply gravity
        self.velocity_y += 0.1
        
        # Update lifetime and alpha
        self.lifetime -= 1
        self.alpha = int((self.lifetime / self.max_lifetime) * 255)
        
        # Slow down
        self.velocity_x *= 0.98
        self.velocity_y *= 0.98
    
    def is_alive(self):
        return self.lifetime > 0

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def update(self):
        # Update all particles and remove dead ones
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
    
    def draw(self, screen, camera):
        # Draw all particles
        for particle in self.particles:
            if particle.alpha > 0:
                # Create a surface for the particle with alpha
                particle_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
                
                # Draw the particle with current alpha
                pygame.draw.circle(
                    particle_surface,
                    (*particle.color, particle.alpha),
                    (particle.size, particle.size),
                    particle.size
                )
                
                # Apply camera offset and draw
                pos = camera.apply_rect(pygame.Rect(
                    particle.x - particle.size,
                    particle.y - particle.size,
                    particle.size * 2,
                    particle.size * 2
                ))
                screen.blit(particle_surface, pos)
    
    def create_hit_effect(self, x, y, color=(255, 255, 255)):
        """Create particles for a hit effect"""
        num_particles = random.randint(5, 8)
        for _ in range(num_particles):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.randint(20, 30)
            size = random.randint(2, 4)
            self.particles.append(Particle(x, y, color, velocity, lifetime, size))
    
    def create_death_effect(self, x, y, color=(255, 0, 0)):
        """Create particles for a death effect"""
        num_particles = random.randint(15, 20)
        for _ in range(num_particles):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3, 7)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.randint(30, 45)
            size = random.randint(3, 6)
            self.particles.append(Particle(x, y, color, velocity, lifetime, size))
    
    def create_movement_trail(self, x, y, color=(100, 100, 255)):
        """Create particles for movement trail"""
        if random.random() < 0.3:  # Only create particles sometimes
            velocity = (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            lifetime = random.randint(10, 20)
            size = random.randint(2, 3)
            self.particles.append(Particle(x, y, color, velocity, lifetime, size))
    
    def create_attack_effect(self, x, y, direction, color=(255, 255, 0)):
        """Create particles for attack effect"""
        num_particles = random.randint(8, 12)
        spread = math.pi / 4  # 45-degree spread
        
        for _ in range(num_particles):
            angle = direction + random.uniform(-spread, spread)
            speed = random.uniform(4, 8)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.randint(15, 25)
            size = random.randint(2, 4)
            self.particles.append(Particle(x, y, color, velocity, lifetime, size)) 