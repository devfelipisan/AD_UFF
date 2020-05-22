#!/usr/bin/env python
# coding: UTF-8
#
## @package DNAStrand
#
#   Playing with string matching.
#
#   @author Paulo Roma
#   @since 15/12/2019
#   @see https://www.sciencedirect.com/topics/medicine-and-dentistry/dna-strand
#
import sys

class DNAStrand:

    ## Valid DNA symbols.
    symbols = 'ATCG'


    ##
     # Constructs a DNAStrand with the given string of data, 
     # normally consisting of characters 'A', 'C', 'G', and 'T'.
     # Raises a ValueError exception, in case of an invalid givenData strand.
     #
     # @param givenData string of characters for this DNAStrand.
     #
    def __init__(self, givenData):
        ## Strand of this DNA, in upper case.
        self.strand = givenData.upper()

        # ...


    ## Returns a string representing the strand data of this DNAStrand.
    def __str__(self):
        return self.strand


    ##
     # Returns a new DNAStrand that is the complement of this one,
     # that is, 'A' is replaced with 'T' and so on.
     #
     # @return complement of this DNA.
     #
    def createComplement(self):
        complement = ""
        translator = {'A':'T','T':'A','C':'G','G':'C' } # Criado um dicionario contendo as conversões necessárias para criar o complemento
        for i in self.strand: # Loop que verifica todos os caracteres e procede com a
            complement += translator[i] # tradução conforme dicionario tradutor
    
        return DNAStrand(complement)
    

    ##
     # Returns a string showing which characters in this strand are matched with 'other', 
     # when shifted left by the given amount.
     #
     # @param other given DNAStrand.
     # @param shift number of positions to shift other to the left.
     # @return a copy of this strand, where matched characters are upper case and unmatched, lower case.
     #
    def findMatchesWithLeftShift(self, other, shift):
        

        if (shift < 0 or len(other.strand) - shift <= 0 ):
            return self.countMatchesWithLeftShift(other, shift), self.strand.lower()

        matches = ''

        loop = min(len(self.strand), len(other.strand)-shift)

        for i in range(loop):
            matches += self.strand[i].upper() if self.matches(self.strand[i], other.createComplement().strand[i+shift]) else self.strand[i].lower()

        matches = matches + self.strand[len(matches):].lower()

        assert(self.strand.lower() == matches.lower())

        matches = self.countMatchesWithLeftShift(other, shift), matches
 
        return matches  

    ##
     # Returns a string showing which characters in this strand are matched with 'other',
     # when shifted right by the given amount.
     #
     # @param other given DNAStrand.
     # @param shift number of positions to shift other to the right.
     # @return a copy of this strand, where matched characters are upper case and unmatched, lower case.
     #
    def findMatchesWithRightShift(self, other, shift):
        
        if (shift < 0 or len(self.strand) - shift <= 0 ):
            return self.countMatchesWithRightShift(other, shift), self.strand.lower()
        
        loop = min(len(self.strand)-shift, len(other.strand))
        
        matches = ''

        for i in range(loop):
            matches += self.strand[shift+i] if self.matches(self.createComplement().strand[shift+i], other.strand[i]) else self.strand[shift+i].lower()
        
        #matches = self.strand[:shift].lower() + matches
        matches = self.strand[:shift].lower() + matches + self.strand[shift+len(matches):].lower()
        assert(self.strand.lower() == matches.lower())

        matches = self.countMatchesWithRightShift(other, shift), matches

        return matches
    
    ##
     # Returns the maximum possible number of matching base pairs,
     # when the given sequence is shifted left or right by any amount.
     #
     # @param other given DNAStrand to be matched with this one.
     # @return maximum number of matching pairs.
     #
    def findMaxPossibleMatches(self, other, shift:int = None):
        COUNT, POSX = 0, 0
        SENSE = ''

        if shift == None:
            shift = len(other.strand)

        for i in range(shift):
            if self.countMatchesWithRightShift(other, i) > COUNT:
                COUNT = self.countMatchesWithRightShift(other, i)
                POSX = i
                SENSE = 'Right'

            elif self.countMatchesWithLeftShift(other, i) > COUNT:
                COUNT = self.countMatchesWithLeftShift(other, i)
                POSX = i*(-1)
                SENSE = 'Left'

        return COUNT, POSX, SENSE

    ##
     # Returns the number of matching pairs,
     # when 'other' is shifted to the left by 'shift' positions.
     #
     # @param other given DNAStrand to match with this strand.
     # @param shift number of positions to shift other to the left.
     # @return number of matching pairs.
     #
    def countMatchesWithLeftShift(self, other, shift):
        count = 0

        if (shift < 0 or len(other.strand) - shift <= 0 ):
            return count

        loop = min(len(self.strand), len(other.strand)-shift)

        for i in range(loop):
            count += 1 if self.matches(self.createComplement().strand[i], other.strand[shift+i]) else 0
                    
        return count
    

    ##
     # Returns the number of matching pairs,
     # when 'other' is shifted to the right by 'shift' positions.
     #
     # @param other given DNAStrand to be matched with this one.
     # @param shift number of positions to shift other to the right.
     # @return number of matching pairs.
     #
    def countMatchesWithRightShift (self, other, shift):
        count = 0

        if (shift < 0 or len(self.strand) - shift <= 0 ):
            return count

        loop = min(len(self.strand)-shift, len(other.strand))
        
        for i in range(loop):
            count += 1 if self.matches(
                self.createComplement().strand[shift+i], other.strand[i]) else 0

        return count

    ##
     # Determines whether all characters in this strand are valid ('A', 'G', 'C', or 'T').
     #
     # @return True if valid, and False otherwise.
     #
    def isValid(self):
        valid = True

        if set(self.symbols).issuperset(set(self.strand)):
            pass
        else:
            valid = False
        
        return valid
    

    ##
     # Counts the number of occurrences of the given character in this strand.
     #
     # @param ch given character.
     # @return number of occurrences of ch.
     #
    def letterCount(self,ch):
        count = 0

        for i in self.strand: # loop selecionando cada caracteres
            if i == ch: # validando se a condição do caractere é igual a setada na variavel ch
                count += 1 #caso a condição seja atendida este acrescentará ao total do contador count
        
        return count


    ##
     # Returns True if the two characters form a base pair ('A' with 'T' or 'C' with 'G').
     #
     # @param c1 first character.
     # @param c2 second character.
     # @return True if they form a base pair, and False otherwise.
     #
    def matches(self, c1, c2):
        match = False
        
        if c1 == c2:
            match = True

        return match
    

## Main program for testing.
 #
 # @param args two DNA strands.
 #
def main (args=None):

    if args is None:
       args = sys.argv

    if len(args) == 5:
       d = DNAStrand(args[1])
       d2 = DNAStrand(args[2])
       ls = int(args[3])
       rs = int(args[4])
    else:
       d = DNAStrand ("AGAGCAT")
       d2 = DNAStrand ("TCAT")
       ls = 2
       rs = 3

    print("Complement: %s" % d.createComplement()) 
    print("Count A in %s: %d" % (d, d.letterCount('A')))
    print("%s isValid: %r" % (d, d.isValid()))
    print("Strand: %s" % d2)
    print("RightShift: %s, %d = %s" % (d, rs, d2.findMatchesWithRightShift(d,rs)))
    print("Left Shift: %s, %d = %s" % (d, ls, d2.findMatchesWithLeftShift(d,ls)))
    print("Maximum Matches: %d" % d.findMaxPossibleMatches(d2)[0])
    print("Number of matches left shift: %s, %d = %s" % (d2, ls+rs, d.countMatchesWithLeftShift(d2,ls+rs)))

if __name__ == "__main__":
   sys.exit(main())
