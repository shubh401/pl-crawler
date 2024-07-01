from helper import serialize_object
from config import *

async def __dispatch(data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:9000/constrainterror", data=json.dumps(data, default=serialize_object)) as __response:
                pass
    except:
        logging.error(f""" Error while dispatching error data while testing for extension: {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
