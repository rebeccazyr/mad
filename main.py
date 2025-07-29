import argparse
import json
from tqdm import tqdm
import os
from agents.single_agent import verify_claim
from agents.multi_agents import (
    opening_pro, rebuttal_pro, closing_pro,
    opening_con, rebuttal_con, closing_con,
    judge_final_verdict
)
from agents.multi_agents_3p import (
    opening_true, rebuttal_true, closing_true,
    opening_halftrue, rebuttal_halftrue, closing_halftrue,
    opening_false, rebuttal_false, closing_false,
    judge_final_verdict as judge_final_verdict_3p
)
from agents.multi_agent_people import (
    opening_politician, rebuttal_politician, closing_politician,
    opening_scientist, rebuttal_scientist, closing_scientist,
    judge_final_verdict as judge_final_verdict_people
)
from agents.intent_enhanced_retrieval import intent_enhanced_reformulation
from agents.single_agent_intent import infer_intent, final_verdict
# from agents.multi_agents_role import (
#     infer_intent_and_roles,
#     opening_pro, rebuttal_pro, closing_pro,
#     opening_con, rebuttal_con, closing_con,
#     judge_final_verdict
# )
import torch
def get_example():
    claim = "\"You know what the biggest lie is, is that restaurants are spreaders of COVID. There's no science for that.\""
    evidence_list = [
        "Fox News host Laura Ingraham downplayed the risk of contracting the coronavirus while dining at a restaurant, wrongly claiming restrictions on eating out are not supported by science.",
        "\"You know what the biggest lie is, is that restaurants are spreaders of COVID,\" Ingraham told host Sean Hannity during the handoff between their TV shows. \"There's no science for that.\"",
        "Hannity later specified that he was talking about \"outside\" dining in California. But Ingraham’s claim about restaurants was far more sweeping — and more wrong. It’s inaccurate to say that \"there’s no science\" to show \"restaurants are spreaders of COVID.\"",
        "\"There is a lot of information showing that restaurants are a high-risk environment,\" said Emily Landon, an epidemiologist and associate professor of medicine at the University of Chicago.",
        "\"Anytime people congregate, there exist increased opportunities for transmission should someone be infected,\" added Jeffrey Shaman, a professor of environmental health sciences at Columbia University. \"A restaurant is no different.\"",
        "The risks associated with dining out vary based on the safety precautions the restaurants take and the coronavirus situation in their geographic areas. Many restaurants have become safer over time, but case surges in many states make running into an infected person more likely.",
        "\"It’s hard to make universal claims because the pandemic is different in different parts of the country and even in different parts of the state,\" said Amesh Adalja, a senior scholar at the Johns Hopkins University Center for Health Security. \"In some parts of the country, restaurants aren’t driving cases. In others, they have been identified in case investigations.\"",
        "City data in Washington, D.C., for example, has shown restaurants and bars to be among the most common places for virus spread. Data in and around Los Angeles has been less clear.",
        "Still, there’s plenty of evidence that COVID-19 has and can spread at restaurants — and especially at those that let groups of people congregate indoors without masks.",
        "\"Modeling studies have indicated that restaurants are high-risk environments for COVID-19 transmission,\" said Jason McDonald, a spokesperson for the Centers for Disease Control and Prevention. \"In places like restaurants, people remove their masks to consume food and beverages, which increases the risk of transmission.\"",
        "One CDC report in September, based on a survey of 314 symptomatic people who got tested for the coronavirus in July, found a link between testing positive for the coronavirus and going to locations with on-site eating and drinking options, such as restaurants.",
        "The authors wrote that those with positive test results were \"approximately twice as likely to have reported dining at a restaurant\" than those who tested negative.",
        "In a November study published in Nature, researchers at Stanford University and Northwestern University analyzed anonymized cell phone mobility data from 10 U.S. cities from March to May.",
        "Full-service restaurants, gyms and other crowded places accounted for a disproportionate share of COVID-19 infections, the study’s simulations showed. \"Restaurants were by far the riskiest places,\" Stanford’s Jure Leskovec, an author of the report, told reporters in November.",
        "Patrons enjoy food and drink at The Brass Rail in Hoboken, N.J., on Nov. 11, 2020. (AP)"
    ]
    evidence_text = "\n".join(evidence_list)
    return claim, evidence_text

