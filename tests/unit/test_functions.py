from datetime import UTC, datetime, time, timedelta
from typing import Any, Literal

import orjson
import pytest

from tracecat.expressions.functions import (
    _bool,
    add,
    add_prefix,
    add_suffix,
    and_,
    b64_to_str,
    b64url_to_str,
    capitalize,
    cast,
    check_ip_version,
    create_days,
    create_hours,
    create_minutes,
    create_range,
    create_seconds,
    create_weeks,
    days_between,
    deserialize_ndjson,
    dict_keys,
    dict_lookup,
    dict_values,
    div,
    endswith,
    flatten,
    format_datetime,
    format_string,
    from_timestamp,
    generate_uuid,
    get_day,
    get_day_of_week,
    get_hour,
    get_minute,
    get_month,
    get_second,
    get_year,
    greater_than,
    greater_than_or_equal,
    hours_between,
    index_by_key,
    ipv4_in_subnet,
    ipv4_is_public,
    ipv6_in_subnet,
    ipv6_is_public,
    is_empty,
    is_equal,
    is_in,
    is_null,
    is_working_hours,
    iter_product,
    less_than,
    less_than_or_equal,
    lowercase,
    map_dict_keys,
    mappable,
    merge_dicts,
    minutes_between,
    mod,
    mul,
    not_,
    not_empty,
    not_equal,
    not_in,
    not_null,
    or_,
    parse_datetime,
    parse_time,
    pow,
    prettify_json,
    regex_extract,
    regex_match,
    regex_not_match,
    seconds_between,
    serialize_json,
    set_timezone,
    slice_str,
    split,
    startswith,
    str_to_b64,
    str_to_b64url,
    strip,
    sub,
    sum_,
    titleize,
    to_datetime,
    to_time,
    to_timestamp,
    unset_timezone,
    uppercase,
    url_decode,
    url_encode,
    weeks_between,
    zip_iterables,
)


@pytest.mark.parametrize(
    "input,prefix,expected",
    [
        ("test", "prefix", "prefixtest"),
        (["hello", "world"], "prefix", ["prefixhello", "prefixworld"]),
    ],
)
def test_add_prefix(
    input: str | list[str], prefix: str, expected: str | list[str]
) -> None:
    assert add_prefix(input, prefix) == expected


@pytest.mark.parametrize(
    "input,suffix,expected",
    [
        ("test", "suffix", "testsuffix"),
        (["hello", "world"], "suffix", ["hellosuffix", "worldsuffix"]),
    ],
)
def test_add_suffix(
    input: str | list[str], suffix: str, expected: str | list[str]
) -> None:
    assert add_suffix(input, suffix) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ('{"key": "value"}\n{"key": "value"}\n', [{"key": "value"}, {"key": "value"}]),
        ('{"key": "value"}\n', [{"key": "value"}]),
        ('{"key": "value"}', [{"key": "value"}]),
        ('{"key": "value"}\n{"key": "value"}', [{"key": "value"}, {"key": "value"}]),
    ],
)
def test_deserialize_ndjson(input, expected):
    assert deserialize_ndjson(input) == expected


@pytest.mark.parametrize(
    "input_val,expected",
    [
        (True, True),
        (False, False),
        ("true", True),
        ("TRUE", True),
        ("1", True),
        ("false", False),
        ("FALSE", False),
        ("0", False),
        (1, True),
        (0, False),
        ([], False),
        ([1], True),
    ],
)
def test_bool(input_val: Any, expected: bool) -> None:
    assert _bool(input_val) == expected


@pytest.mark.parametrize(
    "template,values,expected",
    [
        ("Hello {}", ["World"], "Hello World"),
        ("{} {} {}", ["a", "b", "c"], "a b c"),
        ("Value: {:.2f}", [3.14159], "Value: 3.14"),
    ],
)
def test_format_string(template: str, values: list[Any], expected: str) -> None:
    assert format_string(template, *values) == expected


@pytest.mark.parametrize(
    "invalid_input,decode_func",
    [
        ("invalid base64", b64_to_str),
        ("invalid base64url", b64url_to_str),
    ],
)
def test_base64_invalid_input(invalid_input: str, decode_func) -> None:
    with pytest.raises(ValueError):
        decode_func(invalid_input)


@pytest.mark.parametrize(
    "input_val,timezone,expected",
    [
        (1609459200, "UTC", datetime(2021, 1, 1, 0, 0, tzinfo=UTC)),
        ("2021-01-01T00:00:00", None, datetime(2021, 1, 1, 0, 0)),
        ("2021-01-01T00:00:00+00:00", None, datetime(2021, 1, 1, 0, 0, tzinfo=UTC)),
        ("2021-01-01T00:00:00", "UTC", datetime(2021, 1, 1, 0, 0, tzinfo=UTC)),
        ("2021-01-01", None, datetime(2021, 1, 1, 0, 0)),
        (datetime(2021, 1, 1, 0, 0), None, datetime(2021, 1, 1, 0, 0)),
        ("2021-01-01T00:00:00Z", None, datetime(2021, 1, 1, 0, 0, tzinfo=UTC)),
        ("2021-01-01T00:00:00Z", "UTC", datetime(2021, 1, 1, 0, 0, tzinfo=UTC)),
    ],
)
def test_to_datetime(input_val: Any, timezone: str | None, expected: datetime) -> None:
    assert to_datetime(input_val, timezone) == expected


