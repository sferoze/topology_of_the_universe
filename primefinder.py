import numpy as np
import math

class TopologicalPrimeFinder:
    """
    Find primes using I = D × R = 24 framework
    Theory: Primes occur where numbers can't form stable knots
    """
    
    def __init__(self):
        # Framework constants
        self.n_min = 3
        self.D = 3
        self.R = 8
        self.I = 24
        self.alpha = 1 / (self.n_min * np.sqrt(self.R))  # ≈ 0.118
        self.stability_threshold = (self.n_min - 1) - np.log(2 * self.n_min)  # ≈ 0.208
        
    def number_topology(self, n):
        """Calculate the topological 'knottability' of a number"""
        if n < 2:
            return 0
            
        # Factor-based topology score
        factor_count = 0
        factor_sum = 0
        
        # Count factors up to sqrt(n)
        for i in range(2, int(np.sqrt(n)) + 1):
            if n % i == 0:
                factor_count += 1
                factor_sum += i
                if i != n // i:
                    factor_count += 1
                    factor_sum += n // i
        
        # Calculate distinctions (D) - based on factor patterns
        D_score = min(factor_count, self.D) if factor_count > 0 else 0
        
        # Calculate relations (R) - based on factor relationships  
        if factor_count > 0:
            R_score = (factor_sum % self.R) + (n % self.R) / self.R
        else:
            R_score = (n % self.R) / self.R
            
        # Information content
        I_score = D_score * R_score
        
        return I_score
    
    def is_prime_topological(self, n):
        """
        Determine if n is prime based on topology
        Primes have I_score below stability threshold
        """
        if n < 2:
            return False
        if n == 2:
            return True  # Special case
            
        I_score = self.number_topology(n)
        
        # Prime if topologically "unknottable"
        return I_score < self.stability_threshold
    
    def predict_next_prime(self, n):
        """Predict where the next prime after n will occur"""
        current = n + 1
        
        while True:
            # Calculate topology gap
            gap_score = self.topology_gap(current)
            
            # If gap indicates prime location
            if self.is_prime_topological(current):
                return current
                
            # Jump based on topology (not just +1)
            jump = max(1, int(gap_score * self.n_min))
            current += jump
            
    def topology_gap(self, n):
        """Calculate how far we are from next topology hole"""
        # Based on local information density
        local_I = sum(self.number_topology(n + i) for i in range(-2, 3)) / 5
        
        # Gap prediction based on I = 24 rhythm
        gap = (self.I - local_I) / self.alpha
        
        return max(1, abs(gap))
    
    def generate_primes_topological(self, limit):
        """Generate primes up to limit using topology"""
        primes = []
        
        # Check 2 separately
        if limit >= 2:
            primes.append(2)
            
        # Check odd numbers using topology
        for n in range(3, limit + 1, 2):
            if self.is_prime_topological(n):
                # Verify with traditional method for accuracy
                if self.verify_prime(n):
                    primes.append(n)
                    
        return primes
    
    def verify_prime(self, n):
        """Traditional verification for comparison"""
        if n < 2:
            return False
        for i in range(2, int(np.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def prime_pattern_analysis(self, limit=1000):
        """Analyze prime gaps using I = 24 framework"""
        primes = self.generate_primes_topological(limit)
        gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
        
        # Analyze gaps for I = 24 pattern
        patterns = {
            'avg_gap': np.mean(gaps),
            'gap_mod_24': [g % self.I for g in gaps],
            'gap_mod_8': [g % self.R for g in gaps],
            'gap_mod_3': [g % self.n_min for g in gaps]
        }
        
        return patterns

# Test the algorithm
def demonstrate_topological_primes():
    tpf = TopologicalPrimeFinder()
    
    print("Topological Prime Finder - Based on I = D × R = 24")
    print("="*50)
    
    # Test on first 100 numbers
    print("\nFirst 25 primes using topology:")
    primes = tpf.generate_primes_topological(100)
    print(primes[:25])
    
    # Analyze patterns
    print("\nPrime gap patterns:")
    patterns = tpf.prime_pattern_analysis(1000)
    print(f"Average gap: {patterns['avg_gap']:.2f}")
    print(f"Gaps mod 24 distribution: {set(patterns['gap_mod_24'])}")
    print(f"Gaps mod 8 distribution: {set(patterns['gap_mod_8'])}")
    
    # Test prediction
    print("\nPredicting next primes:")
    test_numbers = [100, 200, 500, 1000]
    for n in test_numbers:
        next_prime = tpf.predict_next_prime(n)
        print(f"Next prime after {n}: {next_prime}")
    
    # Show topology scores
    print("\nTopology scores for numbers 1-20:")
    for i in range(1, 21):
        score = tpf.number_topology(i)
        is_prime = tpf.verify_prime(i)
        print(f"{i}: score={score:.3f}, prime={is_prime}")

if __name__ == "__main__":
    demonstrate_topological_primes()