def run_single_agent(claim, evidence):
    return verify_claim(claim, evidence)

def run_multi_agent(claim, evidence):
    print("\n=== Running Multi-Agent Debate (3 rounds) ===")
    pro_open = opening_pro(claim, evidence)
    con_open = opening_con(claim, evidence)
    pro_rebut = rebuttal_pro(claim, evidence, con_open)
    con_rebut = rebuttal_con(claim, evidence, pro_open)
    pro_close = closing_pro(claim, evidence)
    con_close = closing_con(claim, evidence)
    final_result = judge_final_verdict(
        claim, evidence,
        pro_open, con_open,
        pro_rebut, con_rebut,
        pro_close, con_close
    )
    return pro_open, con_open, pro_rebut, con_rebut, pro_close, con_close, final_result

def run_multi_agent_3p(claim, evidence):
    print("\n=== Running Three-Agent Debate (True, Half-True, False) ===")
    # Opening statements
    true_open = opening_true(claim, evidence)
    halftrue_open = opening_halftrue(claim, evidence)
    false_open = opening_false(claim, evidence)
    
    # Rebuttals
    true_rebut = rebuttal_true(claim, evidence, halftrue_open, false_open)
    halftrue_rebut = rebuttal_halftrue(claim, evidence, true_open, false_open)
    false_rebut = rebuttal_false(claim, evidence, true_open, halftrue_open)
    
    # Closing statements
    true_close = closing_true(claim, evidence)
    halftrue_close = closing_halftrue(claim, evidence)
    false_close = closing_false(claim, evidence)
    
    # Final judge verdict
    final_result = judge_final_verdict_3p(
        claim, evidence,
        true_open, halftrue_open, false_open,
        true_rebut, halftrue_rebut, false_rebut,
        true_close, halftrue_close, false_close
    )
    return (true_open, halftrue_open, false_open, 
            true_rebut, halftrue_rebut, false_rebut,
            true_close, halftrue_close, false_close, final_result)