@pytest.mark.parametrize(
    "input",
    [
        # US mm/dd/yyyy format
        "1/1/2021",
        # ISO 8601 string with invalid date
        "2021-02-31T00:00:00",
    ],
)
def test_to_datetime_invalid_date_string(input: str) -> None:
    with pytest.raises(ValueError):
        to_datetime(input)


@pytest.mark.parametrize(
    "pattern,text,expected",
    [
        (r"\d+", "abc123def", "123"),
        (r"[a-z]+", "ABC123def", "def"),
        (r"test", "no match", None),
    ],
)
def test_regex_extract(pattern: str, text: str, expected: str | None) -> None:
    assert regex_extract(pattern, text) == expected


@pytest.mark.parametrize(
    "pattern,text,expected",
    [
        (r"^test", "test123", True),
        (r"^test", "123test", False),
        (r"\d+", "123", True),
        (r"[A-Z]+", "abc", False),
    ],
)
def test_regex_match(pattern: str, text: str, expected: bool) -> None:
    assert regex_match(pattern, text) == expected
    assert regex_not_match(pattern, text) == (not expected)


def test_generate_uuid() -> None:
    uuid1 = generate_uuid()
    uuid2 = generate_uuid()
    assert isinstance(uuid1, str)
    assert len(uuid1) == 36  # Standard UUID length
    assert uuid1 != uuid2  # Should generate unique values


@pytest.mark.parametrize(
    "ipv4,subnet,expected",
    [
        ("192.168.1.1", "192.168.1.0/24", True),
        ("192.168.1.1", "192.168.2.0/24", False),
        ("10.0.0.1", "10.0.0.0/8", True),
        ("172.16.0.1", "192.168.0.0/16", False),
    ],
)
def test_ipv4_in_subnet(ipv4: str, subnet: str, expected: bool) -> None:
    assert ipv4_in_subnet(ipv4, subnet) == expected


@pytest.mark.parametrize(
    "ipv6,subnet,expected",
    [
        ("2001:db8::1", "2001:db8::/32", True),
        ("2001:db8::1", "2001:db9::/32", False),
        ("fe80::1", "fe80::/10", True),
        ("2001:db8::1", "fe80::/10", False),
    ],
)
def test_ipv6_in_subnet(ipv6: str, subnet: str, expected: bool) -> None:
    assert ipv6_in_subnet(ipv6, subnet) == expected


@pytest.mark.parametrize(
    "ip,expected",
    [
        ("192.168.1.1", False),  # Private
        ("10.0.0.1", False),  # Private
        ("172.16.0.1", False),  # Private
        ("8.8.8.8", True),  # Public
        ("1.1.1.1", True),  # Public
    ],
)
def test_ipv4_is_public(ip: str, expected: bool) -> None:
    assert ipv4_is_public(ip) == expected


@pytest.mark.parametrize(
    "ip,expected",
    [
        ("fe80::1", False),  # Link-local
        ("fc00::1", False),  # Unique local
        ("2001:db8::1", False),  # Documentation prefix (not public)
        ("2606:4700:4700::1111", True),  # Public (Cloudflare DNS)
        ("2404:6800:4000::1", True),  # Public (Google)
    ],
)
def test_ipv6_is_public(ip: str, expected: bool) -> None:
    assert ipv6_is_public(ip) == expected


@pytest.mark.parametrize(
    "ip,expected",
    [
        # IPv4 addresses
        ("192.168.1.1", 4),
        ("10.0.0.1", 4),
        ("172.16.0.1", 4),
        ("8.8.8.8", 4),
        # IPv6 addresses
        ("2001:db8::1", 6),
        ("fe80::1", 6),
        ("2606:4700:4700::1111", 6),
        ("::1", 6),
    ],
)
def test_check_ip_version(ip: str, expected: int) -> None:
    assert check_ip_version(ip) == expected


@pytest.mark.parametrize(
    "func,a,b,expected",
    [
        (less_than, 1, 2, True),
        (less_than, 2, 2, False),
        (less_than, 3, 2, False),
        (less_than, "a", "b", True),
        (less_than, "b", "a", False),
        (less_than, 1.5, 2.5, True),
        (greater_than, 2, 1, True),
        (greater_than, 2, 2, False),
        (greater_than, 1, 2, False),
        (greater_than_or_equal, 2, 1, True),
        (greater_than_or_equal, 2, 2, True),
        (greater_than_or_equal, 1, 2, False),
        (less_than_or_equal, 1, 2, True),
        (less_than_or_equal, 2, 2, True),
        (less_than_or_equal, 3, 2, False),
    ],
)
def test_comparison_operations(func, a: Any, b: Any, expected: bool) -> None:
    assert func(a, b) == expected


@pytest.mark.parametrize(
    "func,value,expected",
    [
        (is_null, None, True),
        (is_null, "test", False),
        (not_null, None, False),
        (not_null, "test", True),
        (is_empty, "", True),
        (is_empty, [], True),
        (is_empty, {}, True),
        (is_empty, "test", False),
        (is_empty, [1], False),
        (not_empty, "", False),
        (not_empty, [], False),
        (not_empty, {}, False),
        (not_empty, "test", True),
        (not_empty, [1], True),
    ],
)
def test_null_and_empty_checks(func, value: Any, expected: bool) -> None:
    assert func(value) == expected


