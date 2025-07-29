# === System Prompt ===
def get_system_prompt(role: str = "fact_checker") -> str:
    if role == "fact_checker":
        return "You are a precise and critical fact checker."
    elif role == "debater":
        return "You are a critical thinker participating in a factual debate."
    elif role == "judge":
        return "You are a neutral judge who evaluates factual debates."
    else:
        return "You are a helpful assistant."

def system_prompt_fact_checker():
    return get_system_prompt("fact_checker")

# # === Single-Agent Fact-Checking ===
# def user_prompt_single_agent(claim: str, evidence: str) -> str:
#     """
#     User prompt template for single-agent fact verification.
#     Fills in the claim and retrieved evidence.
#     """
#     return f"""
# Given a claim and some retrieved evidence, determine whether the claim is TRUE, FALSE, or HALF-TRUE.

# Claim: {claim}

# Retrieved Evidence:
# {evidence}

# Answer format:
# [VERDICT]: TRUE / FALSE / HALF-TRUE  
# [REASON]: <your explanation>
# """
# === Single-Agent Fact-Checking ===
def user_prompt_single_agent(claim: str, evidence: str) -> str:
    """
    Single-agent fact verification prompt: reason first (step-by-step with evidence reference), then verdict.
    """
    return f"""
You are given a factual claim and a list of retrieved evidence, each labeled with a number [1] to [20].

Your task is to evaluate whether the claim is TRUE, FALSE, or HALF-TRUE based solely on the provided evidence.

First, write a clear, step-by-step reasoning process. For **each step**, explicitly reference the relevant evidence by number (e.g., "[3]", "[8]") to justify your thinking.

Then, based on your reasoning, provide a final verdict.

---

Claim:
{claim}

Retrieved Evidence:
{evidence}

---

Answer format:
[REASON]:
- Step 1: ... (reference [x], [y])
- Step 2: ... (reference [z])
- ...
[VERDICT]: TRUE / FALSE / HALF-TRUE
"""
def user_prompt_single_agent_intent(claim: str, evidence: str, intent: str) -> str:
    """
    Single-agent fact verification prompt: reason first (step-by-step with evidence reference), then verdict.
    Includes claim intent to guide deeper reasoning.
    """
    return f"""
You are given:
- A factual claim
- A corresponding inferred **intent**, representing what the speaker is ultimately trying to assert
- A list of 20 retrieved evidence snippets, each labeled with a number [1] to [20].

Your task is to determine whether the claim is TRUE, FALSE, or HALF-TRUE based solely on the provided evidence and in light of the **intent behind the claim**.

First, write a clear, step-by-step reasoning process. For **each step**, explicitly reference the relevant evidence by number (e.g., "[3]", "[8]") to justify your thinking.  
In your reasoning, consider not just the literal truth of the claim, but also whether the speaker's intended implication is supported or contradicted by the evidence.

Then, based on your reasoning, provide a final verdict.

---

Claim:
{claim}

Inferred Intent:
"{intent}"

Retrieved Evidence:
{evidence}

---

Answer format:
[REASON]:
- Step 1: ...
- Step 2: ...
- (Include references like [2], [5] in each step)
[VERDICT]: TRUE / FALSE / HALF-TRUE
"""
# # === Multi-Agent Fact-Checking ===
# # === Opening Round ===
# # def user_prompt_opening_pro(claim, evidence):
# #     return f"""You are the supporting agent in a factual debate. Your task is to present a strong opening argument **supporting** the claim, using the provided evidence.

# # Claim:
# # {claim}

# # Evidence:
# # {evidence}

# # Instructions:
# # - Begin with a clear statement of support.
# # - Highlight specific facts or evidence that support the claim.
# # - You **must cite** relevant evidence by quoting or referencing its number (e.g., [3], [7]).
# # - Avoid generalities — ground your argument in the evidence.

# # Your Opening Statement:"""

# # def user_prompt_opening_con(claim, evidence):
# #     return f"""You are the opposing agent in a factual debate. Your task is to present a strong opening argument **challenging** the claim, using the provided evidence.

# # Claim:
# # {claim}

# # Evidence:
# # {evidence}

