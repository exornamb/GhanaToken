"""
src/train_ghanatok.py
Trains small, Ghanaian-language-specific tokenizers (Byte-level BPE and SentencePiece Unigram)
on combined Twi and Ewe training data, testing whether custom vocabularies and pre-tokenization
reduce fragmentation compared with general multilingual tokenizers.
"""
from pathlib import Path
import sentencepiece as spm
from tokenizers import Regex, Tokenizer, decoders
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Split, ByteLevel, Sequence
from tokenizers.trainers import BpeTrainer

# Known Twi and Ewe morphemes and common words, injected so they are
# guaranteed a slot in GhanaTok's vocabulary rather than left to chance
# frequency counts. Prefixes/suffixes are written with a hyphen to show
# where they attach, matching normal Ghanaian-language teaching materials.
SEED_MORPHEMES = [
    # Twi prefixes and suffixes
    "mbe-", "n-", "bɛ-", "-foɔ", "-nom", "-yeɛ",
    # Ewe affixes and particles
    "-wo", "-m", "mega-", "ɖe-",
    # Common greetings and high-frequency roots, both languages (including capitalized sentence-initial forms)
    "Akwaaba", "akwaaba", "Medaase", "medaase", "Woezɔ", "woezɔ", "Aleke", "aleke", "Akpe", "akpe",
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
VOCAB_SIZE = 8000
MODEL_DIR = PROJECT_ROOT / "models" / "ghanatok"
UNIGRAM_MODEL_DIR = PROJECT_ROOT / "models" / "ghanatok_unigram"


def get_model_dir(vocab_size: int, algorithm: str) -> Path:
    """Returns a vocab-size-specific model directory, e.g. models/ghanatok_bpe_16000."""
    folder_name = f"ghanatok_{algorithm}_{vocab_size}"
    return PROJECT_ROOT / "models" / folder_name


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


def train_ghanatok(
    corpus_path: Path = CORPUS_PATH,
    vocab_size: int = VOCAB_SIZE,
    model_dir: Path = None,
) -> Path:
    """
    Trains a byte-level BPE tokenizer on the Twi and Ewe training corpus,
    using a dialect-aware pre-tokenizer (so ɛ, ɔ, ɖ, ŋ, ʋ, ƒ stay attached
    to their words) and a seed vocabulary of known Twi and Ewe morphemes
    (so they are guaranteed a slot, not left purely to frequency counts).
    """
    if model_dir is None:
        model_dir = get_model_dir(vocab_size, "bpe")
    tokenizer = Tokenizer(BPE(unk_token="<unk>"))
    tokenizer.pre_tokenizer = Sequence([
        Split(pattern=GHANA_PRETOKENIZER_PATTERN, behavior="isolated"),
        # use_regex=False stops ByteLevel from running its own default GPT-2
        # regex on top of ours; it just byte-encodes the pieces we already split.
        ByteLevel(add_prefix_space=False, use_regex=False),
    ])
    tokenizer.decoder = decoders.ByteLevel()

    trainer = BpeTrainer(
        vocab_size=vocab_size,
        min_frequency=2,
        # Special tokens are always kept whole and never split, so listing
        # the seed morphemes here guarantees each one gets its own slot.
        special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"] + SEED_MORPHEMES,
    )

    tokenizer.train([str(corpus_path)], trainer)
    model_dir.mkdir(parents=True, exist_ok=True)
    save_path = model_dir / "ghanatok_tokenizer.json"
    tokenizer.save(str(save_path))
    print(f"GhanaTok (BPE) trained and saved to {save_path}")
    return save_path


def train_ghanatok_unigram(
    corpus_path: Path = CORPUS_PATH,
    vocab_size: int = VOCAB_SIZE,
    model_dir: Path = None,
) -> Path:
    """
    Trains a SentencePiece Unigram tokenizer on the same Twi/Ewe corpus,
    as a second, optional GhanaTok variant to compare against the BPE
    version above. Unigram starts from a large candidate vocabulary and
    prunes probabilistically, which can segment agglutinative prefixes
    and suffixes differently, sometimes better, than greedy BPE merges.
    """
    if model_dir is None:
        model_dir = get_model_dir(vocab_size, "unigram")
    model_dir.mkdir(parents=True, exist_ok=True)
    model_prefix = str(model_dir / "ghanatok_unigram")

    spm.SentencePieceTrainer.train(
        input=str(corpus_path),
        model_prefix=model_prefix,
        vocab_size=vocab_size,
        model_type="unigram",
        character_coverage=1.0,  # keep every character, including ɛɔɖŋʋƒ
        user_defined_symbols=SEED_MORPHEMES,  # same seed list as GhanaTok-BPE
        hard_vocab_limit=False,  # allows corpus saturation without hard failure at large target sizes
        unk_id=0,
        pad_id=1,
        bos_id=2,
        eos_id=3,
    )
    model_path = Path(f"{model_prefix}.model")
    print(f"GhanaTok-Unigram trained and saved to {model_path}")
    return model_path


class SentencePieceWrapper:
    """
    A thin wrapper so a raw SentencePiece model exposes the same
    .encode() and .tokenize() methods that mBERT, XLM-R, AfroXLMR, ABENA,
    and GhanaTok-BPE all already use. This means analyze_sentence() and
    run_benchmark() from Day 4 and Day 5 work on GhanaTok-Unigram with
    no changes needed.
    """
    def __init__(self, model_path: str):
        self.sp = spm.SentencePieceProcessor(model_file=model_path)

    def encode(self, text: str, add_special_tokens: bool = False):
        return self.sp.encode(text, out_type=int)

    def tokenize(self, text: str):
        return self.sp.encode(text, out_type=str)
