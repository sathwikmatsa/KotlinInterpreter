# KotlinInterpreter
A simple interpreter for a small subset of Kotlin language

# Usage
```
ki.py kotlinFilename
```

### Supported data types
* Number/decimal
  - Example: 1.0
* Boolean
  - Supports constants 'true' and 'false'
* String
  - Example: "Justin Bieber"

### Supported Operations
* +		- addition  (numbers, string concatenation)
* -		- subtraction (numbers)
* \/		- divide
* \*		- multiply
* =		- assign
* <>	- not equal to
* <		- less than
* >		- greater than
* >=	- greater than or equal to
* <=	- less than or equal to
* ==  - equals
* OR	- logical or
* AND	- logical and
* %   - modulo

### Supported constructs (conditional/loop)
* if/else if/else*(condition){block}
  - nested if, while
* while(condition){block}
  - nested while, if

### Some more features
* Supports readLine()
  - Example: var a = readLine()!!.toInt()
* Supports println() and print()
* type inference
* type casting
  - toInt(), toDouble(), toString(), toBoolean()
* Unary operations
  - ++, -- : (postfix/prefix)
  - unary (-)
* Syntactic sugar
  - +=, -=, *=
* val, var - immutability & mutability
