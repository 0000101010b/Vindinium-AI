import numpy as np
from Vmap import *
map = VGridMap(6,12)


map.set_disabled(3,4)

map.set_disabled(3,5)
map.set_disabled(3,6)
map.set_disabled(4,4)
map.set_disabled(5,4)
map.set_disabled(5,5)
map.set_disabled(5,6)
map.set_disabled(0,11)
map.print_grid()

map.remove_player()
map.set_player(2,4)
map.remove_player()
map1= map.get_taged_map(Pos(0,5))

map1.print_grid()

print(map.get_distance(map1,0,5))
#print(map.get_direction(map1,0,5))




#print(g)

#import network1 as net
#n = net.FC_net();
#n.add_param('a')
#n.add_param('b')
#n.add_param('c')
#n.add_action('1')
#n.add_action('2')

#n.generate_weight();
#input = [1,2,3]

#print (n.make_selection(input))
