Some tools that can be useful.

- `bun seed` will insert test data into the postgresql db.
  Setup:
-
    1. conda create -y -n audioma python==3.9 -c conda-forge
    2. conda activate audioma
    3. conda install -c conda-forge montreal-forced-aligner
    4. conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
    5. pip install -r requirements.txt
  6. Test  python afa_mfa.py ./generated/Category.SCIENCE_intro_FR_1734168282639.txt ./generated/Category.SCIENCE_intro_FR_1734168282639.wav FR ./generated/out.TextGrid .\generated\out.word.srt .\generated\out.srt
pip install --upgrade pip setuptools numpy lxml
