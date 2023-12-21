import pygame
import json

from circuit import Goal

pygame.init()
window = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

rect = pygame.Rect(180, 180, 40, 40)
speed = 5

goals = []
current_active = 0
with open('goals.json', 'r') as file:
    data = json.load(file)
    json_goals = data['map2']['goals']
    for i,goal in enumerate(json_goals):
        goals.append(Goal(goal['p1'], goal['p2'], i == current_active))
        
def draw_goals():
    global window
    global goals
    
    window.fill(0)
    for goal in goals:
        pygame.draw.line(window, "white" if goal.is_active() else 'blue', *goal.get_line())
        
def cross_goal(goal: Goal):
    if goal.is_active():
        has_crossed = any(rect.clipline(goal.get_line()))
        if has_crossed:
            activate_next()
            draw_goals()
        return has_crossed
    else:
        return False
    
def activate_next():
    global current_active
    global goals
    
    if current_active == len(goals) - 1:
        current_active = 0
    else:
        current_active += 1
        
    for i,g in enumerate(goals):
        #goals[i].switch_to(i == current_active)
        g.switch_to(i == current_active)
        
    return goals

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    keys = pygame.key.get_pressed()
    rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
    rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed
    rect.centerx %= window.get_width()
    rect.centery %= window.get_height()

    color = "red" if any(cross_goal(goal) for goal in goals) else "green"

    window.fill(0)
    
    draw_goals()
    pygame.draw.rect(window, color, rect)
    pygame.display.flip()

pygame.quit()
exit()