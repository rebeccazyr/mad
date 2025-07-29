def get_system_prompt(role: str = "fact_checker") -> str:
    if role == "fact_checker":
        return "You are a precise and critical fact checker."
    elif role == "judge":
        return "You are a neutral judge who evaluates multi-agent factual debates."
    elif role == "true_agent":
        return "You are a critical thinker who argues that the claim is TRUE."
    elif role == "halftrue_agent":
        return "You are a critical thinker who argues that the claim is HALF-TRUE."
    elif role == "false_agent":
        return "You are a critical thinker who argues that the claim is FALSE."
    else:
        return "You are a helpful assistant."

def system_prompt_fact_checker():
    return get_system_prompt("fact_checker")

def user_prompt_opening_true(claim, evidence):
    return f"""You believe the claim is TRUE. Present your opening argument using the evidence.

Claim: {claim}

Evidence:
{evidence}

Begin by stating your stance. Highlight facts that support the claim as entirely TRUE."""

def user_prompt_opening_halftrue(claim, evidence):
    return f"""You believe the claim is HALF-TRUE. Present your opening argument using the evidence.

Claim: {claim}

Evidence:
{evidence}

Begin by explaining why the claim contains some truth but also includes misleading or incorrect aspects."""

def user_prompt_opening_false(claim, evidence):
    return f"""You believe the claim is FALSE. Present your opening argument using the evidence.

Claim: {claim}

Evidence:
{evidence}

Begin by stating your position. Explain why the claim is incorrect or misleading, referencing specific points in the evidence."""

def user_prompt_rebuttal_true(claim, evidence, halftrue_argument, false_argument):
    return f"""You believe the claim is TRUE. Respond to the opposing arguments from agents who claim it's HALF-TRUE and FALSE.

Claim: {claim}

Evidence:
{evidence}

Half-True Agent's Argument:
{halftrue_argument}

False Agent's Argument:
{false_argument}

Write your rebuttal defending why the claim is TRUE and addressing the flaws in the other arguments."""

def user_prompt_rebuttal_halftrue(claim, evidence, true_argument, false_argument):
    return f"""You believe the claim is HALF-TRUE. Respond to the opposing arguments from agents who claim it's TRUE and FALSE.

Claim: {claim}

Evidence:
{evidence}

True Agent's Argument:
{true_argument}

False Agent's Argument:
{false_argument}

Write your rebuttal defending your middle-ground position and pointing out issues in the other arguments."""

def user_prompt_rebuttal_false(claim, evidence, true_argument, halftrue_argument):
    return f"""You believe the claim is FALSE. Respond to the opposing arguments from agents who claim it's TRUE and HALF-TRUE.

Claim: {claim}

Evidence:
{evidence}

True Agent's Argument:
{true_argument}

Half-True Agent's Argument:
{halftrue_argument}

Write your rebuttal defending why the claim is FALSE and pointing out flaws in the other arguments."""

def user_prompt_closing_true(claim, evidence):
    return f"""You believe the claim is TRUE. Provide your closing statement.

Claim: {claim}

Evidence:
{evidence}

Reinforce why the claim is entirely TRUE and summarize your strongest points."""

def user_prompt_closing_halftrue(claim, evidence):
    return f"""You believe the claim is HALF-TRUE. Provide your closing statement.

Claim: {claim}

Evidence:
{evidence}

Reinforce why the claim is partially accurate but still misleading or incomplete."""

def user_prompt_closing_false(claim, evidence):
    return f"""You believe the claim is FALSE. Provide your closing statement.

Claim: {claim}

Evidence:
{evidence}

Reinforce why the claim is FALSE and summarize the key issues you’ve highlighted."""

def user_prompt_judge_full_triagent(
    claim, evidence,
    true_open, halftrue_open, false_open,
    true_rebut, halftrue_rebut, false_rebut,
    true_close, halftrue_close, false_close
):
    return f"""You are a neutral judge evaluating a three-agent factual debate.

Claim: {claim}

Evidence:
{evidence}

--- Opening Statements ---
TRUE Agent:
{true_open}

HALF-TRUE Agent:
{halftrue_open}

FALSE Agent:
{false_open}

--- Rebuttals ---
TRUE Agent:
{true_rebut}

HALF-TRUE Agent:
{halftrue_rebut}

FALSE Agent:
{false_rebut}

--- Closing Statements ---
TRUE Agent:
{true_close}

HALF-TRUE Agent:
{halftrue_close}

FALSE Agent:
{false_close}

Based on the arguments and evidence, decide whether the claim is TRUE, HALF-TRUE, or FALSE.

Answer format:
[VERDICT]: TRUE / HALF-TRUE / FALSE  
[REASON]: <your justification>
"""