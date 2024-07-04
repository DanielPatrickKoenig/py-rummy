import rg

game = rg.RummyGame(player_list=['computer', 'computer'])

def player_turn():
    if game.get_current_player()['type'] == 'human':
        print('i am human')
        game.draw_card(game.get_current_player())
        game.discard(3)

for n in range(0, 20):
    game.take_turn(player_turn)


# print('hand options')
# print(list(game.get_set_options()['unique_options']))

# print('pile options')
# print(list(game.get_set_options(include_hand=False, include_pile=True)['unique_options']))

# print('hand and pile options')
# print(list(game.get_set_options(include_hand=True, include_pile=True)['unique_options']))