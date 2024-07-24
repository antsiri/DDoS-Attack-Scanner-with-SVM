# DDoS Attack Scanner with Machine Learning (SVM)
## DDoS detection and management in a Mininet topology

In this project, it's possible to see how to implement a Machine Learning model in a network attack. 
For details read the [documentation](documentation.pdf) (for several reasons is in Italian).

To run the code in Linux

- Run the controller: `ryu-manager controller.py`
- Run the topology: `sudo python3 topology.py`
- Run the scanner: `sudo python3 collector.py`

> To train the model, run `sudo python3 svm.py` before running the scanner.

After that, in the Mininet terminal, it's possible to try to generate traffic:
For example:
- For a normal traffic generation run: `h2 ping h3`
- For a DDoA attack simulation: `h1 hping3 --source-rand --flood h2`