@pytest.mark.parametrize(
    "func,a,b,expected",
    [
        (is_equal, 1, 1, True),
        (is_equal, "test", "test", True),
        (is_equal, 1, 2, False),
        (not_equal, 1, 2, True),
        (not_equal, "test", "test", False),
    ],
)
def test_equality(func, a: Any, b: Any, expected: bool) -> None:
    assert func(a, b) == expected


@pytest.mark.parametrize(
    "func,a,b,expected",
    [
        (is_in, 2, [1, 2, 3], True),
        (is_in, "el", "hello", True),
        (is_in, 4, [1, 2, 3], False),
        (not_in, 4, [1, 2, 3], True),
        (not_in, "x", "hello", True),
        (not_in, 2, [1, 2, 3], False),
    ],
)
def test_is_in(func, a: Any, b: Any, expected: bool) -> None:
    assert func(a, b) == expected


@pytest.mark.parametrize(
    "func,input_str,expected",
    [
        (slice_str, ("hello", 1, 3), "ell"),
        (format_string, ("Hello {}", "World"), "Hello World"),
        (lowercase, "HELLO", "hello"),
        (uppercase, "hello", "HELLO"),
        (capitalize, "hello world", "Hello world"),
        (titleize, "hello world", "Hello World"),
        (strip, ("  hello  ", " "), "hello"),
    ],
)
def test_string_operations(func, input_str: str | tuple, expected: str) -> None:
    """Test string manipulation functions."""
    if func in (slice_str, format_string, strip):
        assert func(*input_str) == expected
    else:
        assert func(input_str) == expected


def test_split() -> None:
    assert split("a,b,c", ",") == ["a", "b", "c"]
    assert split("a b c", " ") == ["a", "b", "c"]  # default whitespace splitting
    assert split("a||b||c", "||") == ["a", "b", "c"]


def test_sum_() -> None:
    assert sum_([1, 2, 3]) == 6
    assert sum_([0.1, 0.2, 0.3]) == pytest.approx(0.6)
    assert sum_([]) == 0  # empty list


def test_mappable_decorator() -> None:
    # Test regular function call
    mapped_add = mappable(add)
    result = mapped_add(2, 3)
    assert result == 5

    # Test mapped function call with scalars
    result = mapped_add.map(2, 3)
    assert result == [5]

    # Test mapped function call with sequences
    result = mapped_add.map([1, 2, 3], [4, 5, 6])
    assert result == [5, 7, 9]

    # Test mapped function with mixed scalar and sequence
    result = mapped_add.map([1, 2, 3], 1)
    assert result == [2, 3, 4]


def test_cast_operations() -> None:
    assert cast("123", "int") == 123
    assert cast("123.45", "float") == 123.45
    assert cast("true", "bool") is True
    assert isinstance(cast("2023-01-01T00:00:00", "datetime"), datetime)


@pytest.mark.parametrize(
    "func,date_input,format,expected",
    [
        # Month tests
        (get_month, datetime(2024, 1, 1), "number", 1),
        (get_month, datetime(2024, 12, 1), "number", 12),
        (get_month, datetime(2024, 1, 1), "full", "January"),
        (get_month, datetime(2024, 12, 1), "full", "December"),
        (get_month, datetime(2024, 1, 1), "short", "Jan"),
        (get_month, datetime(2024, 12, 1), "short", "Dec"),
        # Day of week tests
        (get_day_of_week, datetime(2024, 3, 18), "number", 0),  # Monday
        (get_day_of_week, datetime(2024, 3, 24), "number", 6),  # Sunday
        (get_day_of_week, datetime(2024, 3, 18), "full", "Monday"),
        (get_day_of_week, datetime(2024, 3, 24), "full", "Sunday"),
        (get_day_of_week, datetime(2024, 3, 18), "short", "Mon"),
        (get_day_of_week, datetime(2024, 3, 24), "short", "Sun"),
    ],
)
def test_date_formatters(
    func, date_input: datetime, format: str, expected: int | str
) -> None:
    assert func(date_input, format) == expected


@pytest.mark.parametrize(
    "func,input_str,prefix_suffix,expected",
    [
        (startswith, "Hello World", "Hello", True),
        (startswith, "Hello World", "World", False),
        (endswith, "Hello World", "World", True),
        (endswith, "Hello World", "Hello", False),
        (startswith, "", "", True),
        (endswith, "", "", True),
        (startswith, "", "x", False),
        (endswith, "", "x", False),
    ],
)
def test_string_boundary_functions(
    func, input_str: str, prefix_suffix: str, expected: bool
) -> None:
    assert func(input_str, prefix_suffix) == expected


@pytest.mark.parametrize(
    "func,dt,expected",
    [
        (get_day, datetime(2024, 3, 1), 1),
        (get_day, datetime(2024, 3, 31), 31),
        (get_hour, datetime(2024, 3, 15, 23), 23),
        (get_minute, datetime(2024, 3, 15, 12, 59), 59),
        (get_second, datetime(2024, 3, 15, 12, 30, 45), 45),
        (get_year, datetime(2024, 3, 15), 2024),
    ],
)
def test_date_component_getters(func, dt: datetime, expected: int) -> None:
    """Test all date/time component getter functions."""
    assert func(dt) == expected


@pytest.mark.parametrize(
    "dt,format,expected",
    [
        (datetime(2024, 1, 1), "number", 1),
        (datetime(2024, 12, 1), "number", 12),
        (datetime(2024, 1, 1), "full", "January"),
        (datetime(2024, 12, 1), "full", "December"),
        (datetime(2024, 1, 1), "short", "Jan"),
        (datetime(2024, 12, 1), "short", "Dec"),
    ],
)
def test_get_month(
    dt: datetime, format: Literal["number", "full", "short"], expected: int | str
) -> None:
    assert get_month(dt, format) == expected


