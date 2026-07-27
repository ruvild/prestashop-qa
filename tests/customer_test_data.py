import pytest


class CustomerTestData:

    VALID_NAMES = [
        pytest.param("J", id="min_length"),
        pytest.param("J" * 255, id="max_length"),
        pytest.param("John-David", id="hyphen"),
        pytest.param("J.", id="period"),
        pytest.param("O'Connor", id="apostrophe"),
        pytest.param("John III", id="space"),
        pytest.param("Jöhn", id="diacritic"),
        pytest.param("john", id="all_lowercase"),
        pytest.param("JOHN", id="all_uppercase"),
        pytest.param(" John ", id="lead_trail_spaces"),
    ]

    INVALID_NAMES = [
        pytest.param("", id="empty"),
        pytest.param("J" * 256, id="too_long"),
        pytest.param("<John>", id="xss"),
        pytest.param("John'; DROP TABLE --", id="sql_injection"),
        pytest.param("John&status=admin", id="url_delimiters"),
        pytest.param("John123", id="numbers"),
        pytest.param("J.C.", id="two_periods"),
        pytest.param("   ", id="pure_whitespace"),
    ]

    VALID_EMAILS = [
        pytest.param("J@e.c", id="min_length"),
        pytest.param(
            "J" * 64 + "@" + ("e" * 62 + ".") * 2 + "x" * 59 + ".com", id="max_length"
        ),
        pytest.param("John123@example.com", id="numbers"),
        pytest.param("John-Connor@example.com", id="hyphen"),
        pytest.param("J.Connor@example.com", id="period"),
        pytest.param("J!#?-_Connor@example.com", id="special_symbol"),
    ]

    INVALID_EMAILS = [
        pytest.param("John @example.com", id="space"),
        pytest.param("John@@example.com", id="double_@_sign"),
        pytest.param("John..Connor@example.com", id="double_period"),
        pytest.param("<John@example.com>", id="xss"),
        pytest.param("John@example", id="no_domain_extension"),
        pytest.param("John@.com", id="no_domain"),
        pytest.param("@example.com", id="no_local"),
        pytest.param("", id="empty"),
        pytest.param(" John@example.com ", id="lead_and_trail_spaces"),
        pytest.param("john.example@com", id="trailing_period"),
        pytest.param("jöhn@example.com", id="diacritic"),
        pytest.param("anonymous@psgdpr.com", id="existing_user"),
    ]

    VALID_PASSWORDS = [
        pytest.param("John123!", id="min_length"),
        pytest.param("John123!" * 9, id="max_length"),
        pytest.param("John 123!", id="space"),
        # These should be treated as simple strings and pass
        pytest.param("<script>alert('xss')</script>", id="xss"),
        pytest.param("password' OR '1'='1", id="sql_injection"),
    ]

    INVALID_PASSWORDS = [
        pytest.param(
            "A" * 10,
            marks=pytest.mark.xfail(
                reason="BUG: API ignores password complexity/length rules enforced by UI",
            ),
            id="simple_repeating_letter",
        ),
        pytest.param(
            "K9#mX2!",
            marks=pytest.mark.xfail(
                reason="BUG: API ignores password complexity/length rules enforced by UI",
            ),
            id="short",
        ),
        pytest.param(
            "K9#mX2!v" * 9 + "a",
            id="long",
        ),
        pytest.param(
            "Pineapple1!",
            marks=pytest.mark.xfail(
                reason="BUG: API ignores password complexity/length rules enforced by UI",
            ),
            id="simple_dictionary_word",
        ),
        pytest.param(
            "         ",
            marks=pytest.mark.xfail(
                reason="BUG: API ignores password complexity/length rules enforced by UI",
            ),
            id="pure_whitespace",
        ),
        pytest.param("", id="empty"),
        pytest.param(" ", id="single_space"),
    ]

    VALID_GROUPS = [
        pytest.param([1], 1, id="single_group_1"),
        pytest.param([2], 2, id="single_group_2"),
        pytest.param([1, 2], 1, id="multiple_groups_default_1"),
        pytest.param([1, 3], 3, id="multiple_groups_default_3"),
        pytest.param([1, 2, 3], 2, id="all_groups_default_2"),
        pytest.param([1, 3, 1], 1, id="repeating_group"),
    ]

    INVALID_GROUPS = [
        pytest.param([], 1, id="no_groups"),
        pytest.param([1], None, id="no_def_group"),
        pytest.param([1, 3], 2, id="default_outside_of_group"),
        pytest.param(
            [999],
            999,
            marks=pytest.mark.xfail(
                reason="API allows non-existent group IDs (999), causing PHP warning in UI"
            ),
            id="non_existent_group",
        ),
    ]
