# -*- coding: utf-8 -*-

# This script builds the Unicode tables used by the regex module.
#
# It downloads the data from the Unicode website, saving it locally, and then
# calculates the minimum size of the tables.
#
# Finally, it creates 2 code files, namely "_regex_unicode.h" and
# "_regex_unicode.c".
#
# Various parameters are stored in a local "shelve" file in order to reduce
# the amount of recalculation.
#
# This script is written in Python 3.

import os
import shelve
import sys
import shutil
from collections import defaultdict
from contextlib import closing
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve

this_folder = os.path.dirname(__file__)

# The location of the Unicode data folder.
unicode_folder = os.path.join(this_folder, "Unicode")

# The location of the C sources for the regex engine.
c_folder = os.path.join(this_folder, "regex")

# The paths of the source files to be generated.
h_path = os.path.join(c_folder, "_regex_unicode.h")
c_path = os.path.join(c_folder, "_regex_unicode.c")
properties_path = os.path.join(this_folder, "UnicodeProperties.txt")

# The paths of the C source files.
c_header_path = os.path.join(c_folder, "_regex_unicode.h")
c_source_path = os.path.join(c_folder, "_regex_unicode.c")

# The path of the shelve file.
shelf_path = os.path.splitext(__file__)[0] + ".shf"

# The number of columns in each table.
COLUMNS = 16

# The maximum number of codepoints.
NUM_CODEPOINTS = 0x110000

# The maximum depth of the multi-stage tables.
MAX_STAGES = 5

# Whether to force an update of the Unicode data.
#
# Data is downloaded if needed, but if the Unicode data has been updated on
# the website then you need to force an update.
FORCE_UPDATE = False

# Whether to force recalculation of the smallest table size.
FORCE_RECALC = False

# Whether to count the number of codepoints as a check.
COUNT_CODEPOINTS = False

# If we update then we must recalculate.
if FORCE_UPDATE:
    FORCE_RECALC = True

# Ensure that the Unicode data folder exists.
try:
    os.mkdir(unicode_folder)
except OSError:
    pass

# If the maximum number of stages has changed, then force recalculation.
with closing(shelve.open(shelf_path, writeback=True)) as shelf:
    if shelf.get("MAXSTAGES") != MAX_STAGES:
        shelf["MAXSTAGES"] = MAX_STAGES
        FORCE_RECALC = True
    if FORCE_RECALC:
        try:
            del shelf["CASEFOLDING"]
        except KeyError:
            pass

# Redefine "print" so that it flushes.
real_print = print

def print(*args, **kwargs):
    real_print(*args, **kwargs)
    sys.stdout.flush()

class UnicodeDataError(Exception):
    pass

def determine_data_type(min_value, max_value):
    "Determines the smallest C data type which can store values in a range."

    # 1 byte, unsigned and signed.
    if 0 <= min_value <= max_value <= 0xFF:
        return "RE_UINT8", 1
    if -0x80 <= min_value <= max_value <= 0x7F:
        return "RE_INT8", 1

    # 2 bytes, unsigned and signed.
    if 0 <= min_value <= max_value <= 0xFFFF:
        return "RE_UINT16", 2
    if -0x8000 <= min_value <= max_value <= 0x7FFF:
        return "RE_INT16", 2

    # 4 bytes, unsigned and signed.
    if 0 <= min_value <= max_value <= 0xFFFFFFFF:
        return "RE_UINT32", 4
    if -0x80000000 <= min_value <= max_value <= 0x7FFFFFFF:
        return "RE_INT32", 4

    raise ValueError("value range too big for 32 bits")

def smallest_data_type(min_value, max_value):
    """Determines the smallest integer data type required to store all of the
    values in a range.
    """

    return determine_data_type(min_value, max_value)[0]

def smallest_bytesize(min_value, max_value):
    """Determines the minimum number of bytes required to store all of the
    values in a range.
    """

    return determine_data_type(min_value, max_value)[1]

def product(numbers):
    """Calculates the product of a series of numbers."""

    if not product:
        raise ValueError("product of empty sequence")

    result = 1
    for n in numbers:
        result *= n

    return result

def mul_to_shift(number):
    "Converts a multiplier into a shift."

    shift = number.bit_length() - 1
    if shift < 0 or (1 << shift) != number:
        raise ValueError("can't convert multiplier into shift")

    return shift

class MultistageTable:
    "A multi-stage table."

    def __init__(self, block_sizes, stages, binary):
        self.block_sizes = block_sizes
        self.stages = stages
        self.binary = binary

        self.num_stages = len(self.block_sizes) + 1

        # How many bytes of storage are needed for this table?
        self.bytesize = 0

        for stage in self.stages[ : -1]:
            self.bytesize += (smallest_bytesize(min(stage), max(stage)) *
              len(stage))

        if binary:
            self.bytesize += len(self.stages[-1]) // 8
        else:
            self.bytesize += smallest_bytesize(min(self.stages[-1]),
              max(self.stages[-1])) * len(self.stages[-1])

        # Calculate the block-size products for lookup.
        self._size_products = []
        for stage in range(self.num_stages - 1):
            self._size_products.append(product(self.block_sizes[stage : ]))

class PropertyValue:
    "A property value."

    def __init__(self, name, id):
        self.name = name
        self.id = id

        self.aliases = set()

    def use_pref_name(self):
        """Uses better names for the properties and values if the current one
        is poor.
        """

        self.name, self.aliases = pick_pref_name(self.name, self.aliases)