@pytest.mark.parametrize(
    "func,input_val,expected",
    [
        (create_days, 1, timedelta(days=1)),
        (create_days, 0.5, timedelta(hours=12)),
        (create_hours, 24, timedelta(days=1)),
        (create_hours, 1.5, timedelta(minutes=90)),
        (create_minutes, 60, timedelta(hours=1)),
        (create_minutes, 1.5, timedelta(seconds=90)),
        (create_seconds, 3600, timedelta(hours=1)),
        (create_seconds, 90, timedelta(seconds=90)),
        (create_weeks, 1, timedelta(weeks=1)),
        (create_weeks, 0.5, timedelta(days=3.5)),
    ],
)
def test_time_interval_creators(func, input_val: float, expected: timedelta) -> None:
    """Test all time interval creation functions."""
    assert func(input_val) == expected


@pytest.mark.parametrize(
    "func,start,end,expected",
    [
        (weeks_between, datetime(2024, 1, 1), datetime(2024, 1, 8), 1.0),
        (weeks_between, datetime(2024, 1, 1), datetime(2024, 1, 15), 2.0),
        (days_between, datetime(2024, 1, 1), datetime(2024, 1, 2), 1.0),
        (days_between, datetime(2024, 1, 1, 12), datetime(2024, 1, 2), 0.5),
        (hours_between, datetime(2024, 1, 1), datetime(2024, 1, 1, 6), 6.0),
        (minutes_between, datetime(2024, 1, 1), datetime(2024, 1, 1, 0, 30), 30.0),
        (seconds_between, datetime(2024, 1, 1), datetime(2024, 1, 1, 0, 0, 30), 30.0),
    ],
)
def test_time_between_calculations(
    func, start: datetime, end: datetime, expected: float
) -> None:
    assert func(start, end) == pytest.approx(expected)


@pytest.mark.parametrize(
    "func,input_dict,expected",
    [
        (dict_keys, {"a": 1, "b": 2, "c": 3}, {"a", "b", "c"}),
        (dict_values, {"a": 1, "b": 2, "c": 3}, {1, 2, 3}),
        (dict_keys, {}, set()),  # Empty dict
        (dict_values, {}, set()),  # Empty dict
    ],
)
def test_dict_operations(func, input_dict: dict, expected: set) -> None:
    assert set(func(input_dict)) == expected


@pytest.mark.parametrize(
    "func,a,b,expected",
    [
        (add, 2, 3, 5),
        (sub, 5, 3, 2),
        (mul, 4, 3, 12),
        (div, 6, 2, 3.0),
        (mod, 7, 3, 1),
        (pow, 2, 3, 8),
        # Edge cases
        (div, 5, 2, 2.5),
        (mod, 5, 2, 1),
        (pow, 3, 0, 1),
    ],
)
def test_math_operations(func, a: Any, b: Any, expected: Any) -> None:
    assert func(a, b) == expected


@pytest.mark.parametrize(
    "func,a,b,expected",
    [
        (and_, True, True, True),
        (and_, True, False, False),
        (or_, False, True, True),
        (or_, False, False, False),
        (not_, True, None, False),
        (not_, False, None, True),
    ],
)
def test_logical_operations(func, a: bool, b: Any, expected: bool) -> None:
    if b is None:
        assert func(a) == expected
    else:
        assert func(a, b) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ({"a": 1, "b": 2}, {"a": 1, "b": 2}),
        ([1, 2, 3], [1, 2, 3]),
        ("test", "test"),
        (123, 123),
    ],
)
def test_serialize_json(input_data: Any, expected: Any) -> None:
    result = serialize_json(input_data)
    assert orjson.loads(result) == expected


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ({"a": 1}, '{\n  "a": 1\n}'),
        ([1, 2], "[\n  1,\n  2\n]"),
        ("test", '"test"'),
    ],
)
def test_prettify_json(input_data: Any, expected: str) -> None:
    assert prettify_json(input_data) == expected


@pytest.mark.parametrize(
    "iterables,expected",
    [
        (([1, 2], [3, 4]), [(1, 3), (2, 4)]),
        (([1], [2, 3]), [(1, 2)]),
        (([], [1, 2]), []),
    ],
)
def test_zip_iterables(iterables: tuple[list, ...], expected: list[tuple]) -> None:
    assert zip_iterables(*iterables) == expected


@pytest.mark.parametrize(
    "iterables,expected",
    [
        (([1, 2], [3, 4]), [(1, 3), (1, 4), (2, 3), (2, 4)]),
        (([1], [2]), [(1, 2)]),
        (([], [1, 2]), []),
    ],
)
def test_iter_product(iterables: tuple[list, ...], expected: list[tuple]) -> None:
    assert iter_product(*iterables) == expected


