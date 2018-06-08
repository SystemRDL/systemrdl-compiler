
from rdl_unittest import RDLSourceTestCase

import systemrdl.rdltypes as rdlt

#===============================================================================
class TestLiterals(RDLSourceTestCase):
    
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
        self.assertEqual((int, 1), self.eval_RDL_expr("(true)"))
        self.assertEqual((int, 0), self.eval_RDL_expr("(false)"))
    
    def test_string(self):
        self.assertEqual((str, ''), self.eval_RDL_expr('""'))
        self.assertEqual((str, 'Hello World'), self.eval_RDL_expr('"Hello World"'))
        self.assertEqual((str, '"quotes" quotes!"'), self.eval_RDL_expr('"\\"quotes\\" quotes!\\""'))
    
    
    def test_builtin(self):
        self.assertEqual((rdlt.AccessType, rdlt.AccessType.na), self.eval_RDL_expr('(na)'))
        self.assertEqual((rdlt.AddressingType, rdlt.AddressingType.fullalign), self.eval_RDL_expr('(fullalign)'))
        self.assertEqual((rdlt.OnReadType, rdlt.OnReadType.rclr), self.eval_RDL_expr('(rclr)'))
        self.assertEqual((rdlt.OnWriteType, rdlt.OnWriteType.woclr), self.eval_RDL_expr('(woclr)'))
    
    
    def test_array(self):
        with self.subTest("valid"):
            self.assertEqual((rdlt.ArrayPlaceholder(None), []), self.eval_RDL_expr("('{})"))
            self.assertEqual((rdlt.ArrayPlaceholder(int), [1,2,3,4]), self.eval_RDL_expr("('{1,2,3,4})"))
            self.assertEqual((rdlt.ArrayPlaceholder(str), ["foo", "bar", "baz"]), self.eval_RDL_expr('(\'{"foo", "bar", "baz"})'))
            self.assertEqual(
                (rdlt.ArrayPlaceholder(rdlt.AccessType), [rdlt.AccessType.rw, rdlt.AccessType.na]),
                self.eval_RDL_expr("('{rw, na})")
            )
        
        with self.subTest("err"):
            self.assertRDLExprError("('{rw, 1234})", "Elements of an array shall be the same type")
    
#===============================================================================
class TestListOperators(RDLSourceTestCase):
    def test_concatenate(self):
        with self.subTest("int"):
            self.assertEqual((int, 123), self.eval_RDL_expr("{123}"))
            self.assertEqual((int, 0xABCD), self.eval_RDL_expr("{8'hAB, 8'hCD}"))
            self.assertEqual((int, 0xAB0000000000000000), self.eval_RDL_expr("{8'hAB, 0}"))
            self.assertEqual((int, 0xFF), self.eval_RDL_expr("{1'b1, 7'h7F}"))
            self.assertEqual((int, 0xFF), self.eval_RDL_expr("{true, 7'h7F}"))
            self.assertEqual((int, 0xABCDEF), self.eval_RDL_expr("{{4'hA, 8'hBC}, {8'hDE, 4'hF}}"))
    
        with self.subTest("str"):
            self.assertEqual((str, ''), self.eval_RDL_expr('{""}'))
            self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"foobar"}'))
            self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"foo","bar"}'))
            self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"fo","ob", "ar"}'))
            self.assertEqual((str, 'foobar'), self.eval_RDL_expr('{"foobar", ""}'))

        with self.subTest("err"):
            self.assertRDLExprError('{woclr}', "Concatenation operator can only be used for integral or string types")
            self.assertRDLExprError('{"hi", 123}', "Elements of a concatenation shall be the same type")
    
    
    def test_replicate(self):
        with self.subTest("int"):
            self.assertEqual((int, 0xFFF), self.eval_RDL_expr("{3{4'hF}}"))
            self.assertEqual((int, 0), self.eval_RDL_expr("{0{4'hF}}"))
            self.assertEqual((int, 0xAB), self.eval_RDL_expr("{4'hA, {0{4'hF}}, 4'hB}"))
        
        with self.subTest("str"):
            self.assertEqual((str, "hihihi"), self.eval_RDL_expr('{3{"hi"}}'))
            self.assertEqual((str, ""), self.eval_RDL_expr('{3{""}}'))
            self.assertEqual((str, ""), self.eval_RDL_expr('{0{"hi"}}'))
        
        with self.subTest("err"):
            self.assertRDLExprError('{"hi"{"hi"}}', "Replication count operand of replication expression is not a compatible numeric type")
        
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
        self.assertEqual((rdlt.ArrayPlaceholder(str), ['foo','bar']), self.eval_RDL_expr('true ? \'{"foo", "bar"} : \'{"baz"}'))
        self.assertEqual((rdlt.ArrayPlaceholder(str), ['baz']), self.eval_RDL_expr('false ? \'{"foo", "bar"} : \'{"baz"}'))
    
    def test_err(self):
        self.assertRDLExprError('"hey" ? 0 : 1234', "Conditional operand of expression is not a compatible boolean type")
        self.assertRDLExprError('true ? \'{"foo", "bar"} : 1234', "True/False results of ternary conditional are not compatible types")
    
#===============================================================================
class TestCast(RDLSourceTestCase):
    def test_width_cast(self):
        self.assertEqual((int, 0x0100), self.eval_RDL_expr("(16)'(8'hFF + 8'h1) + 8'h0)"))
        self.assertEqual((int, 0x000F), self.eval_RDL_expr("(4)'(8'hFF)"))
        self.assertEqual((int, 0x00FE), self.eval_RDL_expr("(8)'(-3 + 1)"))
        self.assertEqual((int, 0x00FE), self.eval_RDL_expr("(8)'(1 - 3)"))
    
    def test_bool_cast(self):
        self.assertEqual((bool, True), self.eval_RDL_expr("boolean'(0x10)"))
        self.assertEqual((bool, False), self.eval_RDL_expr("boolean'(0x0)"))
    
    def test_err(self):
        self.assertRDLExprError("(0)'(1 - 3)", "Cannot cast to width of zero")
        self.assertRDLExprError("(woclr)'(1 - 3)", "Width operand of cast expression is not a compatible numeric type")
        self.assertRDLExprError("(12)'(woclr)", "Value operand of cast expression cannot be cast to an integer")
        self.assertRDLExprError("boolean'(woclr)", "Value operand of cast expression cannot be cast to a boolean")

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
    
    

