import random
import math

from tqdm import tqdm

def build_dj_set(tracks, set_length, min_rating, algorithm):
    algorithms = {
        "greedy": build_dj_set_greedy,
        "dynamic": build_dj_set_dynamic,
        "genetic": build_dj_set_genetic,
        "simulated_annealing": build_dj_set_simulated_annealing,
        "glued": build_dj_set_glued,
    }

    return algorithms[algorithm](tracks, set_length, min_rating)

'''
Greedy algorithm with randomization: Randomly select a track. Iteratively choose the next track in the set 
by selecting the track with the highest compatibility score (based on both key and 
BPM) from a random subset of the remaining tracks. This will create a set that 
generally follows the key and BPM rules while allowing for some variation and 
creativity.
'''
def build_dj_set_greedy(tracks, set_length, min_rating):
    sorted_tracks = sorted(tracks, key=lambda t: t.bpm)

    # Separate prioritized tracks and other tracks
    prioritized_tracks = [track for track in sorted_tracks if track.rating >= min_rating]
    other_tracks = [track for track in sorted_tracks if track.rating < min_rating]

    dj_set = []

    # Add the first track (prioritized if available, otherwise the first other track)
    if prioritized_tracks:
        dj_set.append(prioritized_tracks.pop(0))
    elif other_tracks:
        dj_set.append(other_tracks.pop(0))

    # Fill in the set with prioritized tracks and other tracks
    while len(dj_set) < set_length and (prioritized_tracks or other_tracks):
        last_track = dj_set[-1]

        # Compute compatibility scores for prioritized tracks
        prioritized_compatibility_scores = [
            (0.6 * last_track.key_compatibility_score(track)) + (0.4 * last_track.bpm_compatibility_score(track))
            for track in prioritized_tracks
        ]

        # Compute compatibility scores for other tracks
        other_compatibility_scores = [
            (0.6 * last_track.key_compatibility_score(track)) + (0.4 * last_track.bpm_compatibility_score(track))
            for track in other_tracks
        ]

        # Find the best matching track
        if prioritized_compatibility_scores:
            best_prioritized_track_index = prioritized_compatibility_scores.index(max(prioritized_compatibility_scores))
            best_track = prioritized_tracks.pop(best_prioritized_track_index)
        else:
            best_other_track_index = other_compatibility_scores.index(max(other_compatibility_scores))
            best_track = other_tracks.pop(best_other_track_index)

        # Add the best track to the set
        dj_set.append(best_track)

    return dj_set

def build_dj_set_glued(tracks, set_length, min_rating, key_importance=0.6, bpm_importance=0.4):
    sorted_tracks = sorted(tracks, key=lambda t: (t.bpm, t.key))

    # Separate prioritized tracks and other tracks
    prioritized_tracks = [track for track in sorted_tracks if track.rating >= min_rating]
    other_tracks = [track for track in sorted_tracks if track.rating < min_rating]

    dj_set = []

    # Iterate through prioritized tracks, and glue them together with the other tracks
    for i, prioritized_track in enumerate(prioritized_tracks):
        # Append the prioritized track to the set
        dj_set.append(prioritized_track)

        # If this is the last prioritized track or the set reaches the desired length, break the loop
        if i == len(prioritized_tracks) - 1 or len(dj_set) == set_length:
            break

        next_prioritized_track = prioritized_tracks[i + 1]

        # Continue adding glue tracks until the next prioritized track is reached or the set reaches the desired length
        while len(dj_set) < set_length - 1 and other_tracks:
            # Compute compatibility scores for the other tracks with both the current and the next prioritized tracks
            compatibility_scores = [
                (key_importance * prioritized_track.key_compatibility_score(track) + 
                 bpm_importance * prioritized_track.bpm_compatibility_score(track)) *
                (key_importance * next_prioritized_track.key_compatibility_score(track) + 
                 bpm_importance * next_prioritized_track.bpm_compatibility_score(track))
                for track in other_tracks
            ]

            # Find the best matching glue track
            best_glue_track_index = compatibility_scores.index(max(compatibility_scores))
            best_glue_track = other_tracks.pop(best_glue_track_index)

            # Append the best glue track to the set
            dj_set.append(best_glue_track)

            # Check if the best glue track is compatible with the next prioritized track
            glue_track_next_compatibility = (key_importance * best_glue_track.key_compatibility_score(next_prioritized_track)) + \
                                             (bpm_importance * best_glue_track.bpm_compatibility_score(next_prioritized_track))

            if glue_track_next_compatibility >= 0.75:
                break

    # Fill the remaining set slots with other tracks if there is still room
    while len(dj_set) < set_length and other_tracks:
        dj_set.append(other_tracks.pop(0))

    return dj_set