@pytest.mark.parametrize(
    "dt,timezone,expected_range",
    [
        # America/New_York varies between UTC-5 (EST) and UTC-4 (EDT)
        (datetime(2024, 1, 1, tzinfo=UTC), "America/New_York", (-5, -4)),
        # UTC is always +0
        (datetime(2024, 1, 1, tzinfo=UTC), "UTC", (0, 0)),
        # Asia/Tokyo is always UTC+9
        (datetime(2024, 1, 1, tzinfo=UTC), "Asia/Tokyo", (9, 9)),
    ],
)
def test_set_timezone(
    dt: datetime, timezone: str, expected_range: tuple[int, int]
) -> None:
    """Test timezone conversion, accounting for possible DST variations."""
    result = set_timezone(dt, timezone)
    offset = result.utcoffset()
    assert offset is not None
    offset_hours = offset.total_seconds() / 3600
    min_offset, max_offset = expected_range
    assert min_offset <= offset_hours <= max_offset, (
        f"Offset {offset_hours} not in expected range [{min_offset}, {max_offset}]"
    )


@pytest.mark.parametrize(
    "dt",
    [
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 1),
    ],
)
def test_unset_timezone(dt: datetime) -> None:
    assert unset_timezone(dt) == dt.replace(tzinfo=None)


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("admin+tracecat1@gmail.com", "admin%2Btracecat1%40gmail.com"),
        ("admin+tracecat1-org@gmail.com", "admin%2Btracecat1-org%40gmail.com"),
    ],
)
def test_url_encode(input_str: str, expected: str) -> None:
    assert url_encode(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("admin%2Btracecat1%40gmail.com", "admin+tracecat1@gmail.com"),
        ("admin%2Btracecat1-org%40gmail.com", "admin+tracecat1-org@gmail.com"),
    ],
)
def test_url_decode(input_str: str, expected: str) -> None:
    assert url_decode(input_str) == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("Hello, World!", "SGVsbG8sIFdvcmxkIQ=="),
        ("", ""),
        ("Special chars: !@#$%^&*()", "U3BlY2lhbCBjaGFyczogIUAjJCVeJiooKQ=="),
    ],
)
def test_str_to_b64(input_str: str, expected: str) -> None:
    assert str_to_b64(input_str) == expected
    # Test URL-safe version
    url_result = str_to_b64url(input_str)
    assert b64url_to_str(url_result) == input_str


@pytest.mark.parametrize(
    "input_dict,key,expected",
    [
        ({"a": 1}, "a", 1),
        ({"a": None}, "a", None),
        ({}, "a", None),
        ({1: "one"}, 1, "one"),
        ({(1, 2): "tuple"}, (1, 2), "tuple"),
    ],
)
def test_dict_lookup(input_dict: dict, key: Any, expected: Any) -> None:
    assert dict_lookup(input_dict, key) == expected


