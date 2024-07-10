import rg

game = rg.RummyGame(player_list=['computer', 'computer', 'computer'])

game.set_discard_rating_value('p0', card_point_factor=4)
game.set_discard_rating_value('p1', card_point_factor=2.5)

def player_turn():
    if game.get_current_player()['type'] == 'human':
        print('i am human')
        game.draw_card(game.get_current_player())
        game.discard(3)

while not game.game_over:
    game.take_turn(player_turn)

# for n in range(0, 12):
#     game.take_turn(player_turn)


# print('hand options')
# print(list(game.get_set_options()['unique_options']))

# print('pile options')
# print(list(game.get_set_options(include_hand=False, include_pile=True)['unique_options']))

# print('hand and pile options')
# print(list(game.get_set_options(include_hand=True, include_pile=True)['unique_options']))