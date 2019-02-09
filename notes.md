# WordNet Interface Documentation

Words:
"SynSet()":
Basically you look up words with this function, and gets you back the related synsets.

SynSet:
Set of synonyms that share a common meaning.

- Lemmas represent a specific sense of a specific word.
- Hypernym: Word with broad meaning, constituing a category into which words with more
  specific meaning
  wn.synset('dog.n.01').lowest_common_hypernyms(wn.synset('cat.n.01')) // is an example

Lemmas

- Lemmas have either "a,v,n" as options when you're iterating through them

## Language and Syntax

[This is from here](https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72)

[This is a list of all possible tags and their meaning in the following sections](https://web.archive.org/web/20130517134339/http://bulba.sdsu.edu/jeanette/thesis/PennTags.html)

### Parts of Speech

Just labels each part of the sentence with different tags that the ML models can learn from
Broken down into - Nouns - Verbs - Adjectives - Adverbs.

### Shallow Parsing

Similar to PoS, it breaks it down into groups of words, or _phrases_.
Allows for light parsing or chunking. It analyses the structure of the sentence to break it down
to its smallest constituents.

  - Noun Phrase(NP): Phrases where a noun is the head word
  - Verb Phrase(VP): Lexical units that verb acting as the head word.
  - Adjective Phrase(ADJP): Phrases with an adjective as the head word. Describes the nouns/pronouncs in a sentence.
  - Adverb Phrase(ADVP): Phrases act like adverbs, since the adverb is the head of the phrase.
  - Propositional Phrase(PP): Contain prepositions as the head word, and other lexical components.

### Constituency Parsing

Used to analyze and determine the constituents of a sentence. The grammer models the
internal structure of sentences, based on a hierarchichally ordered structure of their constituents.

Every word belongs to a specific lexical category, and forms the head word of different phrases.
These phrases are formed based on rules called "phrase structure rules".

"Phrase structure rules" form the core of the constituency grammers as they talk about syntax and
rules that govern the hierarchy and ordering of the various consistuents in the sentences.
They determine:
  - What words are used to construct the phrases or constituents.
  - Determine how we need to order these consistuents together.

Essentially it just shows how different phrases are connected.
It's defined using the "phrase structure rules"
If needed, it can be done using the "Stanford Parser"

### Dependency Parsing
