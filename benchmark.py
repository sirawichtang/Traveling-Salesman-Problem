import csv
import time

import algorithm
import config
import node

ALGORITHMS = (
    ("Brute Force", algorithm.brute_force_tsp),
    ("ACO", algorithm.ant_colony_tsp),
    ("Nearest Neighbor", algorithm.nearest_neighbor_tsp),
    ("Held-Karp", algorithm.held_karp_tsp),
    ("two-opt", algorithm.two_opt_tsp),
)


def run_benchmarks():
    start_count = config.benchmarkStartNodeCount
    end_count = config.benchmarkEndNodeCount
    step_size = config.benchmarkStepCount
    repeats = config.benchmarkRepeats

    node_counts = range(start_count, end_count + 1, step_size)
    config.doDraw = False
    test_cases = {
        node_count: [node.generateNode(node_count) for _ in range(repeats)]
        for node_count in node_counts
    }
    summaries = {
        name: {"completed": 0, "skipped": 0, "elapsed_seconds": 0.0}
        for name, _ in ALGORITHMS
    }

    # making csv file
    with open(
        config.benchmarkResultsFile, "w", newline="", encoding="utf-8"
    ) as results_file:
        writer = csv.DictWriter(
            results_file,
            fieldnames=(
                "algorithm",
                "node_count",
                "repeat",
                "status",
                "elapsed_seconds",
                "total_distance",
                "iterations",
            ),
        )
        writer.writeheader()

        total_cases = len(node_counts) * repeats
        for name, algorithm_fn in ALGORITHMS:
            print(f"Starting {name} benchmark.")
            for count_index, node_count in enumerate(node_counts, start=1):
                for repeat, node_list in enumerate(test_cases[node_count], start=1):
                    if node_count > config.benchmarkMaxNodeCount[name]:
                        writer.writerow(
                            {
                                "algorithm": name,
                                "node_count": node_count,
                                "repeat": repeat,
                                "status": "skipped",
                            }
                        )
                        summaries[name]["skipped"] += 1
                        continue

                    started_at = time.perf_counter()
                    _, total_distance, iterations = algorithm_fn(node_list)
                    elapsed_seconds = time.perf_counter() - started_at
                    writer.writerow(
                        {
                            "algorithm": name,
                            "node_count": node_count,
                            "repeat": repeat,
                            "status": "completed",
                            "elapsed_seconds": f"{elapsed_seconds:.6f}",
                            "total_distance": total_distance,
                            "iterations": iterations,
                        }
                    )
                    summaries[name]["completed"] += 1
                    summaries[name]["elapsed_seconds"] += elapsed_seconds

                completed_cases = count_index * repeats
                results_file.flush()
                print(
                    f"{name}: completed node count {node_count} "
                    f"({completed_cases}/{total_cases} cases)."
                )

    print(f"Benchmark results saved to {config.benchmarkResultsFile}")
    for name, summary in summaries.items():
        completed = summary["completed"]
        average_time = summary["elapsed_seconds"] / completed if completed else 0.0
        print(
            f"{name}: {completed} completed, {summary['skipped']} skipped, "
        )
