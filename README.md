⸻

🧠 Multi-Agent Claim Verification

This project implements a factual claim verification system using a single-agent and a multi-agent debate framework with LLaMA 3 8B Instruct. Given a claim and a list of retrieved evidences, the system determines whether the claim is TRUE, HALF-TRUE, or FALSE.

⸻

📁 Project Structure

llama_debate_verification/
├── main.py                      # Entry point: supports single or multi-agent mode
├── agents/
│   ├── single_agent.py          # One-shot verification agent
│   └── multi_agents.py          # Three-round debate agents: Pro, Con, Judge
├── prompts/
│   └── templates.py             # Prompt templates for each agent and round
├── model/
│   └── loader.py                # Loads LLaMA 3 model and tokenizer from local path
├── data/
│   └── example.json             # Input data (claim + evidence)


⸻

🔧 Requirements

pip install torch transformers accelerate sentencepiece

Make sure your environment has sufficient GPU memory (e.g., 1x H100) and the LLaMA 3 8B Instruct model is downloaded to a local folder (e.g., ./llama3-8b-instruct).

⸻

🚀 Running the System

✅ Single Agent Mode (one-step factual check)

python main.py --mode single

The model receives the claim and evidence, and outputs a [VERDICT]: TRUE / FALSE / HALF-TRUE with reasoning.

🤼 Multi-Agent Debate Mode (3 rounds + judge)

python main.py --mode multi

Three rounds of debate are run:
	•	Opening: Pro and Con present initial arguments
	•	Rebuttal: Each side refutes the other
	•	Closing: Each side summarizes its stance
	•	Judge: Evaluates the full exchange and returns a final decision

⸻

📌 Example Output (Multi-Agent)

--- Pro Agent Opening ---
The claim is true because...

--- Con Agent Rebuttal ---
The claim ignores important context...

=== Final Judge Verdict ===
[VERDICT]: HALF-TRUE  
[REASON]: While the claim highlights a debated topic, the evidence indicates...


⸻

📂 LLaMA Model Setup

Ensure you have downloaded the LLaMA 3 8B Instruct model from HuggingFace:

huggingface-cli login
huggingface-cli download meta-llama/Meta-Llama-3-8B-Instruct \
    --local-dir ./llama3-8b-instruct \
    --local-dir-use-symlinks False

In model/loader.py, make sure model_path = "./llama3-8b-instruct"

⸻

🧩 TODO / Extensions
	•	Support multi-turn debate (more than 3 rounds)
	•	Confidence scoring or verdict justification grading
	•	Batch evaluation from dataset (.jsonl)
	•	GUI or visualization of debate flow

⸻

Let me know if you’d like this in Chinese or want to include example data or results in the README!