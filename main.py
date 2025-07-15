import argparse
from agents.single_agent import verify_claim
from agents.multi_agents import (
    opening_pro, rebuttal_pro, closing_pro,
    opening_con, rebuttal_con, closing_con,
    judge_final_verdict
)
import json
from tqdm import tqdm

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
    # print("\n=== Running Single Agent Verification ===")
    result = verify_claim(claim, evidence)
    # print(result)
    return result

def run_multi_agent(claim, evidence):
    print("\n=== Running Multi-Agent Debate (3 rounds) ===")

    # Round 1: Opening
    pro_open = opening_pro(claim, evidence)
    con_open = opening_con(claim, evidence)

    # Round 2: Rebuttal
    pro_rebut = rebuttal_pro(claim, evidence, con_open)
    con_rebut = rebuttal_con(claim, evidence, pro_open)

    # Round 3: Closing
    pro_close = closing_pro(claim, evidence)
    con_close = closing_con(claim, evidence)

    # Final Verdict
    final_result = judge_final_verdict(
        claim, evidence,
        pro_open, con_open,
        pro_rebut, con_rebut,
        pro_close, con_close
    )

    # Output
    # print("\n--- Pro Agent Opening ---\n", pro_open)
    # print("\n--- Con Agent Opening ---\n", con_open)
    # print("\n--- Pro Agent Rebuttal ---\n", pro_rebut)
    # print("\n--- Con Agent Rebuttal ---\n", con_rebut)
    # print("\n--- Pro Agent Closing ---\n", pro_close)
    # print("\n--- Con Agent Closing ---\n", con_close)

    # print("\n=== Final Judge Verdict ===")
    # print(final_result)
    return pro_open, con_open, pro_rebut, con_rebut, pro_close, con_close, final_result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["single", "multi"], default="single", help="Choose inference mode.")
    args = parser.parse_args()

    # claim, evidence = get_example()
    # with open("dataset/test.json", "r") as f:
    #     all_examples = json.load(f)
    with open("/home/yirui/mad/data/retrived_evidence_query.json", "r") as f:
        all_examples = json.load(f)
    answer_map = {}
    
    # Load existing results if file exists  
    # output_file = "answer_map_single.json" if args.mode == "single" else "answer_map_multi.json"
    output_file = "answer_map_retrived_evidence_single.json" if args.mode == "single" else "answer_map_retrived_evidence_multi.json"
    try:
        with open(output_file, "r") as f:
            answer_map = json.load(f)
    except FileNotFoundError:
        answer_map = {}

    if args.mode == "single":
        for example in tqdm(all_examples, desc="Processing examples"):
            example_id = example["example_id"]
            claim = example["claim"]
            evidence = example["evidence"]
            result = run_single_agent(claim, evidence)
            answer_map[example_id] = [result]
            
            # Write after each example
            with open(output_file, "w") as f:
                json.dump(answer_map, f, indent=2)
    else:
        for example in tqdm(all_examples, desc="Processing examples"):
            example_id = example["example_id"]
            # Skip if already processed
            if example_id in answer_map:
                continue
                
            claim = example["claim"]
            evidence = example["evidence"]
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
            
            # Write after each example
            with open(output_file, "w") as f:
                json.dump(answer_map, f, indent=2)
if __name__ == "__main__":
    main()