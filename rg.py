import cg

CardGame = cg.CardGame

class RummyGame (CardGame):
    def __init__(self, player_list=['computer', 'human'], suite_size=13, card_type_count=4, match_min_length=3, run_min_length=3, point_matrix={ 13: 2, 12: 2, 11: 2, 10: 2, 1: 3 }):
        CardGame.__init__(self, 7, player_list, suite_size, card_type_count, point_matrix=point_matrix)
        self.match_min_length = match_min_length
        self.run_min_length = run_min_length
        self.discard_pile = []
        self.sets = []
    
    def turn_action(self):
        super().turn_action()

        print('current player = ' + self.get_current_player()['name'])

        # pile_options = self.get_set_options(include_hand=False, include_pile=True)
        # if len(pile_options['options']) > 0:
        #     # process hand sets
        #     print('pile options')
        #     print(pile_options['options'][0]) # iterate through options
        #     # if has options add cards to hand

        print('opportunities')
        print(self.get_existing_set_opportunitie())
        
        combo_options = self.get_set_options(include_hand=True, include_pile=True)
        hand_before_combo = len(self.get_current_player()['hand'])
        print(str(hand_before_combo) + ' cards')
        if len(combo_options['options']) > 0:
            first_card_picked_up = self.draw_from_discard_pile(combo_options['unique_options'])
            print('first card picked up')
            print(first_card_picked_up)

        hand_after_combo = len(self.get_current_player()['hand'])
        print(str(hand_after_combo) + ' cards')
        if (hand_before_combo == hand_after_combo):
            self.draw_card(self.get_current_player()) # only if there are no pile related options

        hand_options = self.get_set_options()
        if len(hand_options['options']) > 0:
            # process hand sets
            for i, n in enumerate(hand_options['options']):
                self.add_set(self.get_current_player(), hand_options['options'][i]['cards'])
            print('sets')
            print(self.sets)

        self.discard(0)
    
    def discard(self, card_index):
        card_to_discard = self.get_current_player()['hand'].pop(card_index)
        self.discard_pile.append(card_to_discard)

    def get_matchables(self, lst):
        return list(filter(lambda z: z['count'] >= self.match_min_length, map(lambda y: { 'card': y, 'count': len(list(filter(lambda x: x['card'] == y, lst ))) }, self.suites)))
    
    def card_matches(self, lst):
        matchables = self.get_matchables(lst)
        return [list(filter(lambda x: n['card'] == x['card'], lst)) for n in matchables]
    
    def card_runs(self, lst):
        suite_groups = [list(filter(lambda x: n == x['suite'], lst)) for n in self.suites]
        eligible_suite_groups = list(filter(lambda x: len(x) >= self.run_min_length, suite_groups))
        sorted_esgs = [list(sorted(n, key=lambda x: x['card'])) for n in eligible_suite_groups]
        runs = []
        for group in sorted_esgs:
            run = []
            for n in group:
                if len(run) == 0 or run[len(run) - 1]['card'] == n['card'] - 1:
                    run.append(n)
                elif len(run) < 3:
                    run = []
            if len(run) >= 3:
                runs.append(run)
        return runs
    
    def get_options(self, include_hand=True, include_pile=False):
        option_list = []
        if include_pile:
            pile_matches = self.card_matches(self.discard_pile)
            pile_runs = self.card_runs(self.discard_pile)
            option_list.append(pile_matches)
            option_list.append(pile_runs)
        if include_hand:
            hand_matches = self.card_matches(self.get_current_player()['hand'])
            hand_runs = self.card_runs(self.get_current_player()['hand'])
            option_list.append(hand_matches)
            option_list.append(hand_runs)
        if include_pile and include_hand:
            hand_pile_combo = [n for n in self.discard_pile]
            hand_pile_combo.extend(self.get_current_player()['hand'])
            combo_matches = self.card_matches(hand_pile_combo)
            combo_runs = self.card_runs(hand_pile_combo)
            option_list.append(combo_matches)
            option_list.append(combo_runs)
        return option_list
    
    def get_set_options(self, include_hand=True, include_pile=False):
        option_list = self.get_options(include_hand=include_hand, include_pile=include_pile)
        valid_match_matrix = list(filter(lambda x: len(x) > 0, option_list))
        match_manifest = []
        full_list = []
        if len(valid_match_matrix) > 0:
            for entry in valid_match_matrix:
                for n in entry:
                    point_sum = sum(list(map(lambda x: x['points'], n)))
                    match_manifest.append({ 'cards': n, 'point_totals': point_sum })
                    full_list.extend(n)
        return { 'options': list(reversed(list(sorted(match_manifest, key=lambda x: x['point_totals'])))), 'unique_options': self.unique_card_list(full_list) }
    
    def get_used_cards(self):
        used_cards = []
        for n in self.sets:
            cards_in_set = map(lambda x: { 'card': x['card']['card'], 'suite': x['card']['suite'] }, n)
            used_cards.extend(cards_in_set)
        return used_cards

    def get_existing_set_opportunitie(self):
        match_sets = list(filter(lambda x: x[0]['card']['card'] == x[1]['card']['card'], self.sets))
        match_opportunities = []
        combo_list = [n for n in self.discard_pile]
        combo_list.extend(self.get_current_player()['hand'])
        for n in match_sets:
            match_opp = list(filter(lambda x: x['card'] == n[0]['card']['card'], combo_list))
            if len(match_opp) > 0:
                match_opportunities.extend(map(lambda x: { 'card': x, 'set': n[0]['index'] } , match_opp))
        # print('match opportunities')
        # print(match_opportunities)
        
        run_sets = list(filter(lambda x: x[0]['card']['suite'] == x[1]['card']['suite'], self.sets))
        # print('run sets')
        # print(run_sets)
        run_opportunities = []
        for n in run_sets:
            first_in_run = n[0]
            last_in_run = n[-1]
            values_before_first = list(reversed(list(filter(lambda x: x < first_in_run['card']['card'], self.suites))))
            values_after_first = list(filter(lambda x: x > last_in_run['card']['card'], self.suites))
            run_opp = []
            for vb in values_before_first:
                filtered_run = list(filter(lambda x: x['card'] == vb and n[0]['card']['suite'] == x['suite'], combo_list))
                if len(filtered_run) > 0:
                    run_opp.extend(filtered_run)
                else:
                    break
            
            for va in values_after_first:
                filtered_run = list(filter(lambda x: x['card'] == va and n[0]['card']['suite'] == x['suite'], combo_list))
                if len(filtered_run) > 0:
                    run_opp.extend(filtered_run)
                else:
                    break
            if len(run_opp) > 0:
                run_opportunities.extend(map(lambda x: { 'card': x, 'set': n[0]['index'] } , run_opp))
        # iterate forward and backward to check for run additions
        opportunities = []
        opportunities.extend(match_opportunities)
        opportunities.extend(run_opportunities)
        return opportunities

    def add_set(self, player, cards):
        cards_for_set = []
        for n in cards:
            card_in_hand = self.find_card(n, self.get_current_player()['hand'])
            if card_in_hand:
                removed_hand_card = self.get_current_player()['hand'].pop(card_in_hand['index'])
                cards_for_set.append(removed_hand_card)
            # else:
            #     card_in_pile = self.find_card(n, self.discard_pile)
            #     if card_in_pile:
            #         removed_pile_card = self.discard_pile.pop(card_in_hand['index'])
            #         cards_for_set.append(removed_pile_card)
        if len(cards_for_set) >= self.match_min_length:
            set_index = len(self.sets)
            self.sets.append(list(map(lambda x: { 'card': x, 'player': player['name'], 'index': set_index } ,cards_for_set)))

    def draw_from_discard_pile(self, target_cards):
        discard_pile_with_indexes = []
        for i, n in enumerate(self.discard_pile):
            discard_pile_with_indexes.append({ 'card': n['card'], 'suite': n['suite'], 'index': i })
        print('draw_from_discard_pile')
        filtered_indexed_discard_matches = list(filter(None, [self.find_card(n, target_cards) for n in discard_pile_with_indexes]))
        sorted_discard_matches = list(sorted(list(map(lambda x: x['index'], filtered_indexed_discard_matches))))
        print(sorted_discard_matches)

        first_card_pulled = None
        if len(sorted_discard_matches) > 0:
            cards_to_pickup = list(reversed(list(range(sorted_discard_matches[0], len(self.discard_pile)))))
            for i, n in enumerate(cards_to_pickup):
                pulled_card = self.discard_pile.pop(n)
                if i == 0:
                    first_card_pulled = pulled_card
                self.get_current_player()['hand'].append(pulled_card)
        return first_card_pulled