"""
.load /usr/lib/sqlite3/pcre.so

# no even moduli

select count(input) from calls where recipient="0x0000000000000000000000000000000000000005" and input REGEXP '[0,2,4,6,8,a,c,e]$';

# bases larger than modulus?

TODO

# gas usage breakdown by number of occurances
select gasUsed, count(gasUsed) from calls where recipient="0x0000000000000000000000000000000000000005" group by gasUsed

# invocation count per exponent 

TODO 

# all modexp size configurations

select substr(input, 0, 195) as `num` from calls where recipient="0x0000000000000000000000000000000000000005";

"""

distinct_modexp_input_size_query = """
select distinct substr(input, 0, 195) as `num` from calls where recipient="0x0000000000000000000000000000000000000005";
"""

# return breakdown of different exponents used per contract per input configuration
def breakdown_exponent(cursor):
    pass

# check whether all inputs have equal base and modulus size
def check_equal_base_and_mod_size(cursor):
    res = cursor.execute(distinct_modexp_input_size_query)
    input_sizes = res.fetchall()
    input_sizes = [x[0][2:] for x in input_sizes]
    for input_size in input_sizes:
        if input_size[0:64] != input_size[128:192]:
            print("not equal size")

import sqlite3
conn = sqlite3.connect("precompiles.db")
conn.enable_load_extension(True)
conn.load_extension("/usr/lib/sqlite3/pcre.so")

cursor = conn.cursor()

# check if that there are no inputs with even modulus

result = conn.execute("select count(input) from calls where recipient=\"0x0000000000000000000000000000000000000005\" and input REGEXP '[0,2,4,6,8,a,c,e]$';")
count = result.fetchall()[0][0]

print("{} inputs with even modulus".format(count))
check_equal_base_and_mod_size(cursor)

print("checking base and mod size are equal for all inputs")
check_equal_base_and_mod_size(cursor)
