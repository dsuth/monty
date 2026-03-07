from __future__ import annotations

class SeriesModel:
    def __init__(self, ps: list[float]) -> None:
        
        if len(ps) == 0:
            raise ValueError("ps must contain at least one entry")
        for p in ps:
            if not 0 <= p <= 1:
                raise ValueError("ps must be between 0..1")
        self.ps = ps

    def trial(self, rng) -> bool:
        
        for p in self.ps:
             if rng.random() < p:
                 return True
             
        return False
    

class ParallelModel:
    def __init__(self, ps: list[float]) -> None:
        
        if len(ps) == 0:
            raise ValueError("ps must contain at least one entry")
        for p in ps:
            if not 0 <= p <= 1:
                raise ValueError("ps must be between 0..1")
        self.ps = ps

    def trial(self, rng) -> bool:
        
        for p in self.ps:
            if rng.random() >= p:
                return False
             
        return True
        

