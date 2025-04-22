# JSTargetFuzzer

JSTargetFuzzer-v2.0 is an approach that utilizes novel history-based fuzzing guidance with tailored seeds and mutation operators, using Fuzzilli as base software.

## Install

* System configuration:
  * Intel i9 14900F (24 cores)
  * Kali Linux 2024.1

* Third-Party Software:
  * Install Swift version 5.6.3 (swift-5.6.2-RELEASE-ubuntu20.04)
  * Extract the tarball file and add to the $PATH:
  * ```bash
    export $PATH=$PATH:/home/user/swift-5.6.2/

* Instructions to install JSTargetFuzzer
  * In the terminal, run the following commands to clone the repository
  * ```bash
    git clone git@github.com:brunogoliveira-ufpr/JSTargetFuzzer-V2.git
  
## Usage
If everything is working correctly, you can run JSTargetFuzzer using command-line:
* ```bash
   swift-run FuzzilliCli --help

### Targets & Instrumentation

JSTargetFuzzer utilizes the JavaScript engine's instrumentation to target security-relevant address space and redirect the fuzzing campaigns towards it.
Instrumentation examples are found in [TargetsJST](./TargetsJST/) folder.

## Experimental Package
All the statistics and results for four RQs are saved in the directory [results](./results). 

Basic JST command-line with minimum corpus size = 2,000:
```bash
swift-run FuzzilliCli --profile=duktape /home/kali/JSEs/duktape/build/duk-fuzzilli --minCorpusSize=2000
```

### RQ1
* Install Streamlit
```bash
pip install streamlit
```
* Run Streamlit from the folder ./cli/. A front-end interface will be available for the evaluation.
```bash
streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.27.114.46:8501
```
### RQ2
All the programs for RQ2 are saved in IL (Intermediate Language) files within the `programs/files` folder during execution. Programs with no flag are saved with _weight1 suffix and with security flag are saved with _weight1000.

For program analysis, utilize the `streamlet` client.
* To convert the IL to JavaScript:
```bash
swift-run FuzzILTool --liftCorpusToJS /programs/files/
```  

The programs analyzed during the experiment are compressed in ZIP files and saved in [Analyzed Programs](./analyzed-programs/) folder.
The script used to calculate the metrics for the JavaScript files is in the same folder, [program_metrics.py](./analyzed_programs/program_metrics.py).

### RQ3
The JavaScript files that caused the crashes are saved in a directory determined by command-line, for example:
```bash
swift-run FuzzilliCli --profile=duktape /home/kali/JSEs/duktape/build/duk-fuzzilli --storagePath=./crashes-duktape/
```
Then the directory ./crashes-duktape/crashes will store the files responsible for crashes during the fuzzing campaign.


### RQ4
The mutation operators and seeds are set by command-line, as an example:
```bash
swift-run FuzzilliCli --profile=duktape /home/kali/JSEs/duktape/build/duk-fuzzilli --mutators=splice,combine,operation,exploration,codegen --minCorpusSize=2000
```




