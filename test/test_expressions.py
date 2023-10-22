from systemrdl import RDLCompiler

from unittest_utils import RDLSourceTestCase

import systemrdl.rdltypes as rdlt

#===============================================================================
class TestIntLiterals(RDLSourceTestCase):

    def test_verilog(self):
        with self.subTest("hex"):
            self.assertEqual((int, 0xcafebabe), self.eval_RDL_expr("(32'hcafebabe)"))
            self.assertEqual((int, 0x12345678), self.eval_RDL_expr("(32'h12_345__678)"))

        with self.subTest("dec"):
            self.assertEqual((int, 1234), self.eval_RDL_expr("(16'd1234)"))
            self.assertEqual((int, 987), self.eval_RDL_expr("(10'd9_8_7)"))

        with self.subTest("bin"):
            self.assertEqual((int, 0xb19), self.eval_RDL_expr("(12'b101100011001)"))
            self.assertEqual((int, 0x7A), self.eval_RDL_expr("(16'b0111_1010)"))

        with self.subTest("err"):
            self.assertRDLExprError("(16'h12345)", "Value of integer literal exceeds the specified width")
            self.assertRDLExprError("(0'h12345)", "Integer literal width must be greater than zero")


    def test_hex(self):
        self.assertEqual((int, 0xcafebabe), self.eval_RDL_expr("(0xcafebabe)"))
        self.assertEqual((int, 0x12345678), self.eval_RDL_expr("(0x12_345__678)"))


    def test_decimal(self):
        self.assertEqual((int, 1234), self.eval_RDL_expr("(1234)"))
        self.assertEqual((int, 987654), self.eval_RDL_expr("(987_654)"))

    def test_bool(self):
        self.assertEqual((bool, True), self.eval_RDL_expr("(true)"))
        self.assertEqual((bool, False), self.eval_RDL_expr("(false)"))

#===============================================================================
class TestStrLiteral(RDLSourceTestCase):
    def test_string(self):
        self.assertEqual((str, ''), self.eval_RDL_expr('""'))
        self.assertEqual((str, 'Hello World'), self.eval_RDL_expr('"Hello World"'))
        self.assertEqual((str, '"quotes" quotes!"'), self.eval_RDL_expr('"\\"quotes\\" quotes!\\""'))

#===============================================================================
class TestBuiltinLiteral(RDLSourceTestCase):
    def test_builtin(self):
        self.assertEqual((rdlt.AccessType, rdlt.AccessType.na), self.eval_RDL_expr('(na)'))
        self.assertEqual((rdlt.AddressingType, rdlt.AddressingType.fullalign), self.eval_RDL_expr('(fullalign)'))
        self.assertEqual((rdlt.OnReadType, rdlt.OnReadType.rclr), self.eval_RDL_expr('(rclr)'))
        self.assertEqual((rdlt.OnWriteType, rdlt.OnWriteType.woclr), self.eval_RDL_expr('(woclr)'))

#===============================================================================
class TestArrayLiteral(RDLSourceTestCase):
    def test_valid(self):
        self.assertEqual((rdlt.ArrayedType(None), []), self.eval_RDL_expr("('{})"))
        self.assertEqual((rdlt.ArrayedType(int), [1,2,3,4]), self.eval_RDL_expr("('{1,2,3,4})"))
        self.assertEqual((rdlt.ArrayedType(str), ["foo", "bar", "baz"]), self.eval_RDL_expr('(\'{"foo", "bar", "baz"})'))
        self.assertEqual(
            (rdlt.ArrayedType(rdlt.AccessType), [rdlt.AccessType.rw, rdlt.AccessType.na]),
            self.eval_RDL_expr("('{rw, na})")
        )

    def test_invalid(self):
        self.assertRDLExprError("('{rw, 1234})", "Elements of an array shall be the same type")