class Property:
    "A Unicode property."

    def __init__(self, name, entries, value_dict):
        self.name = name
        self.entries = entries

        self._value_list = []
        self._value_dict = {}

        for name, value in sorted(value_dict.items(), key=lambda pair:
          pair[1]):
            val = PropertyValue(name, value)
            self._value_list.append(val)
            self._value_dict[name.upper()] = val

        self.binary = len(self._value_dict.values()) == 2
        self.aliases = set()

    def add(self, val):
        "Adds a value."

        # Make it case-insensitive.
        upper_name = val.name.upper()

        if upper_name in self._value_dict:
            raise KeyError("duplicate value name: {}".format(val.name))

        self._value_list.append(val)
        self._value_dict[upper_name] = val

    def use_pref_name(self):
        """Use a better name for a property or value if the current one is
        poor.
        """

        self.name, self.aliases = pick_pref_name(self.name, self.aliases)

    def make_binary_property(self):
        "Makes this property a binary property."

        if self._value_list:
            raise UnicodeDataError("property '{}' already has values".format(self.name))

        binary_values = [
          ("No", 0, {"N", "False", "F"}),
          ("Yes", 1, {"Y", "True", "T"})
        ]

        for name, v, aliases in binary_values:
            val = PropertyValue(name, v)
            val.aliases |= aliases
            self._value_list.append(val)
            self._value_dict[name.upper()] = val

        self.binary = True

    def generate_code(self, h_file, c_file, info):
        "Generates the code for a property."

        # Build the tables.
        self._build_tables()

        print("Generating code for {}".format(self.name))

        table = self.table

        # Write the property tables.
        c_file.write("""
/* {name}. */
""".format(name=self.name))

        self.generate_tables(c_file)

        # Write the lookup function.
        prototype = "RE_UINT32 re_get_{name}(RE_UINT32 ch)".format(name=self.name.lower())

        h_file.write("{prototype};\n".format(prototype=prototype))

        c_file.write("""
{prototype} {{
""".format(prototype=prototype))

        self._generate_locals(c_file)

        c_file.write("\n")

        self._generate_lookup(c_file)

        c_file.write("""
    return value;
}
""")

    def generate_tables(self, c_file):
        table = self.table

        for stage in range(table.num_stages):
            # The contents of this table.
            entries = table.stages[stage]

            # What data type should we use for the entries?
            if self.binary and stage == table.num_stages - 1:
                data_type = "RE_UINT8"

                entries = self._pack_to_bitflags(entries)
            else:
                data_type = smallest_data_type(min(entries), max(entries))

            # The entries will be stored in an array.
            c_file.write("""
static {data_type} re_{name}_stage_{stage}[] = {{
""".format(data_type=data_type, name=self.name.lower(), stage=stage + 1))

            # Write the entries, nicely aligned in columns.
            entries = ["{},".format(e) for e in entries]

            entry_width = max(len(e) for e in entries)
            entries = [e.rjust(entry_width) for e in entries]

            for start in range(0, len(entries), COLUMNS):
                c_file.write("    {}\n".format(" ".join(entries[start : start +
                  COLUMNS])))

            c_file.write("};\n")

        # Write how much storage will be used by all of the tables.
        c_file.write("""
/* {name}: {bytesize} bytes. */
""".format(name=self.name, bytesize=table.bytesize))

    def _pack_to_bitflags(self, entries):
        entries = tuple(entries)
        new_entries = []

        for start in range(0, len(entries), 8):
            new_entries.append(bitflag_dict[entries[start : start + 8]])

        return new_entries

    def _generate_locals(self, c_file):
        c_file.write("""\
    RE_UINT32 code;
    RE_UINT32 f;
    RE_UINT32 pos;
    RE_UINT32 value;
""")

    def _generate_lookup(self, c_file):
        table = self.table
        name = self.name.lower()

        # Convert the block sizes into shift values.
        shifts = [mul_to_shift(size) for size in table.block_sizes]

        c_file.write("""\
    f = ch >> {field_shift};
    code = ch ^ (f << {field_shift});
    pos = (RE_UINT32)re_{name}_stage_1[f] << {block_shift};
""".format(field_shift=sum(shifts), name=name, block_shift=shifts[0]))

        for stage in range(1, table.num_stages - 1):
            c_file.write("""\
    f = code >> {field_shift};
    code ^= f << {field_shift};
    pos = (RE_UINT32)re_{name}_stage_{stage}[pos + f] << {block_shift};
""".format(field_shift=sum(shifts[stage : ]), name=name, stage=stage + 1,
              block_shift=shifts[stage]))

        # If it's a binary property, we're using bitflags.
        if self.binary:
            c_file.write("""\
    pos += code;
    value = (re_{name}_stage_{stage}[pos >> 3] >> (pos & 0x7)) & 0x1;
""".format(name=self.name.lower(), stage=table.num_stages))
        else:
            c_file.write("""\
    value = re_{name}_stage_{stage}[pos + code];
""".format(name=self.name.lower(), stage=table.num_stages))

    def get(self, name, default=None):
        try:
            return self.__getitem__(name)
        except KeyError:
            return default

    def __len__(self):
        return len(self._value_list)

    def __getitem__(self, name):
        # Make it case-insensitive.
        upper_name = name.upper()

        val = self._value_dict.get(upper_name)
        if not val:
            # Can't find a value with that name, so collect the aliases and try
            # again.
            for val in self._value_list:
                for alias in {val.name} | val.aliases:
                    self._value_dict[alias.upper()] = val

            val = self._value_dict.get(upper_name)

            if not val:
                raise KeyError(name)

        return val

    def __iter__(self):
        for val in self._value_list:
            yield val

    def _build_tables(self):
        "Builds the multi-stage tables."

        stored_name = reduce_name(self.name)

        # Do we already know the best block sizes?
        shelf = shelve.open(shelf_path, writeback=True)

        if FORCE_RECALC:
            # Force calculation of the block sizes and build the tables.
            table = self._build_smallest_table()
        else:
            try:
                # What are the best block sizes?
                block_sizes = shelf[stored_name]["block_sizes"]

                # Build the tables.
                table = self._build_multistage_table(block_sizes)
            except KeyError:
                # Something isn't known, so calculate the best block sizes and
                # build the tables.
                table = self._build_smallest_table()

        # Save the info.
        shelf[stored_name] = {}
        shelf[stored_name]["block_sizes"] = table.block_sizes

        shelf.close()

        self.table = table

    def _build_smallest_table(self):
        """Calculates the block sizes to give the smallest storage requirement
        and builds the multi-stage table.
        """

        print("Determining smallest storage for {}".format(self.name))

        # Initialise with a large value.
        best_block_sizes, smallest_bytesize = None, len(self.entries) * 4

        # Try different numbers and sizes of blocks.
        for block_sizes, bytesize in self._table_sizes(self.entries, 1,
          self.binary):
            print("Block sizes are {}, bytesize is {}".format(block_sizes,
              bytesize))
            if bytesize < smallest_bytesize:
                best_block_sizes, smallest_bytesize = block_sizes, bytesize

        print("Smallest for {} has block sizes {} and bytesize {}".format(self.name,
          best_block_sizes, smallest_bytesize))

        return self._build_multistage_table(best_block_sizes)

    def _table_sizes(self, entries, num_stages, binary):
        """Yields different numbers and sizes of blocks, up to MAX_STAGES.

        All the sizes are powers of 2 and for a binary property the final block
        size is at least 8 because the final stage of the table will be using
        bitflags.
        """

        # What if this is the top stage?
        if binary:
            bytesize = len(entries) // 8
        else:
            bytesize = (smallest_bytesize(min(entries), max(entries)) *
              len(entries))

        yield [], bytesize

        if num_stages >= MAX_STAGES:
            return

        entries = tuple(entries)

        # Initialise the block size and double it on each iteration. Usually an
        # index entry is 1 byte, so a data block should be at least 2 bytes.
        size = 16 if binary else 2

        # There should be at least 2 blocks.
        while size * 2 <= len(entries) and len(entries) % size == 0:
            # Group the entries into blocks.
            indexes = []
            block_dict = {}
            for start in range(0, len(entries), size):
                block = entries[start : start + size]
                indexes.append(block_dict.setdefault(block, len(block_dict)))

            # Collect all the blocks.
            blocks = []
            for block in sorted(block_dict, key=lambda block:
              block_dict[block]):
                blocks.extend(block)

            # How much storage will the blocks stage need?
            if binary:
                block_bytesize = len(blocks) // 8
            else:
                block_bytesize = (smallest_bytesize(min(blocks), max(blocks)) *
                  len(blocks))

            # Yield the higher stages for the indexes.
            for block_sizes, total_bytesize in self._table_sizes(indexes,
              num_stages + 1, False):
                yield block_sizes + [size], total_bytesize + block_bytesize

            # Next size up.
            size *= 2

    def _build_multistage_table(self, block_sizes):
        "Builds a multi-stage table."

        if product(block_sizes) > len(self.entries):
            raise UnicodeDataError("product of block sizes greater than number of entries")


        # Build the stages from the bottom one up.
        entries = self.entries
        stages = []

        for block_size in reversed(block_sizes):
            entries = tuple(entries)

            # Group the entries into blocks.
            block_dict = {}
            indexes = []
            for start in range(0, len(entries), block_size):
                block = entries[start : start + block_size]
                indexes.append(block_dict.setdefault(block, len(block_dict)))

            # Collect all the blocks.
            blocks = []
            for block in sorted(block_dict, key=lambda block:
              block_dict[block]):
                blocks.extend(block)

            # We have a new stage.
            stages.append(blocks)

            # Prepare for the next higher stage.
            entries = indexes

        # We have the top stage.
        stages.append(entries)

        # Put the stages into the correct order (top-down).
        stages.reverse()

        return MultistageTable(block_sizes, stages, self.binary)

