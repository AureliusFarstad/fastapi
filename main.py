from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List

from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
from chinese_english_lookup import Dictionary

from itertools import chain
from json import dumps

ws_driver = CkipWordSegmenter(model="bert-base")
pos_driver = CkipPosTagger(model="bert-base")
ner_driver = CkipNerChunker(model="bert-base")

d = Dictionary()

app = FastAPI()

origins = [    
    "http://chinesehelp.me",    
    "https://chinesehelp.me",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    sentences: List[str]

def transform_dict_lookup(dict_entry):
    jsonable_object = []
    for entry in dict_entry.definition_entries: 
        jsonable_object.append({
            'pinyin': entry.pinyin,
            'definitions': entry.definitions
        })
    return jsonable_object

@app.post("/transform/")
async def segment_chinese(data: Data):
    # Word Segment and Part of Sentence
    ws  = ws_driver(data.sentences, use_delim=True)
    pos = pos_driver(data.sentences, use_delim=True)
    # Named Entity Recognition returns Token Objects
    ner = ner_driver(data.sentences, use_delim=True)

    # Pack together WS and POS
    assert len(ws) == len(pos)
    ws_flattened = chain(*ws)
    pos_flattened = list(chain(*pos))

    segments = []
    char_index = 0
    for segment in ws_flattened:
        dict_lookup = d.lookup(segment)
        if dict_lookup is not None:
            dict_lookup = transform_dict_lookup(dict_lookup)
        
        segment_tags = set()
        for char in segment:
            segment_tags.add(pos_flattened[char_index])
            char_index += 1
        
        seg = {
            'ws': segment, 
            'pos': list(segment_tags),
            'def': dict_lookup
        }
        segments.append(seg)

    return Response(
        dumps({
            "segments": segments, 
            "ner": ner
        }),
    )