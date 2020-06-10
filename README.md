# Simple HTTP wrapper around [Dat Quoc Nguyen's ](https://github.com/datquocnguyen) [Joint POS Tagger and Dependency parser.](https://github.com/datquocnguyen/jPTDP)


### Installation steps


* conda create -n py27 python=2.7
* cond activate py27
* [`DyNet` v2.0](http://dynet.readthedocs.io/en/latest/python.html)

      $ pip install cython numpy
      $ pip install dynet==2.0.3
      $ pip install gdown
      
* Once installed, run fetch_model.sh to download pretrained  model

* then execute run_server.sh to expose tagging as a simple HTTP service



## License

See [original license (GPL)](https://github.com/datquocnguyen/jPTDP/blob/master/License.txt)
