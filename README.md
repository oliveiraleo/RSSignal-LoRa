# RSSignal-LoRa

This repository contains the source code of a proposed validation framework called `RSSignal`.

RSSignal uses [RSSI](https://en.wikipedia.org/wiki/Received_signal_strength_indication) (Received Signal Strength Indication) measurements as input, process them through some steps and generates a key/password ready to be used by any cryptographically secure encryption algorithms (such as [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)).

The limited resources of IoT devices, the reproducibility of the obtained results and the key randomness aspects were taken into consideration during the process of development of the framework.

## NOTE

This README file still in a "work in progress" state, so expect to see some TODO's

## Motivation

Given the number of IoT devices already deployed worldwide, the wide range of possibilities related to the LoRa and LoRaWAN technologies, the [key distribution](https://en.wikipedia.org/wiki/Key_distribution) problem and the lack of reproducibility of experiments related to key generation in IoT environments, this work proposes an open source framework that tries to address some of those issues.

As explained on other work [[Gao et al., 2019]](https://doi.org/10.3390/s19235122), [[Yang et al., 2017]](https://www.dit.uoi.gr/e-class/modules/document/file.php/193/LPWAN/LPWAN%20Security%20Options/Thesis_Xueying%20%281%29.pdf), [[Yang et al., 2018]](https://doi.org/10.1109/IoTDI.2018.00022), sending such an important request (as the Join Request is) in plain text can be considered a security vulnerability because it opens up the possibility of a wide range of attacks to be performed. To avoid situations like this and to help developing another solution to key generation based on RSSI measurements and PHY techniques, an open source validation framework was deployed.

## File structure

On the root of the repository, goes all the files required to run the framework (more details in the subsection below)

The `modules` folder contains all the external modules used by the framework, they should be recursively cloned together with this repository or could be obtained separately later on

The `dataset-files` folder should contain the data set source files which will be used as input in the framework

The `results` folder contains all the intermediate files generated by each step of the framework. Each step creates its own folder to keep everything more clear and easy to find

[TODO] Explain the other sub-folders

### File naming pattern

Each file has the step name which it belongs to appended as a prefix of the file name

[TODO] Expand on the naming pattern

## RSSignal workflow

[TODO] Insert an image that relates the files to each framework step

## Using this project

Please, make sure your environment meets the requirements below if you want to run the framework.

### Requirements

\- An UNIX-like platform

\- [GNU BASH](https://www.gnu.org/software/bash/) 5.1.16 or above or other [Unix shell](https://en.wikipedia.org/wiki/Unix_shell) interpreter

\- Python 3.10.2 or above

\- [Numpy](https://github.com/numpy/numpy) 1.22.2 or above

\- [Reed-Solomon Codec](https://github.com/tomerfiliba/reedsolomon) 1.5.4

\- [OpenSSL](https://www.openssl.org/) 1.1.1n or 3.0 or above

### Installing the framework

#### 1- Clone the source code using:

<code>git clone --recursive https://github.com/oliveiraleo/RSSignal-LoRa.git</code>

**Note:** The option ```--recursive``` will clone our code + all the modules required

#### 2- Enter the project folder

<code>cd RSSignal-Lora</code>

#### 3- Load the virtual environment

```source pyvenv/bin/activate```

#### 4- Run the automated script

```python main_controller.py OPTION```

Where OPTION is the step of the script automation. Please refer to the list below.

### Automated script reference list

- s1: Packet exchange, RSSI data collection* [RSSignal 1st step]
- s2: Preprocess the input [RSSignal 2nd step]
- s3: Quantization [RSSignal 3rd step]
- s4: Index exchange (calculates the indexes to be discarded) [RSSignal 4th step]
- s5: Index exchange (erases the indexes discarded) [RSSignal 4th step]
- s6: Key reconciliation (encodes the data and generates the ecc bits) [RSSignal 5th step]
- s7: Key reconciliation (reconciliates the data and ecc bits) [RSSignal 5th step]
- s8: Privacy amplification [RSSignal 6th step]
- auto-mode: TODO
- key-eval: TODO
- auto-key-eval: TODO
- hash-benchmark: TODO

\* Currently *not* implemented, please refer [to the FAQ](https://github.com/oliveiraleo/RSSignal-LoRa#q2-why-didnt-you-implement-the-frameworks-1st-step-probing). For an example on how it would be, please refer to that [other project](https://github.com/oliveiraleo/LoRaRSSIGrabber).

## FAQ

Some frequently asked questions and their answers

### Q1: Where are the "step 2" files?

A: We didn't focus on any step that involved the real world environment implementation because, as stated in our work, RSSI is available in a range of wireless technologies (e.g. WiFi, ZigBee, LoRa, etc) and each one has its own standards which affects how the implementation would be done.

### Q2: Why didn't you implement the framework's 1st step (Probing)?

A: The same as the question above.

### Q3: Why so many different files? Wouldn't it be better to keep everything together and avoid some overhead?

A: Yes, it might would. However, we tried to be as didactic and modular as possible, then we tried to reduce the dependability between the modules so they can be more easily swapped.

### Q4: Why did you choose Reed Solomon instead of X?

A: As mentioned on the work by [[DaCruz et al., 2022]](https://doi.org/10.1016/j.phycom.2021.101480), for certain applications, maybe a convolutional approach might fit better, but for our project we thought that the RS codec suffices the requirements and still is as easy to understand.

### Q5: What modifications did you make to the Reed Solomon (RS) codec code?

A: We didn't change any of it's internal functionality. The code uploaded here is based on the commit [32ff14c](https://github.com/stevenang/randomness_testsuite/tree/32ff14ce65da3090a57401069a4d2e65673f658b). As it can be verified on our source code, the only modifications we have made are: (i) message related (i.e. suppressing some console messages); (ii) disabled auto input (e.g. the original code had a randomly generated input and now we use our own); and (iii) disabled some tests (some tests require very long inputs to be statistically meaningful, so we choose the tests according to the framework needs).

### Q6: Why the RS codec does not work for me?

A: Please, note that the total number of RSSI measurements obtained from both sides should be equal. If they are different (or for some reason they were modified during the pre processing step), chances are that the RS codec will fail to correct the bits.

## Citing this work

Please, cite this work as:

de Oliveira, L., Chaves, L., & Silva, E. (2022). RSSignal: um Arcabouço para Evolução de Técnicas de Geração de Chaves Baseadas em RSSI. *In Anais do XXII Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais*, (pp. 111-124). Porto Alegre: SBC. doi:10.5753/sbseg.2022.225333

Or use the BibTex code below:

```
@inproceedings{sbseg,
 author = {Leonardo de Oliveira and Luciano Chaves and Edelberto Silva},
 title = {RSSignal: um Arcabouço para Evolução de Técnicas de Geração de Chaves Baseadas em RSSI},
 booktitle = {Anais do XXII Simpósio Brasileiro em Segurança da Informação e de Sistemas Computacionais},
 location = {Santa Maria},
 country = Brazil,
 year = {2022},
 pages = {111--124},
 publisher = {SBC},
 address = {Porto Alegre, RS, Brasil},
 doi = {10.5753/sbseg.2022.225333},
 url = {https://sol.sbc.org.br/index.php/sbseg/article/view/21662}
}
```
For direct access, please link the DOI:

DOI: [https://doi.org/10.5753/sbseg.2022.225333](https://doi.org/10.5753/sbseg.2022.225333)

## Acknowledgments

The authors would like to acknowledge Mr. Pedro Ivo da Cruz for all the knowledge shared and Mr. Rodrigo Oliveira Silva for the technical advice given during the development of the framework

We would like to thank the [Federal University of Juiz de Fora](https://ufjf.br), [FAPEMIG](https://fapemig.br/) and [FAPESP](https://fapesp.br/) for financially supporting this work

We would like to thank also Mr. Marek Simka and Mr. Ladislav Polak for releasing their LoRa RSSI data set (available on [GitHub](https://github.com/xsimka/LoRa-Localization)) which was used for [their work](https://www.radioeng.cz/fulltexts/2022/22_01_0135_0143.pdf) entitled *On the RSSI-based Indoor Localization Employing LoRa in the 2.4 GHz ISM Band*

We would like to acknowledge Mr. [Steven Kho Ang](https://github.com/stevenang), Mr. [Tomer Filiba](https://github.com/tomerfiliba) and Mr. [Stephen Karl Larroque](https://github.com/lrq3000) for their open source work (NIST test suite and RS codec python implementations) that were incorporated as part of the framework

## Repo TODO

- [TODO] Upload (or link) the NIST 800-22 implementation used for the tests
- [TODO] Upload some test results
- [TODO] Write and upload the automation script
- [TODO] Finish up this README file 

**Note:** We can't provide an ETA for this list ATM. However we hope we can finish its activities ASAP

## License

The source code is licensed under the [MIT](https://opensource.org/licenses/MIT) license