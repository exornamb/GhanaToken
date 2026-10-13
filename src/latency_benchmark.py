"""
src/latency_benchmark.py
Measures tokenization speed (encode latency) for each tokenizer on a
fixed set of sentences, used to quantify the runtime cost of high
fertility tokenizers on Twi and Ewe text.
"""

from typing import Dict, List, Any
import time
import numpy as np
import pandas as pd


def benchmark_latency(
    tokenizers: Dict[str, Any],
    sentences: List[str],
    language: str,
    n_repeats: int = 5,
    warmup: int = 1,
) -> pd.DataFrame:
    """
    Times how long each tokenizer takes to encode the full sentence list,
    repeated n_repeats times to get a stable estimate. The first `warmup`
    runs are discarded to eliminate lazy initialization noise.
    
    Total sentences and characters are used to compute throughput (sentences/sec and chars/sec).
    """
    rows = []
    total_chars = sum(len(s) for s in sentences)
    n_sentences = len(sentences)

    for name, tok in tokenizers.items():
        run_times = []
        for run in range(warmup + n_repeats):
            start = time.perf_counter()
            for sentence in sentences:
                tok.encode(sentence, add_special_tokens=False)
            elapsed = time.perf_counter() - start
            if run >= warmup:
                run_times.append(elapsed)

        run_times_arr = np.array(run_times)
        mean_sec = float(run_times_arr.mean())
        std_sec = float(run_times_arr.std())

        rows.append({
            "tokenizer": name,
            "language": language,
            "n_sentences": n_sentences,
            "total_chars": total_chars,
            "mean_seconds_per_run": round(mean_sec, 4),
            "std_seconds_per_run": round(std_sec, 4),
            "sentences_per_second": round(n_sentences / mean_sec, 2),
            "chars_per_second": round(total_chars / mean_sec, 2),
        })

    return pd.DataFrame(rows)
