from ArenaHealthBars import *
from time import sleep
import random
import sys

class Arena:
    def __init__(self, universe, player, monsterIndex, x, y):
        self.universe = universe # Easy access to universe.
        self.player = player
        self.player.arena_x = 5 # Initial player position in Arena.
        self.player.arena_y = 3
        self.monsterIndex = monsterIndex
        self.monster = self.universe.monsters[monsterIndex]
        self.monster.arena_x = 19 # Initial monster position in Arena.
        self.monster.arena_y = 3
        self.arenaHealthBars = ArenaHealthBars(player, self.monster)
        self.x = x  # screen dimensions just in case we need them
        self.y = y
        self.state = 0 # Not sure how the actual arena code will work, but if there are different phases or turns, using states might come in handy

    def animatePlayerAttack(self):
        """Draws and prints intermediate frames for the player's attack animation."""
        # Player raises sword.
        self.arenaHealthBars.draw(self.universe.screen)
        self.player.ASCII = ["_____@", "@@\o/@",
                                "@@/@@@", "@/@\@@", "/@@@\\@"]
        # This needs to be 2 because there's an extra line in this ASCII art.
        self.player.moveInArena(5, 2)
        self.player.drawArena(self.universe.screen)
        self.monster.moveInArena(19, 3)
        self.monster.drawArena(self.universe.screen)
        self.universe.screen.print()
        sleep(0.5)

        # Player swings sword.
        self.arenaHealthBars.draw(self.universe.screen)
        self.player.ASCII = ["@@@o@@", "@@/\@@", "@/@\\\@", "/@@@\\\\"]
        self.player.moveInArena(14, 3)
        self.player.drawArena(self.universe.screen)
        # Monster flinches.
        self.monster.ASCII = ["@@\A/@", "@@@|@|", "@@/\@|", "@@\@\\|"]
        self.monster.drawArena(self.universe.screen)
        self.universe.screen.print()
        sleep(0.5)

        # Update player and monster ASCII with the original positions
        # for the start of the usual draw step.
        self.player.moveInArena(5, 3)
        self.player.ASCII = ["@@@o@/", "@@/</@", "@/@\@@", "/@@@\@"]
        self.monster.moveInArena(19, 3)
        self.monster.ASCII = ["\@@A@@", "@\/|>@", "@@@/\@", "@@@\@\\"]

    def animateMonsterAttack(self):
        """Draws and prints intermediate frames for the monster's attack animation."""
        # Monster raises sword.
        self.arenaHealthBars.draw(self.universe.screen)
        self.monster.ASCII = ["@_____", "@\A/@@",
                                "@@\@@@", "@/@\@@", "/@@@\\@"]
        # This needs to be 2 because there's an extra line in this ASCII art.
        self.monster.moveInArena(19, 2)
        self.monster.drawArena(self.universe.screen)
        self.player.moveInArena(5, 3)
        self.player.drawArena(self.universe.screen)
        self.universe.screen.print()
        sleep(0.5)
    
        # Monster swings sword.
        self.arenaHealthBars.draw(self.universe.screen)
        self.monster.ASCII = ["@@@A@@", "@@/\@@", "@/@\\\@", "/@@@\\\\"]
        self.monster.moveInArena(9, 3)
        self.monster.drawArena(self.universe.screen)
        # Player flinches.
        self.player.ASCII = ["@@\o/@", "@@@|@|", "@@/\@|", "@@\@\\|"]
        self.player.drawArena(self.universe.screen)
        self.universe.screen.print()
        sleep(0.5)
    
        # Update player and monster ASCII with the original positions
        # for the start of the usual draw step.
        self.monster.moveInArena(19, 3)
        self.monster.ASCII = ["\@@A@@", "@\/|>@", "@@@/\@", "@@@\@\\"]
        self.player.moveInArena(5, 3)
        self.player.ASCII = ["@@@o@/", "@@/</@", "@/@\\@@", "/@@@\\@"]

    def update(self, inputs):
        """
        :param inputs: User input.
        """
        acceptable_inputs = ['a', 'r']

        if len(inputs) != 1 or inputs not in acceptable_inputs:
            print('Invalid input')
            return

        if inputs == 'r':
            # Run away.
            print('run away')

            # TODO: We'll need to remember the last position of Player in
            # the Overworld so we can revert to it in case we run.

            # Destroy Arena and return to Overworld.
            self.universe.arena = None
            self.universe.isOverworld = True

        if inputs == 'a':
            # TODO: Either remove this or turn it into a useful dialog.
            print('attack')

            # Hacky drawing of intermediate action frames here.
            self.animatePlayerAttack()

            # Damage is applied after the intermediate action frames show
            # the attack successfully landing. This results in the
            # health bar being shown to shorten only after the attack lands.
            # Otherwise, the health bar is shown to shorten before the
            # attack even lands.
            self.player.attack(self.monster)
            
            #same as above but with the monster
            self.animateMonsterAttack()
            self.monster.attack(self.player)

        if self.monster.currentHealth <= 0:
            # Any number <10 will cause 0 bars to be drawn for the health bar.
            # So although the monster technically still has health left,
            # it's misleading and bad UX to draw 0 bars.

            # Monster defeated.
            # TODO: Draw and print victory screen.
            print('VICTORY!')

            # Remove monster from monster list.
            del self.universe.monsters[self.monsterIndex]

            # This clean up needs to happen after the victory screen is
            # drawn and printed, otherwise there won't be an Arena to refer
            # to.
            self.universe.arena = None
            self.universe.isOverworld = True
            
        if self.player.currentHealth <= 0:
            # Any number <10 will cause 0 bars to be drawn for the health bar.
            # So although the monster technically still has health left,
            # it's misleading and bad UX to draw 0 bars.

            # Player defeated.
            # TODO: Draw and print victory screen.
            print('DEFEAT')

            # Remove player
            del self.universe.player

            # This clean up needs to happen after the drawn screen is
            # drawn and printed, otherwise there won't be an Arena to refer
            # to.
            self.universe.arena = None
            self.universe.isOverworld = True
            
            #terminate game
            sys.exit()



    def draw(self, screen):
        self.player.drawArena(screen)
        self.monster.drawArena(screen)
        self.arenaHealthBars.draw(screen)
