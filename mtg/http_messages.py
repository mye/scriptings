from hypothesis import strategies as st
from hypothesis.strategies import dictionaries, lists, text

# Strategy for HTTP methods
http_methods = st.sampled_from(
    ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
)

# Strategy for request targets (simplified example)
request_targets = text(
    min_size=1, alphabet=st.characters(whitelist_categories=("L", "N"))
)

# Strategy for HTTP versions
http_versions = st.sampled_from(["HTTP/1.1", "HTTP/2.0"])

# Strategy for headers (simplified)
headers = dictionaries(keys=text(min_size=1), values=text(min_size=1), min_size=1)

# Strategy for body content (simplified)
body = st.text()


def format_request(method, target, version, headers, body):
    s = (
        f"{method} {target} {version}\r\n"
        + "\r\n".join(f"{k}: {v}" for k, v in headers.items())
        + f"\r\n\r\n{body}"
    )
    return bytes(s, "utf-8")


# Combining everything into a request message strategy
http_request_strategy = st.builds(
    format_request,
    http_methods,
    request_targets,
    http_versions,
    headers,
    body,
)

# Example of generating a mock HTTP request
# print(http_request_strategy.example())