'''
This implementation first filters the input tracks based on the minimum rating 
requirement. Then, it initializes a dynamic programming table dp, where dp[i][j] 
represents the maximum total score that can be obtained with the first i tracks 
and a set of length j.

The dynamic programming table is built iteratively by considering all possible 
combinations of tracks and set lengths. The total score is calculated as the 
sum of the track rating and the average of key compatibility and BPM compatibility 
scores with the previous track in the set. The optimal set is reconstructed from 
the dynamic programming table by iterating backward and selecting tracks that 
contributed to the maximum total score.

Note that this algorithm prioritizes both key and BPM compatibility, as well as 
track ratings. It is more likely to create a set with smooth transitions and 
a coherent flow, but it might not be as efficient as some other algorithms for 
large track lists.
'''
def build_dj_set_dynamic(tracks, set_length, min_rating):
    prioritized_rating = min_rating + 1
    memo = {}

    def track_score(track, prev_track):
        key_bpm_score = (track.key_compatibility_score(prev_track) + track.bpm_compatibility_score(prev_track)) / 2
        rating_score = track.rating if track.rating >= prioritized_rating else 0
        return key_bpm_score + rating_score

    def dynamic_dj_set(prev_track, remaining_tracks, remaining_length, pbar):
        if remaining_length == 0:
            return []

        memo_key = (prev_track, frozenset(remaining_tracks), remaining_length)
        if memo_key in memo:
            return memo[memo_key]

        max_score = -1
        best_next_track = None
        best_next_dj_set = None

        for track in remaining_tracks:
            score = track_score(track, prev_track)
            next_dj_set = dynamic_dj_set(track, remaining_tracks - {track}, remaining_length - 1, pbar)
            total_score = score + sum(track_score(next_track, prev_track) for prev_track, next_track in zip([track] + next_dj_set[:-1], next_dj_set))

            if total_score > max_score:
                max_score = total_score
                best_next_track = track
                best_next_dj_set = next_dj_set

        best_dj_set = [best_next_track] + best_next_dj_set
        memo[memo_key] = best_dj_set
        pbar.update(1)
        return best_dj_set

    first_track = random.choice(tracks)
    remaining_tracks = set(tracks) - {first_track}
    dj_set = [first_track]
    with tqdm(total=set_length - 1, desc="Building DJ set (Dynamic Programming)") as pbar:
        dj_set += dynamic_dj_set(first_track, remaining_tracks, set_length - 1, pbar)
    
    return dj_set


