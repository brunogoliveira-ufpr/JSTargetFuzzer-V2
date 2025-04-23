# JSTargetFuzzer-V2

**JSTargetFuzzer-v2.0** is a fuzzing approach that incorporates novel history-based guidance, using tailored seeds and custom mutation operators. It is built on top of the Fuzzilli framework.

## Install

### System Configuration

- **CPU**: Intel i9-14900F (24 cores)  
- **OS**: Kali Linux 2024.1

### Third-Party Software

- Install Swift version 5.6.2 (`swift-5.6.2-RELEASE-ubuntu20.04`)
- Extract the tarball and add it to your `$PATH`:

  ```bash
  export PATH=$PATH:/home/user/swift-5.6.2/
  ```

### Cloning JSTargetFuzzer

Clone the repository using:

```bash
git clone git@github.com:brunogoliveira-ufpr/JSTargetFuzzer-V2.git
```

## Usage

If installed correctly, JSTargetFuzzer can be run with:

```bash
swift-run FuzzilliCli --help
```

## Targets & Instrumentation

JSTargetFuzzer uses instrumentation to direct fuzzing toward security-relevant regions of a JavaScript engine’s address space.  
Examples of instrumented targets are available in the `TargetsJST/` folder.

## Experimental Package

To run JSTargetFuzzer with a minimal corpus size of 2,000:

```bash
swift-run FuzzilliCli --profile=duktape /home/kali/JSEs/duktape/build/duk-fuzzilli --minCorpusSize=2000
```

Scripts utilized for the RQs are stored in `scripts/` folder.

## RQ1 – HitCount & UniqueHitCount Analysis

- Install Streamlit:

  ```bash
  pip install streamlit
  ```

- Launch the front-end interface from the `./client/` directory:

  ```bash
  streamlit run app.py
  ```

  The Streamlit app will be accessible at:

  - Local URL: http://localhost:8501  
  - Network URL: http://<your-ip>:8501

## RQ2 – Program Metrics Analysis

All programs for RQ2 are saved as Intermediate Language (IL) files in the `programs/files/` directory.

- Programs with `_nullflag` suffix have no security flags.
- Programs with `_secflag` suffix are tagged with security-relevant behavior.

To convert IL programs to JavaScript:

```bash
swift-run FuzzILTool --liftCorpusToJS /programs/files/
```

The script used to compute JavaScript metrics is available at: `scripts/RQ2-metrics.py`

## RQ3 – Crash Analysis

Crashing inputs are saved in a user-defined directory, for example:

```bash
swift-run FuzzilliCli --profile=duktape /home/kali/JSEs/duktape/build/duk-fuzzilli --storagePath=./crashes-duktape/ --minCorpusSize=2000
```

Crash-inducing files will be stored in:

```
./crashes-duktape/crashes/
```

## RQ4 – Vulnerabilities (Tailored Approach)

Example of how to run a fuzzing campaign using tailored mutation operators and seed configurations:

```bash
swift-run FuzzilliCli --profile=duktape /home/kali/JSEs/duktape/build/duk-fuzzilli --mutators=splice,combine,operation,exploration,codegen --minCorpusSize=2000
```

## Results

All statistical outputs and experimental data for RQ1–RQ4 are saved in the `results/` directory.
