
// Generated from SystemRDL.g4 by ANTLR 4.10.1


#include "SystemRDLVisitor.h"

#include "SystemRDLParser.h"


using namespace antlrcpp;

using namespace antlr4;

namespace {

struct SystemRDLParserStaticData final {
  SystemRDLParserStaticData(std::vector<std::string> ruleNames,
                        std::vector<std::string> literalNames,
                        std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  SystemRDLParserStaticData(const SystemRDLParserStaticData&) = delete;
  SystemRDLParserStaticData(SystemRDLParserStaticData&&) = delete;
  SystemRDLParserStaticData& operator=(const SystemRDLParserStaticData&) = delete;
  SystemRDLParserStaticData& operator=(SystemRDLParserStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

std::once_flag systemrdlParserOnceFlag;
SystemRDLParserStaticData *systemrdlParserStaticData = nullptr;

void systemrdlParserInitialize() {
  assert(systemrdlParserStaticData == nullptr);
  auto staticData = std::make_unique<SystemRDLParserStaticData>(
    std::vector<std::string>{
      "root", "root_elem", "component_def", "explicit_component_inst", "component_inst_alias", 
      "component_named_def", "component_anon_def", "component_body", "component_body_elem", 
      "component_insts", "component_inst", "field_inst_reset", "inst_addr_fixed", 
      "inst_addr_stride", "inst_addr_align", "component_inst_type", "component_type", 
      "component_type_primary", "param_def", "param_def_elem", "param_inst", 
      "param_assignment", "expr", "expr_primary", "concatenate", "replicate", 
      "paren_expr", "cast", "cast_width_expr", "range_suffix", "array_suffix", 
      "array_type_suffix", "data_type", "basic_data_type", "literal", "number", 
      "string_literal", "boolean_literal", "array_literal", "struct_literal", 
      "struct_kv", "enum_literal", "accesstype_literal", "onreadtype_literal", 
      "onwritetype_literal", "addressingtype_literal", "precedencetype_literal", 
      "instance_ref", "instance_ref_element", "prop_ref", "local_property_assignment", 
      "dynamic_property_assignment", "normal_prop_assign", "encode_prop_assign", 
      "prop_mod_assign", "prop_assignment_rhs", "prop_keyword", "prop_mod", 
      "udp_def", "udp_attr", "udp_type", "udp_data_type", "udp_usage", "udp_comp_type", 
      "udp_default", "udp_constraint", "enum_def", "enum_entry", "enum_prop_assign", 
      "struct_def", "struct_elem", "struct_type", "constraint_def", "constraint_named_def", 
      "constraint_anon_def", "constraint_body", "constraint_body_elem", 
      "constraint_insts", "constr_relational", "constr_prop_assign", "constr_inside_values", 
      "constr_inside_enum", "constr_lhs", "constr_inside_value"
    },
    std::vector<std::string>{
      "", "';'", "'{'", "'}'", "','", "'#'", "'('", "')'", "'.'", "'\\u003F'", 
      "':'", "'''", "'['", "']'", "'::'", "'->'", "", "", "'boolean'", "'bit'", 
      "'longint'", "'unsigned'", "'string'", "'accesstype'", "'addressingtype'", 
      "'onreadtype'", "'onwritetype'", "'alias'", "'external'", "'internal'", 
      "'addrmap'", "'regfile'", "'reg'", "'field'", "'mem'", "'signal'", 
      "'true'", "'false'", "'na'", "'rw'", "'wr'", "'r'", "'w'", "'rw1'", 
      "'w1'", "'rclr'", "'rset'", "'ruser'", "'woset'", "'woclr'", "'wot'", 
      "'wzs'", "'wzc'", "'wzt'", "'wclr'", "'wset'", "'wuser'", "'compact'", 
      "'regalign'", "'fullalign'", "'hw'", "'sw'", "'posedge'", "'negedge'", 
      "'bothedge'", "'level'", "'nonsticky'", "'abstract'", "'all'", "'component'", 
      "'componentwidth'", "'constraint'", "'default'", "'enum'", "'encode'", 
      "'inside'", "'number'", "'property'", "'ref'", "'struct'", "'this'", 
      "'type'", "'alternate'", "'byte'", "'int'", "'precedencetype'", "'real'", 
      "'shortint'", "'shortreal'", "'signed'", "'with'", "'within'", "", 
      "", "", "", "'+'", "'-'", "'!'", "'~'", "'&&'", "'~&'", "'&'", "'|'", 
      "'||'", "'~|'", "'^'", "", "'<<'", "'>>'", "'*'", "'**'", "'/'", "'%'", 
      "'=='", "'='", "'!='", "'<='", "'<'", "'>='", "'>'", "'@'", "'+='", 
      "'%='"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "SL_COMMENT", 
      "ML_COMMENT", "BOOLEAN_kw", "BIT_kw", "LONGINT_kw", "UNSIGNED_kw", 
      "STRING_kw", "ACCESSTYPE_kw", "ADDRESSINGTYPE_kw", "ONREADTYPE_kw", 
      "ONWRITETYPE_kw", "ALIAS_kw", "EXTERNAL_kw", "INTERNAL_kw", "ADDRMAP_kw", 
      "REGFILE_kw", "REG_kw", "FIELD_kw", "MEM_kw", "SIGNAL_kw", "TRUE_kw", 
      "FALSE_kw", "NA_kw", "RW_kw", "WR_kw", "R_kw", "W_kw", "RW1_kw", "W1_kw", 
      "RCLR_kw", "RSET_kw", "RUSER_kw", "WOSET_kw", "WOCLR_kw", "WOT_kw", 
      "WZS_kw", "WZC_kw", "WZT_kw", "WCLR_kw", "WSET_kw", "WUSER_kw", "COMPACT_kw", 
      "REGALIGN_kw", "FULLALIGN_kw", "HW_kw", "SW_kw", "POSEDGE_kw", "NEGEDGE_kw", 
      "BOTHEDGE_kw", "LEVEL_kw", "NONSTICKY_kw", "ABSTRACT_kw", "ALL_kw", 
      "COMPONENT_kw", "COMPONENTWIDTH_kw", "CONSTRAINT_kw", "DEFAULT_kw", 
      "ENUM_kw", "ENCODE_kw", "INSIDE_kw", "NUMBER_kw", "PROPERTY_kw", "REF_kw", 
      "STRUCT_kw", "THIS_kw", "TYPE_kw", "ALTERNATE_kw", "BYTE_kw", "INT_kw", 
      "PRECEDENCETYPE_kw", "REAL_kw", "SHORTINT_kw", "SHORTREAL_kw", "SIGNED_kw", 
      "WITH_kw", "WITHIN_kw", "INT", "HEX_INT", "VLOG_INT", "STRING", "PLUS", 
      "MINUS", "BNOT", "NOT", "BAND", "NAND", "AND", "OR", "BOR", "NOR", 
      "XOR", "XNOR", "LSHIFT", "RSHIFT", "MULT", "EXP", "DIV", "MOD", "EQ", 
      "ASSIGN", "NEQ", "LEQ", "LT", "GEQ", "GT", "AT", "INC", "ALIGN", "WS", 
      "ID"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,1,125,799,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,2,
  	7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,7,
  	14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,7,
  	21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,7,
  	28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,7,33,2,34,7,34,2,35,7,
  	35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,2,40,7,40,2,41,7,41,2,42,7,
  	42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,7,46,2,47,7,47,2,48,7,48,2,49,7,
  	49,2,50,7,50,2,51,7,51,2,52,7,52,2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,
  	56,2,57,7,57,2,58,7,58,2,59,7,59,2,60,7,60,2,61,7,61,2,62,7,62,2,63,7,
  	63,2,64,7,64,2,65,7,65,2,66,7,66,2,67,7,67,2,68,7,68,2,69,7,69,2,70,7,
  	70,2,71,7,71,2,72,7,72,2,73,7,73,2,74,7,74,2,75,7,75,2,76,7,76,2,77,7,
  	77,2,78,7,78,2,79,7,79,2,80,7,80,2,81,7,81,2,82,7,82,2,83,7,83,1,0,1,
  	0,1,0,5,0,172,8,0,10,0,12,0,175,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,
  	1,1,1,3,1,187,8,1,1,2,1,2,1,2,1,2,1,2,3,2,194,8,2,3,2,196,8,2,1,2,1,2,
  	1,2,1,2,1,2,3,2,203,8,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,213,8,2,1,
  	3,3,3,216,8,3,1,3,3,3,219,8,3,1,3,1,3,1,3,1,4,1,4,1,4,1,5,1,5,1,5,3,5,
  	230,8,5,1,5,1,5,1,6,1,6,1,6,1,7,1,7,1,7,1,7,5,7,241,8,7,10,7,12,7,244,
  	9,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,255,8,8,1,9,3,9,258,8,9,1,
  	9,1,9,1,9,5,9,263,8,9,10,9,12,9,266,9,9,1,10,1,10,4,10,270,8,10,11,10,
  	12,10,271,1,10,3,10,275,8,10,1,10,3,10,278,8,10,1,10,3,10,281,8,10,1,
  	10,3,10,284,8,10,1,10,3,10,287,8,10,1,11,1,11,1,11,1,12,1,12,1,12,1,13,
  	1,13,1,13,1,14,1,14,1,14,1,15,1,15,1,16,1,16,3,16,305,8,16,1,17,1,17,
  	1,18,1,18,1,18,1,18,1,18,5,18,314,8,18,10,18,12,18,317,9,18,1,18,1,18,
  	1,19,1,19,1,19,3,19,324,8,19,1,19,1,19,3,19,328,8,19,1,20,1,20,1,20,1,
  	20,1,20,5,20,335,8,20,10,20,12,20,338,9,20,1,20,1,20,1,21,1,21,1,21,1,
  	21,1,21,1,21,1,22,1,22,1,22,1,22,3,22,352,8,22,1,22,1,22,1,22,1,22,1,
  	22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,
  	22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,
  	22,1,22,1,22,1,22,1,22,1,22,1,22,5,22,393,8,22,10,22,12,22,396,9,22,1,
  	23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,3,23,407,8,23,1,24,1,24,1,
  	24,1,24,5,24,413,8,24,10,24,12,24,416,9,24,1,24,1,24,1,25,1,25,1,25,1,
  	25,1,25,1,26,1,26,1,26,1,26,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,
  	27,1,27,1,27,1,27,3,27,441,8,27,1,28,1,28,3,28,445,8,28,1,29,1,29,1,29,
  	1,29,1,29,1,29,1,30,1,30,1,30,1,30,1,31,1,31,1,31,1,32,1,32,3,32,462,
  	8,32,1,33,1,33,3,33,466,8,33,1,33,3,33,469,8,33,1,34,1,34,1,34,1,34,1,
  	34,1,34,1,34,1,34,1,34,3,34,480,8,34,1,35,1,35,1,35,3,35,485,8,35,1,36,
  	1,36,1,37,1,37,1,38,1,38,1,38,1,38,1,38,1,38,1,38,1,38,5,38,499,8,38,
  	10,38,12,38,502,9,38,1,38,1,38,3,38,506,8,38,1,39,1,39,1,39,1,39,1,39,
  	1,39,5,39,514,8,39,10,39,12,39,517,9,39,1,39,1,39,1,40,1,40,1,40,1,40,
  	1,41,1,41,1,41,1,41,1,42,1,42,1,43,1,43,1,44,1,44,1,45,1,45,1,46,1,46,
  	1,47,1,47,1,47,5,47,542,8,47,10,47,12,47,545,9,47,1,48,1,48,5,48,549,
  	8,48,10,48,12,48,552,9,48,1,49,1,49,1,49,1,49,3,49,558,8,49,1,50,3,50,
  	561,8,50,1,50,1,50,3,50,565,8,50,1,50,1,50,3,50,569,8,50,1,50,3,50,572,
  	8,50,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,3,51,582,8,51,1,52,1,52,
  	3,52,586,8,52,1,52,1,52,3,52,590,8,52,1,53,1,53,1,53,1,53,1,54,1,54,1,
  	54,1,55,1,55,3,55,601,8,55,1,56,1,56,1,57,1,57,1,58,1,58,1,58,1,58,1,
  	58,1,58,4,58,613,8,58,11,58,12,58,614,1,58,1,58,1,59,1,59,1,59,1,59,3,
  	59,623,8,59,1,60,1,60,1,60,1,60,3,60,629,8,60,1,61,1,61,1,61,3,61,634,
  	8,61,1,62,1,62,1,62,1,62,1,62,5,62,641,8,62,10,62,12,62,644,9,62,1,63,
  	1,63,3,63,648,8,63,1,64,1,64,1,64,1,64,1,65,1,65,1,65,1,65,1,66,1,66,
  	1,66,1,66,1,66,1,66,4,66,664,8,66,11,66,12,66,665,1,66,1,66,1,67,1,67,
  	1,67,3,67,673,8,67,1,67,1,67,1,67,1,67,5,67,679,8,67,10,67,12,67,682,
  	9,67,1,67,3,67,685,8,67,1,68,1,68,1,68,1,68,1,69,3,69,692,8,69,1,69,1,
  	69,1,69,1,69,3,69,698,8,69,1,69,1,69,1,69,1,69,5,69,704,8,69,10,69,12,
  	69,707,9,69,1,69,1,69,1,70,1,70,1,70,3,70,714,8,70,1,71,1,71,3,71,718,
  	8,71,1,72,1,72,3,72,722,8,72,1,72,1,72,1,72,3,72,727,8,72,1,73,1,73,1,
  	73,1,73,1,74,1,74,1,74,1,75,1,75,1,75,1,75,5,75,740,8,75,10,75,12,75,
  	743,9,75,1,75,1,75,1,76,1,76,1,76,1,76,3,76,751,8,76,1,77,1,77,1,77,5,
  	77,756,8,77,10,77,12,77,759,9,77,1,78,1,78,1,78,1,78,1,79,1,79,1,79,1,
  	79,1,80,1,80,1,80,1,80,1,80,1,80,5,80,775,8,80,10,80,12,80,778,9,80,1,
  	80,1,80,1,81,1,81,1,81,1,81,1,82,1,82,3,82,788,8,82,1,83,1,83,1,83,1,
  	83,1,83,1,83,1,83,3,83,797,8,83,1,83,0,1,44,84,0,2,4,6,8,10,12,14,16,
  	18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,
  	64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,
  	108,110,112,114,116,118,120,122,124,126,128,130,132,134,136,138,140,142,
  	144,146,148,150,152,154,156,158,160,162,164,166,0,24,1,0,28,29,1,0,30,
  	34,3,0,96,99,101,103,105,107,2,0,110,110,112,113,1,0,96,97,1,0,108,109,
  	1,0,117,120,2,0,114,114,116,116,1,0,106,107,1,0,18,20,1,0,23,26,1,0,19,
  	20,3,0,18,18,22,22,125,125,1,0,36,37,1,0,38,44,1,0,45,47,1,0,48,56,1,
  	0,57,59,1,0,60,61,3,0,45,46,48,49,60,61,1,0,62,66,2,0,76,76,78,78,2,0,
  	68,68,71,71,2,0,114,114,116,120,832,0,173,1,0,0,0,2,186,1,0,0,0,4,212,
  	1,0,0,0,6,215,1,0,0,0,8,223,1,0,0,0,10,226,1,0,0,0,12,233,1,0,0,0,14,
  	236,1,0,0,0,16,254,1,0,0,0,18,257,1,0,0,0,20,267,1,0,0,0,22,288,1,0,0,
  	0,24,291,1,0,0,0,26,294,1,0,0,0,28,297,1,0,0,0,30,300,1,0,0,0,32,304,
  	1,0,0,0,34,306,1,0,0,0,36,308,1,0,0,0,38,320,1,0,0,0,40,329,1,0,0,0,42,
  	341,1,0,0,0,44,351,1,0,0,0,46,406,1,0,0,0,48,408,1,0,0,0,50,419,1,0,0,
  	0,52,424,1,0,0,0,54,440,1,0,0,0,56,444,1,0,0,0,58,446,1,0,0,0,60,452,
  	1,0,0,0,62,456,1,0,0,0,64,461,1,0,0,0,66,468,1,0,0,0,68,479,1,0,0,0,70,
  	484,1,0,0,0,72,486,1,0,0,0,74,488,1,0,0,0,76,505,1,0,0,0,78,507,1,0,0,
  	0,80,520,1,0,0,0,82,524,1,0,0,0,84,528,1,0,0,0,86,530,1,0,0,0,88,532,
  	1,0,0,0,90,534,1,0,0,0,92,536,1,0,0,0,94,538,1,0,0,0,96,546,1,0,0,0,98,
  	553,1,0,0,0,100,571,1,0,0,0,102,581,1,0,0,0,104,585,1,0,0,0,106,591,1,
  	0,0,0,108,595,1,0,0,0,110,600,1,0,0,0,112,602,1,0,0,0,114,604,1,0,0,0,
  	116,606,1,0,0,0,118,622,1,0,0,0,120,624,1,0,0,0,122,633,1,0,0,0,124,635,
  	1,0,0,0,126,647,1,0,0,0,128,649,1,0,0,0,130,653,1,0,0,0,132,657,1,0,0,
  	0,134,669,1,0,0,0,136,686,1,0,0,0,138,691,1,0,0,0,140,710,1,0,0,0,142,
  	717,1,0,0,0,144,726,1,0,0,0,146,728,1,0,0,0,148,732,1,0,0,0,150,735,1,
  	0,0,0,152,750,1,0,0,0,154,752,1,0,0,0,156,760,1,0,0,0,158,764,1,0,0,0,
  	160,768,1,0,0,0,162,781,1,0,0,0,164,787,1,0,0,0,166,796,1,0,0,0,168,169,
  	3,2,1,0,169,170,5,1,0,0,170,172,1,0,0,0,171,168,1,0,0,0,172,175,1,0,0,
  	0,173,171,1,0,0,0,173,174,1,0,0,0,174,176,1,0,0,0,175,173,1,0,0,0,176,
  	177,5,0,0,1,177,1,1,0,0,0,178,187,3,4,2,0,179,187,3,132,66,0,180,187,
  	3,116,58,0,181,187,3,138,69,0,182,187,3,144,72,0,183,187,3,6,3,0,184,
  	187,3,100,50,0,185,187,3,102,51,0,186,178,1,0,0,0,186,179,1,0,0,0,186,
  	180,1,0,0,0,186,181,1,0,0,0,186,182,1,0,0,0,186,183,1,0,0,0,186,184,1,
  	0,0,0,186,185,1,0,0,0,187,3,1,0,0,0,188,195,3,10,5,0,189,190,3,30,15,
  	0,190,191,3,18,9,0,191,196,1,0,0,0,192,194,3,18,9,0,193,192,1,0,0,0,193,
  	194,1,0,0,0,194,196,1,0,0,0,195,189,1,0,0,0,195,193,1,0,0,0,196,213,1,
  	0,0,0,197,202,3,12,6,0,198,199,3,30,15,0,199,200,3,18,9,0,200,203,1,0,
  	0,0,201,203,3,18,9,0,202,198,1,0,0,0,202,201,1,0,0,0,203,213,1,0,0,0,
  	204,205,3,30,15,0,205,206,3,10,5,0,206,207,3,18,9,0,207,213,1,0,0,0,208,
  	209,3,30,15,0,209,210,3,12,6,0,210,211,3,18,9,0,211,213,1,0,0,0,212,188,
  	1,0,0,0,212,197,1,0,0,0,212,204,1,0,0,0,212,208,1,0,0,0,213,5,1,0,0,0,
  	214,216,3,30,15,0,215,214,1,0,0,0,215,216,1,0,0,0,216,218,1,0,0,0,217,
  	219,3,8,4,0,218,217,1,0,0,0,218,219,1,0,0,0,219,220,1,0,0,0,220,221,5,
  	125,0,0,221,222,3,18,9,0,222,7,1,0,0,0,223,224,5,27,0,0,224,225,5,125,
  	0,0,225,9,1,0,0,0,226,227,3,32,16,0,227,229,5,125,0,0,228,230,3,36,18,
  	0,229,228,1,0,0,0,229,230,1,0,0,0,230,231,1,0,0,0,231,232,3,14,7,0,232,
  	11,1,0,0,0,233,234,3,32,16,0,234,235,3,14,7,0,235,13,1,0,0,0,236,242,
  	5,2,0,0,237,238,3,16,8,0,238,239,5,1,0,0,239,241,1,0,0,0,240,237,1,0,
  	0,0,241,244,1,0,0,0,242,240,1,0,0,0,242,243,1,0,0,0,243,245,1,0,0,0,244,
  	242,1,0,0,0,245,246,5,3,0,0,246,15,1,0,0,0,247,255,3,4,2,0,248,255,3,
  	132,66,0,249,255,3,138,69,0,250,255,3,144,72,0,251,255,3,6,3,0,252,255,
  	3,100,50,0,253,255,3,102,51,0,254,247,1,0,0,0,254,248,1,0,0,0,254,249,
  	1,0,0,0,254,250,1,0,0,0,254,251,1,0,0,0,254,252,1,0,0,0,254,253,1,0,0,
  	0,255,17,1,0,0,0,256,258,3,40,20,0,257,256,1,0,0,0,257,258,1,0,0,0,258,
  	259,1,0,0,0,259,264,3,20,10,0,260,261,5,4,0,0,261,263,3,20,10,0,262,260,
  	1,0,0,0,263,266,1,0,0,0,264,262,1,0,0,0,264,265,1,0,0,0,265,19,1,0,0,
  	0,266,264,1,0,0,0,267,274,5,125,0,0,268,270,3,60,30,0,269,268,1,0,0,0,
  	270,271,1,0,0,0,271,269,1,0,0,0,271,272,1,0,0,0,272,275,1,0,0,0,273,275,
  	3,58,29,0,274,269,1,0,0,0,274,273,1,0,0,0,274,275,1,0,0,0,275,277,1,0,
  	0,0,276,278,3,22,11,0,277,276,1,0,0,0,277,278,1,0,0,0,278,280,1,0,0,0,
  	279,281,3,24,12,0,280,279,1,0,0,0,280,281,1,0,0,0,281,283,1,0,0,0,282,
  	284,3,26,13,0,283,282,1,0,0,0,283,284,1,0,0,0,284,286,1,0,0,0,285,287,
  	3,28,14,0,286,285,1,0,0,0,286,287,1,0,0,0,287,21,1,0,0,0,288,289,5,115,
  	0,0,289,290,3,44,22,0,290,23,1,0,0,0,291,292,5,121,0,0,292,293,3,44,22,
  	0,293,25,1,0,0,0,294,295,5,122,0,0,295,296,3,44,22,0,296,27,1,0,0,0,297,
  	298,5,123,0,0,298,299,3,44,22,0,299,29,1,0,0,0,300,301,7,0,0,0,301,31,
  	1,0,0,0,302,305,3,34,17,0,303,305,5,35,0,0,304,302,1,0,0,0,304,303,1,
  	0,0,0,305,33,1,0,0,0,306,307,7,1,0,0,307,35,1,0,0,0,308,309,5,5,0,0,309,
  	310,5,6,0,0,310,315,3,38,19,0,311,312,5,4,0,0,312,314,3,38,19,0,313,311,
  	1,0,0,0,314,317,1,0,0,0,315,313,1,0,0,0,315,316,1,0,0,0,316,318,1,0,0,
  	0,317,315,1,0,0,0,318,319,5,7,0,0,319,37,1,0,0,0,320,321,3,64,32,0,321,
  	323,5,125,0,0,322,324,3,62,31,0,323,322,1,0,0,0,323,324,1,0,0,0,324,327,
  	1,0,0,0,325,326,5,115,0,0,326,328,3,44,22,0,327,325,1,0,0,0,327,328,1,
  	0,0,0,328,39,1,0,0,0,329,330,5,5,0,0,330,331,5,6,0,0,331,336,3,42,21,
  	0,332,333,5,4,0,0,333,335,3,42,21,0,334,332,1,0,0,0,335,338,1,0,0,0,336,
  	334,1,0,0,0,336,337,1,0,0,0,337,339,1,0,0,0,338,336,1,0,0,0,339,340,5,
  	7,0,0,340,41,1,0,0,0,341,342,5,8,0,0,342,343,5,125,0,0,343,344,5,6,0,
  	0,344,345,3,44,22,0,345,346,5,7,0,0,346,43,1,0,0,0,347,348,6,22,-1,0,
  	348,349,7,2,0,0,349,352,3,46,23,0,350,352,3,46,23,0,351,347,1,0,0,0,351,
  	350,1,0,0,0,352,394,1,0,0,0,353,354,10,13,0,0,354,355,5,111,0,0,355,393,
  	3,44,22,14,356,357,10,12,0,0,357,358,7,3,0,0,358,393,3,44,22,13,359,360,
  	10,11,0,0,360,361,7,4,0,0,361,393,3,44,22,12,362,363,10,10,0,0,363,364,
  	7,5,0,0,364,393,3,44,22,11,365,366,10,9,0,0,366,367,7,6,0,0,367,393,3,
  	44,22,10,368,369,10,8,0,0,369,370,7,7,0,0,370,393,3,44,22,9,371,372,10,
  	7,0,0,372,373,5,102,0,0,373,393,3,44,22,8,374,375,10,6,0,0,375,376,7,
  	8,0,0,376,393,3,44,22,7,377,378,10,5,0,0,378,379,5,103,0,0,379,393,3,
  	44,22,6,380,381,10,4,0,0,381,382,5,100,0,0,382,393,3,44,22,5,383,384,
  	10,3,0,0,384,385,5,104,0,0,385,393,3,44,22,4,386,387,10,2,0,0,387,388,
  	5,9,0,0,388,389,3,44,22,0,389,390,5,10,0,0,390,391,3,44,22,2,391,393,
  	1,0,0,0,392,353,1,0,0,0,392,356,1,0,0,0,392,359,1,0,0,0,392,362,1,0,0,
  	0,392,365,1,0,0,0,392,368,1,0,0,0,392,371,1,0,0,0,392,374,1,0,0,0,392,
  	377,1,0,0,0,392,380,1,0,0,0,392,383,1,0,0,0,392,386,1,0,0,0,393,396,1,
  	0,0,0,394,392,1,0,0,0,394,395,1,0,0,0,395,45,1,0,0,0,396,394,1,0,0,0,
  	397,407,3,68,34,0,398,407,3,48,24,0,399,407,3,50,25,0,400,407,3,52,26,
  	0,401,407,3,54,27,0,402,407,3,98,49,0,403,407,3,94,47,0,404,407,3,78,
  	39,0,405,407,3,76,38,0,406,397,1,0,0,0,406,398,1,0,0,0,406,399,1,0,0,
  	0,406,400,1,0,0,0,406,401,1,0,0,0,406,402,1,0,0,0,406,403,1,0,0,0,406,
  	404,1,0,0,0,406,405,1,0,0,0,407,47,1,0,0,0,408,409,5,2,0,0,409,414,3,
  	44,22,0,410,411,5,4,0,0,411,413,3,44,22,0,412,410,1,0,0,0,413,416,1,0,
  	0,0,414,412,1,0,0,0,414,415,1,0,0,0,415,417,1,0,0,0,416,414,1,0,0,0,417,
  	418,5,3,0,0,418,49,1,0,0,0,419,420,5,2,0,0,420,421,3,44,22,0,421,422,
  	3,48,24,0,422,423,5,3,0,0,423,51,1,0,0,0,424,425,5,6,0,0,425,426,3,44,
  	22,0,426,427,5,7,0,0,427,53,1,0,0,0,428,429,7,9,0,0,429,430,5,11,0,0,
  	430,431,5,6,0,0,431,432,3,44,22,0,432,433,5,7,0,0,433,441,1,0,0,0,434,
  	435,3,56,28,0,435,436,5,11,0,0,436,437,5,6,0,0,437,438,3,44,22,0,438,
  	439,5,7,0,0,439,441,1,0,0,0,440,428,1,0,0,0,440,434,1,0,0,0,441,55,1,
  	0,0,0,442,445,3,68,34,0,443,445,3,52,26,0,444,442,1,0,0,0,444,443,1,0,
  	0,0,445,57,1,0,0,0,446,447,5,12,0,0,447,448,3,44,22,0,448,449,5,10,0,
  	0,449,450,3,44,22,0,450,451,5,13,0,0,451,59,1,0,0,0,452,453,5,12,0,0,
  	453,454,3,44,22,0,454,455,5,13,0,0,455,61,1,0,0,0,456,457,5,12,0,0,457,
  	458,5,13,0,0,458,63,1,0,0,0,459,462,3,66,33,0,460,462,7,10,0,0,461,459,
  	1,0,0,0,461,460,1,0,0,0,462,65,1,0,0,0,463,465,7,11,0,0,464,466,5,21,
  	0,0,465,464,1,0,0,0,465,466,1,0,0,0,466,469,1,0,0,0,467,469,7,12,0,0,
  	468,463,1,0,0,0,468,467,1,0,0,0,469,67,1,0,0,0,470,480,3,70,35,0,471,
  	480,3,72,36,0,472,480,3,74,37,0,473,480,3,84,42,0,474,480,3,86,43,0,475,
  	480,3,88,44,0,476,480,3,90,45,0,477,480,3,92,46,0,478,480,3,82,41,0,479,
  	470,1,0,0,0,479,471,1,0,0,0,479,472,1,0,0,0,479,473,1,0,0,0,479,474,1,
  	0,0,0,479,475,1,0,0,0,479,476,1,0,0,0,479,477,1,0,0,0,479,478,1,0,0,0,
  	480,69,1,0,0,0,481,485,5,92,0,0,482,485,5,93,0,0,483,485,5,94,0,0,484,
  	481,1,0,0,0,484,482,1,0,0,0,484,483,1,0,0,0,485,71,1,0,0,0,486,487,5,
  	95,0,0,487,73,1,0,0,0,488,489,7,13,0,0,489,75,1,0,0,0,490,491,5,11,0,
  	0,491,492,5,2,0,0,492,506,5,3,0,0,493,494,5,11,0,0,494,495,5,2,0,0,495,
  	500,3,44,22,0,496,497,5,4,0,0,497,499,3,44,22,0,498,496,1,0,0,0,499,502,
  	1,0,0,0,500,498,1,0,0,0,500,501,1,0,0,0,501,503,1,0,0,0,502,500,1,0,0,
  	0,503,504,5,3,0,0,504,506,1,0,0,0,505,490,1,0,0,0,505,493,1,0,0,0,506,
  	77,1,0,0,0,507,508,5,125,0,0,508,509,5,11,0,0,509,510,5,2,0,0,510,515,
  	3,80,40,0,511,512,5,4,0,0,512,514,3,80,40,0,513,511,1,0,0,0,514,517,1,
  	0,0,0,515,513,1,0,0,0,515,516,1,0,0,0,516,518,1,0,0,0,517,515,1,0,0,0,
  	518,519,5,3,0,0,519,79,1,0,0,0,520,521,5,125,0,0,521,522,5,10,0,0,522,
  	523,3,44,22,0,523,81,1,0,0,0,524,525,5,125,0,0,525,526,5,14,0,0,526,527,
  	5,125,0,0,527,83,1,0,0,0,528,529,7,14,0,0,529,85,1,0,0,0,530,531,7,15,
  	0,0,531,87,1,0,0,0,532,533,7,16,0,0,533,89,1,0,0,0,534,535,7,17,0,0,535,
  	91,1,0,0,0,536,537,7,18,0,0,537,93,1,0,0,0,538,543,3,96,48,0,539,540,
  	5,8,0,0,540,542,3,96,48,0,541,539,1,0,0,0,542,545,1,0,0,0,543,541,1,0,
  	0,0,543,544,1,0,0,0,544,95,1,0,0,0,545,543,1,0,0,0,546,550,5,125,0,0,
  	547,549,3,60,30,0,548,547,1,0,0,0,549,552,1,0,0,0,550,548,1,0,0,0,550,
  	551,1,0,0,0,551,97,1,0,0,0,552,550,1,0,0,0,553,554,3,94,47,0,554,557,
  	5,15,0,0,555,558,3,112,56,0,556,558,5,125,0,0,557,555,1,0,0,0,557,556,
  	1,0,0,0,558,99,1,0,0,0,559,561,5,72,0,0,560,559,1,0,0,0,560,561,1,0,0,
  	0,561,562,1,0,0,0,562,572,3,104,52,0,563,565,5,72,0,0,564,563,1,0,0,0,
  	564,565,1,0,0,0,565,566,1,0,0,0,566,572,3,106,53,0,567,569,5,72,0,0,568,
  	567,1,0,0,0,568,569,1,0,0,0,569,570,1,0,0,0,570,572,3,108,54,0,571,560,
  	1,0,0,0,571,564,1,0,0,0,571,568,1,0,0,0,572,101,1,0,0,0,573,574,3,94,
  	47,0,574,575,5,15,0,0,575,576,3,104,52,0,576,582,1,0,0,0,577,578,3,94,
  	47,0,578,579,5,15,0,0,579,580,3,106,53,0,580,582,1,0,0,0,581,573,1,0,
  	0,0,581,577,1,0,0,0,582,103,1,0,0,0,583,586,3,112,56,0,584,586,5,125,
  	0,0,585,583,1,0,0,0,585,584,1,0,0,0,586,589,1,0,0,0,587,588,5,115,0,0,
  	588,590,3,110,55,0,589,587,1,0,0,0,589,590,1,0,0,0,590,105,1,0,0,0,591,
  	592,5,74,0,0,592,593,5,115,0,0,593,594,5,125,0,0,594,107,1,0,0,0,595,
  	596,3,114,57,0,596,597,5,125,0,0,597,109,1,0,0,0,598,601,3,92,46,0,599,
  	601,3,44,22,0,600,598,1,0,0,0,600,599,1,0,0,0,601,111,1,0,0,0,602,603,
  	7,19,0,0,603,113,1,0,0,0,604,605,7,20,0,0,605,115,1,0,0,0,606,607,5,77,
  	0,0,607,608,5,125,0,0,608,612,5,2,0,0,609,610,3,118,59,0,610,611,5,1,
  	0,0,611,613,1,0,0,0,612,609,1,0,0,0,613,614,1,0,0,0,614,612,1,0,0,0,614,
  	615,1,0,0,0,615,616,1,0,0,0,616,617,5,3,0,0,617,117,1,0,0,0,618,623,3,
  	120,60,0,619,623,3,124,62,0,620,623,3,128,64,0,621,623,3,130,65,0,622,
  	618,1,0,0,0,622,619,1,0,0,0,622,620,1,0,0,0,622,621,1,0,0,0,623,119,1,
  	0,0,0,624,625,5,81,0,0,625,626,5,115,0,0,626,628,3,122,61,0,627,629,3,
  	62,31,0,628,627,1,0,0,0,628,629,1,0,0,0,629,121,1,0,0,0,630,634,3,34,
  	17,0,631,634,7,21,0,0,632,634,3,66,33,0,633,630,1,0,0,0,633,631,1,0,0,
  	0,633,632,1,0,0,0,634,123,1,0,0,0,635,636,5,69,0,0,636,637,5,115,0,0,
  	637,642,3,126,63,0,638,639,5,103,0,0,639,641,3,126,63,0,640,638,1,0,0,
  	0,641,644,1,0,0,0,642,640,1,0,0,0,642,643,1,0,0,0,643,125,1,0,0,0,644,
  	642,1,0,0,0,645,648,3,32,16,0,646,648,7,22,0,0,647,645,1,0,0,0,647,646,
  	1,0,0,0,648,127,1,0,0,0,649,650,5,72,0,0,650,651,5,115,0,0,651,652,3,
  	44,22,0,652,129,1,0,0,0,653,654,5,71,0,0,654,655,5,115,0,0,655,656,5,
  	70,0,0,656,131,1,0,0,0,657,658,5,73,0,0,658,659,5,125,0,0,659,663,5,2,
  	0,0,660,661,3,134,67,0,661,662,5,1,0,0,662,664,1,0,0,0,663,660,1,0,0,
  	0,664,665,1,0,0,0,665,663,1,0,0,0,665,666,1,0,0,0,666,667,1,0,0,0,667,
  	668,5,3,0,0,668,133,1,0,0,0,669,672,5,125,0,0,670,671,5,115,0,0,671,673,
  	3,44,22,0,672,670,1,0,0,0,672,673,1,0,0,0,673,684,1,0,0,0,674,680,5,2,
  	0,0,675,676,3,136,68,0,676,677,5,1,0,0,677,679,1,0,0,0,678,675,1,0,0,
  	0,679,682,1,0,0,0,680,678,1,0,0,0,680,681,1,0,0,0,681,683,1,0,0,0,682,
  	680,1,0,0,0,683,685,5,3,0,0,684,674,1,0,0,0,684,685,1,0,0,0,685,135,1,
  	0,0,0,686,687,5,125,0,0,687,688,5,115,0,0,688,689,3,44,22,0,689,137,1,
  	0,0,0,690,692,5,67,0,0,691,690,1,0,0,0,691,692,1,0,0,0,692,693,1,0,0,
  	0,693,694,5,79,0,0,694,697,5,125,0,0,695,696,5,10,0,0,696,698,5,125,0,
  	0,697,695,1,0,0,0,697,698,1,0,0,0,698,699,1,0,0,0,699,705,5,2,0,0,700,
  	701,3,140,70,0,701,702,5,1,0,0,702,704,1,0,0,0,703,700,1,0,0,0,704,707,
  	1,0,0,0,705,703,1,0,0,0,705,706,1,0,0,0,706,708,1,0,0,0,707,705,1,0,0,
  	0,708,709,5,3,0,0,709,139,1,0,0,0,710,711,3,142,71,0,711,713,5,125,0,
  	0,712,714,3,62,31,0,713,712,1,0,0,0,713,714,1,0,0,0,714,141,1,0,0,0,715,
  	718,3,64,32,0,716,718,3,32,16,0,717,715,1,0,0,0,717,716,1,0,0,0,718,143,
  	1,0,0,0,719,721,3,146,73,0,720,722,3,154,77,0,721,720,1,0,0,0,721,722,
  	1,0,0,0,722,727,1,0,0,0,723,724,3,148,74,0,724,725,3,154,77,0,725,727,
  	1,0,0,0,726,719,1,0,0,0,726,723,1,0,0,0,727,145,1,0,0,0,728,729,5,71,
  	0,0,729,730,5,125,0,0,730,731,3,150,75,0,731,147,1,0,0,0,732,733,5,71,
  	0,0,733,734,3,150,75,0,734,149,1,0,0,0,735,741,5,2,0,0,736,737,3,152,
  	76,0,737,738,5,1,0,0,738,740,1,0,0,0,739,736,1,0,0,0,740,743,1,0,0,0,
  	741,739,1,0,0,0,741,742,1,0,0,0,742,744,1,0,0,0,743,741,1,0,0,0,744,745,
  	5,3,0,0,745,151,1,0,0,0,746,751,3,156,78,0,747,751,3,158,79,0,748,751,
  	3,160,80,0,749,751,3,162,81,0,750,746,1,0,0,0,750,747,1,0,0,0,750,748,
  	1,0,0,0,750,749,1,0,0,0,751,153,1,0,0,0,752,757,5,125,0,0,753,754,5,4,
  	0,0,754,756,5,125,0,0,755,753,1,0,0,0,756,759,1,0,0,0,757,755,1,0,0,0,
  	757,758,1,0,0,0,758,155,1,0,0,0,759,757,1,0,0,0,760,761,3,44,22,0,761,
  	762,7,23,0,0,762,763,3,44,22,0,763,157,1,0,0,0,764,765,5,125,0,0,765,
  	766,5,115,0,0,766,767,3,44,22,0,767,159,1,0,0,0,768,769,3,164,82,0,769,
  	770,5,75,0,0,770,771,5,2,0,0,771,776,3,166,83,0,772,773,5,4,0,0,773,775,
  	3,166,83,0,774,772,1,0,0,0,775,778,1,0,0,0,776,774,1,0,0,0,776,777,1,
  	0,0,0,777,779,1,0,0,0,778,776,1,0,0,0,779,780,5,3,0,0,780,161,1,0,0,0,
  	781,782,3,164,82,0,782,783,5,75,0,0,783,784,5,125,0,0,784,163,1,0,0,0,
  	785,788,5,80,0,0,786,788,3,94,47,0,787,785,1,0,0,0,787,786,1,0,0,0,788,
  	165,1,0,0,0,789,797,3,44,22,0,790,791,5,12,0,0,791,792,3,44,22,0,792,
  	793,5,10,0,0,793,794,3,44,22,0,794,795,5,13,0,0,795,797,1,0,0,0,796,789,
  	1,0,0,0,796,790,1,0,0,0,797,167,1,0,0,0,73,173,186,193,195,202,212,215,
  	218,229,242,254,257,264,271,274,277,280,283,286,304,315,323,327,336,351,
  	392,394,406,414,440,444,461,465,468,479,484,500,505,515,543,550,557,560,
  	564,568,571,581,585,589,600,614,622,628,633,642,647,665,672,680,684,691,
  	697,705,713,717,721,726,741,750,757,776,787,796
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  systemrdlParserStaticData = staticData.release();
}

}

SystemRDLParser::SystemRDLParser(TokenStream *input) : SystemRDLParser(input, antlr4::atn::ParserATNSimulatorOptions()) {}

SystemRDLParser::SystemRDLParser(TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options) : Parser(input) {
  SystemRDLParser::initialize();
  _interpreter = new atn::ParserATNSimulator(this, *systemrdlParserStaticData->atn, systemrdlParserStaticData->decisionToDFA, systemrdlParserStaticData->sharedContextCache, options);
}

SystemRDLParser::~SystemRDLParser() {
  delete _interpreter;
}

const atn::ATN& SystemRDLParser::getATN() const {
  return *systemrdlParserStaticData->atn;
}

std::string SystemRDLParser::getGrammarFileName() const {
  return "SystemRDL.g4";
}

const std::vector<std::string>& SystemRDLParser::getRuleNames() const {
  return systemrdlParserStaticData->ruleNames;
}

const dfa::Vocabulary& SystemRDLParser::getVocabulary() const {
  return systemrdlParserStaticData->vocabulary;
}

antlr4::atn::SerializedATNView SystemRDLParser::getSerializedATN() const {
  return systemrdlParserStaticData->serializedATN;
}


//----------------- RootContext ------------------------------------------------------------------

SystemRDLParser::RootContext::RootContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::RootContext::EOF() {
  return getToken(SystemRDLParser::EOF, 0);
}

std::vector<SystemRDLParser::Root_elemContext *> SystemRDLParser::RootContext::root_elem() {
  return getRuleContexts<SystemRDLParser::Root_elemContext>();
}

SystemRDLParser::Root_elemContext* SystemRDLParser::RootContext::root_elem(size_t i) {
  return getRuleContext<SystemRDLParser::Root_elemContext>(i);
}


size_t SystemRDLParser::RootContext::getRuleIndex() const {
  return SystemRDLParser::RuleRoot;
}


std::any SystemRDLParser::RootContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitRoot(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::RootContext* SystemRDLParser::root() {
  RootContext *_localctx = _tracker.createInstance<RootContext>(_ctx, getState());
  enterRule(_localctx, 0, SystemRDLParser::RuleRoot);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(173);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::ALIAS_kw)
      | (1ULL << SystemRDLParser::EXTERNAL_kw)
      | (1ULL << SystemRDLParser::INTERNAL_kw)
      | (1ULL << SystemRDLParser::ADDRMAP_kw)
      | (1ULL << SystemRDLParser::REGFILE_kw)
      | (1ULL << SystemRDLParser::REG_kw)
      | (1ULL << SystemRDLParser::FIELD_kw)
      | (1ULL << SystemRDLParser::MEM_kw)
      | (1ULL << SystemRDLParser::SIGNAL_kw)
      | (1ULL << SystemRDLParser::RCLR_kw)
      | (1ULL << SystemRDLParser::RSET_kw)
      | (1ULL << SystemRDLParser::WOSET_kw)
      | (1ULL << SystemRDLParser::WOCLR_kw)
      | (1ULL << SystemRDLParser::HW_kw)
      | (1ULL << SystemRDLParser::SW_kw)
      | (1ULL << SystemRDLParser::POSEDGE_kw)
      | (1ULL << SystemRDLParser::NEGEDGE_kw))) != 0) || ((((_la - 64) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 64)) & ((1ULL << (SystemRDLParser::BOTHEDGE_kw - 64))
      | (1ULL << (SystemRDLParser::LEVEL_kw - 64))
      | (1ULL << (SystemRDLParser::NONSTICKY_kw - 64))
      | (1ULL << (SystemRDLParser::ABSTRACT_kw - 64))
      | (1ULL << (SystemRDLParser::CONSTRAINT_kw - 64))
      | (1ULL << (SystemRDLParser::DEFAULT_kw - 64))
      | (1ULL << (SystemRDLParser::ENUM_kw - 64))
      | (1ULL << (SystemRDLParser::ENCODE_kw - 64))
      | (1ULL << (SystemRDLParser::PROPERTY_kw - 64))
      | (1ULL << (SystemRDLParser::STRUCT_kw - 64))
      | (1ULL << (SystemRDLParser::ID - 64)))) != 0)) {
      setState(168);
      root_elem();
      setState(169);
      match(SystemRDLParser::T__0);
      setState(175);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(176);
    match(SystemRDLParser::EOF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Root_elemContext ------------------------------------------------------------------

SystemRDLParser::Root_elemContext::Root_elemContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_defContext* SystemRDLParser::Root_elemContext::component_def() {
  return getRuleContext<SystemRDLParser::Component_defContext>(0);
}

SystemRDLParser::Enum_defContext* SystemRDLParser::Root_elemContext::enum_def() {
  return getRuleContext<SystemRDLParser::Enum_defContext>(0);
}

SystemRDLParser::Udp_defContext* SystemRDLParser::Root_elemContext::udp_def() {
  return getRuleContext<SystemRDLParser::Udp_defContext>(0);
}

SystemRDLParser::Struct_defContext* SystemRDLParser::Root_elemContext::struct_def() {
  return getRuleContext<SystemRDLParser::Struct_defContext>(0);
}

SystemRDLParser::Constraint_defContext* SystemRDLParser::Root_elemContext::constraint_def() {
  return getRuleContext<SystemRDLParser::Constraint_defContext>(0);
}

SystemRDLParser::Explicit_component_instContext* SystemRDLParser::Root_elemContext::explicit_component_inst() {
  return getRuleContext<SystemRDLParser::Explicit_component_instContext>(0);
}

SystemRDLParser::Local_property_assignmentContext* SystemRDLParser::Root_elemContext::local_property_assignment() {
  return getRuleContext<SystemRDLParser::Local_property_assignmentContext>(0);
}

SystemRDLParser::Dynamic_property_assignmentContext* SystemRDLParser::Root_elemContext::dynamic_property_assignment() {
  return getRuleContext<SystemRDLParser::Dynamic_property_assignmentContext>(0);
}


size_t SystemRDLParser::Root_elemContext::getRuleIndex() const {
  return SystemRDLParser::RuleRoot_elem;
}


std::any SystemRDLParser::Root_elemContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitRoot_elem(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Root_elemContext* SystemRDLParser::root_elem() {
  Root_elemContext *_localctx = _tracker.createInstance<Root_elemContext>(_ctx, getState());
  enterRule(_localctx, 2, SystemRDLParser::RuleRoot_elem);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(186);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 1, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(178);
      component_def();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(179);
      enum_def();
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(180);
      udp_def();
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(181);
      struct_def();
      break;
    }

    case 5: {
      enterOuterAlt(_localctx, 5);
      setState(182);
      constraint_def();
      break;
    }

    case 6: {
      enterOuterAlt(_localctx, 6);
      setState(183);
      explicit_component_inst();
      break;
    }

    case 7: {
      enterOuterAlt(_localctx, 7);
      setState(184);
      local_property_assignment();
      break;
    }

    case 8: {
      enterOuterAlt(_localctx, 8);
      setState(185);
      dynamic_property_assignment();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_defContext ------------------------------------------------------------------

SystemRDLParser::Component_defContext::Component_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_named_defContext* SystemRDLParser::Component_defContext::component_named_def() {
  return getRuleContext<SystemRDLParser::Component_named_defContext>(0);
}

SystemRDLParser::Component_inst_typeContext* SystemRDLParser::Component_defContext::component_inst_type() {
  return getRuleContext<SystemRDLParser::Component_inst_typeContext>(0);
}

SystemRDLParser::Component_instsContext* SystemRDLParser::Component_defContext::component_insts() {
  return getRuleContext<SystemRDLParser::Component_instsContext>(0);
}

SystemRDLParser::Component_anon_defContext* SystemRDLParser::Component_defContext::component_anon_def() {
  return getRuleContext<SystemRDLParser::Component_anon_defContext>(0);
}


size_t SystemRDLParser::Component_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_def;
}


std::any SystemRDLParser::Component_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_defContext* SystemRDLParser::component_def() {
  Component_defContext *_localctx = _tracker.createInstance<Component_defContext>(_ctx, getState());
  enterRule(_localctx, 4, SystemRDLParser::RuleComponent_def);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(212);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 5, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(188);
      component_named_def();
      setState(195);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case SystemRDLParser::EXTERNAL_kw:
        case SystemRDLParser::INTERNAL_kw: {
          setState(189);
          component_inst_type();
          setState(190);
          component_insts();
          break;
        }

        case SystemRDLParser::T__0:
        case SystemRDLParser::T__4:
        case SystemRDLParser::ID: {
          setState(193);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if (_la == SystemRDLParser::T__4 || _la == SystemRDLParser::ID) {
            setState(192);
            component_insts();
          }
          break;
        }

      default:
        throw NoViableAltException(this);
      }
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(197);
      component_anon_def();
      setState(202);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case SystemRDLParser::EXTERNAL_kw:
        case SystemRDLParser::INTERNAL_kw: {
          setState(198);
          component_inst_type();
          setState(199);
          component_insts();
          break;
        }

        case SystemRDLParser::T__4:
        case SystemRDLParser::ID: {
          setState(201);
          component_insts();
          break;
        }

      default:
        throw NoViableAltException(this);
      }
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(204);
      component_inst_type();
      setState(205);
      component_named_def();
      setState(206);
      component_insts();
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(208);
      component_inst_type();
      setState(209);
      component_anon_def();
      setState(210);
      component_insts();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Explicit_component_instContext ------------------------------------------------------------------

SystemRDLParser::Explicit_component_instContext::Explicit_component_instContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Explicit_component_instContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::Component_instsContext* SystemRDLParser::Explicit_component_instContext::component_insts() {
  return getRuleContext<SystemRDLParser::Component_instsContext>(0);
}

SystemRDLParser::Component_inst_typeContext* SystemRDLParser::Explicit_component_instContext::component_inst_type() {
  return getRuleContext<SystemRDLParser::Component_inst_typeContext>(0);
}

SystemRDLParser::Component_inst_aliasContext* SystemRDLParser::Explicit_component_instContext::component_inst_alias() {
  return getRuleContext<SystemRDLParser::Component_inst_aliasContext>(0);
}


size_t SystemRDLParser::Explicit_component_instContext::getRuleIndex() const {
  return SystemRDLParser::RuleExplicit_component_inst;
}


std::any SystemRDLParser::Explicit_component_instContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitExplicit_component_inst(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Explicit_component_instContext* SystemRDLParser::explicit_component_inst() {
  Explicit_component_instContext *_localctx = _tracker.createInstance<Explicit_component_instContext>(_ctx, getState());
  enterRule(_localctx, 6, SystemRDLParser::RuleExplicit_component_inst);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(215);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::EXTERNAL_kw

    || _la == SystemRDLParser::INTERNAL_kw) {
      setState(214);
      component_inst_type();
    }
    setState(218);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::ALIAS_kw) {
      setState(217);
      component_inst_alias();
    }
    setState(220);
    match(SystemRDLParser::ID);
    setState(221);
    component_insts();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_inst_aliasContext ------------------------------------------------------------------

SystemRDLParser::Component_inst_aliasContext::Component_inst_aliasContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Component_inst_aliasContext::ALIAS_kw() {
  return getToken(SystemRDLParser::ALIAS_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Component_inst_aliasContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}


size_t SystemRDLParser::Component_inst_aliasContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_inst_alias;
}


std::any SystemRDLParser::Component_inst_aliasContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_inst_alias(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_inst_aliasContext* SystemRDLParser::component_inst_alias() {
  Component_inst_aliasContext *_localctx = _tracker.createInstance<Component_inst_aliasContext>(_ctx, getState());
  enterRule(_localctx, 8, SystemRDLParser::RuleComponent_inst_alias);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(223);
    match(SystemRDLParser::ALIAS_kw);
    setState(224);
    match(SystemRDLParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_named_defContext ------------------------------------------------------------------

SystemRDLParser::Component_named_defContext::Component_named_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_typeContext* SystemRDLParser::Component_named_defContext::component_type() {
  return getRuleContext<SystemRDLParser::Component_typeContext>(0);
}

tree::TerminalNode* SystemRDLParser::Component_named_defContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::Component_bodyContext* SystemRDLParser::Component_named_defContext::component_body() {
  return getRuleContext<SystemRDLParser::Component_bodyContext>(0);
}

SystemRDLParser::Param_defContext* SystemRDLParser::Component_named_defContext::param_def() {
  return getRuleContext<SystemRDLParser::Param_defContext>(0);
}


size_t SystemRDLParser::Component_named_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_named_def;
}


std::any SystemRDLParser::Component_named_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_named_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_named_defContext* SystemRDLParser::component_named_def() {
  Component_named_defContext *_localctx = _tracker.createInstance<Component_named_defContext>(_ctx, getState());
  enterRule(_localctx, 10, SystemRDLParser::RuleComponent_named_def);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(226);
    component_type();
    setState(227);
    match(SystemRDLParser::ID);
    setState(229);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::T__4) {
      setState(228);
      param_def();
    }
    setState(231);
    component_body();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_anon_defContext ------------------------------------------------------------------

SystemRDLParser::Component_anon_defContext::Component_anon_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_typeContext* SystemRDLParser::Component_anon_defContext::component_type() {
  return getRuleContext<SystemRDLParser::Component_typeContext>(0);
}

SystemRDLParser::Component_bodyContext* SystemRDLParser::Component_anon_defContext::component_body() {
  return getRuleContext<SystemRDLParser::Component_bodyContext>(0);
}


size_t SystemRDLParser::Component_anon_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_anon_def;
}


std::any SystemRDLParser::Component_anon_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_anon_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_anon_defContext* SystemRDLParser::component_anon_def() {
  Component_anon_defContext *_localctx = _tracker.createInstance<Component_anon_defContext>(_ctx, getState());
  enterRule(_localctx, 12, SystemRDLParser::RuleComponent_anon_def);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(233);
    component_type();
    setState(234);
    component_body();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_bodyContext ------------------------------------------------------------------

SystemRDLParser::Component_bodyContext::Component_bodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::Component_body_elemContext *> SystemRDLParser::Component_bodyContext::component_body_elem() {
  return getRuleContexts<SystemRDLParser::Component_body_elemContext>();
}

SystemRDLParser::Component_body_elemContext* SystemRDLParser::Component_bodyContext::component_body_elem(size_t i) {
  return getRuleContext<SystemRDLParser::Component_body_elemContext>(i);
}


size_t SystemRDLParser::Component_bodyContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_body;
}


std::any SystemRDLParser::Component_bodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_body(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_bodyContext* SystemRDLParser::component_body() {
  Component_bodyContext *_localctx = _tracker.createInstance<Component_bodyContext>(_ctx, getState());
  enterRule(_localctx, 14, SystemRDLParser::RuleComponent_body);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(236);
    match(SystemRDLParser::T__1);
    setState(242);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::ALIAS_kw)
      | (1ULL << SystemRDLParser::EXTERNAL_kw)
      | (1ULL << SystemRDLParser::INTERNAL_kw)
      | (1ULL << SystemRDLParser::ADDRMAP_kw)
      | (1ULL << SystemRDLParser::REGFILE_kw)
      | (1ULL << SystemRDLParser::REG_kw)
      | (1ULL << SystemRDLParser::FIELD_kw)
      | (1ULL << SystemRDLParser::MEM_kw)
      | (1ULL << SystemRDLParser::SIGNAL_kw)
      | (1ULL << SystemRDLParser::RCLR_kw)
      | (1ULL << SystemRDLParser::RSET_kw)
      | (1ULL << SystemRDLParser::WOSET_kw)
      | (1ULL << SystemRDLParser::WOCLR_kw)
      | (1ULL << SystemRDLParser::HW_kw)
      | (1ULL << SystemRDLParser::SW_kw)
      | (1ULL << SystemRDLParser::POSEDGE_kw)
      | (1ULL << SystemRDLParser::NEGEDGE_kw))) != 0) || ((((_la - 64) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 64)) & ((1ULL << (SystemRDLParser::BOTHEDGE_kw - 64))
      | (1ULL << (SystemRDLParser::LEVEL_kw - 64))
      | (1ULL << (SystemRDLParser::NONSTICKY_kw - 64))
      | (1ULL << (SystemRDLParser::ABSTRACT_kw - 64))
      | (1ULL << (SystemRDLParser::CONSTRAINT_kw - 64))
      | (1ULL << (SystemRDLParser::DEFAULT_kw - 64))
      | (1ULL << (SystemRDLParser::ENUM_kw - 64))
      | (1ULL << (SystemRDLParser::ENCODE_kw - 64))
      | (1ULL << (SystemRDLParser::STRUCT_kw - 64))
      | (1ULL << (SystemRDLParser::ID - 64)))) != 0)) {
      setState(237);
      component_body_elem();
      setState(238);
      match(SystemRDLParser::T__0);
      setState(244);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(245);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_body_elemContext ------------------------------------------------------------------

SystemRDLParser::Component_body_elemContext::Component_body_elemContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_defContext* SystemRDLParser::Component_body_elemContext::component_def() {
  return getRuleContext<SystemRDLParser::Component_defContext>(0);
}

SystemRDLParser::Enum_defContext* SystemRDLParser::Component_body_elemContext::enum_def() {
  return getRuleContext<SystemRDLParser::Enum_defContext>(0);
}

SystemRDLParser::Struct_defContext* SystemRDLParser::Component_body_elemContext::struct_def() {
  return getRuleContext<SystemRDLParser::Struct_defContext>(0);
}

SystemRDLParser::Constraint_defContext* SystemRDLParser::Component_body_elemContext::constraint_def() {
  return getRuleContext<SystemRDLParser::Constraint_defContext>(0);
}

SystemRDLParser::Explicit_component_instContext* SystemRDLParser::Component_body_elemContext::explicit_component_inst() {
  return getRuleContext<SystemRDLParser::Explicit_component_instContext>(0);
}

SystemRDLParser::Local_property_assignmentContext* SystemRDLParser::Component_body_elemContext::local_property_assignment() {
  return getRuleContext<SystemRDLParser::Local_property_assignmentContext>(0);
}

SystemRDLParser::Dynamic_property_assignmentContext* SystemRDLParser::Component_body_elemContext::dynamic_property_assignment() {
  return getRuleContext<SystemRDLParser::Dynamic_property_assignmentContext>(0);
}


size_t SystemRDLParser::Component_body_elemContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_body_elem;
}


