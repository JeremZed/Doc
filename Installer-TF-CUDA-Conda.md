# Installation de TensorFlow 2.13 et les librairies CUDA dans un environnement Conda

## Installation de conda

Se rendre à l'adresse suivante : <https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent>
Ici j'ai opté pour la version Miniconda : <https://docs.anaconda.com/free/miniconda/>
Une fois la procédure d'installation réussie on passe à l'installation des bibliothèques CUDA.

    > conda --version
    conda 23.11.0

## Installation de CUDA Toolkit et de cuDNN

    > conda create -n workspace-tf python=3.10
    > conda activate workspace-tf
    > conda install -c conda-forge cudatoolkit=11.8 cudnn=8.8

Ne pas oublier d'initialiser la variable PATH.

    > mkdir -p $CONDA_PREFIX/etc/conda/activate.d
    > echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    > conda deactivate

## Installation de TensorRT via pip

    > conda activate workspace-tf

On vérifie que le chemin de la librairie est reconnu.

    > echo $LD_LIBRARY_PATH

Installation de la version 8.5.3.1 car : <https://github.com/tensorflow/tensorflow/blob/4dacf3f368eb7965e9b5c3bbdd5193986081c3b2/tensorflow/tools/pip_package/setup.py#L169-L181>:

    > python -m pip install tensorrt==8.5.3.1
    > TENSORRT_PATH=$(dirname $(python -c "import tensorrt;print(tensorrt.__file__)"))
    > echo $TENSORRT_PATH

Copier/Coller le chemin affiché dans la variable suivante :

    > export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<COLLER-ICI>
    > conda deactivate

## Installation de TensorFlow

    > conda activate workspace-tf
    > echo $LD_LIBRARY_PATH
    > python -m pip install tensorflow==2.13
    > python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU))"

## Fixer les messages NUMA

On checke les cartes graphiques NVIDIA:

    > lspci | grep -i nvidia

    23:00.0 VGA compatible controller: NVIDIA Corporation GP107 [GeForce GTX 1050 Ti] (rev a1)
    23:00.1 Audio device: NVIDIA Corporation GP107GL High Definition Audio Controller (rev a1)
    2d:00.0 VGA compatible controller: NVIDIA Corporation TU104 [GeForce RTX 2060] (rev a1)
    2d:00.1 Audio device: NVIDIA Corporation TU104 HD Audio Controller (rev a1)
    2d:00.2 USB controller: NVIDIA Corporation TU104 USB 3.1 Host Controller (rev a1)
    2d:00.3 Serial bus controller: NVIDIA Corporation TU104 USB Type-C UCSI Controller (rev a1)

On checke les bus pci des cartes connectées:

    > ls /sys/bus/pci/devices/

    0000:00:00.0  0000:00:03.1  0000:00:14.0  0000:00:18.5  0000:21:05.0  0000:27:00.0  0000:2d:00.1
    0000:00:00.2  0000:00:04.0  0000:00:14.3  0000:00:18.6  0000:21:08.0  0000:2a:00.0  0000:2d:00.2
    0000:00:01.0  0000:00:05.0  0000:00:18.0  0000:00:18.7  0000:21:09.0  0000:2a:00.1  0000:2d:00.3
    0000:00:01.1  0000:00:07.0  0000:00:18.1  0000:01:00.0  0000:21:0a.0  0000:2a:00.3  0000:2e:00.0
    0000:00:01.2  0000:00:07.1  0000:00:18.2  0000:20:00.0  0000:23:00.0  0000:2b:00.0  0000:2f:00.0
    0000:00:02.0  0000:00:08.0  0000:00:18.3  0000:21:01.0  0000:23:00.1  0000:2c:00.0  0000:2f:00.3
    0000:00:03.0  0000:00:08.1  0000:00:18.4  0000:21:04.0  0000:26:00.0  0000:2d:00.0  0000:2f:00.4

On regarde le contenu pour notre carte graphique GTX 1050 Ti alias 23:00:0 :

    > cat /sys/bus/pci/devices/0000\:23\:00.0/numa_node

    -1

A noter que 1 signifie aucune connexion, et 0 signifie connecté.
Nous allons donc connecter ce noeud numa.

    > sudo echo 0 | sudo tee -a /sys/bus/pci/devices/0000\:23\:00.0/numa_node
    > cat /sys/bus/pci/devices/0000\:23\:00.0/numa_node

    0

On relance la commande suivante :

    > python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU))"

On refait la même chose pour la seconde carte graphique RTX 2060 alias 2d:00:0

##  Tips

- Ajouter l'environnement de conda, et la branche de git dans le prompt du terminal :

On indique à conda de ne pas afficher lui même l'environnement activé.

    > conda config --set changeps1 False

On modifie le fichier .bashrc

    > nano ~/.bashrc

Une fois le fichier .bashrc en mode edition copier/coller le code suivant :

    # CONDA
    function parse_conda_env () {
        if [ ! -z "$CONDA_DEFAULT_ENV" ]
        then
            echo "($(basename "$CONDA_DEFAULT_ENV")) "
        fi
    }

    # GIT BRANCH
    function parse_git_branch () {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
    }

    # COLORS
    BLUE="\[\033[0;34m\]"
    RED="\[\033[0;31m\]"
    YELLOW="\[\033[0;33m\]"
    GREEN="\[\033[01;32m\]"
    CYAN="\[\033[0;36m\]"
    NO_COLOR="\[\033[0m\]"

    PROMPT_DIRTRIM=2
    PS1="$CYAN\$(parse_conda_env)$GREEN\u@\h$BLUE:\w $YELLOW\$(parse_git_branch)$NO_COLOR\$ ";

On refresh le fichier .bashrc

    > source ~/.bashrc