class AllCasesProperty(Property):
    "All Unicode cases."

    def __init__(self, name, entries, value_dict):
        self.name = name
        self.entries = entries

        self._value_list = []
        self._value_dict = {}

        for name, value in sorted(value_dict.items(), key=lambda pair:
          pair[1]):
            val = PropertyValue(name, value)
            self._value_list.append(val)
            self._value_dict[name] = val

        self.binary = False
        self.aliases = set()

        # What data type should we use for the cases entries?
        rows = [list(val.name) for val in self._value_list]
        data = [e for r in rows for e in r]
        self.case_data_type = smallest_data_type(min(data), max(data))

    def generate_code(self, h_file, c_file, info):
        "Generates the code for a property."

        print("Generating code for {}".format(self.name))

        # Build the tables.
        self._build_tables()

        # Write the all-cases tables.
        c_file.write("""
/* {name}. */
""".format(name=self.name))

        self.generate_tables(c_file)

        # What data type should we use for the cases entries?
        rows = [list(val.name) for val in self._value_list]

        data = [e for r in rows for e in r[1 : ]]
        data_type, data_size = determine_data_type(min(data), max(data))

        self.case_data_type = data_type

        # Calculate the size of the struct.
        entry_size = data_size * (info["max_cases"] - 1)

        # Pad the cases entries to the same length.
        max_len = max(len(r) for r in rows)
        padding = [0] * (max_len - 1)
        rows = [(r + padding)[ : max_len] for r in rows]

        # Write the entries, nicely aligned in columns.
        rows = [[str(e) for e in r] for r in rows]
        entry_widths = [max(len(e) for e in c) for c in zip(*rows)]
        rows = [[e.rjust(w) for e, w in zip(r, entry_widths)] for r in rows]

        c_file.write("""
static RE_AllCases re_all_cases_table[] = {
""")
        for r in rows:
            c_file.write("    {{{}}},\n".format(", ".join(r)))

        c_file.write("};\n")

        # Write how much storage will be used by the table.
        c_file.write("""
/* {name}: {bytesize} bytes. */
""".format(name=self.name, bytesize=entry_size * len(rows)))

        # Write the lookup function.
        prototype = "int re_get_{name}(RE_UINT32 ch, RE_UINT32* codepoints)".format(name=self.name.lower())

        h_file.write("{prototype};\n".format(prototype=prototype))

        c_file.write("""
{prototype} {{
""".format(name=self.name, prototype=prototype))

        self._generate_locals(c_file)

        c_file.write("""\
    RE_AllCases* all_cases;
    int count;

""")

        self._generate_lookup(c_file)

        c_file.write("""
    all_cases = &re_all_cases_table[value];

    codepoints[0] = ch;
    count = 1;

    while (count < RE_MAX_CASES && all_cases->diffs[count - 1] != 0) {
        codepoints[count] = ch + all_cases->diffs[count - 1];
        ++count;
    }

    return count;
}
""")

class SimpleCaseFoldingProperty(Property):
    "Unicode simple case-folding."

    def __init__(self, name, entries, value_dict):
        self.name = name
        self.entries = entries

        self._value_list = []
        self._value_dict = {}

        for name, value in sorted(value_dict.items(), key=lambda pair:
          pair[1]):
            val = PropertyValue(name, value)
            self._value_list.append(val)
            self._value_dict[name] = val

        self.binary = False
        self.aliases = set()

    def generate_code(self, h_file, c_file, info):
        "Generates the code for a property."

        print("Generating code for {}".format(self.name))

        # Build the tables.
        self._build_tables()

        # Write the case-folding tables.
        c_file.write("""
/* {name}. */
""".format(name=self.name))

        self.generate_tables(c_file)

        # What data type should we use for the case-folding entries?
        rows = [val.name for val in self._value_list]

        # Calculate the size of an entry, including alignment.
        entry_size = 4

        # Write the entries, nicely aligned in columns.
        rows = [str(r) for r in rows]
        entry_width = max(len(r) for r in rows)
        rows = [r.rjust(entry_width) for r in rows]

        c_file.write("""
static RE_INT32 re_simple_case_folding_table[] = {
""")
        for r in rows:
            c_file.write("    {},\n".format(r))

        c_file.write("};\n")

        # Write how much storage will be used by the table.
        c_file.write("""
/* {name}: {bytesize} bytes. */
""".format(name=self.name, bytesize=entry_size * len(rows)))

        # Write the lookup function.
        prototype = "RE_UINT32 re_get_{name}(RE_UINT32 ch)".format(name=self.name.lower())

        h_file.write("{prototype};\n".format(prototype=prototype))

        c_file.write("""
{prototype} {{
""".format(name=self.name, prototype=prototype))

        self._generate_locals(c_file)

        c_file.write("""\
    RE_INT32 diff;

""")

        self._generate_lookup(c_file)

        c_file.write("""
    diff = re_simple_case_folding_table[value];

    return ch + diff;
}
""")

class FullCaseFoldingProperty(Property):
    "Unicode full case-folding."

    def __init__(self, name, entries, value_dict):
        self.name = name
        self.entries = entries

        self._value_list = []
        self._value_dict = {}

        for name, value in sorted(value_dict.items(), key=lambda pair:
          pair[1]):
            val = PropertyValue(name, value)
            self._value_list.append(val)
            self._value_dict[name] = val

        self.binary = False
        self.aliases = set()

    def generate_code(self, h_file, c_file, info):
        "Generates the code for a property."

        print("Generating code for {}".format(self.name))

        # Build the tables.
        self._build_tables()

        # Write the case-folding tables.
        c_file.write("""
/* {name}. */
""".format(name=self.name))

        self.generate_tables(c_file)

        # What data type should we use for the case-folding entries?
        rows = [list(val.name) for val in self._value_list]

        # The diff entry needs to be signed 32-bit, the others should be OK
        # with unsigned 16-bit.
        data = [e for r in rows for e in r[1 : ]]

        # Verify that unsigned 16-bit is OK.
        data_type = smallest_data_type(min(data), max(data))
        if data_type != "RE_UINT16":
            raise UnicodeDataError("full case-folding table entry too big")

        # Calculate the size of an entry, including alignment.
        entry_size = 4 + 2 * (info["max_folded"] - 1)
        excess = entry_size % 4
        if excess > 0:
            entry_size += 4 - excess

        # Pad the case-folding entries to the same length and append the count.
        max_len = max(len(r) for r in rows)
        padding = [0] * (max_len - 1)
        rows = [(r + padding)[ : max_len] for r in rows]

        # Write the entries, nicely aligned in columns.
        rows = [[str(e) for e in r] for r in rows]
        entry_widths = [max(len(e) for e in c) for c in zip(*rows)]
        rows = [[e.rjust(w) for e, w in zip(r, entry_widths)] for r in rows]

        c_file.write("""
static RE_FullCaseFolding re_full_case_folding_table[] = {
""")
        for r in rows:
            c_file.write("    {{{}}},\n".format(", ".join(r)))

        c_file.write("};\n")

        # Write how much storage will be used by the table.
        c_file.write("""
/* {name}: {bytesize} bytes. */
""".format(name=self.name, bytesize=entry_size * len(rows)))

        # Write the lookup function.
        prototype = "int re_get_{name}(RE_UINT32 ch, RE_UINT32* codepoints)".format(name=self.name.lower())

        h_file.write("{prototype};\n".format(prototype=prototype))

        c_file.write("""
{prototype} {{
""".format(name=self.name, prototype=prototype))

        self._generate_locals(c_file)

        c_file.write("""\
    RE_FullCaseFolding* case_folding;
    int count;

""")

        self._generate_lookup(c_file)

        c_file.write("""
    case_folding = &re_full_case_folding_table[value];

    codepoints[0] = ch + case_folding->diff;
    count = 1;

    while (count < RE_MAX_FOLDED && case_folding->codepoints[count - 1] != 0) {
        codepoints[count] = case_folding->codepoints[count - 1];
        ++count;
    }

    return count;
}
""")