#===============================================================================
class TestConcatenate(RDLSourceTestCase):
    def test_int(self):
        self.assertEqual((int, 123), self.eval_RDL_expr("{123}"))
        self.assertEqual((int, 0xABCD), self.eval_RDL_expr("{8'hAB, 8'hCD}"))
        self.assertEqual((int, 0xAB0000000000000000), self.eval_RDL_expr("{8'hAB, 0}"))
        self.assertEqual((int, 0xFF), self.eval_RDL_expr("{1'b1, 7'h7F}"))
        self.assertEqual((int, 0xFF), self.eval_RDL_expr("{longint'(true), 7'h7F}"))

    def test_str(self):
        self.assertEqual((str, ''), self.eval_RDL_expr('{""}'))
        self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"foobar"}'))
        self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"foo","bar"}'))
        self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"fo","ob", "ar"}'))
        self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"foobar", ""}'))

    def test_err(self):
        self.assertRDLExprError('{woclr}', "Concatenation operator can only be used for integral or string types")
        self.assertRDLExprError('{"hi", 123}', "Elements of a concatenation shall be the same type")

    def test_interaction(self):
        with self.subTest('concatenate'):
            self.assertEqual((int, 0xABCDEF), self.eval_RDL_expr("{{4'hA, 8'hBC}, {8'hDE, 4'hF}}"))
            self.assertEqual((str, 'foobarabcdefgh'), self.eval_RDL_expr('{{"foo", "bar"}, {"abcd", "efgh"}}'))

        with self.subTest('replicate'):
            self.assertEqual((int, 0xABCABC), self.eval_RDL_expr("{{2{4'hA, 8'hBC}}, {0{8'hDE, 4'hF}}}"))
            self.assertEqual((str, 'foofoo'), self.eval_RDL_expr('{{2{"foo"}}, {0{"abcd"}}}'))

        with self.subTest('binary'):
            self.assertEqual((int, 0xF0C00D), self.eval_RDL_expr("{4'hF, 8'h0B + 1'b1, 2'b11 + 12'hA}"))

        with self.subTest('unary'):
            self.assertEqual((int, 0x25), self.eval_RDL_expr("{~2'b1, ~4'b1010}"))

        with self.subTest('relational'):
            self.assertEqual((int, 0x2), self.eval_RDL_expr("{30 > 20, 1 < 0}"))

        with self.subTest('reduction'):
            self.assertEqual((int, 0x2), self.eval_RDL_expr("{|8'hFF, &16'hFF}"))

        with self.subTest('boolean'):
            self.assertEqual((int, 0x2), self.eval_RDL_expr("{true && true, false && true}"))

        with self.subTest('shift/exp'):
            self.assertEqual((int, 0xAB04), self.eval_RDL_expr("{8'hAB, 8'h01 << 2}"))

        with self.subTest('ternary'):
            self.assertEqual((int, 0xAB0F), self.eval_RDL_expr("{8'hAB, false ? 8'h01 : 4'hF}"))
            self.assertEqual((int, 0xAB01), self.eval_RDL_expr("{8'hAB, true ? 8'h01 : 4'hF}"))

        with self.subTest('width_cast'):
            self.assertEqual((int, 0xABC), self.eval_RDL_expr("{8'hAB, (4)'(16'hC)}"))

        with self.subTest('int_cast'):
            self.assertEqual((int, 0x10000000000000000), self.eval_RDL_expr("{longint'(true), longint'(false)}"))

        with self.subTest('bit_cast'):
            self.assertEqual((int, 0x2), self.eval_RDL_expr("{bit'(true), bit'(false)}"))

        with self.subTest('bool_cast'):
            self.assertEqual((int, 0x3), self.eval_RDL_expr("{boolean'(16'hC), boolean'(16'hC)}"))


