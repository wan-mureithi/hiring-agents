from .base import RankingAlgorithm


class EloRanking(RankingAlgorithm):
    def __init__(self, k=32):
        self.k = k

    def expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_ratings(self, winner_id, loser_id, ratings):
        rating_winner = ratings[winner_id]["elo"]
        rating_loser = ratings[loser_id]["elo"]

        expected_winner = self.expected_score(
            rating_winner, rating_loser
        )  # if rating is same: win expectation is 0.5, if rating A is higher: win expectation is > 0.5
        expected_loser = self.expected_score(rating_loser, rating_winner)

        new_rating_winner = rating_winner + self.k * (
            1 - expected_winner
        )  # 1000 + 32 * (1 - 0.5) = 1000 + 16 = 1016
        new_rating_loser = rating_loser + self.k * (
            0 - expected_loser
        )  # 1000 + 32 * (0 - 0.5) = 1000 - 16 = 984

        new_n_games_winner = ratings[winner_id]["n_games"] + 1
        new_n_games_loser = ratings[loser_id]["n_games"] + 1

        return {
            winner_id: {"elo": new_rating_winner, "n_games": new_n_games_winner},
            loser_id: {"elo": new_rating_loser, "n_games": new_n_games_loser},
        }
