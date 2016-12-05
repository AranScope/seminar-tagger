import nltk

class UnigramChunker(nltk.ChunkParserI):
    """
    Taken from example 3.1 in NLTK book.

    src: http://www.nltk.org/book/pylisting/code_unigram_chunker.py
    """
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)

class BigramChunker(nltk.ChunkParserI):
    """
    Adapted from example 3.1 in NLTK book.

    src: http://www.nltk.org/book/pylisting/code_unigram_chunker.py
    """
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.BigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)


class NeChunker:

    def __init__(self):
        pass

    def generate_chunks(self, text):
        """
        Generate entity chunks from a text.
        Using Python generator to yield entities when they are found.

        e.g.
        generate_chunks("Pierre Vinken, 61 years old, will join the board as a nonexecutive director Nov. 29. Mr. Vinken is chairman of Elsevier N.V., the Dutch publishing group.")

        will yield:
            Pierre Vinken
            Mr. Vinken
            Elsevier
            Dutch

        :param text: The input text, containing entities
        :return: Yield the entities found.
        """

        tokens = nltk.word_tokenize(text)
        pos_tagged_tokens = nltk.pos_tag(tokens)
        chunked_tokens = nltk.ne_chunk(pos_tagged_tokens)

        continuous_chunk = []
        current_chunk = []

        for chunk in chunked_tokens:
            if type(chunk) == nltk.Tree:
                tree_tokens = [token for token, position in chunk.leaves()]
                current_chunk.append(" ".join(tree_tokens))

            elif current_chunk:
                entity = " ".join(current_chunk)
                if entity not in continuous_chunk:
                    continuous_chunk.append(entity)
                    yield entity

                current_chunk = []

class RegexpChunker:

    def __init__(self):
        pass

    def generate_chunks(self, tagged_sentence):
        """
        Extract the entities from a sentence (noun-phrases) using
        nltk regexp grammar parser.

        :param tagged_sentence:
        :return:
        """
        grammar = """
            NP:
                {<[CDJNP].*>+}
        """
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(tagged_sentence)

        # we are only interested in noun phrases
        def filt(x):
            return x.label() == "NP"

        # filter out any subtrees that are not noun phrases
        nps_tree = [b for b in result.subtrees(filter=filt)]

        return nps_tree