#===============================================================================
class TestReplicate(RDLSourceTestCase):
    def test_int(self):
        self.assertEqual((int, 0xFFF), self.eval_RDL_expr("{3{4'hF}}"))
        self.assertEqual((int, 0), self.eval_RDL_expr("{0{4'hF}}"))
        self.assertEqual((int, 0xAB), self.eval_RDL_expr("{4'hA, {0{4'hF}}, 4'hB}"))

    def test_str(self):
        self.assertEqual((str, "hihihi"), self.eval_RDL_expr('{3{"hi"}}'))
        self.assertEqual((str, ""), self.eval_RDL_expr('{3{""}}'))
        self.assertEqual((str, ""), self.eval_RDL_expr('{0{"hi"}}'))

    def test_err(self):
        self.assertRDLExprError('{"hi"{"hi"}}', "Replication count operand of replication expression is not a compatible numeric type")

    def test_interaction(self):
        with self.subTest('concatenate'):
            self.assertEqual((int, 0xABCABC), self.eval_RDL_expr("{2{4'hA, 8'hBC}}"))
            self.assertEqual((int, 0xABCABC), self.eval_RDL_expr("{{1'b1, 1'b0}{4'hA, 8'hBC}}"))
            self.assertEqual((str, 'foobarfoobar'), self.eval_RDL_expr('{2{"foo", "bar"}}'))

        with self.subTest('replicate'):
            self.assertEqual((int, 0xABCABCABCABC), self.eval_RDL_expr("{2{{2{4'hA, 8'hBC}}}}"))
            self.assertEqual((int, 0xABCABCABC), self.eval_RDL_expr("{{2{1'b1}}{4'hA, 8'hBC}}"))
            self.assertEqual((str, 'foofoofoofoo'), self.eval_RDL_expr('{2{{2{"foo"}}}}'))

        with self.subTest('binary'):
            self.assertEqual((int, 0x092), self.eval_RDL_expr("{3{2'b1 + 3'b1}}"))

        with self.subTest('unary'):
            self.assertEqual((int, 0x2A), self.eval_RDL_expr("{3{~2'b1}}"))

        with self.subTest('relational'):
            self.assertEqual((int, 0x7), self.eval_RDL_expr("{3{30 > 20}}"))

        with self.subTest('reduction'):
            self.assertEqual((int, 0x7), self.eval_RDL_expr("{3{|16'h1}}"))

        with self.subTest('boolean'):
            self.assertEqual((int, 0x7), self.eval_RDL_expr("{3{true && true}}"))

        with self.subTest('shift/exp'):
            self.assertEqual((int, 0x040404), self.eval_RDL_expr("{3{8'h01 << 2}}"))

        with self.subTest('ternary'):
            self.assertEqual((int, 0x0F0F0F), self.eval_RDL_expr("{3{false ? 8'h01 : 4'hF}}"))
            self.assertEqual((int, 0x010101), self.eval_RDL_expr("{3{true ? 8'h01 : 4'hF}}"))

        with self.subTest('width_cast'):
            self.assertEqual((int, 0xCCC), self.eval_RDL_expr("{3{(4)'(16'hC)}}"))

        with self.subTest('bool_cast'):
            self.assertEqual((int, 0x7), self.eval_RDL_expr("{3{boolean'(16'hC)}}"))

