# Lab 2 Analysis Answers

**1. How did GitHub Actions improve experiment reproducibility?**
GitHub Actions ensures that every experiment is run in a clean, isolated environment (ubuntu-latest) with the exact same dependencies (installed via requirements.txt) and steps. This eliminates "it works on my machine" issues and guarantees that anyone (or any machine) running the workflow will get the same results for the same code commitment.

**2. How easy was it to compare results across runs?**
It was very easy because GitHub Actions extracts the metrics (MSE, R2) and displays them in the "Job Summary" for each run. We can simply open the "Actions" tab, click on different workflow runs, and compare the summary tables side-by-side without needing to dig into log files manually.

**3. What role does Git commit history play in experiment tracking?**
Git commit history acts as a timeline of experiments. Each commit represents a specific version of the model/code (e.g., "Experiment 2: Lasso Regression"). By checking out a specific commit, we can revert to that exact state. The commit message serves as a label for the experiment, making it easy to identify what changed.

**4. What were the benefits of this approach compared to Lab 1?**
In Lab 1, training was likely manual, repetitive, and prone to human error. In this approach:
- **Automation:** Training happens automatically on push.
- **Reporting:** Metrics are automatically reported.
- **Artifacts:** Models are automatically saved and downloadable.
- **Collaboration:** Anyone on the team can see the results of changes immediately.

**5. What limitations does this approach have?**
- **Resource Limits:** GitHub Actions has usage limits (minutes/storage) for free accounts.
- **Debugging:** Debugging a failed pipeline in the cloud can be slower than debugging locally (waiting for the container to spin up).
- **Latency:** There is a delay between pushing code and seeing results compared to running a script locally.
