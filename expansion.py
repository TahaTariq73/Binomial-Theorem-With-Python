import re
from math import factorial
from fractions import Fraction

class Expansion:
    BINOMIAL_REGEX = r"^[\(][0-9]+(\.[a-z])?(\^[0-9]+)? (\+|\-) [0-9]+(\.[a-z])?(\^[0-9]+)?\)\^[\-]?[0-9]+"

    def __init__(self, a, b, n, operator, x=None, y=None):
        self.operator = operator       
        self.a = a
        self.b = b
        self.n = n
        self.algebricExpOfa = tuple(x.split("^")) if (x != None) else None
        self.algebricExpOfb = tuple(y.split("^")) if (y != None) else None

        if (self.algebricExpOfa and len(self.algebricExpOfa) == 1):
            self.algebricExpOfa = tuple([self.algebricExpOfa[0], 1])

        if (self.algebricExpOfb and len(self.algebricExpOfb) == 1):
            self.algebricExpOfb = tuple([self.algebricExpOfb[0], 1])

    def __str__(self):
        x = self.algebricExpOfa
        y = self.algebricExpOfb

        # For debugging
        # print(f"a={self.a}\nax={x}\nope={self.operator}\nb={self.b}\nby={y}\nn={self.n}")

        x = "" if x == None else f".{x[0]}" if x[1] == 1 else f".{x[0]}^{x[1]}"
        y = "" if y == None else f".{y[0]}" if y[1] == 1 else f".{y[0]}^{y[1]}"

        return f"({self.a}{x} {self.operator} {self.b}{y})^{self.n}"

    def solvesTheBinomialExpansion(self):
        """Solves the given Binomial expansion"""

        if (self.n > 0 and type(self.n).__name__ == "int"):
            expansionStr = ""

            for i in range(self.n + 1):
                term = self.theGivenTerm(i + 1)
                sign = " - " if (term[1] == -1 and i != 0) else " + " if (term[1] == 1 and i != 0) else ""
                expansionStr = f"{expansionStr}{sign}{term[0]}"

            return expansionStr
        else:
            raise ValueError("This function can only be applied on expansion where n < 0.Instead try Binomial series")

    def solvesTheBinomialSeries(self):
        """Solves the binomial series"""

        if (self.n < 0 or type(self.n).__name__ == "float"):            
            expansionStr = ""

            for i in range(4):
                term = self.theGivenTerm(i + 1)
                sign = " - " if (term[1] == -1 and i != 0) else " + " if (term[1] == 1 and i != 0) else ""
                expansionStr = f"{expansionStr}{sign}{term[0]}"
            
            expansionStr = expansionStr + " -------------- ∞"
            return expansionStr
        else:
            raise ValueError("This function can only be applied on series where n > 0.Instead try Binomial expansion")

    def theGivenTerm(self, tn):
        """Solve the given term using binomial formulae"""
        
        n = self.n
        r = tn - 1

        # The formulae to solve a given term is 
        # {[n(n-1)(n-2)------(n-(r-1))] / r!}.a^(n-r).b^r

        ax = self.algebricExpOfa
        bx = self.algebricExpOfb
        variableOfa = f".{ax[0]}^{int(ax[1]) * (n - r)}" if (ax != None and (int(ax[1]) * (n - r)) != 0) else ""
        variableOfb = f".{bx[0]}^{int(bx[1]) * r}" if (bx != None and (int(bx[1]) * r) != 0) else ""

        sign = -1 if (tn % 2 == 0 and self.operator == "-") else 1
        combinationPart = self.theCombinationPartOfTerm(n=n, r=r)
        termCoefficient = combinationPart * (self.a ** (n - r)) * (self.b ** r)

        # Debug easily ;)
        # print(f"{combinationPart}*{(self.a ** (n - r))}{variableOfa}*{(self.b ** r)}{variableOfb}")

        if termCoefficient == int(termCoefficient):
            termCoefficient = int(termCoefficient)
        else:
            pointIndex = str(termCoefficient).find(".")
            # termCoefficient = float(str(termCoefficient)[:pointIndex + 2])
            termCoefficient = str(Fraction(termCoefficient).limit_denominator())

        if (termCoefficient != 0):
            term = f"{termCoefficient}{variableOfa}{variableOfb}" 
        else:
            term = int(termCoefficient)

        return (term, sign)

    def theCombinationPartOfTerm(self, n, r):
        """Solve the combination part of the given term"""

        # Logic to solve this part n(n-1)(n-2)------(n-(r-1)) of the formulae 
        y = n if r > 0 else 1
        for i in range((r - 1)):
            y = y * (n - (i + 1))
       
        numerator = y
        denominator = factorial(r)

        # Simply return this [n(n-1)(n-2)------(n-(r-1))] / r! 
        return numerator/denominator

    def theExpansionType(self):
        return "EXPANSION" if self.n > 0 and type(self.n).__name__ != "float" else "SERIES"

    @classmethod
    def isExpansion(cls, expansion):
        """Check the string weather it contains expansion or not"""

        search = re.search(cls.BINOMIAL_REGEX, expansion)
        search = True if search != None else False

        return search
    
    @classmethod
    def strToExpansion(cls, str):
        "Creates the class by using only expansion in string form"

        # Breaking the string into required parameters with Indexing
        # The string is verified with a fixed regex

        operatorIndex = str.find("+") if str.find("+") != -1 else str.find("-")
        aIndexes = (str.find("(") + 1, operatorIndex - 1)
        bIndexes = (operatorIndex + 2, str.find(")"))
        nIndexes = (str.find("^", str.find(")")) + 1, len(str)) 
        
        # Sperating the co-efficient & variable from the term of expansion
        splitOfa = str[aIndexes[0] : aIndexes[1]].split(".")
        splitOfb = str[bIndexes[0] : bIndexes[1]].split(".")

        operator = str[operatorIndex] # Shaping the values for class arguments
        n = int(str[nIndexes[0] : nIndexes[1]])
        a = int(splitOfa[0])
        b = int(splitOfb[0])
        
        algebricExpOfa = None if len(splitOfa) == 1 else splitOfa[1]
        algebricExpOfb = None if len(splitOfb) == 1 else splitOfb[1]

        return cls(a, b, n, operator, algebricExpOfa, algebricExpOfb)