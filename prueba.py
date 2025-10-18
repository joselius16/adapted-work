from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl
from sklearn.metrics import jaccard_score


def clean_labels(label_string):
    return set(l.strip().lower() for l in label_string.replace('\n', '').replace(' del habla','del habla').split(',') if l.strip())

# Asumiendo que real_set y pred_set son listas de sets del mismo tamaño
def calculate_set_metrics(real_sets, pred_sets):
    metrics = {
        'jaccard_scores': [],
        'precision_scores': [],
        'recall_scores': [],
        'f1_scores': []
    }

    for real, pred in zip(real_sets, pred_sets):
        # Jaccard Index
        intersection = len(real & pred)
        union = len(real | pred)
        jaccard = intersection / union if union > 0 else 0

        # Precision
        precision = intersection / len(pred) if len(pred) > 0 else 0

        # Recall
        recall = intersection / len(real) if len(real) > 0 else 0

        # F1 Score
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        metrics['jaccard_scores'].append(jaccard)
        metrics['precision_scores'].append(precision)
        metrics['recall_scores'].append(recall)
        metrics['f1_scores'].append(f1)

    return metrics

def analyze_label_distribution(real_sets, pred_sets):
    # Contar frecuencias
    real_counts = {}
    pred_counts = {}

    for s in real_sets:
        for label in s:
            real_counts[label] = real_counts.get(label, 0) + 1

    for s in pred_sets:
        for label in s:
            pred_counts[label] = pred_counts.get(label, 0) + 1

    # Crear DataFrame para comparación
    all_labels = set(real_counts.keys()) | set(pred_counts.keys())

    comparison_df = pd.DataFrame({
        'Real': [real_counts.get(label, 0) for label in all_labels],
        'Predicho': [pred_counts.get(label, 0) for label in all_labels]
    }, index=list(all_labels))

    return comparison_df

def exact_match_analysis(real_sets, pred_sets):
    exact_matches = sum(1 for r, p in zip(real_sets, pred_sets) if r == p)
    total = len(real_sets)

    print(f"Coincidencias exactas: {exact_matches}/{total} ({exact_matches/total*100:.2f}%)")

    # Análisis de casos comunes
    from collections import Counter

    real_combinations = Counter([frozenset(s) for s in real_sets])
    pred_combinations = Counter([frozenset(s) for s in pred_sets])

    print("\nCombinaciones más comunes (Real):")
    for combo, count in real_combinations.most_common(5):
        print(f"  {set(combo)}: {count}")

    print("\nCombinaciones más comunes (Predicho):")
    for combo, count in pred_combinations.most_common(5):
        print(f"  {set(combo)}: {count}")


if __name__=="__main__":
    data_real = pl.read_csv('/home/joselu/tfm/adapted-work/data/validated_data.csv')

    # Prompt 1
    p1_gemma = pl.read_json('/home/joselu/tfm/adapted-work/data/prompt_1/gemma.json')




    real_set = []

    for dat in data_real["pred_disability"]:
        real_set.append(clean_labels(dat))



    p1_gemma_set = []

    for dat in p1_gemma["pred_disability"]:
        p1_gemma_set.append(clean_labels(dat))



    metrics = calculate_set_metrics(real_set, p1_gemma_set)

    # Estadísticas resumen
    print("Métricas promedio:")
    print(f"Jaccard Index: {np.mean(metrics['jaccard_scores']):.3f} ± {np.std(metrics['jaccard_scores']):.3f}")
    print(f"Precision: {np.mean(metrics['precision_scores']):.3f} ± {np.std(metrics['precision_scores']):.3f}")
    print(f"Recall: {np.mean(metrics['recall_scores']):.3f} ± {np.std(metrics['recall_scores']):.3f}")
    print(f"F1 Score: {np.mean(metrics['f1_scores']):.3f} ± {np.std(metrics['f1_scores']):.3f}")