# # Instructions:
# # - Begin with a clear position that the claim is FALSE or HALF-TRUE.
# # - Support your case with specific evidence that contradicts, weakens, or adds necessary nuance to the claim.
# # - You **must cite** relevant evidence by quoting or referencing its number (e.g., [5], [10]).
# # - Focus on factual contradictions, missing context, or misleading aspects.

# # Your Opening Statement:"""
# def user_prompt_opening_pro(claim, evidence):
#     return f"""You support the following claim. Present your opening argument using the evidence.

# Claim: {claim}

# Evidence:
# {evidence}

# Begin your argument with your position. Highlight facts that support the claim as TRUE."""

# def user_prompt_opening_con(claim, evidence):
#     return f"""You oppose the following claim. Present your opening argument using the evidence.

# Claim: {claim}

# Evidence:
# {evidence}

# Begin your argument by explaining why the claim is FALSE or misleading, referencing specific points in the evidence."""


# # === Rebuttal Round ===
# # def user_prompt_rebuttal_pro(claim, evidence, con_argument):
# #     return f"""You are the supporting agent in a factual debate. The opposing agent has made the following counterargument:

# # Opponent's Argument:
# # {con_argument}

# # Claim:
# # {claim}

# # Evidence:
# # {evidence}

# # Instructions:
# # - Rebut the opponent's claims with evidence and reasoning.
# # - Show why the opponent's interpretation is flawed or incomplete.
# # - You **must cite** specific evidence (e.g., [2], [6]) to support your rebuttal.
# # - Ensure your response is fact-based and logically structured.

# # Your Rebuttal:"""

# # def user_prompt_rebuttal_con(claim, evidence, pro_argument):
# #     return f"""You are the opposing agent in a factual debate. The supporting agent has made the following argument:

# # Opponent's Argument:
# # {pro_argument}

# # Claim:
# # {claim}

# # Evidence:
# # {evidence}

# # Instructions:
# # - Rebut the opponent's argument using facts and logic.
# # - Point out errors, omissions, or contradictions in their reasoning.
# # - You **must cite** specific evidence (e.g., [1], [9]) to support your rebuttal.
# # - Avoid repetition; focus on weaknesses in the opposing case.

# # Your Rebuttal:"""
# def user_prompt_rebuttal_pro(claim, evidence, con_argument):
#     return f"""You are the supporting agent in a debate about the claim below. Your opponent has made an argument against the claim.

# Claim: {claim}

# Evidence:
# {evidence}

# Opponent's argument:
# {con_argument}

# Write your rebuttal, explaining why the opponent is wrong and defending the claim."""

# def user_prompt_rebuttal_con(claim, evidence, pro_argument):
#     return f"""You are the opposing agent in a debate about the claim below. Your opponent has made an argument supporting the claim.

# Claim: {claim}

# Evidence:
# {evidence}

# Opponent's argument:
# {pro_argument}

# Write your rebuttal, explaining why the opponent is incorrect and the claim is still FALSE or HALF-TRUE."""


# # === Closing Round ===
# # def user_prompt_closing_pro(claim, evidence):
# #     return f"""You are the supporting agent in a factual debate. Write your closing statement.

# # Claim:
# # {claim}

# # Evidence:
# # {evidence}

# # Instructions:
# # - Summarize why the claim is TRUE, using the most compelling evidence and arguments presented.
# # - You **must cite** specific evidence (e.g., [4], [8]) and briefly reference strong points made in the debate.
# # - Keep it concise and persuasive.

# # Your Closing Statement:"""

# # def user_prompt_closing_con(claim, evidence):
# #     return f"""You are the opposing agent in a factual debate. Write your closing statement.

# # Claim:
# # {claim}

# # Evidence:
# # {evidence}

# # Instructions:
# # - Summarize why the claim is FALSE or HALF-TRUE.
# # - Cite key pieces of evidence and major points raised in the debate.
# # - You **must reference** specific evidence (e.g., [6], [11]) and rebut significant arguments made by the opposing agent.

# # Your Closing Statement:"""
# def user_prompt_closing_pro(claim, evidence):
#     return f"""You are the supporting agent in a debate. Summarize your final position.

# Claim: {claim}

# Evidence:
# {evidence}

# Provide a closing statement reinforcing why the claim is TRUE."""

