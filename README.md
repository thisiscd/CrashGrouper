# CrashGrouper
we introduce our approach to reducing the overhead caused by redundant crash reports generated by fuzzing tools. Our method is designed to streamline the analysis process by automatically grouping similar crashes, thereby allowing security analysts to focus on representative samples instead of manually reviewing each crash instance.

Our approach is divided into three key phases:

- **Reconstruction of Instruction Flow:** We utilize Intel Processor Trace (PT) to track the program's execution and reconstruct the sequence of instructions that led to the crash. This provides a detailed view of the execution context within the last function where the crash occurred.
- **Extraction and Generalization of Instruction Slice:** Based on the reconstructed instruction flow, we perform backwards slicing to isolate the critical instructions that contributed to the crash. The slice is then generalized by abstracting away specific registers and immediate values to produce a normalized instruction sequence.
- **Grouping of Crashes:** Finally, we apply fuzzy hashing to the generalized instruction slices to compute similarity between crashes. A greedy grouping algorithm is then used to cluster crashes, with each group being represented by a single crash. This drastically reduces the total number of unique crashes that require manual analysis.

![framework](./framework.pdf)
