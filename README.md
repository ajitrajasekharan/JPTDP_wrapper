# Simple HTTP wrapper around [Dat Quoc Nguyen's ](https://github.com/datquocnguyen) [Joint POS Tagger and parser.](https://github.com/datquocnguyen/jPTDP)


### Installation

jPTDP requires the following software packages:

* `Python 2.7`
* [`DyNet` v2.0](http://dynet.readthedocs.io/en/latest/python.html)

      $ pip install cython numpy
      $ pip install dynet==2.0.3
      $ pip install gdown
      
* Once installed, run fetch_model.sh to download pretrained  model

* then execute run_server.sh to expose tagging as a simple HTTP service



## License

See [original license (GPL)](https://github.com/datquocnguyen/jPTDP/blob/master/License.txt)
