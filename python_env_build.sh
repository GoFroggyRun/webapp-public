echo 'installing with conda...'
conda create -n pb_env python=2.7.14 \
    taxcalc=0.17.0 \
    btax=0.2.2 \
    ogusa=0.5.8 \
    numba>=0.33.0 \
    pandas>=0.22.0 \
    bokeh=0.12.7 \
    nomkl \
    gevent \
    pillow \
    pyparsing \
    -c ospc \
    -c ospc/label/dev \
    -c conda-forge \

echo 'successfull created env: pb_env'
echo 'activating pb_env and pip installing remaining requirements'
source activate pb_env

pip install -r requirements.txt
pip install -r requirements_dev.txt
