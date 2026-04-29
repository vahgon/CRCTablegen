# CRCTablegen

CRCTablegen is a python script that quickly creates CRC-8, CRC-16, and CRC-32 lookup tables from user-provided arguments. With it, you can specify your own generator polynomial,
use right shifts for a reflected (LSB) lookup table, customize the string format of the generated table, and more.

### Getting Started

1. Clone the repo:
   
   ```
   $ git clone https://github.com/vahgon/crctablegen
   ```

2. Enter the directory and run the script:

   ```
   $ cd crctablegen
   $ python crctablegen.py
   ```

Running `crctablegen.py` without passing any arguments will generate a standard CRC-32 lookup table with the generator polynomial **0x04c11db7**:

  ```
  ❯ ./crctablegen.py 
  00000000 04c11db7 09823b6e 0d4326d9 130476dc 17c56b6b 1a864db2 1e475005
  2608edb8 22c9f00f 2f8ad6d6 2b4bcb61 350c9b64 31cd86d3 3c8ea00a 384fbdbd
  4c11db70 48d0c6c7 4593e01e 4152fda9 5f15adac 5bd4b01b 569796c2 52568b75
  6a1936c8 6ed82b7f 639b0da6 675a1011 791d4014 7ddc5da3 709f7b7a 745e66cd
  9823b6e0 9ce2ab57 91a18d8e 95609039 8b27c03c 8fe6dd8b 82a5fb52 8664e6e5
  be2b5b58 baea46ef b7a96036 b3687d81 ad2f2d84 a9ee3033 a4ad16ea a06c0b5d
  d4326d90 d0f37027 ddb056fe d9714b49 c7361b4c c3f706fb ceb42022 ca753d95
  f23a8028 f6fb9d9f fbb8bb46 ff79a6f1 e13ef6f4 e5ffeb43 e8bccd9a ec7dd02d
  34867077 30476dc0 3d044b19 39c556ae 278206ab 23431b1c 2e003dc5 2ac12072
  128e9dcf 164f8078 1b0ca6a1 1fcdbb16 018aeb13 054bf6a4 0808d07d 0cc9cdca
  7897ab07 7c56b6b0 71159069 75d48dde 6b93dddb 6f52c06c 6211e6b5 66d0fb02
  5e9f46bf 5a5e5b08 571d7dd1 53dc6066 4d9b3063 495a2dd4 44190b0d 40d816ba
  aca5c697 a864db20 a527fdf9 a1e6e04e bfa1b04b bb60adfc b6238b25 b2e29692
  8aad2b2f 8e6c3698 832f1041 87ee0df6 99a95df3 9d684044 902b669d 94ea7b2a
  e0b41de7 e4750050 e9362689 edf73b3e f3b06b3b f771768c fa325055 fef34de2
  c6bcf05f c27dede8 cf3ecb31 cbffd686 d5b88683 d1799b34 dc3abded d8fba05a
  690ce0ee 6dcdfd59 608edb80 644fc637 7a089632 7ec98b85 738aad5c 774bb0eb
  4f040d56 4bc510e1 46863638 42472b8f 5c007b8a 58c1663d 558240e4 51435d53
  251d3b9e 21dc2629 2c9f00f0 285e1d47 36194d42 32d850f5 3f9b762c 3b5a6b9b
  0315d626 07d4cb91 0a97ed48 0e56f0ff 1011a0fa 14d0bd4d 19939b94 1d528623
  f12f560e f5ee4bb9 f8ad6d60 fc6c70d7 e22b20d2 e6ea3d65 eba91bbc ef68060b
  d727bbb6 d3e6a601 dea580d8 da649d6f c423cd6a c0e2d0dd cda1f604 c960ebb3
  bd3e8d7e b9ff90c9 b4bcb610 b07daba7 ae3afba2 aafbe615 a7b8c0cc a379dd7b
  9b3660c6 9ff77d71 92b45ba8 9675461f 8832161a 8cf30bad 81b02d74 857130c3
  5d8a9099 594b8d2e 5408abf7 50c9b640 4e8ee645 4a4ffbf2 470cdd2b 43cdc09c
  7b827d21 7f436096 7200464f 76c15bf8 68860bfd 6c47164a 61043093 65c52d24
  119b4be9 155a565e 18197087 1cd86d30 029f3d35 065e2082 0b1d065b 0fdc1bec
  3793a651 3352bbe6 3e119d3f 3ad08088 2497d08d 2056cd3a 2d15ebe3 29d4f654
  c5a92679 c1683bce cc2b1d17 c8ea00a0 d6ad50a5 d26c4d12 df2f6bcb dbee767c
  e3a1cbc1 e760d676 ea23f0af eee2ed18 f0a5bd1d f464a0aa f9278673 fde69bc4
  89b8fd09 8d79e0be 803ac667 84fbdbd0 9abc8bd5 9e7d9662 933eb0bb 97ffad0c
  afb010b1 ab710d06 a6322bdf a2f33668 bcb4666d b8757bda b5365d03 b1f740b4
  ```