# def user_prompt_closing_con(claim, evidence):
#     return f"""You are the opposing agent in a debate. Summarize your final position.

# Claim: {claim}

# Evidence:
# {evidence}

# Provide a closing statement reinforcing why the claim is FALSE or HALF-TRUE."""


# # # === Judge Prompt ===
# # # def user_prompt_judge_full(claim, evidence, pro_open, con_open, pro_rebut, con_rebut, pro_close, con_close):
# # #     return f"""You are a neutral judge tasked with evaluating a factual debate.

# # # Claim:
# # # {claim}

# # # Evidence:
# # # {evidence}

# # # --- Opening Statements ---
# # # Pro Agent:
# # # {pro_open}

# # # Con Agent:
# # # {con_open}

# # # --- Rebuttals ---
# # # Pro Agent:
# # # {pro_rebut}

# # # Con Agent:
# # # {con_rebut}

# # # --- Closing Statements ---
# # # Pro Agent:
# # # {pro_close}

# # # Con Agent:
# # # {con_close}

# # # Instructions:
# # # 1. Carefully consider the arguments made by both agents.
# # # 2. Identify which agent made stronger use of the **evidence** (referencing specific numbers like [3], [10]).
# # # 3. Examine whether either side misunderstood or ignored critical facts.
# # # 4. Your reasoning must include references to both:
# # #    - The **evidence** (e.g., "[5] contradicts the claim")
# # #    - The **agents’ arguments** (e.g., "Pro agent incorrectly claims in their rebuttal that...")

# # # Then provide your judgment using the format below.

# # # Answer format:
# # # [REASON]:
# # # <Your structured reasoning and justification. Use evidence references and quote both sides if needed.>

# # # [VERDICT]: TRUE / FALSE / HALF-TRUE
# # # """
# def user_prompt_judge_full(claim, evidence, pro_open, con_open, pro_rebut, con_rebut, pro_close, con_close):
#     return f"""You are a neutral judge evaluating a factual debate.

# Claim: {claim}

# Evidence:
# {evidence}

# --- Opening Statements ---
# Pro Agent:
# {pro_open}

# Con Agent:
# {con_open}

# --- Rebuttals ---
# Pro Agent:
# {pro_rebut}

# Con Agent:
# {con_rebut}

# --- Closing Statements ---
# Pro Agent:
# {pro_close}

# Con Agent:
# {con_close}

# Based on the arguments and evidence, decide whether the claim is TRUE, FALSE, or HALF-TRUE.

# Answer format:  
# [REASON]: <your justification>
# [VERDICT]: TRUE / FALSE / HALF-TRUE
# """

def user_prompt_intent_inference(claim):
    return f"""A claim may be literally accurate but still misleading due to the message it implies.

Your task is to infer the intended message or implied conclusion of the following claim.

Claim: "{claim}"

What is the intended conclusion of this claim?

Respond with one clear and concise sentence."""

def user_prompt_reformulate_pro(claim, intent):
    return f"""You support the following claim and aim to reinforce its implied message.

Claim: "{claim}"

Inferred Intent: "{intent}"

Your task is to reformulate the claim in a way that makes the implied conclusion more explicit and persuasive.

Only output the reformulated claim directly, without any introductory phrases or explanations.

Reformulated (Pro) Claim:"""

def user_prompt_reformulate_con(claim, intent):
    return f"""You oppose the following claim and aim to highlight any issues with its implied message.

Claim: "{claim}"

Inferred Intent: "{intent}"

Your task is to reformulate the claim in a way that emphasizes its potential problems, uncertainties, or misleading assumptions.

Only output the reformulated claim directly, without any introductory phrases or explanations.

Reformulated (Con) Claim:"""

# def user_prompt_reformulate_pro(claim, intent):
#     return f"""You support the following claim and want to restate it in a way that clearly reflects your agreement with its message.

# Claim: "{claim}"

# Inferred Intent: "{intent}"

# Your task is to rephrase the claim using a positive, supporting tone that affirms the claim’s main idea.

# Only output the reformulated claim directly, without extra explanations.

# Reformulated (Pro) Claim:"""

# def user_prompt_reformulate_con(claim, intent):
#     return f"""You oppose the following claim and want to restate it in a way that clearly reflects your disagreement with its message.