#===============================================================================
class TestBinaryOperators(RDLSourceTestCase):
    #   +  -  *  /  %  &  |  ^  ^~  ~^
    def test_basic(self):
        self.assertEqual((int, 32), self.eval_RDL_expr("24 + 8"))
        self.assertEqual((int, 16), self.eval_RDL_expr("24 - 8"))
        self.assertEqual((int, 192), self.eval_RDL_expr("24 * 8"))
        self.assertEqual((int, 3), self.eval_RDL_expr("24 / 8"))
        self.assertEqual((int, 4), self.eval_RDL_expr("24 / 5"))
        self.assertEqual((int, 1), self.eval_RDL_expr("10 % 3"))
        self.assertEqual((int, 0x02), self.eval_RDL_expr("0x12 & 0x23"))
        self.assertEqual((int, 0x33), self.eval_RDL_expr("0x12 | 0x23"))
        self.assertEqual((int, 0x31), self.eval_RDL_expr("0x12 ^ 0x23"))
        self.assertEqual((int, 0xCE), self.eval_RDL_expr("8'h12 ~^ 8'h23"))
        self.assertEqual((int, 0xCE), self.eval_RDL_expr("8'h12 ^~ 8'h23"))

    def test_overflow(self):
        self.assertEqual((int, 1), self.eval_RDL_expr("8'hF0 + 5'h11"))
        self.assertEqual((int, 1), self.eval_RDL_expr("0xFFFFFFFFFFFFFFF0 + 0x11"))
        self.assertEqual((int, 1), self.eval_RDL_expr("68'hFFFFFFFFFFFFFFFF0 + 5'h11"))

    def test_err(self):
        self.assertRDLExprError('10 + "hi"', "Right operand of expression is not a compatible numeric type")
        self.assertRDLExprError('"hi" + 10', "Left operand of expression is not a compatible numeric type")
        self.assertRDLExprError('"hi" + "hi"', r"\w+ operand of expression is not a compatible numeric type")
        self.assertRDLExprError('100 / 0', "Division by zero")
        self.assertRDLExprError('100 % 0', "Modulo by zero")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestUnaryOperators(RDLSourceTestCase):
    #   +  -  ~
    def test_basic(self):
        self.assertEqual((int, 0xA3), self.eval_RDL_expr("+8'hA3"))
        self.assertEqual((int, 0x5D), self.eval_RDL_expr("-8'hA3"))
        self.assertEqual((int, 0x5C), self.eval_RDL_expr("~8'hA3"))
        self.assertEqual((int, 0), self.eval_RDL_expr("~true"))
        self.assertEqual((int, 1), self.eval_RDL_expr("~false"))

    def test_err(self):
        self.assertRDLExprError('~"hi"', "Operand of expression is not a compatible numeric type")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestRelationalOperators(RDLSourceTestCase):
    #   == != < > <= >=
    def test_int(self):
        self.assertEqual((bool, True), self.eval_RDL_expr("123 == 123"))
        self.assertEqual((bool, False), self.eval_RDL_expr("120 == 123"))
        self.assertEqual((bool, False), self.eval_RDL_expr("123 != 123"))
        self.assertEqual((bool, True), self.eval_RDL_expr("120 != 123"))
        self.assertEqual((bool, True), self.eval_RDL_expr("120 < 123"))
        self.assertEqual((bool, False), self.eval_RDL_expr("123 < 120"))
        self.assertEqual((bool, False), self.eval_RDL_expr("120 > 123"))
        self.assertEqual((bool, True), self.eval_RDL_expr("123 > 120"))
        self.assertEqual((bool, False), self.eval_RDL_expr("120 >= 123"))
        self.assertEqual((bool, True), self.eval_RDL_expr("123 >= 123"))
        self.assertEqual((bool, True), self.eval_RDL_expr("123 >= 120"))
        self.assertEqual((bool, False), self.eval_RDL_expr("123 <= 120"))
        self.assertEqual((bool, True), self.eval_RDL_expr("123 <= 123"))
        self.assertEqual((bool, True), self.eval_RDL_expr("120 <= 123"))

    def test_str(self):
        self.assertEqual((bool, False), self.eval_RDL_expr('"hi" == "ho"'))
        self.assertEqual((bool, True), self.eval_RDL_expr('"hi" == "hi"'))
        self.assertEqual((bool, True), self.eval_RDL_expr('"hi" != "ho"'))
        self.assertEqual((bool, False), self.eval_RDL_expr('"hi" != "hi"'))

    def test_array(self):
        self.assertEqual((bool, True), self.eval_RDL_expr("'{} == '{}'"))
        self.assertEqual((bool, False), self.eval_RDL_expr("'{1,2,3} == '{1,2}'"))
        self.assertEqual((bool, True), self.eval_RDL_expr("'{1,2,3} == '{1,2,3}'"))
        self.assertEqual((bool, True), self.eval_RDL_expr("'{1,2,3} != '{1,2}'"))
        self.assertEqual((bool, False), self.eval_RDL_expr("'{1,2,3} != '{1,2,3}'"))

    def test_err(self):
        self.assertRDLExprError('10 > "hi"', "Right operand of expression is not a compatible numeric type")
        self.assertRDLExprError('"hi" > 10', "Left operand of expression is not a compatible numeric type")
        self.assertRDLExprError('10 == "hi"', "Left and right operands of expression are not compatible types")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestReductionOperators(RDLSourceTestCase):
    #   &  ~&  |  ~|  ^  ^~  !
    def test_basic(self):
        self.assertEqual((int, 0), self.eval_RDL_expr("&8'hF0"))
        self.assertEqual((int, 1), self.eval_RDL_expr("&4'h0F"))
        self.assertEqual((int, 1), self.eval_RDL_expr("~&8'hF0"))
        self.assertEqual((int, 0), self.eval_RDL_expr("~&4'h0F"))
        self.assertEqual((int, 0), self.eval_RDL_expr("|8'h00"))
        self.assertEqual((int, 1), self.eval_RDL_expr("|8'h10"))
        self.assertEqual((int, 1), self.eval_RDL_expr("~|8'h00"))
        self.assertEqual((int, 0), self.eval_RDL_expr("~|8'h10"))
        self.assertEqual((int, 0), self.eval_RDL_expr("^8'h12"))
        self.assertEqual((int, 1), self.eval_RDL_expr("^8'h13"))
        self.assertEqual((int, 1), self.eval_RDL_expr("~^8'h12"))
        self.assertEqual((int, 0), self.eval_RDL_expr("~^8'h13"))
        self.assertEqual((bool, False), self.eval_RDL_expr("!true"))
        self.assertEqual((bool, True), self.eval_RDL_expr("!false"))
        self.assertEqual((bool, False), self.eval_RDL_expr("!8'h10"))
        self.assertEqual((bool, False), self.eval_RDL_expr("!8'h01"))
        self.assertEqual((bool, True), self.eval_RDL_expr("!8'h00"))


    def test_err(self):
        self.assertRDLExprError('!"hi"', "Operand of expression is not a compatible numeric type")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestBooleanOperators(RDLSourceTestCase):
    #   && ||
    def test_basic(self):
        self.assertEqual((bool, False), self.eval_RDL_expr("0x0 && 0x0"))
        self.assertEqual((bool, False), self.eval_RDL_expr("0x0 && 0x0F"))
        self.assertEqual((bool, False), self.eval_RDL_expr("0x0F && 0x0"))
        self.assertEqual((bool, True), self.eval_RDL_expr("0xF0 && 0x0F"))
        self.assertEqual((bool, False), self.eval_RDL_expr("0x0 || 0x0"))
        self.assertEqual((bool, True), self.eval_RDL_expr("0x0 || 0x0F"))
        self.assertEqual((bool, True), self.eval_RDL_expr("0xF || 0x0"))
        self.assertEqual((bool, True), self.eval_RDL_expr("0xF || 0xF0"))


    def test_err(self):
        self.assertRDLExprError('10 && "hi"', "Right operand of expression is not a compatible boolean type")
        self.assertRDLExprError('"hi" && 10', "Left operand of expression is not a compatible boolean type")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestShiftExpOperators(RDLSourceTestCase):
    #   **  <<  >>
    def test_exp(self):
        self.assertEqual((int, 1), self.eval_RDL_expr("0 ** 0"))
        self.assertEqual((int, 1), self.eval_RDL_expr("100 ** 0"))
        self.assertEqual((int, 0), self.eval_RDL_expr("0 ** 100"))
        self.assertEqual((int, 100000), self.eval_RDL_expr("10 ** 5"))
        self.assertEqual((int, 1), self.eval_RDL_expr("-1 ** 0"))

        # Note: this intentionally evaluates to zero because in SystemRDL,
        # negative numbers are converted to unsigned 2's complement
        self.assertEqual((int, 0), self.eval_RDL_expr("0 ** -1"))

    def test_lshift(self):
        self.assertEqual((int, 0), self.eval_RDL_expr("0 << 0"))
        self.assertEqual((int, 0x123), self.eval_RDL_expr("0x123 << 0"))
        self.assertEqual((int, 0x1230), self.eval_RDL_expr("0x123 << 4"))
        self.assertEqual((int, 0xB0), self.eval_RDL_expr("8'hAB << 4"))


    def test_rshift(self):
        self.assertEqual((int, 0), self.eval_RDL_expr("0 >> 0"))
        self.assertEqual((int, 0x123), self.eval_RDL_expr("0x123 >> 0"))
        self.assertEqual((int, 0x12), self.eval_RDL_expr("0x123 >> 4"))
        self.assertEqual((int, 0xA), self.eval_RDL_expr("8'hAB >> 4"))


    def test_err(self):
        self.assertRDLExprError('10 ** "hi"', "Right operand of expression is not a compatible numeric type")
        self.assertRDLExprError('"hi" ** 10', "Left operand of expression is not a compatible numeric type")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestTernaryOperator(RDLSourceTestCase):
    #   i ? j : k
    def test_basic(self):
        self.assertEqual((int, 123), self.eval_RDL_expr("true ? 123 : 456"))
        self.assertEqual((int, 456), self.eval_RDL_expr("false ? 123 : 456"))
        self.assertEqual((int, 123), self.eval_RDL_expr("42 ? 123 : 456"))
        self.assertEqual((int, 456), self.eval_RDL_expr("0 ? 123 : 456"))
        self.assertEqual((int, 1), self.eval_RDL_expr("true ? true : false"))
        self.assertEqual((int, 0), self.eval_RDL_expr("false ? true : false"))
        self.assertEqual((rdlt.ArrayedType(str), ['foo','bar']), self.eval_RDL_expr('true ? \'{"foo", "bar"} : \'{"baz"}'))
        self.assertEqual((rdlt.ArrayedType(str), ['baz']), self.eval_RDL_expr('false ? \'{"foo", "bar"} : \'{"baz"}'))

    def test_right_associative(self):
        # A ? B : C ? D : E
        # Right assoc: A ? B : (C ? D : E)
        self.assertEqual((int, 0), self.eval_RDL_expr("1 ? 0 : 2 ? 3 : 4"))

        # A ? B : C ? D : E ? F : G
        # Right: A ? B : (C ? D : (E ? F : G))
        self.assertEqual((int, 3), self.eval_RDL_expr("0 ? 1 : 2 ? 3 : 4 ? 5 : 6"))

    def test_err(self):
        self.assertRDLExprError('"hey" ? 0 : 1234', "Conditional operand of expression is not a compatible boolean type")
        self.assertRDLExprError('true ? \'{"foo", "bar"} : 1234', "True/False results of ternary conditional are not compatible types")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestCast(RDLSourceTestCase):
    def test_width_cast(self):
        self.assertEqual((int, 0x0100), self.eval_RDL_expr("(16)'(8'hFF + 8'h1) + 8'h0)"))
        self.assertEqual((int, 0x000F), self.eval_RDL_expr("(4)'(8'hFF)"))
        self.assertEqual((int, 0x00FE), self.eval_RDL_expr("(8)'(-3 + 1)"))
        self.assertEqual((int, 0x00FE), self.eval_RDL_expr("(8)'(1 - 3)"))
        self.assertEqual((int, 0xABCD1234DEADBEEF), self.eval_RDL_expr("longint'(68'hF_ABCD1234_DEADBEEF)"))

    def test_bool_cast(self):
        self.assertEqual((bool, True), self.eval_RDL_expr("boolean'(0x10)"))
        self.assertEqual((bool, False), self.eval_RDL_expr("boolean'(0x0)"))

    def test_err(self):
        self.assertRDLExprError("(0)'(1 - 3)", "Cannot cast to width of zero")
        self.assertRDLExprError("(woclr)'(1 - 3)", "Width operand of cast expression is not a compatible numeric type")
        self.assertRDLExprError("(12)'(woclr)", "Value operand of cast expression cannot be cast to an integer")
        self.assertRDLExprError("boolean'(woclr)", "Value operand of cast expression cannot be cast to a boolean")

    def test_interaction(self):
        with self.subTest('concatenate'):
            pass # TODO

        with self.subTest('replicate'):
            pass # TODO

        with self.subTest('binary'):
            pass # TODO

        with self.subTest('unary'):
            pass # TODO

        with self.subTest('relational'):
            pass # TODO

        with self.subTest('reduction'):
            pass # TODO

        with self.subTest('boolean'):
            pass # TODO

        with self.subTest('shift/exp'):
            pass # TODO

        with self.subTest('ternary'):
            pass # TODO

        with self.subTest('width_cast'):
            pass # TODO

        with self.subTest('bool_cast'):
            pass # TODO

