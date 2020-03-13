mkdir -p UD_English
( cd UD_English;
gdown https://drive.google.com/uc?id=1p89JamrkUHLZgJ9JI29w8f0-l-CphCDQ
gdown https://drive.google.com/uc?id=1iN2odNq2aorEP_xzkPALYMJqzAtjQIux
mv model256 model
mv model256.params model.params
)
