# MirrorDataGenerator

mirrorGen is an open source tool to generate synthetic data based on a correlation DAG, which describes the relation among the columns in the data. It can be used to produce "dirty" data, mirroring various bias in real life, which can be used in applications, such as classification and ranking tasks [1](https://arxiv.org/abs/2006.08688).

### Prerequisite for language

Python 3: [Install Tutorial](https://installpython3.com/)


### Install MirrorDataGenerator

Step 1 Download MirrorDataGenerator.

Step 2 Unzip the downloaded source file and initiate the python environment.

```bash
cd MirrorDataGenerator  # go to the MirrorDataGenerator repository that is just downloaded
python -m venv venv
source venv/bin/activate  # activate the environment for MirrorDataGenerator
pip install -r requirements.txt
```

 
### Usage of MirrorDataGenerator

We prepared a [demo notebook](Demo_mirror_generator.ipynb) to showcase Mirror Data Generator.


### Methodology 

TBD. 


### License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