class CompoundProperty(Property):
    "A compound Unicode property."

    def __init__(self, name, function):
        Property.__init__(self, name, [], {})
        self.function = function

    def generate_code(self, h_file, c_file, info):
        "Generates the code for a property."

        print("Generating code for {}".format(self.name))

        # Write the lookup function.
        prototype = "RE_UINT32 re_get_{name}(RE_UINT32 ch)".format(name=self.name.lower())

        h_file.write("{prototype};\n".format(prototype=prototype))

        c_file.write("""
/* {name}. */

{prototype} {{
{function}}}
""".format(name=self.name, prototype=prototype, function=self.function))

class PropertySet:
    "An ordered set of Unicode properties."

    def __init__(self):
        self._property_list = []
        self._property_dict = {}

    def add(self, prop):
        "Adds a property."

        # Make it case-insensitive.
        upper_name = prop.name.upper()

        if upper_name in self._property_dict:
            raise KeyError("duplicate property name: {}".format(prop.name))

        prop.id = len(self._property_list)
        self._property_list.append(prop)
        self._property_dict[upper_name] = prop

    def use_pref_name(self):
        """Use a better name for a property or value if the current one is
        poor.
        """

        for prop in self._property_list:
            prop.use_pref_name()

    def get(self, name, default=None):
        try:
            return self.__getitem__(name)
        except KeyError:
            return default

    def __len__(self):
        return len(self._property_list)

    def __getitem__(self, name):
        # Make it case-insensitive.
        upper_name = name.upper()

        prop = self._property_dict.get(upper_name)
        if not prop:
            # Can't find a property with that name, so collect the aliases and
            # try again.
            for prop in self._property_list:
                for alias in {prop.name} | prop.aliases:
                    self._property_dict[alias.upper()] = prop

            prop = self._property_dict.get(upper_name)

            if not prop:
                raise KeyError(name)

        return prop

    def __iter__(self):
        for prop in self._property_list:
            yield prop

def download_unicode_file(url, unicode_folder):
    "Downloads a Unicode file."

    name = urlparse(url).path.rsplit("/")[-1]
    path = os.path.join(unicode_folder, name)

    # Do we need to download it?
    if os.path.isfile(path) and not FORCE_UPDATE:
        return

    print("Downloading {} to {}".format(url, path))

    new_path = os.path.splitext(path)[0] + ".new"

    try:
        urlretrieve(url, new_path)
    except ValueError:
        # Failed to download, so clean up and report it.
        try:
            os.remove(new_path)
        except OSError:
            pass

        raise

    os.remove(path)
    os.rename(new_path, path)

    # Is this a new version of the file?
    with open(path, encoding="utf-8") as file:
        # Normally the first line of the file contains its versioned name.
        line = file.readline()
        if line.startswith("#") and line.endswith(".txt\n"):
            versioned_name = line.strip("# \n")
            versioned_path = os.path.join(unicode_folder, versioned_name)
            if not os.path.isfile(versioned_path):
                # We don't have this version, so copy it.
                shutil.copy2(path, versioned_path)
                print("Updated to {}".format(versioned_name))

def reduce_name(name):
    "Reduces a name to uppercase without punctuation, unless it's numeric."

    r = reduced_names.get(name)
    if r is None:
        if all(part.isdigit() for part in name.lstrip("-").split("/", 1)):
            r = name
        else:
            r = name.translate(reduce_trans).upper()

        reduced_names[name] = r

    return r

def std_name(name):
    "Standardises the form of a name to its first occurrence"

    r = reduce_name(name)
    s = standardised_names.get(r)
    if s is None:
        s = name.replace(" ", "_")
        standardised_names[r] = s

    return s

def parse_property_aliases(unicode_folder, filename):
    "Parses the PropertyAliases data."

    print("Parsing '{}'".format(filename))

    path = os.path.join(unicode_folder, filename)

    property_aliases = {}

    for line in open(path):
        line = line.partition("#")[0].strip()
        if line:
            # Format is: abbrev., pref., other...
            fields = [std_name(f.strip()) for f in line.split(";")]

            pref_name = fields.pop(1)
            aliases = set(fields)

            for name in {pref_name} | aliases:
                property_aliases[name] = (pref_name, aliases)

    return property_aliases

def parse_value_aliases(unicode_folder, filename):
    "Parses the PropertyValueAliases data."

    print("Parsing '{}'".format(filename))

    path = os.path.join(unicode_folder, filename)

    value_aliases = defaultdict(dict)

    for line in open(path):
        line = line.partition("#")[0].strip()
        if line:
            # Format is: property, abbrev., pref., other...
            # except for "ccc": property, numeric, abbrev., pref., other...
            fields = [std_name(f.strip()) for f in line.split(";")]

            prop_name = fields.pop(0)
            if prop_name == "ccc":
                pref_name = fields.pop(2)
            else:
                pref_name = fields.pop(1)

            aliases = set(fields)

            # Sometimes there's no abbreviated name, which is indicated by
            # "n/a".
            aliases.discard("n/a")

            prop = value_aliases[prop_name]
            for name in {pref_name} | aliases:
                prop[name] = (pref_name, aliases)

    return value_aliases

def check_codepoint_count(entries, codepoint_counts):
    "Checks that the number of codepoints is correct."
    counts = defaultdict(int)
    for e in entries:
        counts[e] += 1

    for name, value, expected in codepoint_counts:
        if counts[value] != expected:
            raise UnicodeDataError("codepoint count mismatch: expected {} with '{}' but saw {} [value is {}]".format(expected,
              name, counts[value], value))

