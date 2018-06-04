import time
import sys

sys.path.insert(0, '../../src')

from entities.movement.legs import Legs
from entities.movement.sequences.walking_sequences import *

legs = Legs(leg_0_servos=[
                14,
                61,
                63
            ]
#            leg_1_servos=[
#                21,
#                31,
#                53
#            ],
#            leg_2_servos=[
#                61,
#                63,
#                111
#            ],
#            leg_3_servos=[
#                111,
#                111,
#                111
#            ]
            )

# legs.deploy(150)
walk_forward_repeat(legs, [200, 200, 200], 10)
wave(legs, [150, 150, 150], 10)
enge_dab(legs, [140, 140, 140])
legs.retract(90)