std::any SystemRDLParser::Component_body_elemContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_body_elem(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_body_elemContext* SystemRDLParser::component_body_elem() {
  Component_body_elemContext *_localctx = _tracker.createInstance<Component_body_elemContext>(_ctx, getState());
  enterRule(_localctx, 16, SystemRDLParser::RuleComponent_body_elem);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(254);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 10, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(247);
      component_def();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(248);
      enum_def();
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(249);
      struct_def();
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(250);
      constraint_def();
      break;
    }

    case 5: {
      enterOuterAlt(_localctx, 5);
      setState(251);
      explicit_component_inst();
      break;
    }

    case 6: {
      enterOuterAlt(_localctx, 6);
      setState(252);
      local_property_assignment();
      break;
    }

    case 7: {
      enterOuterAlt(_localctx, 7);
      setState(253);
      dynamic_property_assignment();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_instsContext ------------------------------------------------------------------

SystemRDLParser::Component_instsContext::Component_instsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::Component_instContext *> SystemRDLParser::Component_instsContext::component_inst() {
  return getRuleContexts<SystemRDLParser::Component_instContext>();
}

SystemRDLParser::Component_instContext* SystemRDLParser::Component_instsContext::component_inst(size_t i) {
  return getRuleContext<SystemRDLParser::Component_instContext>(i);
}

SystemRDLParser::Param_instContext* SystemRDLParser::Component_instsContext::param_inst() {
  return getRuleContext<SystemRDLParser::Param_instContext>(0);
}


size_t SystemRDLParser::Component_instsContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_insts;
}


std::any SystemRDLParser::Component_instsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_insts(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_instsContext* SystemRDLParser::component_insts() {
  Component_instsContext *_localctx = _tracker.createInstance<Component_instsContext>(_ctx, getState());
  enterRule(_localctx, 18, SystemRDLParser::RuleComponent_insts);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(257);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::T__4) {
      setState(256);
      param_inst();
    }
    setState(259);
    component_inst();
    setState(264);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::T__3) {
      setState(260);
      match(SystemRDLParser::T__3);
      setState(261);
      component_inst();
      setState(266);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_instContext ------------------------------------------------------------------

SystemRDLParser::Component_instContext::Component_instContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Component_instContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::Range_suffixContext* SystemRDLParser::Component_instContext::range_suffix() {
  return getRuleContext<SystemRDLParser::Range_suffixContext>(0);
}

SystemRDLParser::Field_inst_resetContext* SystemRDLParser::Component_instContext::field_inst_reset() {
  return getRuleContext<SystemRDLParser::Field_inst_resetContext>(0);
}

SystemRDLParser::Inst_addr_fixedContext* SystemRDLParser::Component_instContext::inst_addr_fixed() {
  return getRuleContext<SystemRDLParser::Inst_addr_fixedContext>(0);
}

SystemRDLParser::Inst_addr_strideContext* SystemRDLParser::Component_instContext::inst_addr_stride() {
  return getRuleContext<SystemRDLParser::Inst_addr_strideContext>(0);
}

SystemRDLParser::Inst_addr_alignContext* SystemRDLParser::Component_instContext::inst_addr_align() {
  return getRuleContext<SystemRDLParser::Inst_addr_alignContext>(0);
}

std::vector<SystemRDLParser::Array_suffixContext *> SystemRDLParser::Component_instContext::array_suffix() {
  return getRuleContexts<SystemRDLParser::Array_suffixContext>();
}

SystemRDLParser::Array_suffixContext* SystemRDLParser::Component_instContext::array_suffix(size_t i) {
  return getRuleContext<SystemRDLParser::Array_suffixContext>(i);
}


size_t SystemRDLParser::Component_instContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_inst;
}


std::any SystemRDLParser::Component_instContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_inst(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_instContext* SystemRDLParser::component_inst() {
  Component_instContext *_localctx = _tracker.createInstance<Component_instContext>(_ctx, getState());
  enterRule(_localctx, 20, SystemRDLParser::RuleComponent_inst);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(267);
    match(SystemRDLParser::ID);
    setState(274);
    _errHandler->sync(this);

    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 14, _ctx)) {
    case 1: {
      setState(269); 
      _errHandler->sync(this);
      _la = _input->LA(1);
      do {
        setState(268);
        array_suffix();
        setState(271); 
        _errHandler->sync(this);
        _la = _input->LA(1);
      } while (_la == SystemRDLParser::T__11);
      break;
    }

    case 2: {
      setState(273);
      range_suffix();
      break;
    }

    default:
      break;
    }
    setState(277);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::ASSIGN) {
      setState(276);
      field_inst_reset();
    }
    setState(280);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::AT) {
      setState(279);
      inst_addr_fixed();
    }
    setState(283);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::INC) {
      setState(282);
      inst_addr_stride();
    }
    setState(286);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::ALIGN) {
      setState(285);
      inst_addr_align();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Field_inst_resetContext ------------------------------------------------------------------

SystemRDLParser::Field_inst_resetContext::Field_inst_resetContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::ExprContext* SystemRDLParser::Field_inst_resetContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

tree::TerminalNode* SystemRDLParser::Field_inst_resetContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}