### Detailed Usage

**CRCTablegen** features a CLI that can be utilized to directly effect either the formatting of the generated table and elements or the actual computation of elements themselves.

#### CRC Specific options include:

- `-p`, `--polynomial` - _Hex representation of some generator polynomial_

- `-d`, `--degree` - _Integer value representing the degree of_ `--polynomial`
  - _The degree _must_ be specified if you use your own generator polynomial through `--polynomial` and it is **not** 32-bits_
  
- `-r`, `--reflect-poly` - _Use a LSB implementation for finding table values_
  - _Does not reverse the bits of a polynomial given through_ `--polynomial`, _it simply switches the bitwise shift to use from left to right_

- `--sb8` - _Generates eight tables as seen in slice-by-8 CRC implementations_

- `--sb4` - _Generates four tables as seen in slice-by-4 CRC implementations_

#### Formatting options include:

- `-c`, `--container` - _Encases resulting table in either_ `b`_rackets or_ `c`_urly braces_
  
- `-s`, `--separator` - _String value used as a separator for row elements_
  
- `-i`, `--indent` - _Integer value used as width of indentation for table rows_
  
- `--prefix` - _Prefixes all table elements with_ `0x`

- `-o`, `--output` - _Will create and/or write table to the provided filesystem path_

##### Mutually Exclusive options:

- `--row-len` - _Integer value to use as the maximum number of columns a row can have_

- `--horizontal` - _Output table will have only one row of 256 columns_

- `--vertical` - _Output table will have only one column of 256 rows_

---

