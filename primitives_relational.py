# core/primitives.py

from typing import List, Set, Optional, Dict
import math

from sympy.combinatorics.braids import BraidGroup, Braid

# Relational Primitives (Axiom I, as seen in convergence_relational.py)
# While not directly used in the possibility space representation, they define the context.
ABSENCE = None          # The Negative Space
PRESENCE = (1, ABSENCE) # The Primordial Strand


class InformationLayer:
    """
    Defines the foundational structure of the 24-dimensional Information Layer (I=D x R = 3 x 8).
    """
    DIMENSIONS = 24
    B_GROUP = BraidGroup(DIMENSIONS)
    ALPHABET_SET = frozenset(B_GROUP)
    # Optimization: Pre-calculate the map for faster lookups
    ALPHABET_MAP: Dict[str, int] = {char: i for i, char in enumerate(B_GROUP)}

    @staticmethod
    def get_char_at_index(index: int) -> str:
        """Helper to get character by index, wrapping cyclically around the 24 dimensions."""
        return InformationLayer.BASE24_ALPHABET[index % InformationLayer.DIMENSIONS]

    @staticmethod
    def get_index_of_char(char: str) -> int:
        """Helper to get the index of a character."""
        return InformationLayer.ALPHABET_MAP[char]



class KnotState:
    def __init__(self, braid: Braid = None):
        if braid:
            self.braid = braid
        else:
            self.braid = InformationLayer.B_GROUP.identity

    def calculate_complexity(self) -> int:
        # Topological Complexity
        return len(self.braid.word)

    def copy(self) -> 'KnotState':
        """Creates a deep copy of the current state."""
        # Ensure that the sets within the list are copied.
        new_space = [digit_set.copy() for digit_set in self.possibility_space]
        return KnotState(self.num_digits, initial_state=new_space)

    def is_converged(self) -> bool:
        """Checks if the state has converged to a single solution (minimum entropy)."""
        return all(len(digit_set) == 1 for digit in self.possibility_space)

    def is_invalid(self) -> bool:
        """Checks if the state is invalid (over-constrained; an empty possibility set)."""
        return any(len(digit_set) == 0 for digit in self.possibility_space)

    def calculate_entropy(self) -> float:
        """
        Calculates the current entropy (uncertainty) of the state.
        Uses log base 24 to measure entropy rigorously within the I-Space 24 framework.
        """
        total_entropy = 0.0
        for digit_set in self.possibility_space:
            count = len(digit_set)
            if count > 0:
                # Entropy = log_24(N)
                total_entropy += math.log(count, InformationLayer.DIMENSIONS)
        return total_entropy

    def get_solution(self) -> Optional[str]:
        """Returns the solution string if converged, otherwise None."""
        if not self.is_converged():
            return None
        # Efficiently extract the single element from each set
        return "".join(next(iter(digit_set)) for digit_set in self.possibility_space)

    def __repr__(self):
        if self.is_invalid():
            return f"<KnotState Dimensions={self.num_digits}, Status=Invalid>"
        
        if self.is_converged():
            status = f"Converged: {self.get_solution()}"
        else:
            # Show how many digits have converged and the current entropy
            entropy = self.calculate_entropy()
            converged_count = sum(1 for p in self.possibility_space if len(p) == 1)
            status = f"Entropy: {entropy:.4f}, Converged: {converged_count}/{self.num_digits}"
        return f"<KnotState {status}>"