def parse_data_file(filename, properties, numeric_values=False):
    "Parses a multi-value file."

    print("Parsing '{}'".format(filename))

    path = os.path.join(unicode_folder, filename)

    # Initialise with the default value.
    entries = [0] * NUM_CODEPOINTS
    value_dict = {}
    aliases = {}

    prop_name = prop_alias = None
    default = default_alias = None
    val_alias = None
    listed_values = False

    value_field = 1

    codepoint_counts = []

    if numeric_values:
        prop_name = std_name("Numeric_Value")
        value_field = 3

    # Parse the data file.
    #
    # There is a certain amount of variation in the file format, which is why
    # it takes so many lines of code to parse it.
    for line in open(path):
        if line.startswith("#"):
            if line.startswith("# Property:"):
                # The name of a property.
                prop_name = std_name(line.rsplit(None, 1)[-1])
                prop_alias = None
                print("    Property '{}'".format(prop_name))

                listed_values = True
            elif line.startswith("# Derived Property:"):
                # It's a new property.
                if prop_name:
                    # Should we check the number of codepoints?
                    if COUNT_CODEPOINTS:
                        check_codepoint_count(entries, codepoint_counts)
                        codepoint_counts = []

                    # Save the current property.
                    if any(entries):
                        prop = Property(prop_name, entries, value_dict)
                        if prop_alias:
                            prop.aliases.add(prop_alias)
                        properties.add(prop)

                    # Reset for the new property.
                    entries = [0] * NUM_CODEPOINTS

                words = line.split()

                if words[-1].endswith(")"):
                    # It ends with something in parentheses, possibly more
                    # than one word.
                    while not words[-1].startswith("("):
                        words.pop()

                    prop_name, prop_alias = words[-2], words[-1].strip("()")
                    if prop_alias.lower() in {prop_name.lower(), "deprecated"}:
                        prop_alias = None
                else:
                    prop_name, prop_alias = words[-1], None

                prop_name = std_name(prop_name)
                if prop_alias:
                    prop_alias = std_name(prop_alias)

                if prop_alias:
                    print("    Property '{}' alias '{}'".format(prop_name,
                      prop_alias))
                else:
                    print("    Property '{}'".format(prop_name))
            elif line.startswith("#  All code points not explicitly listed for "):
                # The name of a property.
                new = std_name(line.rsplit(None, 1)[1])
                if prop_name:
                    if new != prop_name:
                        raise UnicodeDataError("property mismatch: saw '{}' and then '{}'".format(prop_name,
                          new))
                else:
                    prop_name = new
                    prop_alias = None
                    print("    Property '{}'".format(prop_name))

                    listed_values = True
            elif line.startswith("#  have the value "):
                # The name of the default value.
                words = line.rsplit(None, 2)

                default, default_alias = words[-1].rstrip("."), None
                if default[ : 1] + default[-1 : ] == "()":
                    # The last word looks line an alias in parentheses.
                    default, default_alias = words[-2], default[1 : -1]

                    if default_alias in {default, "deprecated"}:
                        default_alias = None

                default = std_name(default)
                if default_alias:
                    default_alias = std_name(default_alias)

                value_dict.setdefault(default, 0)

                if default_alias:
                    print("        Default '{}' alias '{}'".format(default, default_alias))
                else:
                    print("        Default '{}'".format(default))

                listed_values = True
            elif line.startswith("# @missing:"):
                # The name of the default value.
                new = std_name(line.rsplit(None, 1)[-1])
                if default:
                    if new != default:
                        raise UnicodeDataError("default mismatch: saw '{}' and then '{}'".format(default,
                          new))
                else:
                    default = new

                    value_dict.setdefault(default, 0)
                    print("        Default '{}' => 0".format(default))

                listed_values = True
            elif line.startswith("# Total code points:"):
                # The number of codepoints with this value or property.
                expected = int(line.rsplit(None, 1)[1])

                if not listed_values:
                    value = 1

                codepoint_counts.append((v, value, expected))
            elif prop_name and line.startswith("# {}=".format(prop_name)):
                # The alias of the value.
                val_alias = std_name(line.rsplit("=")[-1].strip())
                print("        Value '{}'".format(val_alias))
        elif ";" in line:
            # Discard any comment and then split into fields.
            fields = line.split("#", 1)[0].split(";")
            code_range = [int(f, 16) for f in fields[0].split("..")]
            v = std_name(fields[value_field].strip())

            if listed_values:
                # The values of a property.
                if v in {default, default_alias}:
                    value = 0
                else:
                    if not default:
                        if val_alias:
                            default = val_alias
                            print("        Default '{}'".format(default))
                        else:
                            raise UnicodeDataError("unknown default")

                    value = value_dict.get(v)
                    if value is None:
                        value = value_dict.setdefault(v, len(value_dict))

                        if val_alias and val_alias != v:
                            aliases[val_alias] = v

                            print("        Value '{}' alias '{}' => {}".format(val_alias,
                              v, value))

                            val_alias = None
                        else:
                            print("        Value '{}' => {}".format(v, value))
            else:
                # It's a binary property.
                if v != prop_name:
                    if prop_name:
                        # Should we check the number of codepoints?
                        if COUNT_CODEPOINTS:
                            check_codepoint_count(entries, codepoint_counts)
                            codepoint_counts = []

                        # Save the current property.
                        prop = Property(prop_name, entries, value_dict)
                        if prop_alias:
                            prop.aliases.add(prop_alias)
                        properties.add(prop)

                        # Reset for the new property.
                        entries = [0] * NUM_CODEPOINTS

                    prop_name = v
                    print("    Property '{}'".format(prop_name))

                value = 1

            # Store the entries in the range.
            for code in range(code_range[0], code_range[-1] + 1):
                entries[code] = value

    if not prop_name:
        raise UnicodeDataError("unknown property name")

    # Should we check the number of codepoints?
    if COUNT_CODEPOINTS:
        check_codepoint_count(entries, codepoint_counts)
        codepoint_counts = []

    if "Grapheme" in filename:
        # In Unicode 6.1, there are no entries in the
        # "GraphemeBreakProperty.txt" file with the value "Prepend", so we need
        # to add it here in order not to break the code.
        value_dict.setdefault(std_name("Prepend"), len(value_dict))

    # Save the property.
    prop = Property(prop_name, entries, value_dict)
    if prop_alias:
        prop.aliases.add(prop_alias)
    if listed_values and default_alias:
        if default_alias in value_dict:
            default, default_alias = default_alias, default

        prop[default].aliases.add(default_alias)

    for name, alias in aliases.items():
        prop[alias].aliases.add(name)

    properties.add(prop)

def parse_NumericValues_file(filename, properties):
    "Parses the 'NumericValues' file."
    parse_data_file(filename, properties, numeric_values=True)

