import numpy as np
from hmmlearn.hmm import CategoricalHMM


# Gozlem sembolleri:
# 0 -> High
# 1 -> Low
OBSERVATION_LABELS = {0: "High", 1: "Low"}


# Temsili kucuk egitim dizileri
TRAINING_SEQUENCES = {
    "EV": [
        [0, 1],
        [0, 1, 1],
        [0, 0, 1],
    ],
    "OKUL": [
        [1, 0, 1, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
    ],
}


# Siniflandirilacak bilinmeyen test dizisi
TEST_SEQUENCE = [0, 1, 1]


def to_hmm_input(sequence):
    """hmmlearn icin diziyi (n_samples, 1) seklinde hazirlar."""
    return np.array(sequence, dtype=int).reshape(-1, 1)


def format_sequence(sequence):
    """Sayisal gozlemleri okunabilir etiketlere cevirir."""
    return [OBSERVATION_LABELS[value] for value in sequence]


def create_state_sequence(sequence_length, n_states):
    """
    Gozlem konumlarini soldan saga durumlara paylastirir.
    Ornek: 3 gozlem, 2 durum -> [0, 0, 1]
    """
    state_ids = np.floor(np.arange(sequence_length) * n_states / sequence_length).astype(int)
    return np.clip(state_ids, 0, n_states - 1)


def estimate_hmm_parameters(sequences, n_states, n_observations=2, smoothing=1.0):
    """
    Temsili egitim dizilerinden basit bir soldan saga HMM parametresi uretir.
    Burada amac, odevi sade tutarken egitim verilerini gercekten modele dahil etmektir.
    """
    emission_counts = np.full((n_states, n_observations), smoothing, dtype=float)
    transition_counts = np.zeros((n_states, n_states), dtype=float)

    # Her durumda kendinde kalma ve bir sonraki duruma gecme olasiligi olsun.
    for state in range(n_states):
        transition_counts[state, state] += smoothing
        if state < n_states - 1:
            transition_counts[state, state + 1] += smoothing

    for sequence in sequences:
        state_sequence = create_state_sequence(len(sequence), n_states)

        for observation, state in zip(sequence, state_sequence):
            emission_counts[state, observation] += 1

        for current_state, next_state in zip(state_sequence[:-1], state_sequence[1:]):
            transition_counts[current_state, next_state] += 1

    startprob = np.zeros(n_states)
    startprob[0] = 1.0
    transmat = transition_counts / transition_counts.sum(axis=1, keepdims=True)
    emissionprob = emission_counts / emission_counts.sum(axis=1, keepdims=True)
    return startprob, transmat, emissionprob


def build_word_model(sequences, n_states):
    """Temsili egitim dizilerinden bir CategoricalHMM modeli kurar."""
    startprob, transmat, emissionprob = estimate_hmm_parameters(sequences, n_states)

    model = CategoricalHMM(n_components=n_states, init_params="", params="")
    model.n_features = 2
    model.startprob_ = startprob
    model.transmat_ = transmat
    model.emissionprob_ = emissionprob
    return model


def create_ev_model():
    """EV kelimesi icin 2 durumlu basit HMM modeli."""
    return build_word_model(TRAINING_SEQUENCES["EV"], n_states=2)


def create_okul_model():
    """OKUL kelimesi icin 4 durumlu soldan saga basit HMM modeli."""
    return build_word_model(TRAINING_SEQUENCES["OKUL"], n_states=4)


def score_models(sequence, models):
    """Verilen test dizisini butun modellere skorlatir."""
    observation = to_hmm_input(sequence)
    scores = {}

    for word, model in models.items():
        scores[word] = model.score(observation)

    return scores


def predict_word(sequence, models):
    """En yuksek log-likelihood degerine sahip modeli secer."""
    scores = score_models(sequence, models)
    best_word = max(scores, key=scores.get)
    return best_word, scores


def main():
    models = {
        "EV": create_ev_model(),
        "OKUL": create_okul_model(),
    }

    print("Temsili egitim dizileri")
    for word, sequences in TRAINING_SEQUENCES.items():
        readable_sequences = [format_sequence(seq) for seq in sequences]
        print(f"{word}: {readable_sequences}")

    print("\nTest dizisi:")
    print(format_sequence(TEST_SEQUENCE))

    predicted_word, scores = predict_word(TEST_SEQUENCE, models)

    print("\nModel skorları (log-likelihood):")
    for word, score in scores.items():
        print(f"{word}: {score:.4f}")

    print(f"\nTahmin edilen kelime: {predicted_word}")


if __name__ == "__main__":
    main()