size_t SystemRDLParser::Field_inst_resetContext::getRuleIndex() const {
  return SystemRDLParser::RuleField_inst_reset;
}


std::any SystemRDLParser::Field_inst_resetContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitField_inst_reset(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Field_inst_resetContext* SystemRDLParser::field_inst_reset() {
  Field_inst_resetContext *_localctx = _tracker.createInstance<Field_inst_resetContext>(_ctx, getState());
  enterRule(_localctx, 22, SystemRDLParser::RuleField_inst_reset);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(288);
    antlrcpp::downCast<Field_inst_resetContext *>(_localctx)->op = match(SystemRDLParser::ASSIGN);
    setState(289);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Inst_addr_fixedContext ------------------------------------------------------------------

SystemRDLParser::Inst_addr_fixedContext::Inst_addr_fixedContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::ExprContext* SystemRDLParser::Inst_addr_fixedContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

tree::TerminalNode* SystemRDLParser::Inst_addr_fixedContext::AT() {
  return getToken(SystemRDLParser::AT, 0);
}


size_t SystemRDLParser::Inst_addr_fixedContext::getRuleIndex() const {
  return SystemRDLParser::RuleInst_addr_fixed;
}


std::any SystemRDLParser::Inst_addr_fixedContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitInst_addr_fixed(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Inst_addr_fixedContext* SystemRDLParser::inst_addr_fixed() {
  Inst_addr_fixedContext *_localctx = _tracker.createInstance<Inst_addr_fixedContext>(_ctx, getState());
  enterRule(_localctx, 24, SystemRDLParser::RuleInst_addr_fixed);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(291);
    antlrcpp::downCast<Inst_addr_fixedContext *>(_localctx)->op = match(SystemRDLParser::AT);
    setState(292);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Inst_addr_strideContext ------------------------------------------------------------------

SystemRDLParser::Inst_addr_strideContext::Inst_addr_strideContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::ExprContext* SystemRDLParser::Inst_addr_strideContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

tree::TerminalNode* SystemRDLParser::Inst_addr_strideContext::INC() {
  return getToken(SystemRDLParser::INC, 0);
}


size_t SystemRDLParser::Inst_addr_strideContext::getRuleIndex() const {
  return SystemRDLParser::RuleInst_addr_stride;
}


std::any SystemRDLParser::Inst_addr_strideContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitInst_addr_stride(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Inst_addr_strideContext* SystemRDLParser::inst_addr_stride() {
  Inst_addr_strideContext *_localctx = _tracker.createInstance<Inst_addr_strideContext>(_ctx, getState());
  enterRule(_localctx, 26, SystemRDLParser::RuleInst_addr_stride);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(294);
    antlrcpp::downCast<Inst_addr_strideContext *>(_localctx)->op = match(SystemRDLParser::INC);
    setState(295);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Inst_addr_alignContext ------------------------------------------------------------------

SystemRDLParser::Inst_addr_alignContext::Inst_addr_alignContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::ExprContext* SystemRDLParser::Inst_addr_alignContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

tree::TerminalNode* SystemRDLParser::Inst_addr_alignContext::ALIGN() {
  return getToken(SystemRDLParser::ALIGN, 0);
}


size_t SystemRDLParser::Inst_addr_alignContext::getRuleIndex() const {
  return SystemRDLParser::RuleInst_addr_align;
}


std::any SystemRDLParser::Inst_addr_alignContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitInst_addr_align(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Inst_addr_alignContext* SystemRDLParser::inst_addr_align() {
  Inst_addr_alignContext *_localctx = _tracker.createInstance<Inst_addr_alignContext>(_ctx, getState());
  enterRule(_localctx, 28, SystemRDLParser::RuleInst_addr_align);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(297);
    antlrcpp::downCast<Inst_addr_alignContext *>(_localctx)->op = match(SystemRDLParser::ALIGN);
    setState(298);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_inst_typeContext ------------------------------------------------------------------

SystemRDLParser::Component_inst_typeContext::Component_inst_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Component_inst_typeContext::EXTERNAL_kw() {
  return getToken(SystemRDLParser::EXTERNAL_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Component_inst_typeContext::INTERNAL_kw() {
  return getToken(SystemRDLParser::INTERNAL_kw, 0);
}


size_t SystemRDLParser::Component_inst_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_inst_type;
}


std::any SystemRDLParser::Component_inst_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_inst_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_inst_typeContext* SystemRDLParser::component_inst_type() {
  Component_inst_typeContext *_localctx = _tracker.createInstance<Component_inst_typeContext>(_ctx, getState());
  enterRule(_localctx, 30, SystemRDLParser::RuleComponent_inst_type);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(300);
    antlrcpp::downCast<Component_inst_typeContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!(_la == SystemRDLParser::EXTERNAL_kw

    || _la == SystemRDLParser::INTERNAL_kw)) {
      antlrcpp::downCast<Component_inst_typeContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_typeContext ------------------------------------------------------------------

SystemRDLParser::Component_typeContext::Component_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_type_primaryContext* SystemRDLParser::Component_typeContext::component_type_primary() {
  return getRuleContext<SystemRDLParser::Component_type_primaryContext>(0);
}

tree::TerminalNode* SystemRDLParser::Component_typeContext::SIGNAL_kw() {
  return getToken(SystemRDLParser::SIGNAL_kw, 0);
}


size_t SystemRDLParser::Component_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_type;
}


std::any SystemRDLParser::Component_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_typeContext* SystemRDLParser::component_type() {
  Component_typeContext *_localctx = _tracker.createInstance<Component_typeContext>(_ctx, getState());
  enterRule(_localctx, 32, SystemRDLParser::RuleComponent_type);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(304);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::ADDRMAP_kw:
      case SystemRDLParser::REGFILE_kw:
      case SystemRDLParser::REG_kw:
      case SystemRDLParser::FIELD_kw:
      case SystemRDLParser::MEM_kw: {
        enterOuterAlt(_localctx, 1);
        setState(302);
        component_type_primary();
        break;
      }

      case SystemRDLParser::SIGNAL_kw: {
        enterOuterAlt(_localctx, 2);
        setState(303);
        antlrcpp::downCast<Component_typeContext *>(_localctx)->kw = match(SystemRDLParser::SIGNAL_kw);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Component_type_primaryContext ------------------------------------------------------------------

SystemRDLParser::Component_type_primaryContext::Component_type_primaryContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Component_type_primaryContext::ADDRMAP_kw() {
  return getToken(SystemRDLParser::ADDRMAP_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Component_type_primaryContext::REGFILE_kw() {
  return getToken(SystemRDLParser::REGFILE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Component_type_primaryContext::REG_kw() {
  return getToken(SystemRDLParser::REG_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Component_type_primaryContext::FIELD_kw() {
  return getToken(SystemRDLParser::FIELD_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Component_type_primaryContext::MEM_kw() {
  return getToken(SystemRDLParser::MEM_kw, 0);
}


size_t SystemRDLParser::Component_type_primaryContext::getRuleIndex() const {
  return SystemRDLParser::RuleComponent_type_primary;
}


std::any SystemRDLParser::Component_type_primaryContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitComponent_type_primary(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Component_type_primaryContext* SystemRDLParser::component_type_primary() {
  Component_type_primaryContext *_localctx = _tracker.createInstance<Component_type_primaryContext>(_ctx, getState());
  enterRule(_localctx, 34, SystemRDLParser::RuleComponent_type_primary);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(306);
    antlrcpp::downCast<Component_type_primaryContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::ADDRMAP_kw)
      | (1ULL << SystemRDLParser::REGFILE_kw)
      | (1ULL << SystemRDLParser::REG_kw)
      | (1ULL << SystemRDLParser::FIELD_kw)
      | (1ULL << SystemRDLParser::MEM_kw))) != 0))) {
      antlrcpp::downCast<Component_type_primaryContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Param_defContext ------------------------------------------------------------------

SystemRDLParser::Param_defContext::Param_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::Param_def_elemContext *> SystemRDLParser::Param_defContext::param_def_elem() {
  return getRuleContexts<SystemRDLParser::Param_def_elemContext>();
}

SystemRDLParser::Param_def_elemContext* SystemRDLParser::Param_defContext::param_def_elem(size_t i) {
  return getRuleContext<SystemRDLParser::Param_def_elemContext>(i);
}


size_t SystemRDLParser::Param_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleParam_def;
}


std::any SystemRDLParser::Param_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitParam_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Param_defContext* SystemRDLParser::param_def() {
  Param_defContext *_localctx = _tracker.createInstance<Param_defContext>(_ctx, getState());
  enterRule(_localctx, 36, SystemRDLParser::RuleParam_def);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(308);
    match(SystemRDLParser::T__4);
    setState(309);
    match(SystemRDLParser::T__5);
    setState(310);
    param_def_elem();
    setState(315);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::T__3) {
      setState(311);
      match(SystemRDLParser::T__3);
      setState(312);
      param_def_elem();
      setState(317);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(318);
    match(SystemRDLParser::T__6);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Param_def_elemContext ------------------------------------------------------------------

SystemRDLParser::Param_def_elemContext::Param_def_elemContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Data_typeContext* SystemRDLParser::Param_def_elemContext::data_type() {
  return getRuleContext<SystemRDLParser::Data_typeContext>(0);
}

tree::TerminalNode* SystemRDLParser::Param_def_elemContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::Array_type_suffixContext* SystemRDLParser::Param_def_elemContext::array_type_suffix() {
  return getRuleContext<SystemRDLParser::Array_type_suffixContext>(0);
}

tree::TerminalNode* SystemRDLParser::Param_def_elemContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Param_def_elemContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Param_def_elemContext::getRuleIndex() const {
  return SystemRDLParser::RuleParam_def_elem;
}


std::any SystemRDLParser::Param_def_elemContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitParam_def_elem(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Param_def_elemContext* SystemRDLParser::param_def_elem() {
  Param_def_elemContext *_localctx = _tracker.createInstance<Param_def_elemContext>(_ctx, getState());
  enterRule(_localctx, 38, SystemRDLParser::RuleParam_def_elem);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(320);
    data_type();
    setState(321);
    match(SystemRDLParser::ID);
    setState(323);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::T__11) {
      setState(322);
      array_type_suffix();
    }
    setState(327);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::ASSIGN) {
      setState(325);
      match(SystemRDLParser::ASSIGN);
      setState(326);
      expr(0);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Param_instContext ------------------------------------------------------------------

SystemRDLParser::Param_instContext::Param_instContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::Param_assignmentContext *> SystemRDLParser::Param_instContext::param_assignment() {
  return getRuleContexts<SystemRDLParser::Param_assignmentContext>();
}

SystemRDLParser::Param_assignmentContext* SystemRDLParser::Param_instContext::param_assignment(size_t i) {
  return getRuleContext<SystemRDLParser::Param_assignmentContext>(i);
}


size_t SystemRDLParser::Param_instContext::getRuleIndex() const {
  return SystemRDLParser::RuleParam_inst;
}


std::any SystemRDLParser::Param_instContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitParam_inst(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Param_instContext* SystemRDLParser::param_inst() {
  Param_instContext *_localctx = _tracker.createInstance<Param_instContext>(_ctx, getState());
  enterRule(_localctx, 40, SystemRDLParser::RuleParam_inst);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(329);
    match(SystemRDLParser::T__4);
    setState(330);
    match(SystemRDLParser::T__5);
    setState(331);
    param_assignment();
    setState(336);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::T__3) {
      setState(332);
      match(SystemRDLParser::T__3);
      setState(333);
      param_assignment();
      setState(338);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(339);
    match(SystemRDLParser::T__6);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Param_assignmentContext ------------------------------------------------------------------

SystemRDLParser::Param_assignmentContext::Param_assignmentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Param_assignmentContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Param_assignmentContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Param_assignmentContext::getRuleIndex() const {
  return SystemRDLParser::RuleParam_assignment;
}


std::any SystemRDLParser::Param_assignmentContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitParam_assignment(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Param_assignmentContext* SystemRDLParser::param_assignment() {
  Param_assignmentContext *_localctx = _tracker.createInstance<Param_assignmentContext>(_ctx, getState());
  enterRule(_localctx, 42, SystemRDLParser::RuleParam_assignment);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(341);
    match(SystemRDLParser::T__7);
    setState(342);
    match(SystemRDLParser::ID);
    setState(343);
    match(SystemRDLParser::T__5);
    setState(344);
    expr(0);
    setState(345);
    match(SystemRDLParser::T__6);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExprContext ------------------------------------------------------------------

SystemRDLParser::ExprContext::ExprContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t SystemRDLParser::ExprContext::getRuleIndex() const {
  return SystemRDLParser::RuleExpr;
}

void SystemRDLParser::ExprContext::copyFrom(ExprContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- BinaryExprContext ------------------------------------------------------------------

std::vector<SystemRDLParser::ExprContext *> SystemRDLParser::BinaryExprContext::expr() {
  return getRuleContexts<SystemRDLParser::ExprContext>();
}

SystemRDLParser::ExprContext* SystemRDLParser::BinaryExprContext::expr(size_t i) {
  return getRuleContext<SystemRDLParser::ExprContext>(i);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::EXP() {
  return getToken(SystemRDLParser::EXP, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::MULT() {
  return getToken(SystemRDLParser::MULT, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::DIV() {
  return getToken(SystemRDLParser::DIV, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::MOD() {
  return getToken(SystemRDLParser::MOD, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::PLUS() {
  return getToken(SystemRDLParser::PLUS, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::MINUS() {
  return getToken(SystemRDLParser::MINUS, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::LSHIFT() {
  return getToken(SystemRDLParser::LSHIFT, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::RSHIFT() {
  return getToken(SystemRDLParser::RSHIFT, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::LT() {
  return getToken(SystemRDLParser::LT, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::LEQ() {
  return getToken(SystemRDLParser::LEQ, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::GT() {
  return getToken(SystemRDLParser::GT, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::GEQ() {
  return getToken(SystemRDLParser::GEQ, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::EQ() {
  return getToken(SystemRDLParser::EQ, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::NEQ() {
  return getToken(SystemRDLParser::NEQ, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::AND() {
  return getToken(SystemRDLParser::AND, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::XOR() {
  return getToken(SystemRDLParser::XOR, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::XNOR() {
  return getToken(SystemRDLParser::XNOR, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::OR() {
  return getToken(SystemRDLParser::OR, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::BAND() {
  return getToken(SystemRDLParser::BAND, 0);
}

tree::TerminalNode* SystemRDLParser::BinaryExprContext::BOR() {
  return getToken(SystemRDLParser::BOR, 0);
}

SystemRDLParser::BinaryExprContext::BinaryExprContext(ExprContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::BinaryExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitBinaryExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- UnaryExprContext ------------------------------------------------------------------

SystemRDLParser::Expr_primaryContext* SystemRDLParser::UnaryExprContext::expr_primary() {
  return getRuleContext<SystemRDLParser::Expr_primaryContext>(0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::PLUS() {
  return getToken(SystemRDLParser::PLUS, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::MINUS() {
  return getToken(SystemRDLParser::MINUS, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::BNOT() {
  return getToken(SystemRDLParser::BNOT, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::NOT() {
  return getToken(SystemRDLParser::NOT, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::AND() {
  return getToken(SystemRDLParser::AND, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::NAND() {
  return getToken(SystemRDLParser::NAND, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::OR() {
  return getToken(SystemRDLParser::OR, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::NOR() {
  return getToken(SystemRDLParser::NOR, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::XOR() {
  return getToken(SystemRDLParser::XOR, 0);
}

tree::TerminalNode* SystemRDLParser::UnaryExprContext::XNOR() {
  return getToken(SystemRDLParser::XNOR, 0);
}

SystemRDLParser::UnaryExprContext::UnaryExprContext(ExprContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::UnaryExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUnaryExpr(this);
  else
    return visitor->visitChildren(this);
}
//----------------- NOPContext ------------------------------------------------------------------

SystemRDLParser::Expr_primaryContext* SystemRDLParser::NOPContext::expr_primary() {
  return getRuleContext<SystemRDLParser::Expr_primaryContext>(0);
}

SystemRDLParser::NOPContext::NOPContext(ExprContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::NOPContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitNOP(this);
  else
    return visitor->visitChildren(this);
}
//----------------- TernaryExprContext ------------------------------------------------------------------

std::vector<SystemRDLParser::ExprContext *> SystemRDLParser::TernaryExprContext::expr() {
  return getRuleContexts<SystemRDLParser::ExprContext>();
}

SystemRDLParser::ExprContext* SystemRDLParser::TernaryExprContext::expr(size_t i) {
  return getRuleContext<SystemRDLParser::ExprContext>(i);
}

SystemRDLParser::TernaryExprContext::TernaryExprContext(ExprContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::TernaryExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitTernaryExpr(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::ExprContext* SystemRDLParser::expr() {
   return expr(0);
}

SystemRDLParser::ExprContext* SystemRDLParser::expr(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  SystemRDLParser::ExprContext *_localctx = _tracker.createInstance<ExprContext>(_ctx, parentState);
  SystemRDLParser::ExprContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 44;
  enterRecursionRule(_localctx, 44, SystemRDLParser::RuleExpr, precedence);

    size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    unrollRecursionContexts(parentContext);
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(351);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::PLUS:
      case SystemRDLParser::MINUS:
      case SystemRDLParser::BNOT:
      case SystemRDLParser::NOT:
      case SystemRDLParser::NAND:
      case SystemRDLParser::AND:
      case SystemRDLParser::OR:
      case SystemRDLParser::NOR:
      case SystemRDLParser::XOR:
      case SystemRDLParser::XNOR: {
        _localctx = _tracker.createInstance<UnaryExprContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;

        setState(348);
        antlrcpp::downCast<UnaryExprContext *>(_localctx)->op = _input->LT(1);
        _la = _input->LA(1);
        if (!(((((_la - 96) & ~ 0x3fULL) == 0) &&
          ((1ULL << (_la - 96)) & ((1ULL << (SystemRDLParser::PLUS - 96))
          | (1ULL << (SystemRDLParser::MINUS - 96))
          | (1ULL << (SystemRDLParser::BNOT - 96))
          | (1ULL << (SystemRDLParser::NOT - 96))
          | (1ULL << (SystemRDLParser::NAND - 96))
          | (1ULL << (SystemRDLParser::AND - 96))
          | (1ULL << (SystemRDLParser::OR - 96))
          | (1ULL << (SystemRDLParser::NOR - 96))
          | (1ULL << (SystemRDLParser::XOR - 96))
          | (1ULL << (SystemRDLParser::XNOR - 96)))) != 0))) {
          antlrcpp::downCast<UnaryExprContext *>(_localctx)->op = _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        setState(349);
        expr_primary();
        break;
      }

      case SystemRDLParser::T__1:
      case SystemRDLParser::T__5:
      case SystemRDLParser::T__10:
      case SystemRDLParser::BOOLEAN_kw:
      case SystemRDLParser::BIT_kw:
      case SystemRDLParser::LONGINT_kw:
      case SystemRDLParser::TRUE_kw:
      case SystemRDLParser::FALSE_kw:
      case SystemRDLParser::NA_kw:
      case SystemRDLParser::RW_kw:
      case SystemRDLParser::WR_kw:
      case SystemRDLParser::R_kw:
      case SystemRDLParser::W_kw:
      case SystemRDLParser::RW1_kw:
      case SystemRDLParser::W1_kw:
      case SystemRDLParser::RCLR_kw:
      case SystemRDLParser::RSET_kw:
      case SystemRDLParser::RUSER_kw:
      case SystemRDLParser::WOSET_kw:
      case SystemRDLParser::WOCLR_kw:
      case SystemRDLParser::WOT_kw:
      case SystemRDLParser::WZS_kw:
      case SystemRDLParser::WZC_kw:
      case SystemRDLParser::WZT_kw:
      case SystemRDLParser::WCLR_kw:
      case SystemRDLParser::WSET_kw:
      case SystemRDLParser::WUSER_kw:
      case SystemRDLParser::COMPACT_kw:
      case SystemRDLParser::REGALIGN_kw:
      case SystemRDLParser::FULLALIGN_kw:
      case SystemRDLParser::HW_kw:
      case SystemRDLParser::SW_kw:
      case SystemRDLParser::INT:
      case SystemRDLParser::HEX_INT:
      case SystemRDLParser::VLOG_INT:
      case SystemRDLParser::STRING:
      case SystemRDLParser::ID: {
        _localctx = _tracker.createInstance<NOPContext>(_localctx);
        _ctx = _localctx;
        previousContext = _localctx;
        setState(350);
        expr_primary();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
    _ctx->stop = _input->LT(-1);
    setState(394);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 26, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        setState(392);
        _errHandler->sync(this);
        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 25, _ctx)) {
        case 1: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(353);

          if (!(precpred(_ctx, 13))) throw FailedPredicateException(this, "precpred(_ctx, 13)");
          setState(354);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = match(SystemRDLParser::EXP);
          setState(355);
          expr(14);
          break;
        }

        case 2: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(356);

          if (!(precpred(_ctx, 12))) throw FailedPredicateException(this, "precpred(_ctx, 12)");
          setState(357);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 110) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 110)) & ((1ULL << (SystemRDLParser::MULT - 110))
            | (1ULL << (SystemRDLParser::DIV - 110))
            | (1ULL << (SystemRDLParser::MOD - 110)))) != 0))) {
            antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(358);
          expr(13);
          break;
        }

        case 3: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(359);

          if (!(precpred(_ctx, 11))) throw FailedPredicateException(this, "precpred(_ctx, 11)");
          setState(360);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == SystemRDLParser::PLUS

          || _la == SystemRDLParser::MINUS)) {
            antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(361);
          expr(12);
          break;
        }

        case 4: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(362);

          if (!(precpred(_ctx, 10))) throw FailedPredicateException(this, "precpred(_ctx, 10)");
          setState(363);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == SystemRDLParser::LSHIFT

          || _la == SystemRDLParser::RSHIFT)) {
            antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(364);
          expr(11);
          break;
        }

        case 5: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(365);

          if (!(precpred(_ctx, 9))) throw FailedPredicateException(this, "precpred(_ctx, 9)");
          setState(366);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _input->LT(1);
          _la = _input->LA(1);
          if (!(((((_la - 117) & ~ 0x3fULL) == 0) &&
            ((1ULL << (_la - 117)) & ((1ULL << (SystemRDLParser::LEQ - 117))
            | (1ULL << (SystemRDLParser::LT - 117))
            | (1ULL << (SystemRDLParser::GEQ - 117))
            | (1ULL << (SystemRDLParser::GT - 117)))) != 0))) {
            antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(367);
          expr(10);
          break;
        }

        case 6: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(368);

          if (!(precpred(_ctx, 8))) throw FailedPredicateException(this, "precpred(_ctx, 8)");
          setState(369);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == SystemRDLParser::EQ

          || _la == SystemRDLParser::NEQ)) {
            antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(370);
          expr(9);
          break;
        }

        case 7: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(371);

          if (!(precpred(_ctx, 7))) throw FailedPredicateException(this, "precpred(_ctx, 7)");
          setState(372);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = match(SystemRDLParser::AND);
          setState(373);
          expr(8);
          break;
        }

        case 8: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(374);

          if (!(precpred(_ctx, 6))) throw FailedPredicateException(this, "precpred(_ctx, 6)");
          setState(375);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _input->LT(1);
          _la = _input->LA(1);
          if (!(_la == SystemRDLParser::XOR

          || _la == SystemRDLParser::XNOR)) {
            antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = _errHandler->recoverInline(this);
          }
          else {
            _errHandler->reportMatch(this);
            consume();
          }
          setState(376);
          expr(7);
          break;
        }

        case 9: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(377);

          if (!(precpred(_ctx, 5))) throw FailedPredicateException(this, "precpred(_ctx, 5)");
          setState(378);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = match(SystemRDLParser::OR);
          setState(379);
          expr(6);
          break;
        }

        case 10: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(380);

          if (!(precpred(_ctx, 4))) throw FailedPredicateException(this, "precpred(_ctx, 4)");
          setState(381);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = match(SystemRDLParser::BAND);
          setState(382);
          expr(5);
          break;
        }

        case 11: {
          auto newContext = _tracker.createInstance<BinaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(383);

          if (!(precpred(_ctx, 3))) throw FailedPredicateException(this, "precpred(_ctx, 3)");
          setState(384);
          antlrcpp::downCast<BinaryExprContext *>(_localctx)->op = match(SystemRDLParser::BOR);
          setState(385);
          expr(4);
          break;
        }

        case 12: {
          auto newContext = _tracker.createInstance<TernaryExprContext>(_tracker.createInstance<ExprContext>(parentContext, parentState));
          _localctx = newContext;
          pushNewRecursionContext(newContext, startState, RuleExpr);
          setState(386);

          if (!(precpred(_ctx, 2))) throw FailedPredicateException(this, "precpred(_ctx, 2)");
          setState(387);
          antlrcpp::downCast<TernaryExprContext *>(_localctx)->op = match(SystemRDLParser::T__8);
          setState(388);
          expr(0);
          setState(389);
          match(SystemRDLParser::T__9);
          setState(390);
          expr(2);
          break;
        }

        default:
          break;
        } 
      }
      setState(396);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 26, _ctx);
    }
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }
  return _localctx;
}

//----------------- Expr_primaryContext ------------------------------------------------------------------

SystemRDLParser::Expr_primaryContext::Expr_primaryContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::LiteralContext* SystemRDLParser::Expr_primaryContext::literal() {
  return getRuleContext<SystemRDLParser::LiteralContext>(0);
}

SystemRDLParser::ConcatenateContext* SystemRDLParser::Expr_primaryContext::concatenate() {
  return getRuleContext<SystemRDLParser::ConcatenateContext>(0);
}

SystemRDLParser::ReplicateContext* SystemRDLParser::Expr_primaryContext::replicate() {
  return getRuleContext<SystemRDLParser::ReplicateContext>(0);
}

SystemRDLParser::Paren_exprContext* SystemRDLParser::Expr_primaryContext::paren_expr() {
  return getRuleContext<SystemRDLParser::Paren_exprContext>(0);
}

SystemRDLParser::CastContext* SystemRDLParser::Expr_primaryContext::cast() {
  return getRuleContext<SystemRDLParser::CastContext>(0);
}

SystemRDLParser::Prop_refContext* SystemRDLParser::Expr_primaryContext::prop_ref() {
  return getRuleContext<SystemRDLParser::Prop_refContext>(0);
}

SystemRDLParser::Instance_refContext* SystemRDLParser::Expr_primaryContext::instance_ref() {
  return getRuleContext<SystemRDLParser::Instance_refContext>(0);
}

SystemRDLParser::Struct_literalContext* SystemRDLParser::Expr_primaryContext::struct_literal() {
  return getRuleContext<SystemRDLParser::Struct_literalContext>(0);
}

SystemRDLParser::Array_literalContext* SystemRDLParser::Expr_primaryContext::array_literal() {
  return getRuleContext<SystemRDLParser::Array_literalContext>(0);
}


size_t SystemRDLParser::Expr_primaryContext::getRuleIndex() const {
  return SystemRDLParser::RuleExpr_primary;
}


std::any SystemRDLParser::Expr_primaryContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitExpr_primary(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Expr_primaryContext* SystemRDLParser::expr_primary() {
  Expr_primaryContext *_localctx = _tracker.createInstance<Expr_primaryContext>(_ctx, getState());
  enterRule(_localctx, 46, SystemRDLParser::RuleExpr_primary);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(406);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 27, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(397);
      literal();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(398);
      concatenate();
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(399);
      replicate();
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(400);
      paren_expr();
      break;
    }

    case 5: {
      enterOuterAlt(_localctx, 5);
      setState(401);
      cast();
      break;
    }

    case 6: {
      enterOuterAlt(_localctx, 6);
      setState(402);
      prop_ref();
      break;
    }

    case 7: {
      enterOuterAlt(_localctx, 7);
      setState(403);
      instance_ref();
      break;
    }

    case 8: {
      enterOuterAlt(_localctx, 8);
      setState(404);
      struct_literal();
      break;
    }

    case 9: {
      enterOuterAlt(_localctx, 9);
      setState(405);
      array_literal();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConcatenateContext ------------------------------------------------------------------

SystemRDLParser::ConcatenateContext::ConcatenateContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::ExprContext *> SystemRDLParser::ConcatenateContext::expr() {
  return getRuleContexts<SystemRDLParser::ExprContext>();
}

SystemRDLParser::ExprContext* SystemRDLParser::ConcatenateContext::expr(size_t i) {
  return getRuleContext<SystemRDLParser::ExprContext>(i);
}


size_t SystemRDLParser::ConcatenateContext::getRuleIndex() const {
  return SystemRDLParser::RuleConcatenate;
}


std::any SystemRDLParser::ConcatenateContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConcatenate(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::ConcatenateContext* SystemRDLParser::concatenate() {
  ConcatenateContext *_localctx = _tracker.createInstance<ConcatenateContext>(_ctx, getState());
  enterRule(_localctx, 48, SystemRDLParser::RuleConcatenate);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(408);
    match(SystemRDLParser::T__1);
    setState(409);
    expr(0);
    setState(414);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::T__3) {
      setState(410);
      match(SystemRDLParser::T__3);
      setState(411);
      expr(0);
      setState(416);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(417);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ReplicateContext ------------------------------------------------------------------

SystemRDLParser::ReplicateContext::ReplicateContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::ExprContext* SystemRDLParser::ReplicateContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

SystemRDLParser::ConcatenateContext* SystemRDLParser::ReplicateContext::concatenate() {
  return getRuleContext<SystemRDLParser::ConcatenateContext>(0);
}


size_t SystemRDLParser::ReplicateContext::getRuleIndex() const {
  return SystemRDLParser::RuleReplicate;
}


std::any SystemRDLParser::ReplicateContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitReplicate(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::ReplicateContext* SystemRDLParser::replicate() {
  ReplicateContext *_localctx = _tracker.createInstance<ReplicateContext>(_ctx, getState());
  enterRule(_localctx, 50, SystemRDLParser::RuleReplicate);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(419);
    match(SystemRDLParser::T__1);
    setState(420);
    expr(0);
    setState(421);
    concatenate();
    setState(422);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Paren_exprContext ------------------------------------------------------------------

SystemRDLParser::Paren_exprContext::Paren_exprContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::ExprContext* SystemRDLParser::Paren_exprContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Paren_exprContext::getRuleIndex() const {
  return SystemRDLParser::RuleParen_expr;
}


std::any SystemRDLParser::Paren_exprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitParen_expr(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Paren_exprContext* SystemRDLParser::paren_expr() {
  Paren_exprContext *_localctx = _tracker.createInstance<Paren_exprContext>(_ctx, getState());
  enterRule(_localctx, 52, SystemRDLParser::RuleParen_expr);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(424);
    match(SystemRDLParser::T__5);
    setState(425);
    expr(0);
    setState(426);
    match(SystemRDLParser::T__6);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- CastContext ------------------------------------------------------------------

SystemRDLParser::CastContext::CastContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t SystemRDLParser::CastContext::getRuleIndex() const {
  return SystemRDLParser::RuleCast;
}

void SystemRDLParser::CastContext::copyFrom(CastContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- CastWidthContext ------------------------------------------------------------------

SystemRDLParser::Cast_width_exprContext* SystemRDLParser::CastWidthContext::cast_width_expr() {
  return getRuleContext<SystemRDLParser::Cast_width_exprContext>(0);
}

SystemRDLParser::ExprContext* SystemRDLParser::CastWidthContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

SystemRDLParser::CastWidthContext::CastWidthContext(CastContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::CastWidthContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitCastWidth(this);
  else
    return visitor->visitChildren(this);
}
//----------------- CastTypeContext ------------------------------------------------------------------

SystemRDLParser::ExprContext* SystemRDLParser::CastTypeContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

tree::TerminalNode* SystemRDLParser::CastTypeContext::BOOLEAN_kw() {
  return getToken(SystemRDLParser::BOOLEAN_kw, 0);
}

tree::TerminalNode* SystemRDLParser::CastTypeContext::BIT_kw() {
  return getToken(SystemRDLParser::BIT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::CastTypeContext::LONGINT_kw() {
  return getToken(SystemRDLParser::LONGINT_kw, 0);
}

SystemRDLParser::CastTypeContext::CastTypeContext(CastContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::CastTypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitCastType(this);
  else
    return visitor->visitChildren(this);
}
SystemRDLParser::CastContext* SystemRDLParser::cast() {
  CastContext *_localctx = _tracker.createInstance<CastContext>(_ctx, getState());
  enterRule(_localctx, 54, SystemRDLParser::RuleCast);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(440);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::BOOLEAN_kw:
      case SystemRDLParser::BIT_kw:
      case SystemRDLParser::LONGINT_kw: {
        _localctx = _tracker.createInstance<SystemRDLParser::CastTypeContext>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(428);
        antlrcpp::downCast<CastTypeContext *>(_localctx)->typ = _input->LT(1);
        _la = _input->LA(1);
        if (!((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << SystemRDLParser::BOOLEAN_kw)
          | (1ULL << SystemRDLParser::BIT_kw)
          | (1ULL << SystemRDLParser::LONGINT_kw))) != 0))) {
          antlrcpp::downCast<CastTypeContext *>(_localctx)->typ = _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        setState(429);
        antlrcpp::downCast<CastTypeContext *>(_localctx)->op = match(SystemRDLParser::T__10);
        setState(430);
        match(SystemRDLParser::T__5);
        setState(431);
        expr(0);
        setState(432);
        match(SystemRDLParser::T__6);
        break;
      }

      case SystemRDLParser::T__5:
      case SystemRDLParser::TRUE_kw:
      case SystemRDLParser::FALSE_kw:
      case SystemRDLParser::NA_kw:
      case SystemRDLParser::RW_kw:
      case SystemRDLParser::WR_kw:
      case SystemRDLParser::R_kw:
      case SystemRDLParser::W_kw:
      case SystemRDLParser::RW1_kw:
      case SystemRDLParser::W1_kw:
      case SystemRDLParser::RCLR_kw:
      case SystemRDLParser::RSET_kw:
      case SystemRDLParser::RUSER_kw:
      case SystemRDLParser::WOSET_kw:
      case SystemRDLParser::WOCLR_kw:
      case SystemRDLParser::WOT_kw:
      case SystemRDLParser::WZS_kw:
      case SystemRDLParser::WZC_kw:
      case SystemRDLParser::WZT_kw:
      case SystemRDLParser::WCLR_kw:
      case SystemRDLParser::WSET_kw:
      case SystemRDLParser::WUSER_kw:
      case SystemRDLParser::COMPACT_kw:
      case SystemRDLParser::REGALIGN_kw:
      case SystemRDLParser::FULLALIGN_kw:
      case SystemRDLParser::HW_kw:
      case SystemRDLParser::SW_kw:
      case SystemRDLParser::INT:
      case SystemRDLParser::HEX_INT:
      case SystemRDLParser::VLOG_INT:
      case SystemRDLParser::STRING:
      case SystemRDLParser::ID: {
        _localctx = _tracker.createInstance<SystemRDLParser::CastWidthContext>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(434);
        cast_width_expr();
        setState(435);
        antlrcpp::downCast<CastWidthContext *>(_localctx)->op = match(SystemRDLParser::T__10);
        setState(436);
        match(SystemRDLParser::T__5);
        setState(437);
        expr(0);
        setState(438);
        match(SystemRDLParser::T__6);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Cast_width_exprContext ------------------------------------------------------------------

SystemRDLParser::Cast_width_exprContext::Cast_width_exprContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::LiteralContext* SystemRDLParser::Cast_width_exprContext::literal() {
  return getRuleContext<SystemRDLParser::LiteralContext>(0);
}

SystemRDLParser::Paren_exprContext* SystemRDLParser::Cast_width_exprContext::paren_expr() {
  return getRuleContext<SystemRDLParser::Paren_exprContext>(0);
}


size_t SystemRDLParser::Cast_width_exprContext::getRuleIndex() const {
  return SystemRDLParser::RuleCast_width_expr;
}


std::any SystemRDLParser::Cast_width_exprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitCast_width_expr(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Cast_width_exprContext* SystemRDLParser::cast_width_expr() {
  Cast_width_exprContext *_localctx = _tracker.createInstance<Cast_width_exprContext>(_ctx, getState());
  enterRule(_localctx, 56, SystemRDLParser::RuleCast_width_expr);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(444);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::TRUE_kw:
      case SystemRDLParser::FALSE_kw:
      case SystemRDLParser::NA_kw:
      case SystemRDLParser::RW_kw:
      case SystemRDLParser::WR_kw:
      case SystemRDLParser::R_kw:
      case SystemRDLParser::W_kw:
      case SystemRDLParser::RW1_kw:
      case SystemRDLParser::W1_kw:
      case SystemRDLParser::RCLR_kw:
      case SystemRDLParser::RSET_kw:
      case SystemRDLParser::RUSER_kw:
      case SystemRDLParser::WOSET_kw:
      case SystemRDLParser::WOCLR_kw:
      case SystemRDLParser::WOT_kw:
      case SystemRDLParser::WZS_kw:
      case SystemRDLParser::WZC_kw:
      case SystemRDLParser::WZT_kw:
      case SystemRDLParser::WCLR_kw:
      case SystemRDLParser::WSET_kw:
      case SystemRDLParser::WUSER_kw:
      case SystemRDLParser::COMPACT_kw:
      case SystemRDLParser::REGALIGN_kw:
      case SystemRDLParser::FULLALIGN_kw:
      case SystemRDLParser::HW_kw:
      case SystemRDLParser::SW_kw:
      case SystemRDLParser::INT:
      case SystemRDLParser::HEX_INT:
      case SystemRDLParser::VLOG_INT:
      case SystemRDLParser::STRING:
      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 1);
        setState(442);
        literal();
        break;
      }

      case SystemRDLParser::T__5: {
        enterOuterAlt(_localctx, 2);
        setState(443);
        paren_expr();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Range_suffixContext ------------------------------------------------------------------

SystemRDLParser::Range_suffixContext::Range_suffixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::ExprContext *> SystemRDLParser::Range_suffixContext::expr() {
  return getRuleContexts<SystemRDLParser::ExprContext>();
}

SystemRDLParser::ExprContext* SystemRDLParser::Range_suffixContext::expr(size_t i) {
  return getRuleContext<SystemRDLParser::ExprContext>(i);
}


size_t SystemRDLParser::Range_suffixContext::getRuleIndex() const {
  return SystemRDLParser::RuleRange_suffix;
}


std::any SystemRDLParser::Range_suffixContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitRange_suffix(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Range_suffixContext* SystemRDLParser::range_suffix() {
  Range_suffixContext *_localctx = _tracker.createInstance<Range_suffixContext>(_ctx, getState());
  enterRule(_localctx, 58, SystemRDLParser::RuleRange_suffix);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(446);
    match(SystemRDLParser::T__11);
    setState(447);
    expr(0);
    setState(448);
    match(SystemRDLParser::T__9);
    setState(449);
    expr(0);
    setState(450);
    match(SystemRDLParser::T__12);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Array_suffixContext ------------------------------------------------------------------

SystemRDLParser::Array_suffixContext::Array_suffixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::ExprContext* SystemRDLParser::Array_suffixContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Array_suffixContext::getRuleIndex() const {
  return SystemRDLParser::RuleArray_suffix;
}


std::any SystemRDLParser::Array_suffixContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitArray_suffix(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Array_suffixContext* SystemRDLParser::array_suffix() {
  Array_suffixContext *_localctx = _tracker.createInstance<Array_suffixContext>(_ctx, getState());
  enterRule(_localctx, 60, SystemRDLParser::RuleArray_suffix);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(452);
    match(SystemRDLParser::T__11);
    setState(453);
    expr(0);
    setState(454);
    match(SystemRDLParser::T__12);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Array_type_suffixContext ------------------------------------------------------------------

SystemRDLParser::Array_type_suffixContext::Array_type_suffixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t SystemRDLParser::Array_type_suffixContext::getRuleIndex() const {
  return SystemRDLParser::RuleArray_type_suffix;
}


std::any SystemRDLParser::Array_type_suffixContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitArray_type_suffix(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Array_type_suffixContext* SystemRDLParser::array_type_suffix() {
  Array_type_suffixContext *_localctx = _tracker.createInstance<Array_type_suffixContext>(_ctx, getState());
  enterRule(_localctx, 62, SystemRDLParser::RuleArray_type_suffix);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(456);
    match(SystemRDLParser::T__11);
    setState(457);
    match(SystemRDLParser::T__12);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Data_typeContext ------------------------------------------------------------------

SystemRDLParser::Data_typeContext::Data_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Basic_data_typeContext* SystemRDLParser::Data_typeContext::basic_data_type() {
  return getRuleContext<SystemRDLParser::Basic_data_typeContext>(0);
}

tree::TerminalNode* SystemRDLParser::Data_typeContext::ACCESSTYPE_kw() {
  return getToken(SystemRDLParser::ACCESSTYPE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Data_typeContext::ADDRESSINGTYPE_kw() {
  return getToken(SystemRDLParser::ADDRESSINGTYPE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Data_typeContext::ONREADTYPE_kw() {
  return getToken(SystemRDLParser::ONREADTYPE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Data_typeContext::ONWRITETYPE_kw() {
  return getToken(SystemRDLParser::ONWRITETYPE_kw, 0);
}


size_t SystemRDLParser::Data_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleData_type;
}


std::any SystemRDLParser::Data_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitData_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Data_typeContext* SystemRDLParser::data_type() {
  Data_typeContext *_localctx = _tracker.createInstance<Data_typeContext>(_ctx, getState());
  enterRule(_localctx, 64, SystemRDLParser::RuleData_type);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(461);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::BOOLEAN_kw:
      case SystemRDLParser::BIT_kw:
      case SystemRDLParser::LONGINT_kw:
      case SystemRDLParser::STRING_kw:
      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 1);
        setState(459);
        basic_data_type();
        break;
      }

      case SystemRDLParser::ACCESSTYPE_kw:
      case SystemRDLParser::ADDRESSINGTYPE_kw:
      case SystemRDLParser::ONREADTYPE_kw:
      case SystemRDLParser::ONWRITETYPE_kw: {
        enterOuterAlt(_localctx, 2);
        setState(460);
        antlrcpp::downCast<Data_typeContext *>(_localctx)->kw = _input->LT(1);
        _la = _input->LA(1);
        if (!((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & ((1ULL << SystemRDLParser::ACCESSTYPE_kw)
          | (1ULL << SystemRDLParser::ADDRESSINGTYPE_kw)
          | (1ULL << SystemRDLParser::ONREADTYPE_kw)
          | (1ULL << SystemRDLParser::ONWRITETYPE_kw))) != 0))) {
          antlrcpp::downCast<Data_typeContext *>(_localctx)->kw = _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Basic_data_typeContext ------------------------------------------------------------------

SystemRDLParser::Basic_data_typeContext::Basic_data_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Basic_data_typeContext::BIT_kw() {
  return getToken(SystemRDLParser::BIT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Basic_data_typeContext::LONGINT_kw() {
  return getToken(SystemRDLParser::LONGINT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Basic_data_typeContext::UNSIGNED_kw() {
  return getToken(SystemRDLParser::UNSIGNED_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Basic_data_typeContext::STRING_kw() {
  return getToken(SystemRDLParser::STRING_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Basic_data_typeContext::BOOLEAN_kw() {
  return getToken(SystemRDLParser::BOOLEAN_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Basic_data_typeContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}


size_t SystemRDLParser::Basic_data_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleBasic_data_type;
}


std::any SystemRDLParser::Basic_data_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitBasic_data_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Basic_data_typeContext* SystemRDLParser::basic_data_type() {
  Basic_data_typeContext *_localctx = _tracker.createInstance<Basic_data_typeContext>(_ctx, getState());
  enterRule(_localctx, 66, SystemRDLParser::RuleBasic_data_type);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(468);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::BIT_kw:
      case SystemRDLParser::LONGINT_kw: {
        enterOuterAlt(_localctx, 1);
        setState(463);
        antlrcpp::downCast<Basic_data_typeContext *>(_localctx)->kw = _input->LT(1);
        _la = _input->LA(1);
        if (!(_la == SystemRDLParser::BIT_kw

        || _la == SystemRDLParser::LONGINT_kw)) {
          antlrcpp::downCast<Basic_data_typeContext *>(_localctx)->kw = _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        setState(465);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if (_la == SystemRDLParser::UNSIGNED_kw) {
          setState(464);
          match(SystemRDLParser::UNSIGNED_kw);
        }
        break;
      }

      case SystemRDLParser::BOOLEAN_kw:
      case SystemRDLParser::STRING_kw:
      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 2);
        setState(467);
        antlrcpp::downCast<Basic_data_typeContext *>(_localctx)->kw = _input->LT(1);
        _la = _input->LA(1);
        if (!(_la == SystemRDLParser::BOOLEAN_kw

        || _la == SystemRDLParser::STRING_kw || _la == SystemRDLParser::ID)) {
          antlrcpp::downCast<Basic_data_typeContext *>(_localctx)->kw = _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LiteralContext ------------------------------------------------------------------

SystemRDLParser::LiteralContext::LiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::NumberContext* SystemRDLParser::LiteralContext::number() {
  return getRuleContext<SystemRDLParser::NumberContext>(0);
}

SystemRDLParser::String_literalContext* SystemRDLParser::LiteralContext::string_literal() {
  return getRuleContext<SystemRDLParser::String_literalContext>(0);
}

SystemRDLParser::Boolean_literalContext* SystemRDLParser::LiteralContext::boolean_literal() {
  return getRuleContext<SystemRDLParser::Boolean_literalContext>(0);
}

SystemRDLParser::Accesstype_literalContext* SystemRDLParser::LiteralContext::accesstype_literal() {
  return getRuleContext<SystemRDLParser::Accesstype_literalContext>(0);
}

SystemRDLParser::Onreadtype_literalContext* SystemRDLParser::LiteralContext::onreadtype_literal() {
  return getRuleContext<SystemRDLParser::Onreadtype_literalContext>(0);
}

SystemRDLParser::Onwritetype_literalContext* SystemRDLParser::LiteralContext::onwritetype_literal() {
  return getRuleContext<SystemRDLParser::Onwritetype_literalContext>(0);
}

SystemRDLParser::Addressingtype_literalContext* SystemRDLParser::LiteralContext::addressingtype_literal() {
  return getRuleContext<SystemRDLParser::Addressingtype_literalContext>(0);
}

SystemRDLParser::Precedencetype_literalContext* SystemRDLParser::LiteralContext::precedencetype_literal() {
  return getRuleContext<SystemRDLParser::Precedencetype_literalContext>(0);
}

SystemRDLParser::Enum_literalContext* SystemRDLParser::LiteralContext::enum_literal() {
  return getRuleContext<SystemRDLParser::Enum_literalContext>(0);
}


size_t SystemRDLParser::LiteralContext::getRuleIndex() const {
  return SystemRDLParser::RuleLiteral;
}


std::any SystemRDLParser::LiteralContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitLiteral(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::LiteralContext* SystemRDLParser::literal() {
  LiteralContext *_localctx = _tracker.createInstance<LiteralContext>(_ctx, getState());
  enterRule(_localctx, 68, SystemRDLParser::RuleLiteral);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(479);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::INT:
      case SystemRDLParser::HEX_INT:
      case SystemRDLParser::VLOG_INT: {
        enterOuterAlt(_localctx, 1);
        setState(470);
        number();
        break;
      }

      case SystemRDLParser::STRING: {
        enterOuterAlt(_localctx, 2);
        setState(471);
        string_literal();
        break;
      }

      case SystemRDLParser::TRUE_kw:
      case SystemRDLParser::FALSE_kw: {
        enterOuterAlt(_localctx, 3);
        setState(472);
        boolean_literal();
        break;
      }

      case SystemRDLParser::NA_kw:
      case SystemRDLParser::RW_kw:
      case SystemRDLParser::WR_kw:
      case SystemRDLParser::R_kw:
      case SystemRDLParser::W_kw:
      case SystemRDLParser::RW1_kw:
      case SystemRDLParser::W1_kw: {
        enterOuterAlt(_localctx, 4);
        setState(473);
        accesstype_literal();
        break;
      }

      case SystemRDLParser::RCLR_kw:
      case SystemRDLParser::RSET_kw:
      case SystemRDLParser::RUSER_kw: {
        enterOuterAlt(_localctx, 5);
        setState(474);
        onreadtype_literal();
        break;
      }

      case SystemRDLParser::WOSET_kw:
      case SystemRDLParser::WOCLR_kw:
      case SystemRDLParser::WOT_kw:
      case SystemRDLParser::WZS_kw:
      case SystemRDLParser::WZC_kw:
      case SystemRDLParser::WZT_kw:
      case SystemRDLParser::WCLR_kw:
      case SystemRDLParser::WSET_kw:
      case SystemRDLParser::WUSER_kw: {
        enterOuterAlt(_localctx, 6);
        setState(475);
        onwritetype_literal();
        break;
      }

      case SystemRDLParser::COMPACT_kw:
      case SystemRDLParser::REGALIGN_kw:
      case SystemRDLParser::FULLALIGN_kw: {
        enterOuterAlt(_localctx, 7);
        setState(476);
        addressingtype_literal();
        break;
      }

      case SystemRDLParser::HW_kw:
      case SystemRDLParser::SW_kw: {
        enterOuterAlt(_localctx, 8);
        setState(477);
        precedencetype_literal();
        break;
      }

      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 9);
        setState(478);
        enum_literal();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- NumberContext ------------------------------------------------------------------

SystemRDLParser::NumberContext::NumberContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t SystemRDLParser::NumberContext::getRuleIndex() const {
  return SystemRDLParser::RuleNumber;
}

void SystemRDLParser::NumberContext::copyFrom(NumberContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- NumberHexContext ------------------------------------------------------------------

tree::TerminalNode* SystemRDLParser::NumberHexContext::HEX_INT() {
  return getToken(SystemRDLParser::HEX_INT, 0);
}

SystemRDLParser::NumberHexContext::NumberHexContext(NumberContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::NumberHexContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitNumberHex(this);
  else
    return visitor->visitChildren(this);
}
//----------------- NumberVerilogContext ------------------------------------------------------------------

tree::TerminalNode* SystemRDLParser::NumberVerilogContext::VLOG_INT() {
  return getToken(SystemRDLParser::VLOG_INT, 0);
}

SystemRDLParser::NumberVerilogContext::NumberVerilogContext(NumberContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::NumberVerilogContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitNumberVerilog(this);
  else
    return visitor->visitChildren(this);
}
//----------------- NumberIntContext ------------------------------------------------------------------

tree::TerminalNode* SystemRDLParser::NumberIntContext::INT() {
  return getToken(SystemRDLParser::INT, 0);
}

SystemRDLParser::NumberIntContext::NumberIntContext(NumberContext *ctx) { copyFrom(ctx); }


std::any SystemRDLParser::NumberIntContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitNumberInt(this);
  else
    return visitor->visitChildren(this);
}
SystemRDLParser::NumberContext* SystemRDLParser::number() {
  NumberContext *_localctx = _tracker.createInstance<NumberContext>(_ctx, getState());
  enterRule(_localctx, 70, SystemRDLParser::RuleNumber);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(484);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::INT: {
        _localctx = _tracker.createInstance<SystemRDLParser::NumberIntContext>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(481);
        match(SystemRDLParser::INT);
        break;
      }

      case SystemRDLParser::HEX_INT: {
        _localctx = _tracker.createInstance<SystemRDLParser::NumberHexContext>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(482);
        match(SystemRDLParser::HEX_INT);
        break;
      }

      case SystemRDLParser::VLOG_INT: {
        _localctx = _tracker.createInstance<SystemRDLParser::NumberVerilogContext>(_localctx);
        enterOuterAlt(_localctx, 3);
        setState(483);
        match(SystemRDLParser::VLOG_INT);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- String_literalContext ------------------------------------------------------------------

SystemRDLParser::String_literalContext::String_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::String_literalContext::STRING() {
  return getToken(SystemRDLParser::STRING, 0);
}


size_t SystemRDLParser::String_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleString_literal;
}


std::any SystemRDLParser::String_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitString_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::String_literalContext* SystemRDLParser::string_literal() {
  String_literalContext *_localctx = _tracker.createInstance<String_literalContext>(_ctx, getState());
  enterRule(_localctx, 72, SystemRDLParser::RuleString_literal);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(486);
    match(SystemRDLParser::STRING);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Boolean_literalContext ------------------------------------------------------------------

SystemRDLParser::Boolean_literalContext::Boolean_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Boolean_literalContext::TRUE_kw() {
  return getToken(SystemRDLParser::TRUE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Boolean_literalContext::FALSE_kw() {
  return getToken(SystemRDLParser::FALSE_kw, 0);
}


size_t SystemRDLParser::Boolean_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleBoolean_literal;
}


std::any SystemRDLParser::Boolean_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitBoolean_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Boolean_literalContext* SystemRDLParser::boolean_literal() {
  Boolean_literalContext *_localctx = _tracker.createInstance<Boolean_literalContext>(_ctx, getState());
  enterRule(_localctx, 74, SystemRDLParser::RuleBoolean_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(488);
    antlrcpp::downCast<Boolean_literalContext *>(_localctx)->val = _input->LT(1);
    _la = _input->LA(1);
    if (!(_la == SystemRDLParser::TRUE_kw

    || _la == SystemRDLParser::FALSE_kw)) {
      antlrcpp::downCast<Boolean_literalContext *>(_localctx)->val = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Array_literalContext ------------------------------------------------------------------

SystemRDLParser::Array_literalContext::Array_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::ExprContext *> SystemRDLParser::Array_literalContext::expr() {
  return getRuleContexts<SystemRDLParser::ExprContext>();
}

SystemRDLParser::ExprContext* SystemRDLParser::Array_literalContext::expr(size_t i) {
  return getRuleContext<SystemRDLParser::ExprContext>(i);
}


size_t SystemRDLParser::Array_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleArray_literal;
}


std::any SystemRDLParser::Array_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitArray_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Array_literalContext* SystemRDLParser::array_literal() {
  Array_literalContext *_localctx = _tracker.createInstance<Array_literalContext>(_ctx, getState());
  enterRule(_localctx, 76, SystemRDLParser::RuleArray_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(505);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 37, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(490);
      match(SystemRDLParser::T__10);
      setState(491);
      match(SystemRDLParser::T__1);
      setState(492);
      match(SystemRDLParser::T__2);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(493);
      match(SystemRDLParser::T__10);
      setState(494);
      match(SystemRDLParser::T__1);
      setState(495);
      expr(0);
      setState(500);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == SystemRDLParser::T__3) {
        setState(496);
        match(SystemRDLParser::T__3);
        setState(497);
        expr(0);
        setState(502);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(503);
      match(SystemRDLParser::T__2);
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Struct_literalContext ------------------------------------------------------------------

SystemRDLParser::Struct_literalContext::Struct_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Struct_literalContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

std::vector<SystemRDLParser::Struct_kvContext *> SystemRDLParser::Struct_literalContext::struct_kv() {
  return getRuleContexts<SystemRDLParser::Struct_kvContext>();
}

SystemRDLParser::Struct_kvContext* SystemRDLParser::Struct_literalContext::struct_kv(size_t i) {
  return getRuleContext<SystemRDLParser::Struct_kvContext>(i);
}


size_t SystemRDLParser::Struct_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleStruct_literal;
}


std::any SystemRDLParser::Struct_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitStruct_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Struct_literalContext* SystemRDLParser::struct_literal() {
  Struct_literalContext *_localctx = _tracker.createInstance<Struct_literalContext>(_ctx, getState());
  enterRule(_localctx, 78, SystemRDLParser::RuleStruct_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(507);
    match(SystemRDLParser::ID);
    setState(508);
    match(SystemRDLParser::T__10);
    setState(509);
    match(SystemRDLParser::T__1);
    setState(510);
    struct_kv();
    setState(515);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::T__3) {
      setState(511);
      match(SystemRDLParser::T__3);
      setState(512);
      struct_kv();
      setState(517);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(518);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Struct_kvContext ------------------------------------------------------------------

SystemRDLParser::Struct_kvContext::Struct_kvContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Struct_kvContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Struct_kvContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Struct_kvContext::getRuleIndex() const {
  return SystemRDLParser::RuleStruct_kv;
}


std::any SystemRDLParser::Struct_kvContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitStruct_kv(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Struct_kvContext* SystemRDLParser::struct_kv() {
  Struct_kvContext *_localctx = _tracker.createInstance<Struct_kvContext>(_ctx, getState());
  enterRule(_localctx, 80, SystemRDLParser::RuleStruct_kv);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(520);
    match(SystemRDLParser::ID);
    setState(521);
    match(SystemRDLParser::T__9);
    setState(522);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Enum_literalContext ------------------------------------------------------------------

SystemRDLParser::Enum_literalContext::Enum_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> SystemRDLParser::Enum_literalContext::ID() {
  return getTokens(SystemRDLParser::ID);
}

tree::TerminalNode* SystemRDLParser::Enum_literalContext::ID(size_t i) {
  return getToken(SystemRDLParser::ID, i);
}


size_t SystemRDLParser::Enum_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleEnum_literal;
}


std::any SystemRDLParser::Enum_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitEnum_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Enum_literalContext* SystemRDLParser::enum_literal() {
  Enum_literalContext *_localctx = _tracker.createInstance<Enum_literalContext>(_ctx, getState());
  enterRule(_localctx, 82, SystemRDLParser::RuleEnum_literal);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(524);
    match(SystemRDLParser::ID);
    setState(525);
    match(SystemRDLParser::T__13);
    setState(526);
    match(SystemRDLParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Accesstype_literalContext ------------------------------------------------------------------

SystemRDLParser::Accesstype_literalContext::Accesstype_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Accesstype_literalContext::NA_kw() {
  return getToken(SystemRDLParser::NA_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Accesstype_literalContext::RW_kw() {
  return getToken(SystemRDLParser::RW_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Accesstype_literalContext::WR_kw() {
  return getToken(SystemRDLParser::WR_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Accesstype_literalContext::R_kw() {
  return getToken(SystemRDLParser::R_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Accesstype_literalContext::W_kw() {
  return getToken(SystemRDLParser::W_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Accesstype_literalContext::RW1_kw() {
  return getToken(SystemRDLParser::RW1_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Accesstype_literalContext::W1_kw() {
  return getToken(SystemRDLParser::W1_kw, 0);
}


size_t SystemRDLParser::Accesstype_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleAccesstype_literal;
}


std::any SystemRDLParser::Accesstype_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitAccesstype_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Accesstype_literalContext* SystemRDLParser::accesstype_literal() {
  Accesstype_literalContext *_localctx = _tracker.createInstance<Accesstype_literalContext>(_ctx, getState());
  enterRule(_localctx, 84, SystemRDLParser::RuleAccesstype_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(528);
    antlrcpp::downCast<Accesstype_literalContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::NA_kw)
      | (1ULL << SystemRDLParser::RW_kw)
      | (1ULL << SystemRDLParser::WR_kw)
      | (1ULL << SystemRDLParser::R_kw)
      | (1ULL << SystemRDLParser::W_kw)
      | (1ULL << SystemRDLParser::RW1_kw)
      | (1ULL << SystemRDLParser::W1_kw))) != 0))) {
      antlrcpp::downCast<Accesstype_literalContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Onreadtype_literalContext ------------------------------------------------------------------

SystemRDLParser::Onreadtype_literalContext::Onreadtype_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Onreadtype_literalContext::RCLR_kw() {
  return getToken(SystemRDLParser::RCLR_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onreadtype_literalContext::RSET_kw() {
  return getToken(SystemRDLParser::RSET_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onreadtype_literalContext::RUSER_kw() {
  return getToken(SystemRDLParser::RUSER_kw, 0);
}


size_t SystemRDLParser::Onreadtype_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleOnreadtype_literal;
}


std::any SystemRDLParser::Onreadtype_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitOnreadtype_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Onreadtype_literalContext* SystemRDLParser::onreadtype_literal() {
  Onreadtype_literalContext *_localctx = _tracker.createInstance<Onreadtype_literalContext>(_ctx, getState());
  enterRule(_localctx, 86, SystemRDLParser::RuleOnreadtype_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(530);
    antlrcpp::downCast<Onreadtype_literalContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::RCLR_kw)
      | (1ULL << SystemRDLParser::RSET_kw)
      | (1ULL << SystemRDLParser::RUSER_kw))) != 0))) {
      antlrcpp::downCast<Onreadtype_literalContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Onwritetype_literalContext ------------------------------------------------------------------

SystemRDLParser::Onwritetype_literalContext::Onwritetype_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WOSET_kw() {
  return getToken(SystemRDLParser::WOSET_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WOCLR_kw() {
  return getToken(SystemRDLParser::WOCLR_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WOT_kw() {
  return getToken(SystemRDLParser::WOT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WZS_kw() {
  return getToken(SystemRDLParser::WZS_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WZC_kw() {
  return getToken(SystemRDLParser::WZC_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WZT_kw() {
  return getToken(SystemRDLParser::WZT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WCLR_kw() {
  return getToken(SystemRDLParser::WCLR_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WSET_kw() {
  return getToken(SystemRDLParser::WSET_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Onwritetype_literalContext::WUSER_kw() {
  return getToken(SystemRDLParser::WUSER_kw, 0);
}


size_t SystemRDLParser::Onwritetype_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleOnwritetype_literal;
}


std::any SystemRDLParser::Onwritetype_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitOnwritetype_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Onwritetype_literalContext* SystemRDLParser::onwritetype_literal() {
  Onwritetype_literalContext *_localctx = _tracker.createInstance<Onwritetype_literalContext>(_ctx, getState());
  enterRule(_localctx, 88, SystemRDLParser::RuleOnwritetype_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(532);
    antlrcpp::downCast<Onwritetype_literalContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::WOSET_kw)
      | (1ULL << SystemRDLParser::WOCLR_kw)
      | (1ULL << SystemRDLParser::WOT_kw)
      | (1ULL << SystemRDLParser::WZS_kw)
      | (1ULL << SystemRDLParser::WZC_kw)
      | (1ULL << SystemRDLParser::WZT_kw)
      | (1ULL << SystemRDLParser::WCLR_kw)
      | (1ULL << SystemRDLParser::WSET_kw)
      | (1ULL << SystemRDLParser::WUSER_kw))) != 0))) {
      antlrcpp::downCast<Onwritetype_literalContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Addressingtype_literalContext ------------------------------------------------------------------

SystemRDLParser::Addressingtype_literalContext::Addressingtype_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Addressingtype_literalContext::COMPACT_kw() {
  return getToken(SystemRDLParser::COMPACT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Addressingtype_literalContext::REGALIGN_kw() {
  return getToken(SystemRDLParser::REGALIGN_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Addressingtype_literalContext::FULLALIGN_kw() {
  return getToken(SystemRDLParser::FULLALIGN_kw, 0);
}


size_t SystemRDLParser::Addressingtype_literalContext::getRuleIndex() const {
  return SystemRDLParser::RuleAddressingtype_literal;
}


std::any SystemRDLParser::Addressingtype_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitAddressingtype_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Addressingtype_literalContext* SystemRDLParser::addressingtype_literal() {
  Addressingtype_literalContext *_localctx = _tracker.createInstance<Addressingtype_literalContext>(_ctx, getState());
  enterRule(_localctx, 90, SystemRDLParser::RuleAddressingtype_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(534);
    antlrcpp::downCast<Addressingtype_literalContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::COMPACT_kw)
      | (1ULL << SystemRDLParser::REGALIGN_kw)
      | (1ULL << SystemRDLParser::FULLALIGN_kw))) != 0))) {
      antlrcpp::downCast<Addressingtype_literalContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Precedencetype_literalContext ------------------------------------------------------------------

SystemRDLParser::Precedencetype_literalContext::Precedencetype_literalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Precedencetype_literalContext::HW_kw() {
  return getToken(SystemRDLParser::HW_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Precedencetype_literalContext::SW_kw() {
  return getToken(SystemRDLParser::SW_kw, 0);
}


size_t SystemRDLParser::Precedencetype_literalContext::getRuleIndex() const {
  return SystemRDLParser::RulePrecedencetype_literal;
}


std::any SystemRDLParser::Precedencetype_literalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitPrecedencetype_literal(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Precedencetype_literalContext* SystemRDLParser::precedencetype_literal() {
  Precedencetype_literalContext *_localctx = _tracker.createInstance<Precedencetype_literalContext>(_ctx, getState());
  enterRule(_localctx, 92, SystemRDLParser::RulePrecedencetype_literal);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(536);
    antlrcpp::downCast<Precedencetype_literalContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!(_la == SystemRDLParser::HW_kw

    || _la == SystemRDLParser::SW_kw)) {
      antlrcpp::downCast<Precedencetype_literalContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Instance_refContext ------------------------------------------------------------------

SystemRDLParser::Instance_refContext::Instance_refContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::Instance_ref_elementContext *> SystemRDLParser::Instance_refContext::instance_ref_element() {
  return getRuleContexts<SystemRDLParser::Instance_ref_elementContext>();
}

SystemRDLParser::Instance_ref_elementContext* SystemRDLParser::Instance_refContext::instance_ref_element(size_t i) {
  return getRuleContext<SystemRDLParser::Instance_ref_elementContext>(i);
}


size_t SystemRDLParser::Instance_refContext::getRuleIndex() const {
  return SystemRDLParser::RuleInstance_ref;
}


std::any SystemRDLParser::Instance_refContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitInstance_ref(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Instance_refContext* SystemRDLParser::instance_ref() {
  Instance_refContext *_localctx = _tracker.createInstance<Instance_refContext>(_ctx, getState());
  enterRule(_localctx, 94, SystemRDLParser::RuleInstance_ref);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(538);
    instance_ref_element();
    setState(543);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 39, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(539);
        match(SystemRDLParser::T__7);
        setState(540);
        instance_ref_element(); 
      }
      setState(545);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 39, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Instance_ref_elementContext ------------------------------------------------------------------

SystemRDLParser::Instance_ref_elementContext::Instance_ref_elementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Instance_ref_elementContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

std::vector<SystemRDLParser::Array_suffixContext *> SystemRDLParser::Instance_ref_elementContext::array_suffix() {
  return getRuleContexts<SystemRDLParser::Array_suffixContext>();
}

SystemRDLParser::Array_suffixContext* SystemRDLParser::Instance_ref_elementContext::array_suffix(size_t i) {
  return getRuleContext<SystemRDLParser::Array_suffixContext>(i);
}


size_t SystemRDLParser::Instance_ref_elementContext::getRuleIndex() const {
  return SystemRDLParser::RuleInstance_ref_element;
}


std::any SystemRDLParser::Instance_ref_elementContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitInstance_ref_element(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Instance_ref_elementContext* SystemRDLParser::instance_ref_element() {
  Instance_ref_elementContext *_localctx = _tracker.createInstance<Instance_ref_elementContext>(_ctx, getState());
  enterRule(_localctx, 96, SystemRDLParser::RuleInstance_ref_element);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(546);
    match(SystemRDLParser::ID);
    setState(550);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 40, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(547);
        array_suffix(); 
      }
      setState(552);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 40, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Prop_refContext ------------------------------------------------------------------

SystemRDLParser::Prop_refContext::Prop_refContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Instance_refContext* SystemRDLParser::Prop_refContext::instance_ref() {
  return getRuleContext<SystemRDLParser::Instance_refContext>(0);
}

SystemRDLParser::Prop_keywordContext* SystemRDLParser::Prop_refContext::prop_keyword() {
  return getRuleContext<SystemRDLParser::Prop_keywordContext>(0);
}

tree::TerminalNode* SystemRDLParser::Prop_refContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}


size_t SystemRDLParser::Prop_refContext::getRuleIndex() const {
  return SystemRDLParser::RuleProp_ref;
}


std::any SystemRDLParser::Prop_refContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitProp_ref(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Prop_refContext* SystemRDLParser::prop_ref() {
  Prop_refContext *_localctx = _tracker.createInstance<Prop_refContext>(_ctx, getState());
  enterRule(_localctx, 98, SystemRDLParser::RuleProp_ref);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(553);
    instance_ref();
    setState(554);
    match(SystemRDLParser::T__14);
    setState(557);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::RCLR_kw:
      case SystemRDLParser::RSET_kw:
      case SystemRDLParser::WOSET_kw:
      case SystemRDLParser::WOCLR_kw:
      case SystemRDLParser::HW_kw:
      case SystemRDLParser::SW_kw: {
        setState(555);
        prop_keyword();
        break;
      }

      case SystemRDLParser::ID: {
        setState(556);
        match(SystemRDLParser::ID);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Local_property_assignmentContext ------------------------------------------------------------------

SystemRDLParser::Local_property_assignmentContext::Local_property_assignmentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Normal_prop_assignContext* SystemRDLParser::Local_property_assignmentContext::normal_prop_assign() {
  return getRuleContext<SystemRDLParser::Normal_prop_assignContext>(0);
}

tree::TerminalNode* SystemRDLParser::Local_property_assignmentContext::DEFAULT_kw() {
  return getToken(SystemRDLParser::DEFAULT_kw, 0);
}

SystemRDLParser::Encode_prop_assignContext* SystemRDLParser::Local_property_assignmentContext::encode_prop_assign() {
  return getRuleContext<SystemRDLParser::Encode_prop_assignContext>(0);
}

SystemRDLParser::Prop_mod_assignContext* SystemRDLParser::Local_property_assignmentContext::prop_mod_assign() {
  return getRuleContext<SystemRDLParser::Prop_mod_assignContext>(0);
}


size_t SystemRDLParser::Local_property_assignmentContext::getRuleIndex() const {
  return SystemRDLParser::RuleLocal_property_assignment;
}


std::any SystemRDLParser::Local_property_assignmentContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitLocal_property_assignment(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Local_property_assignmentContext* SystemRDLParser::local_property_assignment() {
  Local_property_assignmentContext *_localctx = _tracker.createInstance<Local_property_assignmentContext>(_ctx, getState());
  enterRule(_localctx, 100, SystemRDLParser::RuleLocal_property_assignment);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(571);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 45, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(560);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == SystemRDLParser::DEFAULT_kw) {
        setState(559);
        match(SystemRDLParser::DEFAULT_kw);
      }
      setState(562);
      normal_prop_assign();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(564);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == SystemRDLParser::DEFAULT_kw) {
        setState(563);
        match(SystemRDLParser::DEFAULT_kw);
      }
      setState(566);
      encode_prop_assign();
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(568);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == SystemRDLParser::DEFAULT_kw) {
        setState(567);
        match(SystemRDLParser::DEFAULT_kw);
      }
      setState(570);
      prop_mod_assign();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Dynamic_property_assignmentContext ------------------------------------------------------------------

SystemRDLParser::Dynamic_property_assignmentContext::Dynamic_property_assignmentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Instance_refContext* SystemRDLParser::Dynamic_property_assignmentContext::instance_ref() {
  return getRuleContext<SystemRDLParser::Instance_refContext>(0);
}

SystemRDLParser::Normal_prop_assignContext* SystemRDLParser::Dynamic_property_assignmentContext::normal_prop_assign() {
  return getRuleContext<SystemRDLParser::Normal_prop_assignContext>(0);
}

SystemRDLParser::Encode_prop_assignContext* SystemRDLParser::Dynamic_property_assignmentContext::encode_prop_assign() {
  return getRuleContext<SystemRDLParser::Encode_prop_assignContext>(0);
}


size_t SystemRDLParser::Dynamic_property_assignmentContext::getRuleIndex() const {
  return SystemRDLParser::RuleDynamic_property_assignment;
}


std::any SystemRDLParser::Dynamic_property_assignmentContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitDynamic_property_assignment(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Dynamic_property_assignmentContext* SystemRDLParser::dynamic_property_assignment() {
  Dynamic_property_assignmentContext *_localctx = _tracker.createInstance<Dynamic_property_assignmentContext>(_ctx, getState());
  enterRule(_localctx, 102, SystemRDLParser::RuleDynamic_property_assignment);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(581);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 46, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(573);
      instance_ref();
      setState(574);
      match(SystemRDLParser::T__14);
      setState(575);
      normal_prop_assign();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(577);
      instance_ref();
      setState(578);
      match(SystemRDLParser::T__14);
      setState(579);
      encode_prop_assign();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Normal_prop_assignContext ------------------------------------------------------------------

SystemRDLParser::Normal_prop_assignContext::Normal_prop_assignContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Prop_keywordContext* SystemRDLParser::Normal_prop_assignContext::prop_keyword() {
  return getRuleContext<SystemRDLParser::Prop_keywordContext>(0);
}

tree::TerminalNode* SystemRDLParser::Normal_prop_assignContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

tree::TerminalNode* SystemRDLParser::Normal_prop_assignContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

SystemRDLParser::Prop_assignment_rhsContext* SystemRDLParser::Normal_prop_assignContext::prop_assignment_rhs() {
  return getRuleContext<SystemRDLParser::Prop_assignment_rhsContext>(0);
}


size_t SystemRDLParser::Normal_prop_assignContext::getRuleIndex() const {
  return SystemRDLParser::RuleNormal_prop_assign;
}


std::any SystemRDLParser::Normal_prop_assignContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitNormal_prop_assign(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Normal_prop_assignContext* SystemRDLParser::normal_prop_assign() {
  Normal_prop_assignContext *_localctx = _tracker.createInstance<Normal_prop_assignContext>(_ctx, getState());
  enterRule(_localctx, 104, SystemRDLParser::RuleNormal_prop_assign);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(585);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::RCLR_kw:
      case SystemRDLParser::RSET_kw:
      case SystemRDLParser::WOSET_kw:
      case SystemRDLParser::WOCLR_kw:
      case SystemRDLParser::HW_kw:
      case SystemRDLParser::SW_kw: {
        setState(583);
        prop_keyword();
        break;
      }

      case SystemRDLParser::ID: {
        setState(584);
        match(SystemRDLParser::ID);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
    setState(589);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::ASSIGN) {
      setState(587);
      match(SystemRDLParser::ASSIGN);
      setState(588);
      prop_assignment_rhs();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Encode_prop_assignContext ------------------------------------------------------------------

SystemRDLParser::Encode_prop_assignContext::Encode_prop_assignContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Encode_prop_assignContext::ENCODE_kw() {
  return getToken(SystemRDLParser::ENCODE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Encode_prop_assignContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

tree::TerminalNode* SystemRDLParser::Encode_prop_assignContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}


size_t SystemRDLParser::Encode_prop_assignContext::getRuleIndex() const {
  return SystemRDLParser::RuleEncode_prop_assign;
}


std::any SystemRDLParser::Encode_prop_assignContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitEncode_prop_assign(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Encode_prop_assignContext* SystemRDLParser::encode_prop_assign() {
  Encode_prop_assignContext *_localctx = _tracker.createInstance<Encode_prop_assignContext>(_ctx, getState());
  enterRule(_localctx, 106, SystemRDLParser::RuleEncode_prop_assign);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(591);
    match(SystemRDLParser::ENCODE_kw);
    setState(592);
    match(SystemRDLParser::ASSIGN);
    setState(593);
    match(SystemRDLParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Prop_mod_assignContext ------------------------------------------------------------------

SystemRDLParser::Prop_mod_assignContext::Prop_mod_assignContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Prop_modContext* SystemRDLParser::Prop_mod_assignContext::prop_mod() {
  return getRuleContext<SystemRDLParser::Prop_modContext>(0);
}

tree::TerminalNode* SystemRDLParser::Prop_mod_assignContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}


size_t SystemRDLParser::Prop_mod_assignContext::getRuleIndex() const {
  return SystemRDLParser::RuleProp_mod_assign;
}


std::any SystemRDLParser::Prop_mod_assignContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitProp_mod_assign(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Prop_mod_assignContext* SystemRDLParser::prop_mod_assign() {
  Prop_mod_assignContext *_localctx = _tracker.createInstance<Prop_mod_assignContext>(_ctx, getState());
  enterRule(_localctx, 108, SystemRDLParser::RuleProp_mod_assign);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(595);
    prop_mod();
    setState(596);
    match(SystemRDLParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Prop_assignment_rhsContext ------------------------------------------------------------------

SystemRDLParser::Prop_assignment_rhsContext::Prop_assignment_rhsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Precedencetype_literalContext* SystemRDLParser::Prop_assignment_rhsContext::precedencetype_literal() {
  return getRuleContext<SystemRDLParser::Precedencetype_literalContext>(0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Prop_assignment_rhsContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Prop_assignment_rhsContext::getRuleIndex() const {
  return SystemRDLParser::RuleProp_assignment_rhs;
}


std::any SystemRDLParser::Prop_assignment_rhsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitProp_assignment_rhs(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Prop_assignment_rhsContext* SystemRDLParser::prop_assignment_rhs() {
  Prop_assignment_rhsContext *_localctx = _tracker.createInstance<Prop_assignment_rhsContext>(_ctx, getState());
  enterRule(_localctx, 110, SystemRDLParser::RuleProp_assignment_rhs);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(600);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 49, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(598);
      precedencetype_literal();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(599);
      expr(0);
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Prop_keywordContext ------------------------------------------------------------------

SystemRDLParser::Prop_keywordContext::Prop_keywordContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Prop_keywordContext::SW_kw() {
  return getToken(SystemRDLParser::SW_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_keywordContext::HW_kw() {
  return getToken(SystemRDLParser::HW_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_keywordContext::RCLR_kw() {
  return getToken(SystemRDLParser::RCLR_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_keywordContext::RSET_kw() {
  return getToken(SystemRDLParser::RSET_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_keywordContext::WOCLR_kw() {
  return getToken(SystemRDLParser::WOCLR_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_keywordContext::WOSET_kw() {
  return getToken(SystemRDLParser::WOSET_kw, 0);
}


size_t SystemRDLParser::Prop_keywordContext::getRuleIndex() const {
  return SystemRDLParser::RuleProp_keyword;
}


std::any SystemRDLParser::Prop_keywordContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitProp_keyword(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Prop_keywordContext* SystemRDLParser::prop_keyword() {
  Prop_keywordContext *_localctx = _tracker.createInstance<Prop_keywordContext>(_ctx, getState());
  enterRule(_localctx, 112, SystemRDLParser::RuleProp_keyword);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(602);
    antlrcpp::downCast<Prop_keywordContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::RCLR_kw)
      | (1ULL << SystemRDLParser::RSET_kw)
      | (1ULL << SystemRDLParser::WOSET_kw)
      | (1ULL << SystemRDLParser::WOCLR_kw)
      | (1ULL << SystemRDLParser::HW_kw)
      | (1ULL << SystemRDLParser::SW_kw))) != 0))) {
      antlrcpp::downCast<Prop_keywordContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Prop_modContext ------------------------------------------------------------------

SystemRDLParser::Prop_modContext::Prop_modContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Prop_modContext::POSEDGE_kw() {
  return getToken(SystemRDLParser::POSEDGE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_modContext::NEGEDGE_kw() {
  return getToken(SystemRDLParser::NEGEDGE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_modContext::BOTHEDGE_kw() {
  return getToken(SystemRDLParser::BOTHEDGE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_modContext::LEVEL_kw() {
  return getToken(SystemRDLParser::LEVEL_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Prop_modContext::NONSTICKY_kw() {
  return getToken(SystemRDLParser::NONSTICKY_kw, 0);
}


size_t SystemRDLParser::Prop_modContext::getRuleIndex() const {
  return SystemRDLParser::RuleProp_mod;
}


std::any SystemRDLParser::Prop_modContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitProp_mod(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Prop_modContext* SystemRDLParser::prop_mod() {
  Prop_modContext *_localctx = _tracker.createInstance<Prop_modContext>(_ctx, getState());
  enterRule(_localctx, 114, SystemRDLParser::RuleProp_mod);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(604);
    antlrcpp::downCast<Prop_modContext *>(_localctx)->kw = _input->LT(1);
    _la = _input->LA(1);
    if (!(((((_la - 62) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 62)) & ((1ULL << (SystemRDLParser::POSEDGE_kw - 62))
      | (1ULL << (SystemRDLParser::NEGEDGE_kw - 62))
      | (1ULL << (SystemRDLParser::BOTHEDGE_kw - 62))
      | (1ULL << (SystemRDLParser::LEVEL_kw - 62))
      | (1ULL << (SystemRDLParser::NONSTICKY_kw - 62)))) != 0))) {
      antlrcpp::downCast<Prop_modContext *>(_localctx)->kw = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_defContext ------------------------------------------------------------------

SystemRDLParser::Udp_defContext::Udp_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Udp_defContext::PROPERTY_kw() {
  return getToken(SystemRDLParser::PROPERTY_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_defContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

std::vector<SystemRDLParser::Udp_attrContext *> SystemRDLParser::Udp_defContext::udp_attr() {
  return getRuleContexts<SystemRDLParser::Udp_attrContext>();
}

SystemRDLParser::Udp_attrContext* SystemRDLParser::Udp_defContext::udp_attr(size_t i) {
  return getRuleContext<SystemRDLParser::Udp_attrContext>(i);
}


size_t SystemRDLParser::Udp_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_def;
}


std::any SystemRDLParser::Udp_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_defContext* SystemRDLParser::udp_def() {
  Udp_defContext *_localctx = _tracker.createInstance<Udp_defContext>(_ctx, getState());
  enterRule(_localctx, 116, SystemRDLParser::RuleUdp_def);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(606);
    match(SystemRDLParser::PROPERTY_kw);
    setState(607);
    match(SystemRDLParser::ID);
    setState(608);
    match(SystemRDLParser::T__1);
    setState(612); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(609);
      udp_attr();
      setState(610);
      match(SystemRDLParser::T__0);
      setState(614); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while (((((_la - 69) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 69)) & ((1ULL << (SystemRDLParser::COMPONENT_kw - 69))
      | (1ULL << (SystemRDLParser::CONSTRAINT_kw - 69))
      | (1ULL << (SystemRDLParser::DEFAULT_kw - 69))
      | (1ULL << (SystemRDLParser::TYPE_kw - 69)))) != 0));
    setState(616);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_attrContext ------------------------------------------------------------------

SystemRDLParser::Udp_attrContext::Udp_attrContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Udp_typeContext* SystemRDLParser::Udp_attrContext::udp_type() {
  return getRuleContext<SystemRDLParser::Udp_typeContext>(0);
}

SystemRDLParser::Udp_usageContext* SystemRDLParser::Udp_attrContext::udp_usage() {
  return getRuleContext<SystemRDLParser::Udp_usageContext>(0);
}

SystemRDLParser::Udp_defaultContext* SystemRDLParser::Udp_attrContext::udp_default() {
  return getRuleContext<SystemRDLParser::Udp_defaultContext>(0);
}

SystemRDLParser::Udp_constraintContext* SystemRDLParser::Udp_attrContext::udp_constraint() {
  return getRuleContext<SystemRDLParser::Udp_constraintContext>(0);
}


size_t SystemRDLParser::Udp_attrContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_attr;
}


std::any SystemRDLParser::Udp_attrContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_attr(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_attrContext* SystemRDLParser::udp_attr() {
  Udp_attrContext *_localctx = _tracker.createInstance<Udp_attrContext>(_ctx, getState());
  enterRule(_localctx, 118, SystemRDLParser::RuleUdp_attr);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(622);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::TYPE_kw: {
        enterOuterAlt(_localctx, 1);
        setState(618);
        udp_type();
        break;
      }

      case SystemRDLParser::COMPONENT_kw: {
        enterOuterAlt(_localctx, 2);
        setState(619);
        udp_usage();
        break;
      }

      case SystemRDLParser::DEFAULT_kw: {
        enterOuterAlt(_localctx, 3);
        setState(620);
        udp_default();
        break;
      }

      case SystemRDLParser::CONSTRAINT_kw: {
        enterOuterAlt(_localctx, 4);
        setState(621);
        udp_constraint();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_typeContext ------------------------------------------------------------------

SystemRDLParser::Udp_typeContext::Udp_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Udp_typeContext::TYPE_kw() {
  return getToken(SystemRDLParser::TYPE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_typeContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

SystemRDLParser::Udp_data_typeContext* SystemRDLParser::Udp_typeContext::udp_data_type() {
  return getRuleContext<SystemRDLParser::Udp_data_typeContext>(0);
}

SystemRDLParser::Array_type_suffixContext* SystemRDLParser::Udp_typeContext::array_type_suffix() {
  return getRuleContext<SystemRDLParser::Array_type_suffixContext>(0);
}


size_t SystemRDLParser::Udp_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_type;
}


std::any SystemRDLParser::Udp_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_typeContext* SystemRDLParser::udp_type() {
  Udp_typeContext *_localctx = _tracker.createInstance<Udp_typeContext>(_ctx, getState());
  enterRule(_localctx, 120, SystemRDLParser::RuleUdp_type);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(624);
    match(SystemRDLParser::TYPE_kw);
    setState(625);
    match(SystemRDLParser::ASSIGN);
    setState(626);
    udp_data_type();
    setState(628);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::T__11) {
      setState(627);
      array_type_suffix();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_data_typeContext ------------------------------------------------------------------

SystemRDLParser::Udp_data_typeContext::Udp_data_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_type_primaryContext* SystemRDLParser::Udp_data_typeContext::component_type_primary() {
  return getRuleContext<SystemRDLParser::Component_type_primaryContext>(0);
}

tree::TerminalNode* SystemRDLParser::Udp_data_typeContext::REF_kw() {
  return getToken(SystemRDLParser::REF_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_data_typeContext::NUMBER_kw() {
  return getToken(SystemRDLParser::NUMBER_kw, 0);
}

SystemRDLParser::Basic_data_typeContext* SystemRDLParser::Udp_data_typeContext::basic_data_type() {
  return getRuleContext<SystemRDLParser::Basic_data_typeContext>(0);
}


size_t SystemRDLParser::Udp_data_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_data_type;
}


std::any SystemRDLParser::Udp_data_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_data_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_data_typeContext* SystemRDLParser::udp_data_type() {
  Udp_data_typeContext *_localctx = _tracker.createInstance<Udp_data_typeContext>(_ctx, getState());
  enterRule(_localctx, 122, SystemRDLParser::RuleUdp_data_type);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(633);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::ADDRMAP_kw:
      case SystemRDLParser::REGFILE_kw:
      case SystemRDLParser::REG_kw:
      case SystemRDLParser::FIELD_kw:
      case SystemRDLParser::MEM_kw: {
        enterOuterAlt(_localctx, 1);
        setState(630);
        component_type_primary();
        break;
      }

      case SystemRDLParser::NUMBER_kw:
      case SystemRDLParser::REF_kw: {
        enterOuterAlt(_localctx, 2);
        setState(631);
        antlrcpp::downCast<Udp_data_typeContext *>(_localctx)->kw = _input->LT(1);
        _la = _input->LA(1);
        if (!(_la == SystemRDLParser::NUMBER_kw

        || _la == SystemRDLParser::REF_kw)) {
          antlrcpp::downCast<Udp_data_typeContext *>(_localctx)->kw = _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        break;
      }

      case SystemRDLParser::BOOLEAN_kw:
      case SystemRDLParser::BIT_kw:
      case SystemRDLParser::LONGINT_kw:
      case SystemRDLParser::STRING_kw:
      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 3);
        setState(632);
        basic_data_type();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_usageContext ------------------------------------------------------------------

SystemRDLParser::Udp_usageContext::Udp_usageContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Udp_usageContext::COMPONENT_kw() {
  return getToken(SystemRDLParser::COMPONENT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_usageContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

std::vector<SystemRDLParser::Udp_comp_typeContext *> SystemRDLParser::Udp_usageContext::udp_comp_type() {
  return getRuleContexts<SystemRDLParser::Udp_comp_typeContext>();
}

SystemRDLParser::Udp_comp_typeContext* SystemRDLParser::Udp_usageContext::udp_comp_type(size_t i) {
  return getRuleContext<SystemRDLParser::Udp_comp_typeContext>(i);
}

std::vector<tree::TerminalNode *> SystemRDLParser::Udp_usageContext::OR() {
  return getTokens(SystemRDLParser::OR);
}

tree::TerminalNode* SystemRDLParser::Udp_usageContext::OR(size_t i) {
  return getToken(SystemRDLParser::OR, i);
}


size_t SystemRDLParser::Udp_usageContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_usage;
}


std::any SystemRDLParser::Udp_usageContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_usage(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_usageContext* SystemRDLParser::udp_usage() {
  Udp_usageContext *_localctx = _tracker.createInstance<Udp_usageContext>(_ctx, getState());
  enterRule(_localctx, 124, SystemRDLParser::RuleUdp_usage);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(635);
    match(SystemRDLParser::COMPONENT_kw);
    setState(636);
    match(SystemRDLParser::ASSIGN);
    setState(637);
    udp_comp_type();
    setState(642);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::OR) {
      setState(638);
      match(SystemRDLParser::OR);
      setState(639);
      udp_comp_type();
      setState(644);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_comp_typeContext ------------------------------------------------------------------

SystemRDLParser::Udp_comp_typeContext::Udp_comp_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Component_typeContext* SystemRDLParser::Udp_comp_typeContext::component_type() {
  return getRuleContext<SystemRDLParser::Component_typeContext>(0);
}

tree::TerminalNode* SystemRDLParser::Udp_comp_typeContext::CONSTRAINT_kw() {
  return getToken(SystemRDLParser::CONSTRAINT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_comp_typeContext::ALL_kw() {
  return getToken(SystemRDLParser::ALL_kw, 0);
}


size_t SystemRDLParser::Udp_comp_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_comp_type;
}


std::any SystemRDLParser::Udp_comp_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_comp_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_comp_typeContext* SystemRDLParser::udp_comp_type() {
  Udp_comp_typeContext *_localctx = _tracker.createInstance<Udp_comp_typeContext>(_ctx, getState());
  enterRule(_localctx, 126, SystemRDLParser::RuleUdp_comp_type);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(647);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::ADDRMAP_kw:
      case SystemRDLParser::REGFILE_kw:
      case SystemRDLParser::REG_kw:
      case SystemRDLParser::FIELD_kw:
      case SystemRDLParser::MEM_kw:
      case SystemRDLParser::SIGNAL_kw: {
        enterOuterAlt(_localctx, 1);
        setState(645);
        component_type();
        break;
      }

      case SystemRDLParser::ALL_kw:
      case SystemRDLParser::CONSTRAINT_kw: {
        enterOuterAlt(_localctx, 2);
        setState(646);
        antlrcpp::downCast<Udp_comp_typeContext *>(_localctx)->kw = _input->LT(1);
        _la = _input->LA(1);
        if (!(_la == SystemRDLParser::ALL_kw

        || _la == SystemRDLParser::CONSTRAINT_kw)) {
          antlrcpp::downCast<Udp_comp_typeContext *>(_localctx)->kw = _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_defaultContext ------------------------------------------------------------------

SystemRDLParser::Udp_defaultContext::Udp_defaultContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Udp_defaultContext::DEFAULT_kw() {
  return getToken(SystemRDLParser::DEFAULT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_defaultContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Udp_defaultContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Udp_defaultContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_default;
}


std::any SystemRDLParser::Udp_defaultContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_default(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_defaultContext* SystemRDLParser::udp_default() {
  Udp_defaultContext *_localctx = _tracker.createInstance<Udp_defaultContext>(_ctx, getState());
  enterRule(_localctx, 128, SystemRDLParser::RuleUdp_default);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(649);
    match(SystemRDLParser::DEFAULT_kw);
    setState(650);
    match(SystemRDLParser::ASSIGN);
    setState(651);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Udp_constraintContext ------------------------------------------------------------------

SystemRDLParser::Udp_constraintContext::Udp_constraintContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Udp_constraintContext::CONSTRAINT_kw() {
  return getToken(SystemRDLParser::CONSTRAINT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_constraintContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

tree::TerminalNode* SystemRDLParser::Udp_constraintContext::COMPONENTWIDTH_kw() {
  return getToken(SystemRDLParser::COMPONENTWIDTH_kw, 0);
}


size_t SystemRDLParser::Udp_constraintContext::getRuleIndex() const {
  return SystemRDLParser::RuleUdp_constraint;
}


std::any SystemRDLParser::Udp_constraintContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitUdp_constraint(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Udp_constraintContext* SystemRDLParser::udp_constraint() {
  Udp_constraintContext *_localctx = _tracker.createInstance<Udp_constraintContext>(_ctx, getState());
  enterRule(_localctx, 130, SystemRDLParser::RuleUdp_constraint);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(653);
    match(SystemRDLParser::CONSTRAINT_kw);
    setState(654);
    match(SystemRDLParser::ASSIGN);
    setState(655);
    match(SystemRDLParser::COMPONENTWIDTH_kw);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Enum_defContext ------------------------------------------------------------------

SystemRDLParser::Enum_defContext::Enum_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Enum_defContext::ENUM_kw() {
  return getToken(SystemRDLParser::ENUM_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Enum_defContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

std::vector<SystemRDLParser::Enum_entryContext *> SystemRDLParser::Enum_defContext::enum_entry() {
  return getRuleContexts<SystemRDLParser::Enum_entryContext>();
}

SystemRDLParser::Enum_entryContext* SystemRDLParser::Enum_defContext::enum_entry(size_t i) {
  return getRuleContext<SystemRDLParser::Enum_entryContext>(i);
}


size_t SystemRDLParser::Enum_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleEnum_def;
}


std::any SystemRDLParser::Enum_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitEnum_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Enum_defContext* SystemRDLParser::enum_def() {
  Enum_defContext *_localctx = _tracker.createInstance<Enum_defContext>(_ctx, getState());
  enterRule(_localctx, 132, SystemRDLParser::RuleEnum_def);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(657);
    match(SystemRDLParser::ENUM_kw);
    setState(658);
    match(SystemRDLParser::ID);
    setState(659);
    match(SystemRDLParser::T__1);
    setState(663); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(660);
      enum_entry();
      setState(661);
      match(SystemRDLParser::T__0);
      setState(665); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while (_la == SystemRDLParser::ID);
    setState(667);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Enum_entryContext ------------------------------------------------------------------

SystemRDLParser::Enum_entryContext::Enum_entryContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Enum_entryContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

tree::TerminalNode* SystemRDLParser::Enum_entryContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Enum_entryContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}

std::vector<SystemRDLParser::Enum_prop_assignContext *> SystemRDLParser::Enum_entryContext::enum_prop_assign() {
  return getRuleContexts<SystemRDLParser::Enum_prop_assignContext>();
}

SystemRDLParser::Enum_prop_assignContext* SystemRDLParser::Enum_entryContext::enum_prop_assign(size_t i) {
  return getRuleContext<SystemRDLParser::Enum_prop_assignContext>(i);
}


size_t SystemRDLParser::Enum_entryContext::getRuleIndex() const {
  return SystemRDLParser::RuleEnum_entry;
}


std::any SystemRDLParser::Enum_entryContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitEnum_entry(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Enum_entryContext* SystemRDLParser::enum_entry() {
  Enum_entryContext *_localctx = _tracker.createInstance<Enum_entryContext>(_ctx, getState());
  enterRule(_localctx, 134, SystemRDLParser::RuleEnum_entry);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(669);
    match(SystemRDLParser::ID);
    setState(672);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::ASSIGN) {
      setState(670);
      match(SystemRDLParser::ASSIGN);
      setState(671);
      expr(0);
    }
    setState(684);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::T__1) {
      setState(674);
      match(SystemRDLParser::T__1);
      setState(680);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == SystemRDLParser::ID) {
        setState(675);
        enum_prop_assign();
        setState(676);
        match(SystemRDLParser::T__0);
        setState(682);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(683);
      match(SystemRDLParser::T__2);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Enum_prop_assignContext ------------------------------------------------------------------

SystemRDLParser::Enum_prop_assignContext::Enum_prop_assignContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Enum_prop_assignContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

tree::TerminalNode* SystemRDLParser::Enum_prop_assignContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Enum_prop_assignContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Enum_prop_assignContext::getRuleIndex() const {
  return SystemRDLParser::RuleEnum_prop_assign;
}


std::any SystemRDLParser::Enum_prop_assignContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitEnum_prop_assign(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Enum_prop_assignContext* SystemRDLParser::enum_prop_assign() {
  Enum_prop_assignContext *_localctx = _tracker.createInstance<Enum_prop_assignContext>(_ctx, getState());
  enterRule(_localctx, 136, SystemRDLParser::RuleEnum_prop_assign);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(686);
    match(SystemRDLParser::ID);
    setState(687);
    match(SystemRDLParser::ASSIGN);
    setState(688);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Struct_defContext ------------------------------------------------------------------

SystemRDLParser::Struct_defContext::Struct_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Struct_defContext::STRUCT_kw() {
  return getToken(SystemRDLParser::STRUCT_kw, 0);
}

std::vector<tree::TerminalNode *> SystemRDLParser::Struct_defContext::ID() {
  return getTokens(SystemRDLParser::ID);
}

tree::TerminalNode* SystemRDLParser::Struct_defContext::ID(size_t i) {
  return getToken(SystemRDLParser::ID, i);
}

tree::TerminalNode* SystemRDLParser::Struct_defContext::ABSTRACT_kw() {
  return getToken(SystemRDLParser::ABSTRACT_kw, 0);
}

std::vector<SystemRDLParser::Struct_elemContext *> SystemRDLParser::Struct_defContext::struct_elem() {
  return getRuleContexts<SystemRDLParser::Struct_elemContext>();
}

SystemRDLParser::Struct_elemContext* SystemRDLParser::Struct_defContext::struct_elem(size_t i) {
  return getRuleContext<SystemRDLParser::Struct_elemContext>(i);
}


size_t SystemRDLParser::Struct_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleStruct_def;
}


std::any SystemRDLParser::Struct_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitStruct_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Struct_defContext* SystemRDLParser::struct_def() {
  Struct_defContext *_localctx = _tracker.createInstance<Struct_defContext>(_ctx, getState());
  enterRule(_localctx, 138, SystemRDLParser::RuleStruct_def);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(691);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::ABSTRACT_kw) {
      setState(690);
      match(SystemRDLParser::ABSTRACT_kw);
    }
    setState(693);
    match(SystemRDLParser::STRUCT_kw);
    setState(694);
    antlrcpp::downCast<Struct_defContext *>(_localctx)->name = match(SystemRDLParser::ID);
    setState(697);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::T__9) {
      setState(695);
      match(SystemRDLParser::T__9);
      setState(696);
      antlrcpp::downCast<Struct_defContext *>(_localctx)->base = match(SystemRDLParser::ID);
    }
    setState(699);
    match(SystemRDLParser::T__1);
    setState(705);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::BOOLEAN_kw)
      | (1ULL << SystemRDLParser::BIT_kw)
      | (1ULL << SystemRDLParser::LONGINT_kw)
      | (1ULL << SystemRDLParser::STRING_kw)
      | (1ULL << SystemRDLParser::ACCESSTYPE_kw)
      | (1ULL << SystemRDLParser::ADDRESSINGTYPE_kw)
      | (1ULL << SystemRDLParser::ONREADTYPE_kw)
      | (1ULL << SystemRDLParser::ONWRITETYPE_kw)
      | (1ULL << SystemRDLParser::ADDRMAP_kw)
      | (1ULL << SystemRDLParser::REGFILE_kw)
      | (1ULL << SystemRDLParser::REG_kw)
      | (1ULL << SystemRDLParser::FIELD_kw)
      | (1ULL << SystemRDLParser::MEM_kw)
      | (1ULL << SystemRDLParser::SIGNAL_kw))) != 0) || _la == SystemRDLParser::ID) {
      setState(700);
      struct_elem();
      setState(701);
      match(SystemRDLParser::T__0);
      setState(707);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(708);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Struct_elemContext ------------------------------------------------------------------

SystemRDLParser::Struct_elemContext::Struct_elemContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Struct_typeContext* SystemRDLParser::Struct_elemContext::struct_type() {
  return getRuleContext<SystemRDLParser::Struct_typeContext>(0);
}

tree::TerminalNode* SystemRDLParser::Struct_elemContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::Array_type_suffixContext* SystemRDLParser::Struct_elemContext::array_type_suffix() {
  return getRuleContext<SystemRDLParser::Array_type_suffixContext>(0);
}


size_t SystemRDLParser::Struct_elemContext::getRuleIndex() const {
  return SystemRDLParser::RuleStruct_elem;
}


std::any SystemRDLParser::Struct_elemContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitStruct_elem(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Struct_elemContext* SystemRDLParser::struct_elem() {
  Struct_elemContext *_localctx = _tracker.createInstance<Struct_elemContext>(_ctx, getState());
  enterRule(_localctx, 140, SystemRDLParser::RuleStruct_elem);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(710);
    struct_type();
    setState(711);
    match(SystemRDLParser::ID);
    setState(713);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == SystemRDLParser::T__11) {
      setState(712);
      array_type_suffix();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Struct_typeContext ------------------------------------------------------------------

SystemRDLParser::Struct_typeContext::Struct_typeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Data_typeContext* SystemRDLParser::Struct_typeContext::data_type() {
  return getRuleContext<SystemRDLParser::Data_typeContext>(0);
}

SystemRDLParser::Component_typeContext* SystemRDLParser::Struct_typeContext::component_type() {
  return getRuleContext<SystemRDLParser::Component_typeContext>(0);
}


size_t SystemRDLParser::Struct_typeContext::getRuleIndex() const {
  return SystemRDLParser::RuleStruct_type;
}


std::any SystemRDLParser::Struct_typeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitStruct_type(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Struct_typeContext* SystemRDLParser::struct_type() {
  Struct_typeContext *_localctx = _tracker.createInstance<Struct_typeContext>(_ctx, getState());
  enterRule(_localctx, 142, SystemRDLParser::RuleStruct_type);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(717);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::BOOLEAN_kw:
      case SystemRDLParser::BIT_kw:
      case SystemRDLParser::LONGINT_kw:
      case SystemRDLParser::STRING_kw:
      case SystemRDLParser::ACCESSTYPE_kw:
      case SystemRDLParser::ADDRESSINGTYPE_kw:
      case SystemRDLParser::ONREADTYPE_kw:
      case SystemRDLParser::ONWRITETYPE_kw:
      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 1);
        setState(715);
        data_type();
        break;
      }

      case SystemRDLParser::ADDRMAP_kw:
      case SystemRDLParser::REGFILE_kw:
      case SystemRDLParser::REG_kw:
      case SystemRDLParser::FIELD_kw:
      case SystemRDLParser::MEM_kw:
      case SystemRDLParser::SIGNAL_kw: {
        enterOuterAlt(_localctx, 2);
        setState(716);
        component_type();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constraint_defContext ------------------------------------------------------------------

SystemRDLParser::Constraint_defContext::Constraint_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Constraint_named_defContext* SystemRDLParser::Constraint_defContext::constraint_named_def() {
  return getRuleContext<SystemRDLParser::Constraint_named_defContext>(0);
}

SystemRDLParser::Constraint_instsContext* SystemRDLParser::Constraint_defContext::constraint_insts() {
  return getRuleContext<SystemRDLParser::Constraint_instsContext>(0);
}

SystemRDLParser::Constraint_anon_defContext* SystemRDLParser::Constraint_defContext::constraint_anon_def() {
  return getRuleContext<SystemRDLParser::Constraint_anon_defContext>(0);
}


size_t SystemRDLParser::Constraint_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstraint_def;
}


std::any SystemRDLParser::Constraint_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstraint_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constraint_defContext* SystemRDLParser::constraint_def() {
  Constraint_defContext *_localctx = _tracker.createInstance<Constraint_defContext>(_ctx, getState());
  enterRule(_localctx, 144, SystemRDLParser::RuleConstraint_def);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(726);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 66, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(719);
      constraint_named_def();
      setState(721);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == SystemRDLParser::ID) {
        setState(720);
        constraint_insts();
      }
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(723);
      constraint_anon_def();
      setState(724);
      constraint_insts();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constraint_named_defContext ------------------------------------------------------------------

SystemRDLParser::Constraint_named_defContext::Constraint_named_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Constraint_named_defContext::CONSTRAINT_kw() {
  return getToken(SystemRDLParser::CONSTRAINT_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Constraint_named_defContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

SystemRDLParser::Constraint_bodyContext* SystemRDLParser::Constraint_named_defContext::constraint_body() {
  return getRuleContext<SystemRDLParser::Constraint_bodyContext>(0);
}


size_t SystemRDLParser::Constraint_named_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstraint_named_def;
}


std::any SystemRDLParser::Constraint_named_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstraint_named_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constraint_named_defContext* SystemRDLParser::constraint_named_def() {
  Constraint_named_defContext *_localctx = _tracker.createInstance<Constraint_named_defContext>(_ctx, getState());
  enterRule(_localctx, 146, SystemRDLParser::RuleConstraint_named_def);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(728);
    match(SystemRDLParser::CONSTRAINT_kw);
    setState(729);
    match(SystemRDLParser::ID);
    setState(730);
    constraint_body();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constraint_anon_defContext ------------------------------------------------------------------

SystemRDLParser::Constraint_anon_defContext::Constraint_anon_defContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Constraint_anon_defContext::CONSTRAINT_kw() {
  return getToken(SystemRDLParser::CONSTRAINT_kw, 0);
}

SystemRDLParser::Constraint_bodyContext* SystemRDLParser::Constraint_anon_defContext::constraint_body() {
  return getRuleContext<SystemRDLParser::Constraint_bodyContext>(0);
}


size_t SystemRDLParser::Constraint_anon_defContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstraint_anon_def;
}


std::any SystemRDLParser::Constraint_anon_defContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstraint_anon_def(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constraint_anon_defContext* SystemRDLParser::constraint_anon_def() {
  Constraint_anon_defContext *_localctx = _tracker.createInstance<Constraint_anon_defContext>(_ctx, getState());
  enterRule(_localctx, 148, SystemRDLParser::RuleConstraint_anon_def);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(732);
    match(SystemRDLParser::CONSTRAINT_kw);
    setState(733);
    constraint_body();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constraint_bodyContext ------------------------------------------------------------------

SystemRDLParser::Constraint_bodyContext::Constraint_bodyContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::Constraint_body_elemContext *> SystemRDLParser::Constraint_bodyContext::constraint_body_elem() {
  return getRuleContexts<SystemRDLParser::Constraint_body_elemContext>();
}

SystemRDLParser::Constraint_body_elemContext* SystemRDLParser::Constraint_bodyContext::constraint_body_elem(size_t i) {
  return getRuleContext<SystemRDLParser::Constraint_body_elemContext>(i);
}


size_t SystemRDLParser::Constraint_bodyContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstraint_body;
}


std::any SystemRDLParser::Constraint_bodyContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstraint_body(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constraint_bodyContext* SystemRDLParser::constraint_body() {
  Constraint_bodyContext *_localctx = _tracker.createInstance<Constraint_bodyContext>(_ctx, getState());
  enterRule(_localctx, 150, SystemRDLParser::RuleConstraint_body);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(735);
    match(SystemRDLParser::T__1);
    setState(741);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << SystemRDLParser::T__1)
      | (1ULL << SystemRDLParser::T__5)
      | (1ULL << SystemRDLParser::T__10)
      | (1ULL << SystemRDLParser::BOOLEAN_kw)
      | (1ULL << SystemRDLParser::BIT_kw)
      | (1ULL << SystemRDLParser::LONGINT_kw)
      | (1ULL << SystemRDLParser::TRUE_kw)
      | (1ULL << SystemRDLParser::FALSE_kw)
      | (1ULL << SystemRDLParser::NA_kw)
      | (1ULL << SystemRDLParser::RW_kw)
      | (1ULL << SystemRDLParser::WR_kw)
      | (1ULL << SystemRDLParser::R_kw)
      | (1ULL << SystemRDLParser::W_kw)
      | (1ULL << SystemRDLParser::RW1_kw)
      | (1ULL << SystemRDLParser::W1_kw)
      | (1ULL << SystemRDLParser::RCLR_kw)
      | (1ULL << SystemRDLParser::RSET_kw)
      | (1ULL << SystemRDLParser::RUSER_kw)
      | (1ULL << SystemRDLParser::WOSET_kw)
      | (1ULL << SystemRDLParser::WOCLR_kw)
      | (1ULL << SystemRDLParser::WOT_kw)
      | (1ULL << SystemRDLParser::WZS_kw)
      | (1ULL << SystemRDLParser::WZC_kw)
      | (1ULL << SystemRDLParser::WZT_kw)
      | (1ULL << SystemRDLParser::WCLR_kw)
      | (1ULL << SystemRDLParser::WSET_kw)
      | (1ULL << SystemRDLParser::WUSER_kw)
      | (1ULL << SystemRDLParser::COMPACT_kw)
      | (1ULL << SystemRDLParser::REGALIGN_kw)
      | (1ULL << SystemRDLParser::FULLALIGN_kw)
      | (1ULL << SystemRDLParser::HW_kw)
      | (1ULL << SystemRDLParser::SW_kw))) != 0) || ((((_la - 80) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 80)) & ((1ULL << (SystemRDLParser::THIS_kw - 80))
      | (1ULL << (SystemRDLParser::INT - 80))
      | (1ULL << (SystemRDLParser::HEX_INT - 80))
      | (1ULL << (SystemRDLParser::VLOG_INT - 80))
      | (1ULL << (SystemRDLParser::STRING - 80))
      | (1ULL << (SystemRDLParser::PLUS - 80))
      | (1ULL << (SystemRDLParser::MINUS - 80))
      | (1ULL << (SystemRDLParser::BNOT - 80))
      | (1ULL << (SystemRDLParser::NOT - 80))
      | (1ULL << (SystemRDLParser::NAND - 80))
      | (1ULL << (SystemRDLParser::AND - 80))
      | (1ULL << (SystemRDLParser::OR - 80))
      | (1ULL << (SystemRDLParser::NOR - 80))
      | (1ULL << (SystemRDLParser::XOR - 80))
      | (1ULL << (SystemRDLParser::XNOR - 80))
      | (1ULL << (SystemRDLParser::ID - 80)))) != 0)) {
      setState(736);
      constraint_body_elem();
      setState(737);
      match(SystemRDLParser::T__0);
      setState(743);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(744);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constraint_body_elemContext ------------------------------------------------------------------

SystemRDLParser::Constraint_body_elemContext::Constraint_body_elemContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Constr_relationalContext* SystemRDLParser::Constraint_body_elemContext::constr_relational() {
  return getRuleContext<SystemRDLParser::Constr_relationalContext>(0);
}

SystemRDLParser::Constr_prop_assignContext* SystemRDLParser::Constraint_body_elemContext::constr_prop_assign() {
  return getRuleContext<SystemRDLParser::Constr_prop_assignContext>(0);
}

SystemRDLParser::Constr_inside_valuesContext* SystemRDLParser::Constraint_body_elemContext::constr_inside_values() {
  return getRuleContext<SystemRDLParser::Constr_inside_valuesContext>(0);
}

SystemRDLParser::Constr_inside_enumContext* SystemRDLParser::Constraint_body_elemContext::constr_inside_enum() {
  return getRuleContext<SystemRDLParser::Constr_inside_enumContext>(0);
}


size_t SystemRDLParser::Constraint_body_elemContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstraint_body_elem;
}


std::any SystemRDLParser::Constraint_body_elemContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstraint_body_elem(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constraint_body_elemContext* SystemRDLParser::constraint_body_elem() {
  Constraint_body_elemContext *_localctx = _tracker.createInstance<Constraint_body_elemContext>(_ctx, getState());
  enterRule(_localctx, 152, SystemRDLParser::RuleConstraint_body_elem);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(750);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 68, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(746);
      constr_relational();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(747);
      constr_prop_assign();
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(748);
      constr_inside_values();
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(749);
      constr_inside_enum();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constraint_instsContext ------------------------------------------------------------------

SystemRDLParser::Constraint_instsContext::Constraint_instsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> SystemRDLParser::Constraint_instsContext::ID() {
  return getTokens(SystemRDLParser::ID);
}

tree::TerminalNode* SystemRDLParser::Constraint_instsContext::ID(size_t i) {
  return getToken(SystemRDLParser::ID, i);
}


size_t SystemRDLParser::Constraint_instsContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstraint_insts;
}


std::any SystemRDLParser::Constraint_instsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstraint_insts(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constraint_instsContext* SystemRDLParser::constraint_insts() {
  Constraint_instsContext *_localctx = _tracker.createInstance<Constraint_instsContext>(_ctx, getState());
  enterRule(_localctx, 154, SystemRDLParser::RuleConstraint_insts);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(752);
    match(SystemRDLParser::ID);
    setState(757);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::T__3) {
      setState(753);
      match(SystemRDLParser::T__3);
      setState(754);
      match(SystemRDLParser::ID);
      setState(759);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constr_relationalContext ------------------------------------------------------------------

SystemRDLParser::Constr_relationalContext::Constr_relationalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::ExprContext *> SystemRDLParser::Constr_relationalContext::expr() {
  return getRuleContexts<SystemRDLParser::ExprContext>();
}

SystemRDLParser::ExprContext* SystemRDLParser::Constr_relationalContext::expr(size_t i) {
  return getRuleContext<SystemRDLParser::ExprContext>(i);
}

tree::TerminalNode* SystemRDLParser::Constr_relationalContext::LT() {
  return getToken(SystemRDLParser::LT, 0);
}

tree::TerminalNode* SystemRDLParser::Constr_relationalContext::LEQ() {
  return getToken(SystemRDLParser::LEQ, 0);
}

tree::TerminalNode* SystemRDLParser::Constr_relationalContext::GT() {
  return getToken(SystemRDLParser::GT, 0);
}

tree::TerminalNode* SystemRDLParser::Constr_relationalContext::GEQ() {
  return getToken(SystemRDLParser::GEQ, 0);
}

tree::TerminalNode* SystemRDLParser::Constr_relationalContext::EQ() {
  return getToken(SystemRDLParser::EQ, 0);
}

tree::TerminalNode* SystemRDLParser::Constr_relationalContext::NEQ() {
  return getToken(SystemRDLParser::NEQ, 0);
}


size_t SystemRDLParser::Constr_relationalContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstr_relational;
}


std::any SystemRDLParser::Constr_relationalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstr_relational(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constr_relationalContext* SystemRDLParser::constr_relational() {
  Constr_relationalContext *_localctx = _tracker.createInstance<Constr_relationalContext>(_ctx, getState());
  enterRule(_localctx, 156, SystemRDLParser::RuleConstr_relational);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(760);
    expr(0);
    setState(761);
    antlrcpp::downCast<Constr_relationalContext *>(_localctx)->op = _input->LT(1);
    _la = _input->LA(1);
    if (!(((((_la - 114) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - 114)) & ((1ULL << (SystemRDLParser::EQ - 114))
      | (1ULL << (SystemRDLParser::NEQ - 114))
      | (1ULL << (SystemRDLParser::LEQ - 114))
      | (1ULL << (SystemRDLParser::LT - 114))
      | (1ULL << (SystemRDLParser::GEQ - 114))
      | (1ULL << (SystemRDLParser::GT - 114)))) != 0))) {
      antlrcpp::downCast<Constr_relationalContext *>(_localctx)->op = _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
    setState(762);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constr_prop_assignContext ------------------------------------------------------------------

SystemRDLParser::Constr_prop_assignContext::Constr_prop_assignContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Constr_prop_assignContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}

tree::TerminalNode* SystemRDLParser::Constr_prop_assignContext::ASSIGN() {
  return getToken(SystemRDLParser::ASSIGN, 0);
}

SystemRDLParser::ExprContext* SystemRDLParser::Constr_prop_assignContext::expr() {
  return getRuleContext<SystemRDLParser::ExprContext>(0);
}


size_t SystemRDLParser::Constr_prop_assignContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstr_prop_assign;
}


std::any SystemRDLParser::Constr_prop_assignContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstr_prop_assign(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constr_prop_assignContext* SystemRDLParser::constr_prop_assign() {
  Constr_prop_assignContext *_localctx = _tracker.createInstance<Constr_prop_assignContext>(_ctx, getState());
  enterRule(_localctx, 158, SystemRDLParser::RuleConstr_prop_assign);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(764);
    match(SystemRDLParser::ID);
    setState(765);
    match(SystemRDLParser::ASSIGN);
    setState(766);
    expr(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constr_inside_valuesContext ------------------------------------------------------------------

SystemRDLParser::Constr_inside_valuesContext::Constr_inside_valuesContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Constr_lhsContext* SystemRDLParser::Constr_inside_valuesContext::constr_lhs() {
  return getRuleContext<SystemRDLParser::Constr_lhsContext>(0);
}

tree::TerminalNode* SystemRDLParser::Constr_inside_valuesContext::INSIDE_kw() {
  return getToken(SystemRDLParser::INSIDE_kw, 0);
}

std::vector<SystemRDLParser::Constr_inside_valueContext *> SystemRDLParser::Constr_inside_valuesContext::constr_inside_value() {
  return getRuleContexts<SystemRDLParser::Constr_inside_valueContext>();
}

SystemRDLParser::Constr_inside_valueContext* SystemRDLParser::Constr_inside_valuesContext::constr_inside_value(size_t i) {
  return getRuleContext<SystemRDLParser::Constr_inside_valueContext>(i);
}


size_t SystemRDLParser::Constr_inside_valuesContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstr_inside_values;
}


std::any SystemRDLParser::Constr_inside_valuesContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstr_inside_values(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constr_inside_valuesContext* SystemRDLParser::constr_inside_values() {
  Constr_inside_valuesContext *_localctx = _tracker.createInstance<Constr_inside_valuesContext>(_ctx, getState());
  enterRule(_localctx, 160, SystemRDLParser::RuleConstr_inside_values);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(768);
    constr_lhs();
    setState(769);
    match(SystemRDLParser::INSIDE_kw);
    setState(770);
    match(SystemRDLParser::T__1);
    setState(771);
    constr_inside_value();
    setState(776);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == SystemRDLParser::T__3) {
      setState(772);
      match(SystemRDLParser::T__3);
      setState(773);
      constr_inside_value();
      setState(778);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(779);
    match(SystemRDLParser::T__2);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constr_inside_enumContext ------------------------------------------------------------------

SystemRDLParser::Constr_inside_enumContext::Constr_inside_enumContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

SystemRDLParser::Constr_lhsContext* SystemRDLParser::Constr_inside_enumContext::constr_lhs() {
  return getRuleContext<SystemRDLParser::Constr_lhsContext>(0);
}

tree::TerminalNode* SystemRDLParser::Constr_inside_enumContext::INSIDE_kw() {
  return getToken(SystemRDLParser::INSIDE_kw, 0);
}

tree::TerminalNode* SystemRDLParser::Constr_inside_enumContext::ID() {
  return getToken(SystemRDLParser::ID, 0);
}


size_t SystemRDLParser::Constr_inside_enumContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstr_inside_enum;
}


std::any SystemRDLParser::Constr_inside_enumContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstr_inside_enum(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constr_inside_enumContext* SystemRDLParser::constr_inside_enum() {
  Constr_inside_enumContext *_localctx = _tracker.createInstance<Constr_inside_enumContext>(_ctx, getState());
  enterRule(_localctx, 162, SystemRDLParser::RuleConstr_inside_enum);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(781);
    constr_lhs();
    setState(782);
    match(SystemRDLParser::INSIDE_kw);
    setState(783);
    match(SystemRDLParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constr_lhsContext ------------------------------------------------------------------

SystemRDLParser::Constr_lhsContext::Constr_lhsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* SystemRDLParser::Constr_lhsContext::THIS_kw() {
  return getToken(SystemRDLParser::THIS_kw, 0);
}

SystemRDLParser::Instance_refContext* SystemRDLParser::Constr_lhsContext::instance_ref() {
  return getRuleContext<SystemRDLParser::Instance_refContext>(0);
}


size_t SystemRDLParser::Constr_lhsContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstr_lhs;
}


std::any SystemRDLParser::Constr_lhsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstr_lhs(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constr_lhsContext* SystemRDLParser::constr_lhs() {
  Constr_lhsContext *_localctx = _tracker.createInstance<Constr_lhsContext>(_ctx, getState());
  enterRule(_localctx, 164, SystemRDLParser::RuleConstr_lhs);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(787);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::THIS_kw: {
        enterOuterAlt(_localctx, 1);
        setState(785);
        match(SystemRDLParser::THIS_kw);
        break;
      }

      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 2);
        setState(786);
        instance_ref();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Constr_inside_valueContext ------------------------------------------------------------------

SystemRDLParser::Constr_inside_valueContext::Constr_inside_valueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<SystemRDLParser::ExprContext *> SystemRDLParser::Constr_inside_valueContext::expr() {
  return getRuleContexts<SystemRDLParser::ExprContext>();
}

SystemRDLParser::ExprContext* SystemRDLParser::Constr_inside_valueContext::expr(size_t i) {
  return getRuleContext<SystemRDLParser::ExprContext>(i);
}


size_t SystemRDLParser::Constr_inside_valueContext::getRuleIndex() const {
  return SystemRDLParser::RuleConstr_inside_value;
}


std::any SystemRDLParser::Constr_inside_valueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<SystemRDLVisitor*>(visitor))
    return parserVisitor->visitConstr_inside_value(this);
  else
    return visitor->visitChildren(this);
}

SystemRDLParser::Constr_inside_valueContext* SystemRDLParser::constr_inside_value() {
  Constr_inside_valueContext *_localctx = _tracker.createInstance<Constr_inside_valueContext>(_ctx, getState());
  enterRule(_localctx, 166, SystemRDLParser::RuleConstr_inside_value);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(796);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case SystemRDLParser::T__1:
      case SystemRDLParser::T__5:
      case SystemRDLParser::T__10:
      case SystemRDLParser::BOOLEAN_kw:
      case SystemRDLParser::BIT_kw:
      case SystemRDLParser::LONGINT_kw:
      case SystemRDLParser::TRUE_kw:
      case SystemRDLParser::FALSE_kw:
      case SystemRDLParser::NA_kw:
      case SystemRDLParser::RW_kw:
      case SystemRDLParser::WR_kw:
      case SystemRDLParser::R_kw:
      case SystemRDLParser::W_kw:
      case SystemRDLParser::RW1_kw:
      case SystemRDLParser::W1_kw:
      case SystemRDLParser::RCLR_kw:
      case SystemRDLParser::RSET_kw:
      case SystemRDLParser::RUSER_kw:
      case SystemRDLParser::WOSET_kw:
      case SystemRDLParser::WOCLR_kw:
      case SystemRDLParser::WOT_kw:
      case SystemRDLParser::WZS_kw:
      case SystemRDLParser::WZC_kw:
      case SystemRDLParser::WZT_kw:
      case SystemRDLParser::WCLR_kw:
      case SystemRDLParser::WSET_kw:
      case SystemRDLParser::WUSER_kw:
      case SystemRDLParser::COMPACT_kw:
      case SystemRDLParser::REGALIGN_kw:
      case SystemRDLParser::FULLALIGN_kw:
      case SystemRDLParser::HW_kw:
      case SystemRDLParser::SW_kw:
      case SystemRDLParser::INT:
      case SystemRDLParser::HEX_INT:
      case SystemRDLParser::VLOG_INT:
      case SystemRDLParser::STRING:
      case SystemRDLParser::PLUS:
      case SystemRDLParser::MINUS:
      case SystemRDLParser::BNOT:
      case SystemRDLParser::NOT:
      case SystemRDLParser::NAND:
      case SystemRDLParser::AND:
      case SystemRDLParser::OR:
      case SystemRDLParser::NOR:
      case SystemRDLParser::XOR:
      case SystemRDLParser::XNOR:
      case SystemRDLParser::ID: {
        enterOuterAlt(_localctx, 1);
        setState(789);
        antlrcpp::downCast<Constr_inside_valueContext *>(_localctx)->val = expr(0);
        break;
      }

      case SystemRDLParser::T__11: {
        enterOuterAlt(_localctx, 2);
        setState(790);
        match(SystemRDLParser::T__11);
        setState(791);
        antlrcpp::downCast<Constr_inside_valueContext *>(_localctx)->l_val = expr(0);
        setState(792);
        match(SystemRDLParser::T__9);
        setState(793);
        antlrcpp::downCast<Constr_inside_valueContext *>(_localctx)->r_val = expr(0);
        setState(794);
        match(SystemRDLParser::T__12);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

bool SystemRDLParser::sempred(RuleContext *context, size_t ruleIndex, size_t predicateIndex) {
  switch (ruleIndex) {
    case 22: return exprSempred(antlrcpp::downCast<ExprContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool SystemRDLParser::exprSempred(ExprContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 0: return precpred(_ctx, 13);
    case 1: return precpred(_ctx, 12);
    case 2: return precpred(_ctx, 11);
    case 3: return precpred(_ctx, 10);
    case 4: return precpred(_ctx, 9);
    case 5: return precpred(_ctx, 8);
    case 6: return precpred(_ctx, 7);
    case 7: return precpred(_ctx, 6);
    case 8: return precpred(_ctx, 5);
    case 9: return precpred(_ctx, 4);
    case 10: return precpred(_ctx, 3);
    case 11: return precpred(_ctx, 2);

  default:
    break;
  }
  return true;
}

void SystemRDLParser::initialize() {
  std::call_once(systemrdlParserOnceFlag, systemrdlParserInitialize);
}
