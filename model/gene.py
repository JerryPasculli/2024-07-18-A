from dataclasses import dataclass


@dataclass
class Gene:
    GeneID: str
    Function: str
    Essential: str
    Chromosome: int
    num = 0

    def __str__(self):
        return (f"{self.GeneID} - {self.Function} | Ess.: {self.Essential}, Chrom.: {self.Chromosome} | num. archi uscenti"
                f":{self.num}")

    def __hash__(self):
        return hash((self.GeneID, self.Function))

    def aggiungiArco(self):
        self.num = self.num+1

    def __lt__(self, other):
        return self.num<other.num