'''
This implementation initializes a population of random DJ sets and evolves 
the population for a specified number of generations. The fitness function 
combines key compatibility, BPM compatibility, track ratings, and a priority 
for tracks with a certain minimum rating.

The genetic algorithm improves the DJ sets through selection, crossover, 
and mutation operations. The selection function chooses two parent DJ sets 
from the population with probabilities proportional to their fitness. 
The crossover function combines the parents to create a new child DJ set. 
The mutation function applies random swaps to the child DJ set with a specified 
mutation rate.

After the specified number of generations, the algorithm returns the DJ set with 
the highest fitness in the final population. This approach allows for creative and 
unique DJ sets that follow the general rules for smooth transitions and coherent 
flow while giving priority to tracks with a certain minimum rating.

Note: You can adjust the parameters such as population_size, generations, 
mutation_rate, and prioritized_rating based on your preferences and desired 
level of complexity.
'''
def build_dj_set_genetic(tracks, set_length, min_rating):
    population_size = 240
    generations = 1500
    mutation_rate = 0.2
    prioritized_rating = min_rating + 1

    def fitness(dj_set):
        fitness = 0
        for i, track in enumerate(dj_set[:-1]):
            next_track = dj_set[i + 1]
            key_bpm_score = (track.key_compatibility_score(next_track) + track.bpm_compatibility_score(next_track)) / 2
            rating_score = track.rating if track.rating >= prioritized_rating else 0
            fitness += key_bpm_score + rating_score
        return fitness

    def selection(population, fitnesses):
        total_fitness = sum(fitnesses)
        probabilities = [fitness / total_fitness for fitness in fitnesses]
        selected_indices = random.choices(range(len(population)), probabilities, k=2)
        return [population[i] for i in selected_indices]

    def crossover(parents):
        crossover_point = random.randint(1, set_length - 1)
        child = parents[0][:crossover_point] + parents[1][crossover_point:]
        
        # Ensure there are no duplicate tracks in the child
        seen_tracks = set()
        for i, track in enumerate(child):
            if track not in seen_tracks:
                seen_tracks.add(track)
            else:
                remaining_tracks = set(tracks) - seen_tracks
                child[i] = random.choice(list(remaining_tracks))
                seen_tracks.add(child[i])

        return child

    def mutate(dj_set):
        mutated_dj_set = dj_set[:]
        for i in range(set_length):
            if random.random() < mutation_rate:
                swap_index = random.randint(0, set_length - 1)
                mutated_dj_set[i], mutated_dj_set[swap_index] = mutated_dj_set[swap_index], mutated_dj_set[i]
        return mutated_dj_set

    # Initialize the population with random DJ sets
    population = [random.sample(tracks, set_length) for _ in range(population_size)]

    for generation in tqdm(range(generations), desc="Building DJ set (Genetic Algorithm)"):
        fitnesses = [fitness(dj_set) for dj_set in population]

        # Create a new population through selection, crossover, and mutation
        new_population = []
        for _ in range(population_size):
            parents = selection(population, fitnesses)
            child = crossover(parents)
            mutated_child = mutate(child)
            new_population.append(mutated_child)

        population = new_population

    # Return the DJ set with the highest fitness in the final population
    return max(population, key=fitness)


'''
This implementation starts with a random DJ set and iteratively generates 
neighbors of the current set by swapping two tracks. The score function combines 
key compatibility, BPM compatibility, and track ratings, giving priority to 
tracks with a certain minimum rating.

The simulated annealing algorithm improves the DJ set through exploration and 
exploitation. The algorithm can accept worse solutions with a probability that 
decreases over time according to a temperature parameter. This allows the 
algorithm to explore different solutions and avoid getting stuck in local optima.

The temperature is initially set to a high value and gradually decreases over 
time according to a cooling rate. The algorithm terminates when the temperature 
reaches a specified final value.

This approach allows for creative and unique DJ sets that follow the general 
rules for smooth transitions and coherent flow while giving priority to tracks 
with a certain minimum rating.

Note: You can adjust the parameters such as iterations, initial_temperature, 
final_temperature, cooling_rate, and prioritized_rating based on your preferences 
and desired level of complexity.
'''
def build_dj_set_simulated_annealing(tracks, set_length, min_rating):
    iterations = 5000
    initial_temperature = 100
    final_temperature = 0.01
    cooling_rate = 0.99
    prioritized_rating = min_rating + 1

    def score(dj_set):
        total_score = 0
        for i, track in enumerate(dj_set[:-1]):
            next_track = dj_set[i + 1]
            key_bpm_score = (track.key_compatibility_score(next_track) + track.bpm_compatibility_score(next_track)) / 2
            rating_score = track.rating if track.rating >= prioritized_rating else 0
            total_score += key_bpm_score + rating_score
        return total_score

    def generate_neighbor(dj_set):
        neighbor = dj_set[:]
        i, j = random.sample(range(set_length), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    current_set = random.sample(tracks, set_length)
    current_score = score(current_set)
    best_set = current_set[:]
    best_score = current_score

    temperature = initial_temperature
    while temperature > final_temperature:
        for _ in range(iterations):
            neighbor = generate_neighbor(current_set)
            neighbor_score = score(neighbor)

            if neighbor_score > current_score or math.exp((neighbor_score - current_score) / temperature) > random.random():
                current_set = neighbor
                current_score = neighbor_score

                if current_score > best_score:
                    best_set = current_set[:]
                    best_score = current_score

        temperature *= cooling_rate
        print(temperature)

    return best_set