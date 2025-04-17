from abc import ABC, abstractmethod


class RankingAlgorithm(ABC):
    @abstractmethod
    def update_ratings(
        self, winner_id, loser_id, ratings: dict[str, dict]
    ) -> dict[str, dict]:
        pass