def run_multi_agent_people(claim, evidence):
    print("\n=== Running Multi-Agent People Debate (Politician vs Scientist) ===")
    # Opening statements
    pol_open = opening_politician(claim, evidence)
    sci_open = opening_scientist(claim, evidence)
    
    # Rebuttals
    pol_rebut = rebuttal_politician(claim, evidence, sci_open)
    sci_rebut = rebuttal_scientist(claim, evidence, pol_open)
    
    # Closing statements
    pol_close = closing_politician(claim, evidence)
    sci_close = closing_scientist(claim, evidence)
    
    # Final judge verdict
    final_result = judge_final_verdict_people(
        claim, evidence,
        pol_open, sci_open,
        pol_rebut, sci_rebut,
        pol_close, sci_close
    )
    return pol_open, sci_open, pol_rebut, sci_rebut, pol_close, sci_close, final_result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["single", "multi", "multi_role", "intent_enhanced_multi", "intent_enhanced_single_sep", "intent_enhanced_multi_sep", "multi_3p", "multi_people"],
        default="single",
        help="Choose inference mode."
    )
    args = parser.parse_args()

    with open("/home/yirui/mad/ids_400.json", "r") as f:
        ids_400 = json.load(f)

    with open("/home/yirui/mad/intent_enhanced_con_pro_bge_large_400_top20_by_score_with_evi.json", "r") as f:
        all_examples = json.load(f)
    
    all_examples = {k: v for k, v in all_examples.items() if k in ids_400}

    # Choose output file
    output_file = os.path.join("bilin", f"400_answer_map_bge_con_pro_noid_{args.mode}.json")

    try:
        with open(output_file, "r") as f:
            answer_map = json.load(f)
    except FileNotFoundError:
        answer_map = {}

    for example_id, example in tqdm(all_examples.items(), desc=f"Processing examples ({args.mode})"):
        if example_id in answer_map:
            continue

        claim = example["claim"]
        # evidence = example["evidence"]
        evidence = example["evidence_full_text"]
        # evidence_pro_text = example["evidence_pro_text"]
        # evidence_con_text = example["evidence_con_text"]

        if args.mode == "single":
            result = run_single_agent(claim, evidence)
            answer_map[example_id] = [result]

        elif args.mode == "multi_role":
            # Step 1: 推理 intent 和角色
            intent, support_role, oppose_role = infer_intent_and_roles(claim)

            # Step 2: Opening statements
            pro_open = opening_pro(claim, evidence, role=support_role)
            con_open = opening_con(claim, evidence, role=oppose_role)

            # Step 3: Rebuttals
            # pro_rebut = rebuttal_pro(claim, evidence, con_open)
            # con_rebut = rebuttal_con(claim, evidence, pro_open)
            pro_rebut = rebuttal_pro(claim, evidence, con_open, role=support_role)
            con_rebut = rebuttal_con(claim, evidence, pro_open, role=oppose_role)

            # Step 4: Closings
            # pro_close = closing_pro(claim, evidence)
            # con_close = closing_con(claim, evidence)
            pro_close = closing_pro(claim, evidence, role=support_role)
            con_close = closing_con(claim, evidence, role=oppose_role)

            # Step 5: Judge verdict
            final_result = judge_final_verdict(
                claim, evidence,
                pro_open, con_open,
                pro_rebut, con_rebut,
                pro_close, con_close
            )
            answer_map[example_id] = {
                "intent": intent,
                "support_role": support_role,
                "oppose_role": oppose_role,
                "pro_opening": pro_open,
                "con_opening": con_open,
                "pro_rebuttal": pro_rebut,
                "con_rebuttal": con_rebut,
                "pro_closing": pro_close,
                "con_closing": con_close,
                "final_verdict": final_result
            }

        elif args.mode == "multi":
            pro_open, con_open, pro_rebut, con_rebut, pro_close, con_close, final_result = run_multi_agent(claim, evidence)
            answer_map[example_id] = {
                "pro_opening": pro_open,
                "con_opening": con_open,
                "pro_rebuttal": pro_rebut,
                "con_rebuttal": con_rebut,
                "pro_closing": pro_close,
                "con_closing": con_close,
                "final_verdict": final_result
            }

        elif args.mode == "intent_enhanced_single_sep":
            intent = infer_intent(claim)
            result = final_verdict(claim, evidence, intent)
            answer_map[example_id] = [result]

        elif args.mode == "intent_enhanced_multi_sep":
            evidence_transformed = f"### Pro-side Evidence:\n{evidence_pro_text}\n\n### Con-side Evidence:\n{evidence_con_text}"
            pro_open, con_open, pro_rebut, con_rebut, pro_close, con_close, final_result = run_multi_agent(claim, evidence_transformed)
            answer_map[example_id] = {
                "pro_opening": pro_open,
                "con_opening": con_open,
                "pro_rebuttal": pro_rebut,
                "con_rebuttal": con_rebut,
                "pro_closing": pro_close,
                "con_closing": con_close,
                "final_verdict": final_result
            }
            
        elif args.mode == "multi_3p":
            (true_open, halftrue_open, false_open, 
             true_rebut, halftrue_rebut, false_rebut,
             true_close, halftrue_close, false_close, final_result) = run_multi_agent_3p(claim, evidence)
            answer_map[example_id] = {
                "true_opening": true_open,
                "halftrue_opening": halftrue_open,
                "false_opening": false_open,
                "true_rebuttal": true_rebut,
                "halftrue_rebuttal": halftrue_rebut,
                "false_rebuttal": false_rebut,
                "true_closing": true_close,
                "halftrue_closing": halftrue_close,
                "false_closing": false_close,
                "final_verdict": final_result
            }
            
        elif args.mode == "multi_people":
            pol_open, sci_open, pol_rebut, sci_rebut, pol_close, sci_close, final_result = run_multi_agent_people(claim, evidence)
            answer_map[example_id] = {
                "politician_opening": pol_open,
                "scientist_opening": sci_open,
                "politician_rebuttal": pol_rebut,
                "scientist_rebuttal": sci_rebut,
                "politician_closing": pol_close,
                "scientist_closing": sci_close,
                "final_verdict": final_result
            }
            
        with open(output_file, "w") as f:
            json.dump(answer_map, f, indent=2)

if __name__ == "__main__":
    print("CUDA_VISIBLE_DEVICES =", os.environ.get("CUDA_VISIBLE_DEVICES"))
    print(">> Using CUDA device:", torch.cuda.current_device())
    print(">> Device name:", torch.cuda.get_device_name(torch.cuda.current_device()))
    main()