# Claim: "{claim}"

# Inferred Intent: "{intent}"

# Your task is to rephrase the claim using a critical, opposing tone that challenges or rejects its main idea.

# Only output the reformulated claim directly, without extra explanations.

# Reformulated (Con) Claim:"""

def user_prompt_extract_terms(claim):
    return f"""Extract the key specific terms from the following claim. 
These terms should include:

- Numbers and statistics (e.g., "4 in every 5", "75%")
- Named entities such as people, organizations, or places (e.g., "CDC", "Pfizer", "Biden")
- Events or variants (e.g., "Omicron variant", "school shooting")
- Emotionally charged or significant phrases (e.g., "worst ever", "white privilege")

Claim: "{claim}"

Return only the result as a valid Python list of strings.
Do not include any explanatory text, headers, or descriptions.

Example output:
["term1", "term2", "term3"]
"""
def user_prompt_reformulate_pro_with_keywords(claim, intent, keywords):
    return f"""You support the following claim and want to restate it in a way that clearly reflects your agreement with its message.

Claim: "{claim}"

Inferred Intent: "{intent}"

Important Terms to Include: {keywords}

Your task is to rephrase the claim using a positive, supporting tone that affirms the claim’s main idea.
Incorporate as many of the important terms as naturally as possible.

Output only the reformulated claim directly.
Do not include any extra explanation, formatting, or labels.
"""
def user_prompt_reformulate_con_with_keywords(claim, intent, keywords):
    return f"""You oppose the following claim and want to restate it in a way that clearly reflects your disagreement with its message.

Claim: "{claim}"

Inferred Intent: "{intent}"

Important Terms to Include: {keywords}

Your task is to rephrase the claim using a critical, opposing tone that challenges or rejects its main idea.
Incorporate as many of the important terms as naturally as possible.

Output only the reformulated claim directly.
Do not include any extra explanation, formatting, or labels.
"""
def user_prompt_generate_pro_queries(claim, intent, specific_terms):
    return f"""You are an assistant analyzing the following claim.

Claim: "{claim}"

Inferred Intent: "{intent}"

Important Terms: {specific_terms}

Your task is to extract a list of **concise and independent fact-checkable Pro statements** that support the claim’s inferred intent.

Each statement should:
- Affirm or strengthen the intent.
- Be short, specific, and verifiable.
- Use the Important Terms when possible.
- Be suitable for retrieving supporting evidence from a search engine or knowledge base.

Respond in JSON format as follows:

{{
  "pro_statements": [
    "<statement 1>",
    "<statement 2>",
    ...
  ]
}}
"""
def user_prompt_generate_con_queries(claim, intent, specific_terms):
    return f"""You are an assistant analyzing the following claim.

Claim: "{claim}"

Inferred Intent: "{intent}"

Important Terms: {specific_terms}

Your task is to extract a list of **concise and independent fact-checkable Con statements** that challenge the claim’s inferred intent.

Each statement should:
- Refute, contextualize, or cast doubt on the intent.
- Be short, specific, and verifiable.
- Use the Important Terms when possible.
- Be suitable for retrieving opposing evidence from a search engine or knowledge base.

Respond in JSON format as follows:

{{
  "con_statements": [
    "<statement 1>",
    "<statement 2>",
    ...
  ]
}}
"""
# def user_prompt_opening_pro(claim, evidence):
#     return f"""You are the supporting agent in a factual debate.

# Claim:
# {claim}

# Evidence:
# {evidence}

# Your task:
# Present a high-quality opening argument in support of the claim.

# Instructions:
# - Start with a firm position affirming the claim.
# - Make at least 3 distinct, fact-based points in support.
# - For each point, **cite evidence by number in brackets (e.g., [2])** immediately after the sentence that uses it.
# - If any evidence is emotionally charged, vague, or non-factual, **acknowledge this and avoid relying on it as a factual basis**.
# - Be precise, confident, and structured. Use expert-level tone.

# Your Opening Statement:"""
# def user_prompt_opening_con(claim, evidence):
#     return f"""You are the opposing agent in a factual debate.

# Claim:
# {claim}

# Evidence:
# {evidence}

# Your task:
# Present a high-quality opening argument showing why the claim is FALSE or misleading.

