"""

ls -1 *.py | entr -c python draftlog.p

"""

# %%
# %pip install hypothesis httptools
# %%
import asyncio

from httptools import HttpRequestParser  # type: ignore
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule

Q = asyncio.Queue()

## MARK: HTTP Events


class RequestEvents:
    def on_message_begin(self):
        print("on_message_begin")

    def on_url(self, url):
        print("on_url", url)

    def on_header(self, name, value):
        print("on_header", name, value)

    def on_headers_complete(self):
        print("on_headers_complete")

    def on_body(self, body):
        print("on_body", body)

    def on_message_complete(self):
        print("on_message_complete")

    def on_chunk_header(self):
        print("on_chunk_header")

    def on_chunk_complete(self):
        print("on_chunk_complete")

    def on_status(self, status):
        print("on_status", status)


# MARK: Parsing


def make_http_parser():
    http_callbacks = RequestEvents()
    p = HttpRequestParser(http_callbacks)
    return lambda data: p.feed_data(data)


async def handler(reader, writer):

    parse = make_http_parser()

    while data := await reader.read(100):
        # not reader.at_eof():
        parse(data)

    print("parsed")
    addr = writer.get_extra_info("peername")

    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
    await writer.drain()


# MARK: Request Handling

"""
Initially, the handler is in a listening state, ready to handle http parsing events
    - begin, url, header, headers_complete, body, message_complete
    - chunk_header, chunk_complete, status
    - HttpParserUpgrade

The server:
    - verifies the request's validity, checking the syntax and HTTP version compatibility
    - decodes the URI, mapping it to a resource
    - checks the resource's availability and access permissions
    - examines the request's Accept header to determine the client's preferred content types
        - select the most appropriate representation of the resource
        - considering content type, language, and encoding
    - generates the requested resource
    - packages the resource into an HTTP response message
    - examines the connection header
        - if keep-alive, the server start a timeout waiting for the next request from this connection
            - if the timeout expires, the server closes the connection
            - otherwise it processes the next request
        - otherwise, it closes the connection

"""

# MARK: Main


async def main(port=8080):
    server = await asyncio.start_server(handler, "127.0.0.1", port)
    async with server:
        await server.serve_forever()


# MARK: Testing


class TestDraftLog(RuleBasedStateMachine):
    from http_messages import http_request_strategy

    def __init__(self):
        super().__init__()
        self.parse = make_http_parser()

    @rule(http_message=http_request_strategy)
    def test(self, http_message):
        self.parse(http_message)


if __name__ == "__main__":
    import unittest

    TestDraftLog = TestDraftLog.TestCase
    unittest.main()
    # import argparse

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-t", "--test", action="store_true")
    # args = parser.parse_args()

    # if args.test:
    #     import unittest

    #     TestDraftLog = TestDraftLog.TestCase
    #     unittest.main()
    # else:
    #     asyncio.run(main())