As shown with the generated lookup table in [Getting Started](#getting-started), the script will use a default generator polynomial if one is not provided through `--polynomial`.

If `--degree 8` or `--degree 16` is passed without a generator polynomial specified, then the default generator polynomial is set to either [**0x31**](https://onlinedocs.microchip.com/oxy/GUID-1618003F-992B-4E48-9411-5E5D5D952C06-en-US-3/GUID-38D5F63C-5EF7-4E66-94BC-02A9D9A42B27.html) or **0x1021** respectively.

If `--reflect-poly` is set without `--polynomial`, then the generator polynomial used is simply the default ( **0x04c11db7** ) but bit-reversed ( **0xedb88320** ). This is also the case if a degree of 8 or 16 is specified alongside `--reflect-poly` and a polynomial is not given as an argument to the CLI.

---

### Example Use

Lets create a table using some of the options talked about in [Detailed Usage](#detailed-usage).

To create a table using the reflected Castagnoli CRC-32 generator polynomial with row indents set to 2 spaces, the table contained in brackets, table elements separated by a comma and space (`, `), the maximum number of columns for any given row set to 10, table elements prefixed with **0x**, and the result saved to "crc32c_result":

  ```
  $ ./crctablegen.py -r -p 0x82F63B78 --indent 2 -c b -s ", " --row-len 10 --prefix -o crc32c_result
  ```
  > _Note that -d does not need to be specified because the default for **any** execution of the script is 32. If you want to use your own 8 or 16 bit generator polynomial, then you **must** set `-d`_

Then, taking a look at `crc32c_result`:

```
[
  0x00000000, 0xf26b8303, 0xe13b70f7, 0x1350f3f4, 0xc79a971f, 0x35f1141c, 0x26a1e7e8, 0xd4ca64eb, 0x8ad958cf, 0x78b2dbcc,
  0x6be22838, 0x9989ab3b, 0x4d43cfd0, 0xbf284cd3, 0xac78bf27, 0x5e133c24, 0x105ec76f, 0xe235446c, 0xf165b798, 0x030e349b,
  0xd7c45070, 0x25afd373, 0x36ff2087, 0xc494a384, 0x9a879fa0, 0x68ec1ca3, 0x7bbcef57, 0x89d76c54, 0x5d1d08bf, 0xaf768bbc,
  0xbc267848, 0x4e4dfb4b, 0x20bd8ede, 0xd2d60ddd, 0xc186fe29, 0x33ed7d2a, 0xe72719c1, 0x154c9ac2, 0x061c6936, 0xf477ea35,
  0xaa64d611, 0x580f5512, 0x4b5fa6e6, 0xb93425e5, 0x6dfe410e, 0x9f95c20d, 0x8cc531f9, 0x7eaeb2fa, 0x30e349b1, 0xc288cab2,
  0xd1d83946, 0x23b3ba45, 0xf779deae, 0x05125dad, 0x1642ae59, 0xe4292d5a, 0xba3a117e, 0x4851927d, 0x5b016189, 0xa96ae28a,
  0x7da08661, 0x8fcb0562, 0x9c9bf696, 0x6ef07595, 0x417b1dbc, 0xb3109ebf, 0xa0406d4b, 0x522bee48, 0x86e18aa3, 0x748a09a0,
  0x67dafa54, 0x95b17957, 0xcba24573, 0x39c9c670, 0x2a993584, 0xd8f2b687, 0x0c38d26c, 0xfe53516f, 0xed03a29b, 0x1f682198,
  0x5125dad3, 0xa34e59d0, 0xb01eaa24, 0x42752927, 0x96bf4dcc, 0x64d4cecf, 0x77843d3b, 0x85efbe38, 0xdbfc821c, 0x2997011f,
  0x3ac7f2eb, 0xc8ac71e8, 0x1c661503, 0xee0d9600, 0xfd5d65f4, 0x0f36e6f7, 0x61c69362, 0x93ad1061, 0x80fde395, 0x72966096,
  0xa65c047d, 0x5437877e, 0x4767748a, 0xb50cf789, 0xeb1fcbad, 0x197448ae, 0x0a24bb5a, 0xf84f3859, 0x2c855cb2, 0xdeeedfb1,
  0xcdbe2c45, 0x3fd5af46, 0x7198540d, 0x83f3d70e, 0x90a324fa, 0x62c8a7f9, 0xb602c312, 0x44694011, 0x5739b3e5, 0xa55230e6,
  0xfb410cc2, 0x092a8fc1, 0x1a7a7c35, 0xe811ff36, 0x3cdb9bdd, 0xceb018de, 0xdde0eb2a, 0x2f8b6829, 0x82f63b78, 0x709db87b,
  0x63cd4b8f, 0x91a6c88c, 0x456cac67, 0xb7072f64, 0xa457dc90, 0x563c5f93, 0x082f63b7, 0xfa44e0b4, 0xe9141340, 0x1b7f9043,
  0xcfb5f4a8, 0x3dde77ab, 0x2e8e845f, 0xdce5075c, 0x92a8fc17, 0x60c37f14, 0x73938ce0, 0x81f80fe3, 0x55326b08, 0xa759e80b,
  0xb4091bff, 0x466298fc, 0x1871a4d8, 0xea1a27db, 0xf94ad42f, 0x0b21572c, 0xdfeb33c7, 0x2d80b0c4, 0x3ed04330, 0xccbbc033,
  0xa24bb5a6, 0x502036a5, 0x4370c551, 0xb11b4652, 0x65d122b9, 0x97baa1ba, 0x84ea524e, 0x7681d14d, 0x2892ed69, 0xdaf96e6a,
  0xc9a99d9e, 0x3bc21e9d, 0xef087a76, 0x1d63f975, 0x0e330a81, 0xfc588982, 0xb21572c9, 0x407ef1ca, 0x532e023e, 0xa145813d,
  0x758fe5d6, 0x87e466d5, 0x94b49521, 0x66df1622, 0x38cc2a06, 0xcaa7a905, 0xd9f75af1, 0x2b9cd9f2, 0xff56bd19, 0x0d3d3e1a,
  0x1e6dcdee, 0xec064eed, 0xc38d26c4, 0x31e6a5c7, 0x22b65633, 0xd0ddd530, 0x0417b1db, 0xf67c32d8, 0xe52cc12c, 0x1747422f,
  0x49547e0b, 0xbb3ffd08, 0xa86f0efc, 0x5a048dff, 0x8ecee914, 0x7ca56a17, 0x6ff599e3, 0x9d9e1ae0, 0xd3d3e1ab, 0x21b862a8,
  0x32e8915c, 0xc083125f, 0x144976b4, 0xe622f5b7, 0xf5720643, 0x07198540, 0x590ab964, 0xab613a67, 0xb831c993, 0x4a5a4a90,
  0x9e902e7b, 0x6cfbad78, 0x7fab5e8c, 0x8dc0dd8f, 0xe330a81a, 0x115b2b19, 0x020bd8ed, 0xf0605bee, 0x24aa3f05, 0xd6c1bc06,
  0xc5914ff2, 0x37faccf1, 0x69e9f0d5, 0x9b8273d6, 0x88d28022, 0x7ab90321, 0xae7367ca, 0x5c18e4c9, 0x4f48173d, 0xbd23943e,
  0xf36e6f75, 0x0105ec76, 0x12551f82, 0xe03e9c81, 0x34f4f86a, 0xc69f7b69, 0xd5cf889d, 0x27a40b9e, 0x79b737ba, 0x8bdcb4b9,
  0x988c474d, 0x6ae7c44e, 0xbe2da0a5, 0x4c4623a6, 0x5f16d052, 0xad7d5351,
]
```  
