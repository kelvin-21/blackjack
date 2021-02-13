import unittest
from domain.model import CardDeck, Card, Suit, Rank


class TestCardDeck(unittest.TestCase):
    def setUp(self):
        self.card_deck = CardDeck(num_card_set=2)
        self.card_9 = Card(Suit.SPADE, Rank.NINE)
        self.card_10 = Card(Suit.SPADE, Rank.TEN)

    def test_add_card(self):
        self.card_deck.add_card(self.card_10)

        self.assertEqual(len(self.card_deck.deck), 1)
        self.assertEqual(self.card_deck.deck[0].suit, Suit.SPADE)
        self.assertEqual(self.card_deck.deck[0].rank, Rank.TEN)

    def test_init(self):
        self.card_deck.init()

        self.assertEqual(len(self.card_deck.deck), 104)

    def given_empty_deck_then_return_true(self):
        result = self.card_deck.is_card_deck_empty()

        self.assertTrue(result)

    def given_non_empty_deck_then_return_false(self):
        self.card_deck.init()
        result = self.card_deck.is_card_deck_empty()

        self.assertFalse(result)

    def given_card_exist_and_search_card_then_return_card(self):
        self.card_deck.add_card(self.card_9)
        self.card_deck.add_card(self.card_10)
        card = self.card_deck.search_card(Suit.SPADE, Rank.NINE)

        self.assertIsNotNone(card)
        self.assertEqual(card, self.card_9)

    def given_card_not_exist_and_search_card_then_return_none(self):
        self.card_deck.add_card(self.card_9)
        self.card_deck.add_card(self.card_10)
        card = self.card_deck.search_card(Suit.DIAMOND, Rank.K)

        self.assertIsNone(card)

    def given_card_suit_exist_and_search_card_suit_then_return_card(self):
        self.card_deck.add_card(self.card_9)
        self.card_deck.add_card(self.card_10)
        card = self.card_deck.search_card(suit=Suit.SPADE)

        self.assertIsNotNone(card)
        self.assertEqual(card, self.card_9)

    def given_card_suit_not_exist_and_search_card_suit_then_return_none(self):
        self.card_deck.add_card(self.card_9)
        self.card_deck.add_card(self.card_10)
        card = self.card_deck.search_card(suit=Suit.DIAMOND)

        self.assertIsNone(card)

    def given_card_rank_exist_and_search_card_rank_then_return_card(self):
        self.card_deck.add_card(self.card_9)
        self.card_deck.add_card(self.card_10)
        card = self.card_deck.search_card(rank=Rank.NINE)

        self.assertIsNotNone(card)
        self.assertEqual(card, self.card_9)

    def given_card_rank_not_exist_and_search_card_rank_then_return_none(self):
        self.card_deck.add_card(self.card_9)
        self.card_deck.add_card(self.card_10)
        card = self.card_deck.search_card(rank=Rank.J)

        self.assertIsNone(card)

    def test_remove_card(self):
        self.card_deck.add_card(self.card_9)
        self.card_deck.add_card(self.card_10)
        self.card_deck.remove_card(self.card_9)

        search_card_9 = self.card_deck.search_card(Suit.SPADE, Rank.NINE)
        search_card_10 = self.card_deck.search_card(Suit.SPADE, Rank.TEN)
        self.assertEqual(len(self.card_deck.deck), 1)
        self.assertIsNone(search_card_9)
        self.assertIsNotNone(search_card_10)
        self.assertEqual(search_card_10, self.card_10)

    def get_random_card_from_nonempty_card_deck(self):
        card_deck = CardDeck(num_card_set=1)
        card_deck.init()
        card = card_deck.get_random_card()
        search_result = card_deck.search_card(card.suit, card.rank)

        self.assertEqual(len(card_deck.deck), 52)
        self.assertIsNotNone(search_result)

    def get_random_card_from_empty_card_deck_then_return_None(self):
        card = self.card_deck.get_random_card()

        self.assertIsNone(card)
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCardDeck('test_add_card'))
    suite.addTest(TestCardDeck('test_init'))
    suite.addTest(TestCardDeck('given_empty_deck_then_return_true'))
    suite.addTest(TestCardDeck('given_non_empty_deck_then_return_false'))
    suite.addTest(TestCardDeck('given_card_exist_and_search_card_then_return_card'))
    suite.addTest(TestCardDeck('given_card_not_exist_and_search_card_then_return_none'))
    suite.addTest(TestCardDeck('given_card_suit_exist_and_search_card_suit_then_return_card'))
    suite.addTest(TestCardDeck('given_card_suit_not_exist_and_search_card_suit_then_return_none'))
    suite.addTest(TestCardDeck('given_card_rank_exist_and_search_card_rank_then_return_card'))
    suite.addTest(TestCardDeck('given_card_rank_not_exist_and_search_card_rank_then_return_none'))
    suite.addTest(TestCardDeck('test_remove_card'))
    suite.addTest(TestCardDeck('get_random_card_from_nonempty_card_deck'))
    suite.addTest(TestCardDeck('get_random_card_from_empty_card_deck_then_return_None'))

    runner = unittest.TextTestRunner()
    runner.run(suite)