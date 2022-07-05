# Reproduction Package #

This is the reproduction package for Trident. It contains scripts to reproduce two examples chosen to demonstrate the difference in the evaluated configurations.

* Codeflaws 676-A-bug-18247191-18247237
* Coreutils c160afe

This package also path data for Codeflaws dataset.

## File System Contents ##

* `eval` - data and scripts
    1. `codeflaws_test` - one example program from Codeflaws 676-A-bug-18247191-18247237
    2. `coreutils_test` - one example program from Coreutils c160afe
    3. `data` - path count data for Codeflaws
    4. `scripts` - scripts to generate plots
* `Dockerfile` - Dockerfile to build a container for executing examples
* `Trident` - Trident's source code

## Reproduction Instructions ##

This section describes how to reproduce experiments with the two examples from Codeflaws and Coreutils

### Building the Container

Building the Dockerfile
```
docker build . -t reproduction_package
```

Going into the docker container
```
docker run -v $(pwd):/home/Trident/ --rm -ti reproduction_package /bin/bash
```
### Tools

The package helps in running the following tools
- Trident  --> Mentioned in the paper
- Semfix   --> [semfix](https://www.comp.nus.edu.sg/~abhik/pdf/ICSE13-SEMFIX.pdf) with support for l-value patches
- klee-merge --> Runs semfix with support for l-value patches and state merge with klee's `use-merge`.

### Running Codeflaws
Running the sample codeflaws test with semfix
```
cd eval/codeflaws_test
python3 script.py 676-A-bug-18247191-18247237 --semfix
```
with klee
```
python3 script.py 676-A-bug-18247191-18247237 --klee-merge
```
running with Trident, specifying no option defaults it to Trident
```
python3 script.py 676-A-bug-18247191-18247237
```
You can run the patch prioritisation by using `--priority`.
For help run

```
python3 script.py -h
```

### Running Coreutils

The `<tool_name>` can be replaced with `trident`, `semfix` or `klee-merge` 
```
> cd eval/coreutils_test/test_c160afe
> ./run.sh <tool_name>
```
For example we can run klee-merge method with
```
> ./run.sh klee-merge
```

### Retrieve Plot
This command saves the plot in the file codeflaws_paths.png in the current directory
```
>python3 eval/scripts/plot_codeflaws_paths.py
```
