import logging
import time
from django.http import StreamingHttpResponse


logger = logging.getLogger('streaming_log_response_test')


def test(request):
    def long_function():
        logger.info('info!!!!!!!!!!!!!!!!!!!!!!!!!')
        logger.warning('log...')

        time.sleep(1)
        logger.warning('log2...')
        logger.warning('log3...')

        time.sleep(3)
        logger.warning('log4...')

        time.sleep(3)
        logger.warning('log5...')

        time.sleep(3)
        logger.warning('log6!')
    return StreamingHttpResponse(long_function, {'streaming_log_response_test': logging.INFO})


def test2(request):
    def long_function():
        logger.warning('gol...')

        time.sleep(1)
        logger.warning('gol2...')
        logger.warning('gol3...')

        time.sleep(3)
        logger.warning('gol4...')

        time.sleep(3)
        logger.warning('gol5...')

        time.sleep(3)
        logger.warning('gol6!')
    return StreamingLogHttpResponse(long_function, {'streaming_log_response_test': logging.INFO})
