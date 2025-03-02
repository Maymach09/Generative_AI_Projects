from crews.crew import run_crew
from evaluation.batch_evaluator import batch_evaluate

if __name__ == "__main__":
    # Run Crew Tasks
    run_crew()

    # Run Batch Evaluation
    print("\nRunning Batch Evaluation...")
    batch_results = batch_evaluate()
