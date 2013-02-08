"""
Unit tests for the lexer
"""
import pytest
from pypred import parser, ast

class TestAST(object):
    def ast(self, inp):
        lexer = parser.get_lexer()
        p = parser.get_parser(lexer=lexer)
        return p.parse(inp, lexer=lexer)

    def test_jack_and_jill(self):
        a = self.ast("name is Jack and friend_name is Jill")
        valid, info = a.validate()
        assert valid

    def test_bad_number(self):
        a = ast.Number("0..0")
        valid, info = a.validate()
        assert not valid
        assert "Failed to convert" in info["errors"][0]

    def test_bad_constant(self):
        a = ast.Constant(42)
        valid, info = a.validate()
        assert not valid
        assert "Invalid Constant" in info["errors"][0]

    def test_bad_regex_type(self):
        a = ast.Regex(42)
        valid, info = a.validate()
        assert not valid
        assert "Regex must be a string" in info["errors"][0]

    def test_bad_regex(self):
        a = ast.Regex("(abc")
        valid, info = a.validate()
        assert not valid
        assert "Regex compilation failed" in info["errors"][0]
        assert "(abc" in info["regex"]
        assert info["regex"]["(abc"] == "unbalanced parenthesis"

    def test_bad_regex_inp(self):
        a = self.ast("foo matches '(abc'")
        valid, info = a.validate()
        assert not valid
        assert "Regex compilation failed" in info["errors"][0]
        assert "(abc" in info["regex"]
        assert info["regex"]["(abc"] == "unbalanced parenthesis"

    def test_match_bad_arg(self):
        a = ast.MatchOperator(ast.Literal("foo"), ast.Literal("bar"))
        valid, info = a.validate()
        assert not valid
        assert "Match operator must take a regex" in info["errors"][0]

    def test_contains_bad(self):
        a = ast.ContainsOperator(ast.Literal("foo"), ast.Empty())
        valid, info = a.validate()
        assert not valid
        assert "Contains operator must take" in info["errors"][0]

    def test_contains_valid(self):
        a = ast.ContainsOperator(ast.Literal("foo"), ast.Literal("bar"))
        valid, info = a.validate()
        assert valid

    def test_bad_compare(self):
        a = ast.CompareOperator("!", ast.Literal("foo"), ast.Empty())
        valid, info = a.validate()
        assert not valid
        assert "Unknown compare" in info["errors"][0]

    def test_bad_logic(self):
        a = ast.LogicalOperator("!", ast.Literal("foo"), ast.Empty())
        valid, info = a.validate()
        assert not valid
        assert "Unknown logical" in info["errors"][0]

    def test_bad_child(self):
        c = ast.CompareOperator("!", ast.Literal("foo"), ast.Empty())
        a = ast.LogicalOperator("and", ast.Literal("foo"), c)
        valid, info = a.validate()
        assert not valid
        assert "Unknown compare" in info["errors"][0]