def parse_CaseFolding(file_name):
    "Parses the Unicode CaseFolding file."

    path = os.path.join(unicode_folder, file_name)

    print("Parsing '{}'".format(file_name))

    # Initialise with the default value.
    simple_folding_entries = [0] * NUM_CODEPOINTS
    simple_folding_value_dict = {0: 0}

    full_folding_entries = [0] * NUM_CODEPOINTS
    full_folding_value_dict = {(0, ): 0}

    equivalent_dict = defaultdict(set)
    expand_set = set()

    turkic_set = set()
    for line in open(path):
        if not line.startswith("#") and ";" in line:
            fields = line.split(";")
            code = int(fields[0], 16)
            fold_type = fields[1].strip()
            folded = [int(f, 16) for f in fields[2].split()]

            if fold_type in "CFS":
                # Determine the equivalences.
                equiv_set = set()
                for c in [(code, ), tuple(folded)]:
                    equiv_set |= equivalent_dict.get(c, {c})

                for c in equiv_set:
                    equivalent_dict[c] = equiv_set

            entry = [folded[0] - code] + folded[1 : ]

            if fold_type in "CS":
                value = simple_folding_value_dict.setdefault(entry[0],
                  len(simple_folding_value_dict))
                simple_folding_entries[code] = value

            if fold_type in "CF":
                value = full_folding_value_dict.setdefault(tuple(entry),
                  len(full_folding_value_dict))
                full_folding_entries[code] = value

                if len(entry) > 1:
                    expand_set.add(code)

            if fold_type == "T":
                # Turkic folded cases.
                turkic_set.add((code, tuple(folded)))

    # Is the Turkic set what we expected?
    if turkic_set != {(0x49, (0x131, )), (0x130, (0x69, ))}:
        raise UnicodeDataError("Turkic set has changed")

    # Add the Turkic set to the equivalences. Note that:
    #
    #    dotted_capital == dotted_small
    #
    # and:
    #
    #    dotted_small == dotless_capital
    #
    # but:
    #
    #    dotted_capital != dotless_capital
    #
    for code, folded in turkic_set:
        char1, char2 = (code, ), folded
        equivalent_dict[char1] = equivalent_dict[char1] | {char2}
        equivalent_dict[char2] = equivalent_dict[char2] | {char1}

    # Sort the equivalent cases.
    other_cases = []
    for code, equiv_set in equivalent_dict.items():
        if len(code) == 1:
            diff_list = []
            for e in equiv_set - {code}:
                if len(e) == 1:
                    diff_list.append(e[0] - code[0])
            other_cases.append((code[0], sorted(diff_list)))

    other_cases.sort()

    # How many other cases can there be?
    max_other_cases = max(len(diff_list) for code, diff_list in other_cases)

    # Initialise with the default value.
    default_value = [0] * max_other_cases
    others_entries = [0] * NUM_CODEPOINTS
    others_value_dict = {tuple(default_value): 0}

    for code, diff_list in other_cases:
        entry = tuple(diff_list + default_value)[ : max_other_cases]
        value = others_value_dict.setdefault(entry, len(others_value_dict))
        others_entries[code] = value

    # Save the all-cases property.
    all_prop = AllCasesProperty(std_name("All_Cases"), others_entries,
      others_value_dict)

    # Save the simple case-folding property.
    simple_folding_prop = SimpleCaseFoldingProperty(std_name("Simple_Case_Folding"),
      simple_folding_entries, simple_folding_value_dict)

    # Save the full case-folding property.
    full_folding_prop = FullCaseFoldingProperty(std_name("Full_Case_Folding"),
      full_folding_entries, full_folding_value_dict)

    info = dict(all_cases=all_prop, simple_case_folding=simple_folding_prop,
      full_case_folding=full_folding_prop, expand_set=expand_set)

    return info

def define_Alphanumeric_property(properties):
    "Defines the Alphanumeric property."

    prop_name = std_name("Alphanumeric")

    print("Defining '{}'".format(prop_name))

    function = """\
    RE_UINT32 v;

    v = re_get_alphabetic(ch);
    if (v == 1)
        return 1;

    v = re_get_general_category(ch);
    if (v == RE_PROP_ND)
        return 1;

    return 0;
"""

    properties.add(CompoundProperty(prop_name, function))

def define_Any_property(properties):
    "Defines the Any property."

    prop_name = std_name("Any")

    print("Defining '{}'".format(prop_name))

    function = """\
    return 1;
"""

    properties.add(CompoundProperty(prop_name, function))

def define_Assigned_property(properties):
    "Defines the Assigned property."

    prop_name = std_name("Assigned")

    print("Defining '{}'".format(prop_name))

    function = """\
    if (re_get_general_category(ch) != RE_PROP_CN)
        return 1;

    return 0;
"""

    properties.add(CompoundProperty(prop_name, function))

def define_Blank_property(properties):
    "Defines the Blank property."

    prop_name = std_name("Blank")

    print("Defining '{}'".format(prop_name))

    function = """\
    RE_UINT32 v;

    if (0x0A <= ch && ch <= 0x0D || ch == 0x85)
        return 0;

    v = re_get_white_space(ch);
    if (v == 0)
        return 0;

    v = re_get_general_category(ch);
    if ((RE_BLANK_MASK & (1 << v)) != 0)
        return 0;

    return 1;
"""

    properties.add(CompoundProperty(prop_name, function))

def define_Graph_property(properties):
    "Defines the Graph property."

    prop_name = std_name("Graph")

    print("Defining '{}'".format(prop_name))

    function = """\
    RE_UINT32 v;

    v = re_get_white_space(ch);
    if (v == 1)
        return 0;

    v = re_get_general_category(ch);
    if ((RE_GRAPH_MASK & (1 << v)) != 0)
        return 0;

    return 1;
"""

    properties.add(CompoundProperty(prop_name, function))

def define_Print_property(properties):
    "Defines the Print property."

    prop_name = std_name("Print")

    print("Defining '{}'".format(prop_name))

    function = """\
    RE_UINT32 v;

    v = re_get_general_category(ch);
    if (v == RE_PROP_CC)
        return 0;

    v = re_get_graph(ch);
    if (v == 1)
        return 1;

    v = re_get_blank(ch);
    if (v == 1)
        return 1;

    return 0;
"""

    properties.add(CompoundProperty(prop_name, function))

def define_Word_property(properties):
    "Defines the Word property."

    prop_name = std_name("Word")

    print("Defining '{}'".format(prop_name))

    function = """\
    RE_UINT32 v;

    v = re_get_alphabetic(ch);
    if (v == 1)
        return 1;

    v = re_get_general_category(ch);
    if ((RE_WORD_MASK & (1 << v)) != 0)
        return 1;

    return 0;
"""

    properties.add(CompoundProperty(prop_name, function))

def first_true(iterable):
    "Returns the first item which is true."

    for i in iterable:
        if i:
            return i

    return None

def pick_pref_name(name, aliases):
    "Picks a better name if the current one is poor."

    if name.isupper() or name.isdigit():
        aliases = aliases | {name}

        better_name = max(aliases, key=lambda name: len(name))

        name = better_name
        aliases.remove(better_name)

    return name, aliases

def write_properties_description(properties, properties_path):
    "Writes a list of the properties which are supported by this module."

    with open(properties_path, "w", encoding="utf-8", newline="\n") as p_file:
        p_file.write("The following is a list of the {} properties which are supported by this module:\n".format(len(properties)))

        sorted_properties = sorted(properties, key=lambda prop: prop.name)
        for prop in sorted_properties:
            p_file.write("\n")

            name = prop.name
            aliases = sorted(prop.aliases)
            if aliases:
                p_file.write("{} [{}]\n".format(name, ", ".join(aliases)))
            else:
                p_file.write("{}\n".format(name))

            sorted_values = sorted(prop, key=lambda val: val.name)

            for val in sorted_values:
                name = val.name
                aliases = sorted(val.aliases)
                if aliases:
                    p_file.write("    {} [{}]\n".format(name,
                      ", ".join(aliases)))
                else:
                    p_file.write("    {}\n".format(name))

def tabulate(rows):
    "Creates a table with right-justified columns."

    # Convert all the entries to strings.
    rows = [[str(e) for e in row] for row in rows]

    # Determine the widths of the columns.
    widths = [max(len(e) for e in column) for column in zip(*rows)]

    # Pad all the entries.
    rows = [[e.rjust(w) for e, w in zip(row, widths)] for row in rows]

    return rows

