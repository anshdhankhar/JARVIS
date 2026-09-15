import torch
import json
import os
from tokenizers import Tokenizer
from models.transformer import JarvisGPT

# --- Hyperparameters ---
batch_size = 16 
block_size = 32 # Maximum context length
max_iters = 1000
eval_interval = 100
learning_rate = 1e-3
eval_iters = 20
device = 'mps' if torch.backends.mps.is_available() else 'cpu'

print(f"🚀 Using Device: {device}")

# --- 1. Load Tokenizer & Data ---
tokenizer = Tokenizer.from_file("training/jarvis_tokenizer.json")
vocab_size = tokenizer.get_vocab_size()

with open("training/jarvis_dataset.jsonl", "r") as f:
    text_data = [json.loads(line) for line in f]

# We format dataset inputs: Instruction -> Output format
# E.g., "Jarvis open youtube [ACTION:OPEN_YOUTUBE]"
encoded_data = []
for item in text_data:
    sequence = f"{item['instruction']} {item['output']} [EOS]"
    ids = tokenizer.encode(sequence).ids
    encoded_data.extend(ids)

# Convert all text into a massive PyTorch Tensor
data = torch.tensor(encoded_data, dtype=torch.long)

# Train/Test Split
n = int(0.9 * len(data)) 
train_data = data[:n]
val_data = data[n:]

# --- 2. Data Loading Function ---
def get_batch(split):
    # Generate a small batch of data of inputs x and targets y
    data_source = train_data if split == 'train' else val_data
    ix = torch.randint(len(data_source) - block_size, (batch_size,))
    x = torch.stack([data_source[i:i+block_size] for i in ix])
    y = torch.stack([data_source[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y

@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

# --- 3. Initialize Model ---
# We config the model to be extremely small so it can run securely and locally on the Mac
model = JarvisGPT(
    vocab_size=vocab_size,
    n_embd=64,
    n_head=4,
    n_layer=4,
    block_size=block_size,
    dropout=0.1
)
model.to(device)

print(f"Total Parameters: {sum(p.numel() for p in model.parameters())/1e6:.2f} M")

# --- 4. Training Loop ---
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

print("⚡️ Starting Model Training...")

for iter in range(max_iters):

    # Every once in a while evaluate the loss on train and val sets
    if iter % eval_interval == 0 or iter == max_iters - 1:
        losses = estimate_loss()
        print(f"Step {iter}: Train Loss {losses['train']:.4f}, Val Loss {losses['val']:.4f}")

    # Sample a batch of data
    xb, yb = get_batch('train')

    # Evaluate the loss
    logits, loss = model(xb, yb)
    
    # Backpropagation
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# Save final checkpoint
os.makedirs("checkpoints", exist_ok=True)
torch.save(model.state_dict(), "checkpoints/jarvis_gpt_v1.pth")
print(f"✅ Training Complete! Model saved to checkpoints/jarvis_gpt_v1.pth")

# --- 5. Quick Inference Test ---
print("\n--- 🧠 JARVIS Intelligence Test ---")
test_prompt = "Jarvis open google"
test_encoded = tokenizer.encode(test_prompt).ids
context = torch.tensor(test_encoded, dtype=torch.long, device=device).unsqueeze(0)

print(f"Prompt: {test_prompt}")
generated_ids = model.generate(context, max_new_tokens=10)[0].tolist()
response = tokenizer.decode(generated_ids)
print(f"Model Gen: {response}")