# Instructions:
# - Begin by clearly stating your opposition to the claim.
# - Use at least 3 distinct points based on factual evidence that contradicts or undercuts the claim.
# - After each point, include the evidence number in brackets (e.g., [5]).
# - If any evidence is emotionally loaded, lacks facts, or is anecdotal, **point this out explicitly** and explain why it cannot support the claim.
# - Maintain a precise, fact-grounded tone.

# Your Opening Statement:"""
# def user_prompt_rebuttal_pro(claim, evidence, con_argument):
#     return f"""You are the supporting agent in a factual debate.

# Claim:
# {claim}

# Opponent’s Argument:
# {con_argument}

# Evidence:
# {evidence}

# Your task:
# Write a strong rebuttal defending the claim and challenging the opponent’s argument.

# Instructions:
# - Identify flaws, contradictions, or omissions in the opposing argument.
# - Support your counterpoints with specific evidence, citing by number in-line (e.g., [4]).
# - If the opponent relied on emotionally biased or weak evidence, call that out explicitly.
# - Stay focused on factual accuracy and logical reasoning.

# Your Rebuttal:"""
# def user_prompt_rebuttal_con(claim, evidence, pro_argument):
#     return f"""You are the opposing agent in a factual debate.

# Claim:
# {claim}

# Opponent’s Argument:
# {pro_argument}

# Evidence:
# {evidence}

# Your task:
# Write a rebuttal that explains why the claim is still FALSE or misleading.

# Instructions:
# - Point out factual inaccuracies, flawed reasoning, or selective use of evidence in the opponent’s argument.
# - Use specific evidence to counter each claim, citing by number (e.g., [1], [6]).
# - If your opponent used emotionally loaded or vague claims, note this explicitly.
# - Stay sharp and concise, focusing on factual weaknesses.

# Your Rebuttal:"""
# def user_prompt_closing_pro(claim, evidence):
#     return f"""You are the supporting agent in a factual debate.

# Claim:
# {claim}

# Evidence:
# {evidence}

# Your task:
# Write a persuasive closing statement supporting the claim.

# Instructions:
# - Summarize your strongest factual arguments.
# - Reaffirm why the claim is TRUE, citing at least two specific pieces of evidence (with numbers).
# - Emphasize how your argument was more grounded in verifiable facts.
# - If the opposing agent relied on vague, emotional, or weak evidence, highlight this as a weakness in their case.

# Your Closing Statement:"""
# def user_prompt_closing_con(claim, evidence):
#     return f"""You are the opposing agent in a factual debate.

# Claim:
# {claim}

# Evidence:
# {evidence}

# Your task:
# Write a persuasive closing statement explaining why the claim is FALSE or HALF-TRUE.

# Instructions:
# - Reiterate the strongest factual weaknesses in the claim.
# - Cite at least two specific pieces of evidence (with numbers).
# - Emphasize any emotional or speculative reasoning used by the opposing agent, and explain why this undermines the claim.
# - End with a confident, evidence-based conclusion.

# Your Closing Statement:"""
# def user_prompt_judge_full(claim, evidence, pro_open, con_open, pro_rebut, con_rebut, pro_close, con_close):
#     return f"""You are a neutral judge evaluating a factual debate.

# Claim:
# {claim}

# Evidence:
# {evidence}

# --- Opening Statements ---
# Pro Agent:
# {pro_open}

# Con Agent:
# {con_open}

# --- Rebuttals ---
# Pro Agent:
# {pro_rebut}

# Con Agent:
# {con_rebut}

# --- Closing Statements ---
# Pro Agent:
# {pro_close}

# Con Agent:
# {con_close}

# Instructions:
# 1. Decide whether the claim is TRUE, FALSE, or HALF-TRUE.
# 2. Prioritize arguments that are clearly supported by factual, verifiable evidence (cite evidence numbers).
# 3. Penalize any side that relies heavily on vague, emotional, or anecdotal content.
# 4. Identify whether either side misrepresented the evidence or ignored critical facts.
# 5. Be specific and reference both the **evidence** and the **agents' arguments**.

# Answer format:
# [REASON]: <Your structured reasoning and justification>
# [VERDICT]: TRUE / FALSE / HALF-TRUE
# """