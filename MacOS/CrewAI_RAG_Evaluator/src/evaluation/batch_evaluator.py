import json
from evaluation.retrieval_evaluator import evaluate_retrieval
from evaluation.generation_evaluator import evaluate_generation

def load_test_cases(file_path="test_cases.json"):
    """Loads test cases from a JSON file."""
    with open(file_path, "r") as file:
        test_cases = json.load(file)
    return test_cases["tests"]

def batch_evaluate():
    """Runs batch evaluation for all test cases and logs results."""
    test_cases = load_test_cases()
    results = []

    for i, test in enumerate(test_cases):
        retrieval_score = evaluate_retrieval(test["retrieved_docs"], test["expected_response"])
        generation_score = evaluate_generation(test["generated_response"], test["expected_response"])

        result = {
            "test_case": i + 1,
            "query": test["query"],
            "retrieval_score": retrieval_score,
            "generation_score": generation_score
        }

        results.append(result)
        print(f"Test Case {i+1}: {result}")

    return results

if __name__ == "__main__":
    batch_results = batch_evaluate()