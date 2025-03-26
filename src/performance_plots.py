import time
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# -------------------------------------------------------
# 1) Benchmark for the serial version
# -------------------------------------------------------
def benchmark_serial(func_serial, transactions, candidates, process_list=[1, 2, 3, 4, 6]):
    """
    Although the serial version doesn't use multiple processes,
    we measure the time once and replicate it across the process list
    to maintain consistency in the plot.
    """
    times = {}
    start = time.time()
    _ = func_serial(transactions, candidates)
    end = time.time()
    total_time = end - start

    for p in process_list:
        times[p] = total_time

    return times

# -------------------------------------------------------
# 2) Benchmark for the parallel version
# -------------------------------------------------------
def benchmark_parallel(func_parallel, transactions, candidates, process_list=[1, 2, 3, 4, 6]):
    """
    Measures the execution time of the parallel function using different numbers of processes.
    """
    times = {}
    for p in process_list:
        start = time.time()
        _ = func_parallel(transactions, candidates, num_processes=p)
        end = time.time()
        times[p] = end - start
        print(f"Processes={p} -> Time={times[p]:.4f} s")
    return times

# -------------------------------------------------------
# 3) Function to generate the combined plot
# -------------------------------------------------------
def plot_performance_analysis(times_serial, times_parallel, process_list, output_path="plots/performance_analysis.png"):
    """
    Generates two subplots:
      - Left: Execution time (Serial vs Parallel).
      - Right: Speedup (Real vs Ideal).
    """
    # Use the serial time for 1 process as reference
    serial_time_1 = times_serial[1]
    
    x = process_list
    y_serial = [times_serial[p] for p in x]
    y_parallel = [times_parallel[p] for p in x]
    
    # Real speedup: serial_time / parallel_time
    speedup_real = [serial_time_1 / times_parallel[p] for p in x]
    # Ideal speedup: equal to number of processes
    speedup_ideal = [p for p in x]
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Performance: Serial vs Parallel", "Speedup vs Number of Processes")
    )
    
    # Subplot 1: Execution time
    fig.add_trace(
        go.Scatter(x=x, y=y_serial, mode='lines+markers', name='Serial Execution'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=x, y=y_parallel, mode='lines+markers', name='Parallel Execution'),
        row=1, col=1
    )
    fig.update_xaxes(title_text="Number of Processes", row=1, col=1)
    fig.update_yaxes(title_text="Time (seconds)", row=1, col=1)
    
    # Subplot 2: Speedup
    fig.add_trace(
        go.Scatter(x=x, y=speedup_real, mode='lines+markers', name='Real Speedup'),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=x, y=speedup_ideal, mode='lines+markers', line=dict(dash='dash'), name='Ideal Speedup'),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Number of Processes", row=1, col=2)
    fig.update_yaxes(title_text="Speedup", row=1, col=2)
    
    fig.update_layout(
        title="Performance Analysis: Market Basket Analysis",
        template="plotly_white"
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_image(output_path)
    print(f"Performance analysis plot saved to {output_path}")

# -------------------------------------------------------
# 4) Main function to run the entire process
# -------------------------------------------------------
def main(func_serial, func_parallel, transactions, candidates, process_list=[1, 2, 3, 4, 6], output_path="plots/performance_analysis.png"):
    times_serial = benchmark_serial(func_serial, transactions, candidates, process_list)
    times_parallel = benchmark_parallel(func_parallel, transactions, candidates, process_list)
    plot_performance_analysis(times_serial, times_parallel, process_list, output_path)

if __name__ == "__main__":
    print("This module is intended to be imported and used by another script to generate performance plots.")