def parse_unicode_data():
    "Parses the Unicode data."

    # Parse the aliases.
    property_aliases = parse_property_aliases(unicode_folder,
      "PropertyAliases.txt")
    value_aliases = parse_value_aliases(unicode_folder,
      "PropertyValueAliases.txt")

    # The set of properties.
    properties = PropertySet()

    # The parsers for the various file formats.
    parsers = {"": parse_data_file, "NumericValues": parse_NumericValues_file}

    # Parse the property data files.
    for line in unicode_info.splitlines():
        if line and line[0] != "#":
            url, sep, file_format = line.partition(":")

            if file_format != "~":
                filename = url.rpartition("/")[-1]
                parsers[file_format](filename, properties)

    # Parse the case-folding data specially.
    info = parse_CaseFolding("CaseFolding.txt")

    max_cases = max(len(val.name) for val in info["all_cases"]) + 1
    max_folded = max(len(val.name) for val in info["full_case_folding"])

    # Define some additional properties.
    define_Alphanumeric_property(properties)
    define_Any_property(properties)
    define_Assigned_property(properties)
    define_Blank_property(properties)
    define_Graph_property(properties)
    define_Print_property(properties)
    define_Word_property(properties)

    # The additional General_Category properties.
    gc_prop = properties["General_Category"]
    gc_short = {}
    gc_masks = defaultdict(int)
    for val in gc_prop:
        short_name = [a.upper() for a in {val.name} | val.aliases if len(a) ==
          2][0]
        gc_short[short_name] = val.id
        gc_masks[short_name[0]] |= 1 << val.id

    last_id = max(val.id for val in gc_prop)
    for name in sorted(gc_masks):
        last_id += 1
        val = PropertyValue(name, last_id)
        val.aliases.add(name + "&")
        gc_prop.add(val)

    # Add the value aliases for the binary properties.
    print("Checking binary properties")
    for prop in properties:
        if len(prop) == 0:
            prop.make_binary_property()

    # Add the property and value aliases.
    print("Adding aliases")
    for prop in properties:
        try:
            pref_name, aliases = property_aliases[prop.name]
            prop_aliases = {prop.name, pref_name} | aliases
            prop.aliases |= prop_aliases - {prop.name}

            val_aliases = first_true(value_aliases.get(a) for a in prop_aliases)
            if val_aliases:
                for i, val in enumerate(prop):
                    try:
                        pref_name, aliases = val_aliases[val.name]
                        aliases = {val.name, pref_name} | aliases
                        val.aliases |= aliases - {val.name}
                    except KeyError:
                        pass
        except KeyError:
            pass

    # Additional aliases.
    prop = properties["Alphanumeric"]
    prop.aliases.add(std_name("AlNum"))

    prop = properties["Hex_Digit"]
    prop.aliases.add(std_name("XDigit"))

    # Ensure that all the properties and values use the preferred name.
    properties.use_pref_name()

    info.update(dict(properties=properties, max_cases=max_cases,
      max_folded=max_folded, gc_short=gc_short, gc_masks=gc_masks))

    return info

def generate_code(strings):
    "Generates the C files."

    h_file = open(h_path, "w", encoding="utf-8", newline="\n")
    c_file = open(c_path, "w", encoding="utf-8", newline="\n")

    # Useful definitions.
    h_file.write("""\
typedef unsigned char RE_UINT8;
typedef signed char RE_INT8;
typedef unsigned short RE_UINT16;
typedef signed short RE_INT16;
typedef unsigned int RE_UINT32;
typedef signed int RE_INT32;

typedef unsigned char BOOL;
enum {{FALSE, TRUE}};

#define RE_ASCII_MAX 0x7F
#define RE_LOCALE_MAX 0xFF
#define RE_UNICODE_MAX 0x10FFFF

#define RE_MAX_CASES {max_cases}
#define RE_MAX_FOLDED {max_folded}

typedef struct RE_Property {{
    RE_UINT16 name;
    RE_UINT8 id;
    RE_UINT8 value_set;
}} RE_Property;

typedef struct RE_PropertyValue {{
    RE_UINT16 name;
    RE_UINT8 value_set;
    RE_UINT8 id;
}} RE_PropertyValue;

typedef RE_UINT32 (*RE_GetPropertyFunc)(RE_UINT32 ch);

""".format(max_cases=info["max_cases"], max_folded=info["max_folded"]))

    for prop in ("GC", "Cased", "Uppercase", "Lowercase"):
        h_file.write("#define RE_PROP_{} 0x{:X}\n".format(prop.upper(), properties[prop].id))

    h_file.write("\n")

    RE_Property_size = 4
    RE_PropertyValue_size = 4

    # Define the property types.
    last_val_id = max(info["gc_short"].values())
    for val_id, name in enumerate(sorted(info["gc_masks"]), start=last_val_id + 1):
        h_file.write("#define RE_PROP_{} {}\n".format(name, val_id))

    h_file.write("\n")

    # Write the General_Category properties.
    for name, val_id in sorted(info["gc_short"].items(), key=lambda pair: pair[1]):
        h_file.write("#define RE_PROP_{} {}\n".format(name, val_id))

    h_file.write("\n")

    # Define a property masks.
    for name, mask in sorted(info["gc_masks"].items()):
        h_file.write("#define RE_PROP_{}_MASK 0x{:08X}\n".format(name, mask))

    h_file.write("\n")

    # The common abbreviated properties.
    common_props = """
AlNum
Alpha
Any
Assigned
Blank
Cntrl
Digit
Graph
Lower
Print
Punct
Space
Upper
Word
XDigit
""".split()

    for name in common_props:
        prop = properties.get(name)
        if prop is not None:
            h_file.write("#define RE_PROP_{} 0x{:06X}\n".format(name.upper(),
              prop.id << 16 | 1))
        else:
            prop = properties["GC"]
            val = prop.get(name)
            if val is not None:
                h_file.write("#define RE_PROP_{} 0x{:06X}\n".format(name.upper(),
                  prop.id << 16 | val.id))
            else:
                raise UnicodeDataError("unknown abbreviated property: '{}'".format(name))

    prop = properties["Block"]
    h_file.write("#define RE_PROP_ASCII 0x{:06X}\n".format((prop.id << 16) | prop["ASCII"].id))

    h_file.write("\n")

    # Define the word-break values.
    for val in properties["Word_Break"]:
        name = reduce_name(val.name)
        h_file.write("#define RE_BREAK_{} {}\n".format(name, val.id))

    h_file.write("\n")

    # Define the grapheme cluster-break values.
    for val in properties["Grapheme_Cluster_Break"]:
        name = reduce_name(val.name)
        h_file.write("#define RE_GBREAK_{} {}\n".format(name, val.id))

    c_file.write('#include "_regex_unicode.h"\n')

    # Write the standardised strings.
    c_file.write("""
#define RE_BLANK_MASK ((1 << RE_PROP_ZL) | (1 << RE_PROP_ZP))
#define RE_GRAPH_MASK ((1 << RE_PROP_CC) | (1 << RE_PROP_CS) | (1 << RE_PROP_CN))
#define RE_WORD_MASK (RE_PROP_M_MASK | (1 << RE_PROP_ND) | (1 << RE_PROP_PC))

typedef struct RE_AllCases {{
    {data_type} diffs[RE_MAX_CASES - 1];
}} RE_AllCases;

typedef struct RE_FullCaseFolding {{
    RE_INT32 diff;
    RE_UINT16 codepoints[RE_MAX_FOLDED - 1];
}} RE_FullCaseFolding;

/* strings. */

char* re_strings[] = {{
""".format(data_type=info["all_cases"].case_data_type))

    # Calculate the number and size of the string constants.
    bytesize = 0
    for s in strings:
        s = reduce_name(s)
        c_file.write("    \"{}\",\n".format(s))
        bytesize += len(s) + 1

    h_file.write("\nextern char* re_strings[{}];\n".format(len(strings)))

    c_file.write("""}};

/* strings: {bytesize} bytes. */
""".format(bytesize=bytesize))

    # Write the property name tables.
    #
    # Properties which are aliases have the same property id, and properties,
    # such as binary properties, which have the same set of values have the
    # same value set id.

    # The rows of the property and value tables.
    property_rows = []
    value_rows = []

    # The value sets.
    value_sets = {}

    # Give an id to each distinct property or value name.
    strings = {s: i for i, s in enumerate(strings)}
    for prop in properties:
        val_set = tuple(val.name for val in prop)
        new_val_set = val_set not in value_sets
        val_set_id = value_sets.setdefault(val_set, len(value_sets))

        # name of property, id of property, id of value set
        property_rows.append((strings[prop.name], prop.id, val_set_id))
        for alias in prop.aliases:
            property_rows.append((strings[alias], prop.id, val_set_id))

        # We don't want to duplicate value sets.
        if new_val_set:
            for val in prop:
                # name of value, id of value set, value
                value_rows.append((strings[val.name], val_set_id, val.id))
                for alias in val.aliases:
                    value_rows.append((strings[alias], val_set_id, val.id))

    # Fix the column widths of the tables.
    property_rows = tabulate(property_rows)
    value_rows = tabulate(value_rows)

    expand_set = info["expand_set"]

    expand_data_type, expand_data_size = determine_data_type(min(expand_set),
      max(expand_set))

    # write the property tables and the corresponding lookup functions.
    c_file.write("""
/* properties. */

RE_Property re_properties[] = {
""")

    h_file.write("""\
extern RE_Property re_properties[{prop_rows}];
extern RE_PropertyValue re_property_values[{val_rows}];
extern {data_type} re_expand_on_folding[{expand_rows}];
extern RE_GetPropertyFunc re_get_property[{func_count}];

""".format(prop_rows=len(property_rows), val_rows=len(value_rows),
      data_type=expand_data_type, expand_rows=len(expand_set),
      func_count=len(properties)))

    for row in property_rows:
        c_file.write("    {{{}}},\n".format(", ".join(row)))

    c_file.write("""\
}};

/* properties: {bytesize} bytes. */

/* property values. */

RE_PropertyValue re_property_values[] = {{
""".format(bytesize=RE_Property_size * len(property_rows)))

    for row in value_rows:
        c_file.write("    {{{}}},\n".format(", ".join(row)))

    c_file.write("""\
}};

/* property values: {bytesize} bytes. */

/* Codepoints which expand on full case-folding. */

{data_type} re_expand_on_folding[] = {{
""".format(bytesize=RE_PropertyValue_size * len(value_rows),
      data_type=expand_data_type))

    items = ["{},".format(c) for c in sorted(expand_set)]
    width = max(len(i) for i in items)
    items = [i.rjust(width) for i in items]

    columns = 8
    for start in range(0, len(items), columns):
        c_file.write("    {}\n".format(" ".join(items[start : start + columns])))

    c_file.write("""}};

/* expand_on_folding: {bytesize} bytes. */
""".format(bytesize=len(items) * expand_data_size))

    # Build and write the property data tables.
    for property in properties:
        property.generate_code(h_file, c_file, info)

    info["all_cases"].generate_code(h_file, c_file, info)
    info["simple_case_folding"].generate_code(h_file, c_file, info)
    info["full_case_folding"].generate_code(h_file, c_file, info)

    # Write the property function array.
    c_file.write("""
/* Property function table. */

RE_GetPropertyFunc re_get_property[] = {
""")

    for prop in properties:
        c_file.write("    re_get_{},\n".format(prop.name.lower()))

    c_file.write("};\n")

    h_file.close()
    c_file.close()