#===============================================================================
class TestAdvanced(RDLSourceTestCase):
    def test_width_propagation(self):
        self.assertEqual((int, 0x00FF), self.eval_RDL_expr("8'h00 - 1'h1"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("(8'h00 - 1'h1) + 16'h1"))
        self.assertEqual((int, 0x0100), self.eval_RDL_expr("(8'hFF) + 16'h1"))
        self.assertEqual((int, 0xFFFF), self.eval_RDL_expr("(8'h00 - 1'h1) + 16'h0"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("((8'h00 - 1'h1) - 8'hFF)"))
        self.assertEqual((int, 0xFF00), self.eval_RDL_expr("((8'h00- 1'h1) - 8'hFF) + 16'h0"))
        self.assertEqual((int, 0xFFFF), self.eval_RDL_expr("(~(~(8'h00 - 1'h1))) + 16'h0"))
        self.assertEqual((int, 0xFFFF), self.eval_RDL_expr("(~(8'h00)) + 16'h0"))
        self.assertEqual((int, 0xFF00), self.eval_RDL_expr("(~(8'hFF)) + 16'h0"))
        self.assertEqual((int, 0x0100), self.eval_RDL_expr("((8'hFF + 8'h1)) + 16'h0"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("8'hFF + 8'h1"))
        self.assertEqual((int, 0x0100), self.eval_RDL_expr("8'hFF + 16'h1"))
        self.assertEqual((int, 0x00FF), self.eval_RDL_expr("8'hFF + 16'h0"))
        self.assertEqual((int, 0x0100), self.eval_RDL_expr("((8'hFF + 8'h1) + 8'h0) + 16'h0"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("((8'hFF + 8'h1) + 8'h0) + 8'h0"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("(8'hFF + 8'h1) + 8'h0"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("((8'hFF + 8'h1)) + ((8'hFF + 8'h1))"))
        self.assertEqual((int, 0x0200), self.eval_RDL_expr("((8'hFF + 8'h1)) + ((8'hFF + 8'h1) + 16'b0)"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("1'b1 << 3"))
        self.assertEqual((int, 0x0008), self.eval_RDL_expr("(1'b1 << 3) + 8'b0"))
        self.assertEqual((int, 0x0000), self.eval_RDL_expr("(|(~(4'hF))) + 8'b0"))
        self.assertEqual((int, 0x00FF), self.eval_RDL_expr("(~(&(4'b1))) + 8'b0"))

    def test_error(self):
        with self.assertRaises(ValueError):
            rdlc = RDLCompiler()
            rdlc.eval("2abcd")
