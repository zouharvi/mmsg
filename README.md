# Multimodal Shannon's Game

> **Abstract:** The Shannon game has long been used as a thought experiment in linguistics and NLP, asking participants to guess the next letter in a sentence based on its preceding context. We extend the game by introducing an optional extra modality in the form of image information. To investigate the impact of multimodal information in this game, we use human participants and a language model (LM, GPT-2). We show that the addition of image information improves both self-reported confidence and accuracy for both humans and LM. Certain word classes, such as nouns and determiners, benefit more from the additional modality information. The priming effect in both humans and the LM becomes more apparent as the context size (extra modality information + sentence context) increases. These findings highlight the potential of multimodal information in improving language understanding and modeling. 

Visit [vilda.net/s/mmsg/](https://vilda.net/s/mmsg/?uid=demo) for a live demo using the uid `demo`.
For more information contact the authors.

## Sentence Preparation:

1. Download `captions_val2017.json` from [images.cocodataset.org/annotations/annotations_trainval2017.zip](http://images.cocodataset.org/annotations/annotations_trainval2017.zip)
2. `cd object_detection`
3. Run `pick_sentences.py`
4. Run `detect_imgs.py`
5. Run `generate_backed_queues.py`

## User interface

TODO

![image](https://github.com/zouharvi/mmsg/assets/7661193/ea2ff22a-4f8c-4574-b67c-009a85c49219)

## Analysis

TODO
