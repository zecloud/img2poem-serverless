import logging
import uuid
import azure.functions as func
import sys
import os
sys.path.append(os.path.dirname(__file__))
import nn_process
import time
import gc

def main(msg: func.QueueMessage,myblob: func.InputStream,outblob: func.Out[bytes]):
    datatowrite = myblob.read()
    filename=str(uuid.uuid4())
    path='./NewImgForPoem/img/'+filename+'.jpg'
    logging.info(path)
    with open(path,'wb+') as f:
        f.write(datatowrite)
    logging.info("file written")
    logging.info('Loading Extracting Feature Module...')
    extract_feature = nn_process.create('extract_feature')
    logging.info('Loading Generating Poem Module...')
    generate_poem = nn_process.create('generate_poem')
    logging.info('generating')
    img_feature = extract_feature(path)
    poemg=str(generate_poem(img_feature)[0].replace('\n', '\n') )
    outblob.set(poemg)
    del extract_feature
    del generate_poem
    gc.collect()
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