# Build a dict for converting 8-tuples into bytes.
bitflag_dict = {}
for value in range(0x100):
    bits = []
    for pos in range(8):
        bits.append((value >> pos) & 0x1)
    bitflag_dict[tuple(bits)] = value

# Storage and support for reduced names.
#
# A reduced name is a name converted to uppercase and with its punctuation
# removed.
reduced_names = {}

reduce_trans = str.maketrans({" ": "", "_": "","-": ""})

# The names, converted to a standardised form.
standardised_names = {}

# The Unicode data files.
unicode_data_base = "http://www.unicode.org/Public/UNIDATA/"

unicode_info = """
auxiliary/GraphemeBreakProperty.txt
auxiliary/SentenceBreakProperty.txt
auxiliary/WordBreakProperty.txt
Blocks.txt
CaseFolding.txt:~
DerivedCoreProperties.txt
extracted/DerivedBidiClass.txt
extracted/DerivedBinaryProperties.txt
extracted/DerivedCombiningClass.txt
extracted/DerivedDecompositionType.txt
extracted/DerivedEastAsianWidth.txt
extracted/DerivedGeneralCategory.txt
extracted/DerivedJoiningGroup.txt
extracted/DerivedJoiningType.txt
extracted/DerivedLineBreak.txt
extracted/DerivedNumericType.txt
extracted/DerivedNumericValues.txt:NumericValues
HangulSyllableType.txt
IndicMatraCategory.txt
IndicSyllabicCategory.txt
PropertyAliases.txt:~
PropertyValueAliases.txt:~
PropList.txt
Scripts.txt
#UnicodeData.txt
"""

# Download the Unicode data files.
for line in unicode_info.splitlines():
    if line and line[0] != "#":
        url = line.partition(":")[0]
        download_unicode_file(urljoin(unicode_data_base, url), unicode_folder)

# Parse the Unicode data.
info = parse_unicode_data()

properties = info["properties"]

write_properties_description(properties, properties_path)

if len(properties) > 0x100:
    raise UnicodeDataError("more than 256 properties")

for prop in properties:
    if len(prop) > 0x100:
        raise UnicodeDataError("more than 256 values: property '{}'".format(prop.name))

# Create the list of standardised strings.
strings = set()
for prop in properties:
    strings.add(prop.name)
    strings |= prop.aliases

    for val in prop:
        strings.add(val.name)
        strings |= val.aliases

strings = sorted(set(strings), key=reduce_name)

# Generate the code.
generate_code(strings)

print("\nThere are {} properties".format(len(properties)))

import re
code = open(c_path).read()
sizes = defaultdict(int)
for n, s in re.findall(r"(\w+(?: \w+)*): (\d+) bytes", code):
    sizes[n] += int(s)
sizes = sorted(sizes.items(), key=lambda pair: pair[1], reverse=True)
total_size = sum(s for n, s in sizes)
print("\nTotal: {} bytes\n".format(total_size))
prop_width = max(len(row[0]) for row in sizes)
prop_width = max(prop_width, 8)
storage_width = max(len(str(row[1])) for row in sizes)
storage_width = max(storage_width, 7)
print("{:{}}  {:{}}  {}".format("Property", prop_width, "Storage", storage_width, "Percentage"))
print("{:{}}  {:{}}  {}".format("--------", prop_width, "-------", storage_width, "----------"))
format = "{{:<{}}}  {{:>{}}}    {{:>5.1%}}".format(prop_width, storage_width)
for n, s in sizes:
    print(format.format(n, s, s / total_size))

print("\nFinished!")
