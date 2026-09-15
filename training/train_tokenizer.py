from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import json
import os

def load_data(file_path):
    texts = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            # Add BOS and EOS tokens to each sequence logically for training
            texts.append(data["instruction"])
            texts.append(data["output"])
    return texts

def main():
    print("Step 1: Loading JARVIS dataset...")
    # Use absolute paths if possible, but assuming this script runs from the project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "jarvis_dataset.jsonl")
    
    texts = load_data(dataset_path)
    
    # Initialize a BPE (Byte Pair Encoding) Tokenizer
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    
    # Simple whitespace splitting before applying BPE
    tokenizer.pre_tokenizer = Whitespace()
    
    # Setup our trainer with special tags
    trainer = BpeTrainer(
        vocab_size=5000, # A small vocabulary for a small custom project
        special_tokens=["[UNK]", "[PAD]", "[BOS]", "[EOS]", "[ACTION]"]
    )
    
    print("Step 2: Training BPE Tokenizer from scratch...")
    tokenizer.train_from_iterator(texts, trainer=trainer)
    
    # Save the custom tokenizer config file
    save_path = os.path.join(base_dir, "jarvis_tokenizer.json")
    tokenizer.save(save_path)
    print(f"✅ Tokenizer successfully trained & saved to: {save_path}")
    
    # Run a quick demonstration showing how the AI now reads words as numbers
    sample_text = "Jarvis open youtube"
    encoded = tokenizer.encode(sample_text)
    print(f"\n--- 🧠 AI Brain Demonstration ---")
    print(f"Human English: '{sample_text}'")
    print(f"Machine Numbers (IDs): {encoded.ids}")
    print(f"Machine Output (Tokens): {encoded.tokens}")
    print("--------------------------------")

if __name__ == "__main__":
    main()
