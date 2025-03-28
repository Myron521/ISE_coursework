#ISE - coursework
This repository is a collection of code and documentation for the ISE coursework. It mainly focuses on sentiment analysis of multiple open - source projects (such as PyTorch, TensorFlow, Keras, etc.).
#Project Structure
```
ISE - coursework/ 
├── code/ 
│ ├── baseline/                        # Baseline model code (original_NB code) v
│ ├── improved/                       # Improved model code (improved code for each project) 
│ └── utils/                           # General utility scripts (e.g., data merging script) 
├── results/                           # Result files  
│ ├── caffe_NB.csv                    # Baseline results 
│ ├── caffe_improved.csv               # Improved results 
│ ├── incubator - mxnet_NB.csv 
│ ├── incubator - mxnet_improved.csv 
│ └── ... (similarly for other projects) 
├── requirements.pdf                   # Dependency description (Python libraries and versions) 
├── manual.pdf                       # User manual 
├── replication.pdf                    # Reproduction guide 
└── README.md                    # Overall repository description
```
#Environment Requirements
Please check the requirements.pdf file and install the required Python libraries and their corresponding versions.
#Usage
##Clone the Code Repository
```python
git clone <repository address>
cd ISE - coursework
```
##Run the Code
###Baseline Model
```python
cd code/baseline
python pytorch_nb_.py
```
###Improved Model
```python
cd code/improved
python pytorch_improved_.py
```
##View Results
After running the code, the results will be saved in the corresponding CSV files in the results directory.
#Reproduction Guide
Detailed reproduction steps can be found in the replication.pdf file.
#User Manual
For detailed usage instructions of the project, please refer to the manual.pdf file.
#Notes
Before running the code, ensure that the data file paths are correct.
The experimental results may be affected by the random seed and data distribution.