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

## Word2Vec

- For a term-document matrix, you'd map the document to the words used and the count of the occurances of the words
- For a word-word matrix, or a word-context matrix you look at the words surrounding the main word
  rather than the whole document. You take into account some "contexts".
- A word is now defined as a vector of the counts over the context words.
- If you look at a word-word matrix, it's absolutely massive, sometimes 50,000 x 50,000 because of the size of the language
- this makes a very sparse matrix
- If **the size of the windows is SMALL, it's syntactic**
- if **the size of the windows is LARGE, it's semantic**

- There are 2 kinds of co-occurences between words (This is info)[https://cd1.edb.hkedcity.net/cd/eng/vocab09/ch1_3-2.htm] - FirstOrder: (Syntagmatic association): Refer to word combinations, "play football", "go shopping" etc. - SecondOrder: (Paradigmatic Association): Words are grouped together, things like 'piano, guitar, violin, drums' are all instruments and so are grouped as such

### Pointwise Mutual Information:

- Pointwise mutual information is the measure of whether a context word is _particularly informative_ about the target word
- Pointwise mutual information measures whether events `x` and `y` co-occur more than if they were independent
- Calculated by taking the Log(base2) of (P(x,y)/P(x)P(y))

### Measuring similarity of words

- Given 2 words, `v` and `w`.
- We need to measure their similarity
- Since they're vectors, go after their _dot product_

# Parts of Speech Tagging

## Lists of parts of speech

- Noun: Describes an entity
- Pronoun: Substitute for a noun, (eg: them, he, I)
- Adjective: describing word (big, brave)
- Verb: Action words (walking, happen, be)
- Adverb: Modifier to an adjective, (very, quite)
- Preposition: Adds and aids syntactic context (in, of), and shows relation b/w a noun and pronoun
- Conjunction: Connects words, phrases and clauses (and, but)
- Interjection: Expresses emotion (huzzah, alas)
- Article: describes the limits (a, an, the)

Above parts of speeches are called classes, and they're defined based on the morphological properties of the syntactic roles of the words [This is a good resource](http://www.dii.unisi.it/~maggini/Teaching/TEL/slides%20EN/06%20-%20NLP%20-%20PoS%20Tagging.pdf)

Two types of classes:

1. Open : Classes that can have new terms added ( eg verbs and nouns )
2. Closed: Classes that contain a fixed set of terms, i.e articles with a, an, the.

## Nouns:

- There's proper nouns ( Marco, Italy etc )
- Common nouns ( books, lectures etc )

## Verbs and Adverbs:

- Adverbs are **used to modify other terms, not only verbs**.
- There's directional adverbs (up,there,here)
- Degree adverbs specify the extent of an adverb (extremely , very )
- Manner adverbs describe the modality of the action (slowly, delicately etc)
- Temporal adverbs describe the time for an action/event (yesterday, today, before ..)

## Closed Word Classes:

1. Prepositions: occur before noun phrases (express a relationship - spatial / temporal)
2. Determiners: Beginning of the noun phrase (eg "the")
3. Conjunctions: Connect phrases / clauses or sentences
4. Pronouns: Short elements used to refer to noun phrases
5. Auxiliary verbs: Used in combinations with other verbs to give a particular meaning / phrase (have, be do will)

## Tagging algorithms:

1. Rule-Based Taggers: Large "rule-base" to specify conditions to be verified to assign a specific tag in the ambigious case
2. Probabilistic Taggers: Estimate the progbability that a given word as a specific tag in the observed context. Parameters of the prob model are estimated on a reference corpus (supervised learning?)
3. Other: Set as a classification task, which exploits features of the words they're surrounded by. Taggers can exploit the rules learned by examples (unsupervised learning)
