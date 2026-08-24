"""
src/train_ghanatok.py
Trains a small byte-level BPE tokenizer on the combined Twi and Ewe
training data, to test whether a Ghanaian-language-specific vocabulary
reduces fragmentation compared with the general multilingual tokenizers.
"""
from pathlib import Path
from tokenizers import Regex

# Known Twi and Ewe morphemes and common words, injected so they are
# guaranteed a slot in GhanaTok's vocabulary rather than left to chance
# frequency counts. Prefixes/suffixes are written with a hyphen to show
# where they attach, matching normal Ghanaian-language teaching materials.
SEED_MORPHEMES = [
    # Twi prefixes and suffixes
    "mbe-", "n-", "bɛ-", "-foɔ", "-nom", "-yeɛ",
    # Ewe affixes and particles
    "-wo", "-m", "mega-", "ɖe-",
    # Common greetings and high-frequency roots, both languages
    "akwaaba", "medaase", "woezɔ", "aleke", "akpe",
]

# Keeps extended Latin letters used in Twi and Ewe (ɛɔɖŋʋƒ and their
# capitals) attached to their word, and keeps apostrophes and punctuation
# as separate tokens, instead of letting them fuse unpredictably. The
# optional leading \s? on the word branch follows the same convention
# GPT-2 style tokenizers use, so a space stays glued to the word after it
# rather than becoming its own stray token once byte-level encoding runs.
GHANA_PRETOKENIZER_PATTERN = Regex(
    r"'s|'[tmdllve]|\s?[\p{L}\p{M}ɛɔɖŋʋƒƐƆƉŊƲƑ]+|[^\s\p{L}\p{M}]+"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = PROJECT_ROOT / "data" / "processed" / "ghanatok_train_corpus.txt"


def build_training_corpus(
    output_path: Path = CORPUS_PATH,
    data_dir: Path = PROJECT_ROOT / "data" / "processed",
) -> Path:
    """Combines Twi and Ewe training sentences into one file for training."""
    lines = []
    for language in ["twi", "ewe"]:
        train_file = data_dir / language / "train.txt"
        with open(train_file, encoding="utf-8") as f:
            lines.extend(line.strip() for line in f if line.strip())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Combined training corpus: {len(lines)} sentences saved to {output_path}")
    return output_path