@pytest.mark.parametrize(
    "input_list,field_key,value_key,expected",
    [
        # Basic case with value_key
        (
            [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "id",
            "name",
            {1: "Alice", 2: "Bob"},
        ),
        # Basic case without value_key
        (
            [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "id",
            None,
            {1: {"id": 1, "name": "Alice"}, 2: {"id": 2, "name": "Bob"}},
        ),
        # Empty list
        ([], "id", "name", {}),
        # Different key types
        (
            [{"num": 1.5, "val": "a"}, {"num": 2.5, "val": "b"}],
            "num",
            "val",
            {1.5: "a", 2.5: "b"},
        ),
        # Nested dictionaries
        (
            [{"key": "a", "data": {"x": 1}}, {"key": "b", "data": {"x": 2}}],
            "key",
            "data",
            {"a": {"x": 1}, "b": {"x": 2}},
        ),
    ],
)
def test_index_by_key(
    input_list: list[dict], field_key: str, value_key: str | None, expected: dict
) -> None:
    """Test indexing a list of dictionaries by a specified key."""
    assert index_by_key(input_list, field_key, value_key) == expected


@pytest.mark.parametrize(
    "input_dict,key_mapping,expected",
    [
        # Basic key mapping
        ({"a": 1, "b": 2}, {"a": "x", "b": "y"}, {"x": 1, "y": 2}),
        # Empty dictionary
        ({}, {}, {}),
        # All keys must be mapped
        ({"a": 1}, {"a": "x"}, {"x": 1}),
        # Different value types
        (
            {"a": [1, 2], "b": {"c": 3}},
            {"a": "x", "b": "y"},
            {"x": [1, 2], "y": {"c": 3}},
        ),
    ],
)
def test_map_dict_keys(input_dict: dict, key_mapping: dict, expected: dict) -> None:
    """Test mapping dictionary keys using a key mapping dictionary."""
    assert map_dict_keys(input_dict, key_mapping) == expected


def test_map_dict_keys_missing_key() -> None:
    """Test that map_dict_keys raises ValueError when key mapping is missing."""
    with pytest.raises(ValueError, match="Key 'missing' not found in keys mapping"):
        map_dict_keys({"missing": 1}, {"other": "x"})


@pytest.mark.parametrize(
    "dict_list,expected",
    [
        # Basic case
        ([{"a": 1}, {"b": 2}], {"a": 1, "b": 2}),
        # Empty dictionaries
        ([], {}),
        ([{}], {}),
        ([{}, {"a": 1}], {"a": 1}),
        ([{"a": 1}, {}], {"a": 1}),
        # Overlapping keys (last dict takes precedence)
        ([{"a": 1}, {"a": 2}], {"a": 2}),
        # Nested dictionaries
        ([{"a": {"x": 1}}, {"b": {"y": 2}}], {"a": {"x": 1}, "b": {"y": 2}}),
        # Mixed value types
        (
            [{"a": 1, "b": "str"}, {"c": [1, 2], "d": {"x": 1}}],
            {"a": 1, "b": "str", "c": [1, 2], "d": {"x": 1}},
        ),
        # More than two dictionaries
        ([{"a": 1}, {"b": 2}, {"c": 3}], {"a": 1, "b": 2, "c": 3}),
    ],
)
def test_merge_dicts(dict_list: list[dict], expected: dict) -> None:
    """Test merging a list of dictionaries."""
    assert merge_dicts(dict_list) == expected


@pytest.mark.parametrize(
    "input_iterables,expected",
    [
        # Basic flattening
        ([[1, 2], [3, 4]], [1, 2, 3, 4]),
        # Nested lists
        ([[1, [2, 3]], [4]], [1, 2, 3, 4]),
        # Empty cases
        ([], []),  # Empty list
        ([[]], []),  # List containing empty list
        # Different element types
        ([["a", "b"], ["c"]], ["a", "b", "c"]),  # String elements
        ([[1, 2], [], [3]], [1, 2, 3]),  # Some empty sublists
        # Preserve non-list types
        ([[{"a": 1}], [{"b": 2}]], [{"a": 1}, {"b": 2}]),  # Dict elements
        ([[(1, 2)], [(3, 4)]], [1, 2, 3, 4]),  # Tuples get flattened
        # Deep nesting
        ([[1, [2, [3, 4]]], [5]], [1, 2, 3, 4, 5]),
    ],
)
def test_flatten(input_iterables: list, expected: list) -> None:
    """Test flatten function with various input types and structures.
    The function recursively flattens all sequences (including tuples) into a single list.
    """
    assert flatten(input_iterables) == expected


@pytest.mark.parametrize(
    "start,end,step,expected",
    [
        (0, 5, 1, [0, 1, 2, 3, 4]),  # Basic range
        (1, 10, 2, [1, 3, 5, 7, 9]),  # Range with step
        (5, 0, -1, [5, 4, 3, 2, 1]),  # Descending range
        (0, 0, 1, []),  # Empty range
        (-5, 5, 2, [-5, -3, -1, 1, 3]),  # Range with negative start
        (10, 5, -2, [10, 8, 6]),  # Descending range with step
    ],
)
def test_create_range(start: int, end: int, step: int, expected: list[int]) -> None:
    """Test create_range function with various inputs.

    Tests:
    - Basic ascending range
    - Range with custom step size
    - Descending range
    - Empty range
    - Range with negative numbers
    - Descending range with custom step
    """
    result = create_range(start, end, step)
    assert list(result) == expected


@pytest.mark.parametrize(
    "input_val,unit,expected",
    [
        (
            1609459200,
            "s",
            datetime(2021, 1, 1, 0, 0, tzinfo=UTC),
        ),  # 2021-01-01 00:00:00
        (
            1609459200000,
            "ms",
            datetime(2021, 1, 1, 0, 0, tzinfo=UTC),
        ),  # Same time in milliseconds
        (
            1672531200,
            "s",
            datetime(2023, 1, 1, 0, 0, tzinfo=UTC),
        ),  # 2023-01-01 00:00:00
        (
            1672531200000,
            "ms",
            datetime(2023, 1, 1, 0, 0, tzinfo=UTC),
        ),  # Same time in milliseconds
    ],
)
def test_from_timestamp(input_val: int, unit: str, expected: datetime) -> None:
    assert from_timestamp(input_val, unit) == expected


@pytest.mark.parametrize(
    "input_val,unit,expected",
    [
        (
            datetime(2021, 1, 1, 0, 0, tzinfo=UTC),
            "s",
            1609459200,
        ),  # 2021-01-01 00:00:00
        (
            datetime(2021, 1, 1, 0, 0, tzinfo=UTC),
            "ms",
            1609459200000,
        ),  # Same time in milliseconds
        (
            datetime(2023, 1, 1, 0, 0, tzinfo=UTC),
            "s",
            1672531200,
        ),  # 2023-01-01 00:00:00
        (
            datetime(2023, 1, 1, 0, 0, tzinfo=UTC),
            "ms",
            1672531200000,
        ),  # Same time in milliseconds
        ("2021-01-01T00:00:00", "s", 1609459200),  # String input
        ("2023-01-01T00:00:00", "ms", 1672531200000),  # String input with ms
    ],
)
def test_to_timestamp(input_val: datetime | str, unit: str, expected: int) -> None:
    assert to_timestamp(input_val, unit) == expected


@pytest.mark.parametrize(
    "input_str,format_str,expected",
    [
        (
            "2021-01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S",
            datetime(2021, 1, 1, 0, 0, 0),
        ),
        (
            "01/01/2021 15:30",
            "%d/%m/%Y %H:%M",
            datetime(2021, 1, 1, 15, 30),
        ),
        (
            "2023-12-31",
            "%Y-%m-%d",
            datetime(2023, 12, 31),
        ),
    ],
)
def test_parse_datetime(input_str: str, format_str: str, expected: datetime) -> None:
    assert parse_datetime(input_str, format_str) == expected


@pytest.mark.parametrize(
    "input_val,format_str,expected",
    [
        (
            datetime(2021, 1, 1, 0, 0),
            "%Y-%m-%d %H:%M:%S",
            "2021-01-01 00:00:00",
        ),
        (
            datetime(2021, 1, 1, 15, 30),
            "%d/%m/%Y %H:%M",
            "01/01/2021 15:30",
        ),
        (
            "2021-01-01T00:00:00",  # String input
            "%Y-%m-%d",
            "2021-01-01",
        ),
        # With timezone
        (
            datetime(2021, 1, 1, 0, 0, tzinfo=UTC),
            "%Y-%m-%d %H:%M:%S",
            "2021-01-01 00:00:00",
        ),
        # With timezone in ISO 8601 datetime string
        (
            "2021-01-01T00:00:00+00:00",
            "%Y-%m-%d %H:%M:%S",
            "2021-01-01 00:00:00",
        ),
    ],
)
def test_format_datetime(
    input_val: datetime | str, format_str: str, expected: str
) -> None:
    assert format_datetime(input_val, format_str) == expected


@pytest.mark.parametrize(
    "test_time,start_time,end_time,include_weekends,timezone,expected",
    [
        # Normal working hours (9 AM - 5 PM)
        (
            datetime(2024, 3, 18, 12, 0),
            "09:00:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # Monday noon
        (
            datetime(2024, 3, 18, 8, 0),
            "09:00:00",
            "17:00:00",
            False,
            None,
            False,
        ),  # Monday before hours
        (
            datetime(2024, 3, 18, 18, 0),
            "09:00:00",
            "17:00:00",
            False,
            None,
            False,
        ),  # Monday after hours
        # Weekend cases
        (
            datetime(2024, 3, 23, 12, 0),
            "09:00:00",
            "17:00:00",
            False,
            None,
            False,
        ),  # Saturday - excluded
        (
            datetime(2024, 3, 23, 12, 0),
            "09:00:00",
            "17:00:00",
            True,
            None,
            True,
        ),  # Saturday - included
        (
            datetime(2024, 3, 24, 12, 0),
            "09:00:00",
            "17:00:00",
            False,
            None,
            False,
        ),  # Sunday - excluded
        (
            datetime(2024, 3, 24, 12, 0),
            "09:00:00",
            "17:00:00",
            True,
            None,
            True,
        ),  # Sunday - included
        # Edge cases
        (
            datetime(2024, 3, 18, 9, 0),
            "09:00:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # Exactly at start time
        (
            datetime(2024, 3, 18, 17, 0),
            "09:00:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # Exactly at end time
        # Overnight shift (10 PM - 6 AM)
        (
            datetime(2024, 3, 18, 23, 0),
            "22:00:00",
            "06:00:00",
            False,
            None,
            True,
        ),  # During overnight (11 PM)
        (
            datetime(2024, 3, 18, 4, 0),
            "22:00:00",
            "06:00:00",
            False,
            None,
            True,
        ),  # During overnight (4 AM)
        (
            datetime(2024, 3, 18, 12, 0),
            "22:00:00",
            "06:00:00",
            False,
            None,
            False,
        ),  # Outside overnight (noon)
        # String input without timezone
        (
            "2024-03-18T12:00:00",
            "09:00:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # String input during hours
        (
            "2024-03-18T08:00:00",
            "09:00:00",
            "17:00:00",
            False,
            None,
            False,
        ),  # String input before hours
        (
            "2024-03-18T18:00:00",
            "09:00:00",
            "17:00:00",
            False,
            None,
            False,
        ),  # String input after hours
        # String input with timezone in string
        (
            "2024-03-18T12:00:00Z",
            "09:00:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # String with UTC timezone
        (
            "2024-03-18T12:00:00+00:00",
            "09:00:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # String with explicit UTC offset
        (
            "2024-03-18T04:00:00-05:00",
            "09:00:00",
            "17:00:00",
            False,
            None,
            False,
        ),  # String with -5 offset (4am ET = 9am UTC)
        (
            "2024-03-18T10:00:00-05:00",
            "09:00:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # String with -5 offset (10am ET = 3pm UTC)
        # String input without timezone but with timezone parameter
        (
            "2024-03-18T12:00:00",
            "09:00:00",
            "17:00:00",
            False,
            "UTC",
            True,
        ),  # Noon UTC during hours
        (
            "2024-03-18T12:00:00",
            "09:00:00",
            "17:00:00",
            False,
            "America/New_York",
            False,
        ),  # Noon treated as EDT (8am EDT)
        (
            "2024-03-18T16:00:00",
            "09:00:00",
            "17:00:00",
            False,
            "America/New_York",
            True,
        ),  # 4pm treated as EDT (noon EDT)
        # Different timezones
        # 12 PM UTC = 8 AM EDT (outside working hours in US Eastern)
        (
            datetime(2024, 3, 18, 12, 0, tzinfo=UTC),
            "09:00:00",
            "17:00:00",
            False,
            "America/New_York",
            False,
        ),
        # 18 PM UTC = 2 PM EDT (during working hours in US Eastern)
        (
            datetime(2024, 3, 18, 18, 0, tzinfo=UTC),
            "09:00:00",
            "17:00:00",
            False,
            "America/New_York",
            True,
        ),
        # Weekend with timezone conversion
        (
            "2024-03-23T12:00:00",
            "09:00:00",
            "17:00:00",
            False,
            "UTC",
            False,
        ),  # Saturday UTC
        (
            "2024-03-22T23:00:00-05:00",
            "09:00:00",
            "17:00:00",
            False,
            "UTC",
            False,
        ),  # Friday 11pm ET = Saturday 4am UTC
        (
            "2024-03-22T23:00:00-05:00",
            "09:00:00",
            "17:00:00",
            True,
            "UTC",
            False,
        ),  # Outside of hours even with weekends
        # HH:MM format test cases
        (
            datetime(2024, 3, 18, 12, 0),
            "09:00",
            "17:00",
            False,
            None,
            True,
        ),  # Basic HH:MM format
        (
            datetime(2024, 3, 18, 8, 0),
            "09:00",
            "17:00",
            False,
            None,
            False,
        ),  # Before hours with HH:MM
        (
            datetime(2024, 3, 18, 18, 0),
            "09:00",
            "17:00",
            False,
            None,
            False,
        ),  # After hours with HH:MM
        # Mixed format test cases
        (
            datetime(2024, 3, 18, 12, 0),
            "09:00:00",
            "17:00",
            False,
            None,
            True,
        ),  # Mixed format HH:MM:SS and HH:MM
        (
            datetime(2024, 3, 18, 12, 0),
            "09:00",
            "17:00:00",
            False,
            None,
            True,
        ),  # Mixed format HH:MM and HH:MM:SS
        # Overnight with HH:MM format
        (
            datetime(2024, 3, 18, 23, 0),
            "22:00",
            "06:00",
            False,
            None,
            True,
        ),  # During overnight with HH:MM
        (
            datetime(2024, 3, 18, 4, 0),
            "22:00",
            "06:00",
            False,
            None,
            True,
        ),  # During overnight with HH:MM
        (
            datetime(2024, 3, 18, 12, 0),
            "22:00",
            "06:00",
            False,
            None,
            False,
        ),  # Outside overnight with HH:MM
    ],
)
def test_is_working_hours(
    test_time: datetime | str,
    start_time: str,
    end_time: str,
    include_weekends: bool,
    timezone: str | None,
    expected: bool,
) -> None:
    """Test is_working_hours with various scenarios including weekend handling and timezone conversion."""
    assert (
        is_working_hours(test_time, start_time, end_time, include_weekends, timezone)
        == expected
    )


@pytest.mark.parametrize(
    "time_str,expected",
    [
        # HH:MM:SS format
        ("12:34:56", time(12, 34, 56)),
        ("00:00:00", time(0, 0, 0)),
        ("23:59:59", time(23, 59, 59)),
        # HH:MM format
        ("12:34", time(12, 34, 0)),
        ("00:00", time(0, 0, 0)),
        ("23:59", time(23, 59, 0)),
    ],
)
def test_parse_time(time_str: str, expected: time) -> None:
    """Test that parse_time supports both HH:MM:SS and HH:MM formats."""
    assert parse_time(time_str) == expected


@pytest.mark.parametrize(
    "invalid_time_str",
    [
        "25:00:00",  # Hour out of range
        "12:60:00",  # Minute out of range
        "12:00:60",  # Second out of range
        "12.00.00",  # Invalid separators
        "12-00-00",  # Invalid separators
        "12:00",  # Invalid for HH:MM:SS format but valid for HH:MM format
        "12",  # Missing components
        "12:",  # Incomplete
        ":30:00",  # Missing hour
        "",  # Empty string
    ],
)
def test_parse_time_invalid_input(invalid_time_str: str) -> None:
    """Test that parse_time correctly handles invalid inputs."""
    # Some of these might pass with the enhanced format support, so we need to adapt the test
    if invalid_time_str == "12:00":
        # This should now be valid with the HH:MM format support
        assert parse_time(invalid_time_str) == time(12, 0, 0)
    else:
        # All other cases should still raise ValueError
        with pytest.raises(ValueError):
            parse_time(invalid_time_str)


@pytest.mark.parametrize(
    "input_val,expected",
    [
        # Datetime objects
        (datetime(2024, 3, 18, 12, 34, 56), time(12, 34, 56)),
        (datetime(2024, 3, 18, 0, 0, 0), time(0, 0, 0)),
        (datetime(2024, 3, 18, 23, 59, 59), time(23, 59, 59)),
        # Datetime strings in ISO format
        ("2024-03-18T12:34:56", time(12, 34, 56)),
        ("2024-03-18T00:00:00", time(0, 0, 0)),
        ("2024-03-18T23:59:59", time(23, 59, 59)),
        # Datetime strings with timezone information
        ("2024-03-18T12:34:56Z", time(12, 34, 56)),
        ("2024-03-18T12:34:56+00:00", time(12, 34, 56)),
        # Converting from UTC to local time is handled in to_datetime, to_time just extracts the time component
        # Edge cases
        (datetime(2024, 2, 29, 12, 34, 56), time(12, 34, 56)),  # Leap year
        (datetime(1970, 1, 1, 0, 0, 0), time(0, 0, 0)),  # Unix epoch
    ],
)
def test_to_time(input_val: datetime | str, expected: time) -> None:
    """Test that to_time correctly converts datetime objects and strings to time objects."""
    assert to_time(input_val) == expected


@pytest.mark.parametrize(
    "input_val,expected_error",
    [
        ("invalid", ValueError),  # Not a valid datetime string
        ("25:00:00", ValueError),  # Invalid time string (hours out of range)
        ("12:60:00", ValueError),  # Invalid time string (minutes out of range)
        ("12:00:60", ValueError),  # Invalid time string (seconds out of range)
        (123, AttributeError),  # Integer (not string or datetime)
        (None, AttributeError),  # None
    ],
)
def test_to_time_errors(input_val: Any, expected_error: type[Exception]) -> None:
    """Test that to_time raises appropriate errors for invalid inputs."""
    with pytest.raises(expected_error):
        to_time(input_val)
