#!/usr/bin/env python

"""The ``inputfile`` module can be imported as such::

    from pyne.simplesim import inputfile

Below is the reference for this module.



This module employs the modules `reactordef` and `material` to generate
plaintext input files for a general code. Support is provided for MCNPX, and
support for Serpent is not complete but should be straightforward. The
extension to other codes may require more effort.

- Write out
- Read in a JSON file input def.
"""
# TODO need to be able to tell the user the numbers given to the different
# cards, for parsing.

import abc
import datetime
import textwrap

class IInputFile(object):
    """Abstract base class for classes that take system and option definitions
    to create an input file for a certain code (e.g. MCNPX, Serpent, MCODE,
    etc.).

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, fname, simdef, comments=True, header=None, plug=True,
                 float_format="%.5e"):
        """

        Parameters
        ----------
        fname : str
            Filename/path at which to create the input file.
        simdef: :py:class:`SimulationDefinition` or subclass.
            TODO
        comments : bool, optional
            TODO

        """
        self.fname = fname
        self.sim = simdef
        self.comments = comments
        self.header = header
        self.plug = plug
        self.float_format = num_format

    def write(self):
        self.set_up()
        # Should write the plug in the appropriate place.
        self._writesubclass()
        self.fid.close()

    def set_up(self):
        self.fid = open(self.fname, 'w')

    def clean_up(self):
        self.fid.close()
    
    @abc.abstractmethod
    def _write_subclass(self):
        return NotImplementedError

    def _write_plug(self):
        if self.plug:
            self._write_plug_subclass(
                    "Generated by the Python package PyNE (pyne.github.com).")
    
    @abc.abstractmethod
    def _write_plug_subclass(self, string):
        return NotImplementedError

    @abc.abstractmethod
    def add_user_card(self, block, card, comment=None):
        return NotImplementedError

    @abc.abstractmethod
    def add_user_card_literal(self, block, string):
        return NotImplementedError

    @abc.abstractmethod
    def _cell(self, cell):
        """Returns a cell card string."""
        return


class MCNPInput(IInputFile):
    """Contains a write method for each type of surface.
    """
    # TODO user can overload commenting methods.
    def __init__(self, fname, simdef, comments=True, header=None,
            description=None, plug=True, float_format="%.5f"):
        """

        """
        # TODO could cleanup keyword arguments wiht **kwarg.
        # Be careful with the order of inputs here for the kwargs.
        super(MCNPInput, self).__init__(fname, simdef, comments, header,
                plug, float_format, cont_by_blanks=True)
        self.description = description
        self.cont_by_blanks = cont_by_blanks
        self.commentwrap = Textwrapper(initial_indent='C',
                subsequent_indent='C', break_long_words=True)
        if self.cont_by_blanks:
            card_cont = 5 * ' '
        else:
            card_cont = '& '
        self.cardwrap = TextWrapper(subsequent_indent=card_cont,
                break_long_words=True)

    def _write_subclass(self):
        # Header
        if self.header:
            self._write_comment(self.header)
        else:
            self._write_comment("datetime: %s" % str(datetime.datetime.now()))
        if self.description:
            self._write_comment(self.description)
        self._write_plug()

        # Write cell cards.
        self._write_deck_header("Cell")
        self._write_dictionary(self.sim.sys.cells)

        # Write surface cards.
        self._write_deck_header("Surface")
        self._write_dictionary(self.sim.sys.surfaces)

        # Write data cards.
        self._write_deck_header("Data")
        # Material cards.
        self._write_data_header("Material")
        self._write_dictionary(self.sim.material)
        # Source cards.
        self._write_data_header("Source")
        self._write_dictionary(self.sim.source)
        # Tally cards.
        self._write_data_header("Tally")
        self._write_dictionary(self.sim.tally)
        # Misc cards.
        self._write_data_header("Miscellaneous")
        self._write_dictionary(self.sim.misc)

    def _write_dictionary(self, dictionary):
        for card in dictionary:
            if self.comments:
                self._write_comment(card.comment())
            self._write_card(card.mcnp(self.float_format, self.sim))

    def add_user_card(self, block, card, comment=None):
        # TODO
        # use textwrap
        pass


    def add_user_card_literal(self, block, string):
        # TODO
        pass

    def _write_plug_subclass(self, string):
        self._write_comment(string)

    def _write_deck_heading(self, string):
        heading = " %s Cards" % heading
        n_chars = len(" %s Cards" % heading)
        self._write_comment(n_chars * "=")
        self._write_comment(heading)
        self._write_comment(n_chars * "=")

    def _write_data_heading(self, string):
        heading = " %s Cards" % heading
        n_chars = len(" %s Cards" % heading)
        self._write_comment(n_chars * "*")
        self._write_comment(heading)
        self._write_comment(n_chars * "*")

    def _write_comment(self, comment=""):
        self.fid.write(self.commentwrap.wrap(comment))

    def _write_card(self, string):
        self.fid.write(self.cardwrap.wrap(string))

    def _cell(self, cell):
        """Returns a cell card string given a Cell card."""
        return


class SerpentInput(IInputFile):
    """Must find the cell used for a given material, and would need to create
    more than one material if necessary.

    """
    pass

