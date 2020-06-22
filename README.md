# MirrorDataGenerator

MirrorDataGenerator is a python tool that generates synthetic data based on user-specified causal relations among features in the data. It focuses on how features relate with demographic attributes (e.g. gender, race, disability status, etc), which are considered as sensitive information for certain domains (e.g. employment, housing, etc). 

### Prerequisite for language

Python 3: [Install Tutorial](https://installpython3.com/)


### Install MirrorDataGenerator

Step 1 Download MirrorDataGenerator.

Step 2 Unzip the downloaded source file and initiate the python environment.

```bash
cd MirrorDataGenerator  # go to the MirrorDataGenerator repository that is just downloaded
python -m venv MirrDataGen
source MirrDataGen/bin/activate  # activate the environment for MirrorDataGenerator
pip install -r requirements.txt
```

### Run MirrorDataGenerator

Using MirrorDataGenerator to generate a dataset that is specified as in mv_m2.json, use the following command:

```python
python gen_orig_data.py --data_flag mv --para_file mv_m2.json --run 1

```

Input parameters:
- data_flag: str, specify the folder name to store the generated CSV files.
- para_file: str, the file name of the parameter json file. Path need to be included if it is not in the same repository.
- run: int, the number of datasets to be generated.

Output:

The generated CSV files are stored in "out/DATA_FLAG" with names of "R#.csv".


### Methodology 

TBD. 


### License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
