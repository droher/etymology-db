# etymology-db
(Download the data here) (Last generated 9/24/2019)

A structured, comprehensive, and multilingual etymology dataset created by parsing Wiktionary's etymology sections. Key features:
*  2.8 million etymological relationships between 1.62 million terms in 2500 languages/dialects
*  27 different types of etymological relations, distinguishing between inheritance, borrowing, etc.
*  Hierarchical data that preserves relationship structures, such as the evolution of a term across languages

Caveat for people interested in using this for research: all information is pulled directly from Wiktionary via semi-structured text parsing, and I've made no effort yet to validate any particular result. That said, I would love for this to be useful, so please [contact me](mailto:david@boxball.io) if you have questions.

Here is a description of the table schema:


| Column Name | Description |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------|
| term_id | A hash of the term and its language. |
| lang | The language/dialect of the term. |
| term | The term itself. Usually a word, but can also be a prefix or a multi-word expression, hence "term" instead of word. |
| reltype | The kind of etymological relation being specified (see below for details on each possible value). |
| related_term_id | A hash of the related term and its language (useful for assembling relationships across multiple terms). |
| related_lang | The language/dialect of the related term. NULL for parent root nodes. |
| related_term | The term that is etymologically related to the original entry. NULL for parent root nodes. |
| position | Zero-indexed position of the term when the relation is made up of multiple terms (e.g. a compound). |
| group_tag | Randomly generated ID. populated only for the root nodes of nested relationships. |
| parent_tag | If this relation is inside of a nested structure, this will be populated with the `group_tag` of its immediate parent. NULL otherwise. |
| parent_position | Zero-indexed position of the relation inside of its nested structure. NULL if not nested. |

And here is a description of each relation type. Note that these are all derived directly from Wiktionary's etymology templates -- all rows are classified according to the name of the template from which the info was extracted, and no further inferences are made. The only exception to this is the `group` relations, which are based on formulaic and reoccuring patterns in natural language sections.

| Relation Type | Description |
|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| inherited_from | Indicates that `term` has an unbroken chain of inheritance from `related_term`. |
| borrowed_from | Indicates that `term` is a loanword borrowed during the time the borrowing language was spoken. |
| derived_from | A catch-all for a derivation relationship that is not specifically inherited/borrowed. |
| learned_borrowing_from | Borrowed from the original language via atypical ("inorganic") means of language contact. |
| orthographic_borrowing_from | Borrows the spelling of `related_term` but not the pronunciaton. |
| pie_root | Constructed root(s) of `term` in Proto-Indo-European.  |
| has_prefix | Indicates that `term` is partially based on the prefix `related_term`. |
| has_prefix_with_root | `related_term` is the term attached to a prefix (not necessarily a suffix, e.g. "normal" in "abnormal") |
| has_suffix | Same as above, but for suffixes. |
| has_suffix_with_root | Same as above, but for suffixes. |
| has_confix | A confix is a term whose first element is a prefix and whose last is a suffix. Position 0 of a confix is the prefix, and the last position is the suffix. |
| has_affix | Affix is the general form of prefix/suffix/confix and indicates some kind of compound structure without further detail. |
| compound_of | Indicates that `related_term` is the `position`-indexed term of a compound that makes up `term`. Used interchangeably with affix above. |
| back-formation_from | Indicates that `term` was formed from `related_term` by removing a prefix/suffix. |
| doublet_with | Indicates that `term` and `related_term` have the same etymological origin, especially when the relationship is unintuitive. |
| is_onomatopoeic | Indicates that `term` is an onomatopoeia (a word form from a sound associated with its meaning). |
| calque_of | Indicates that `term` is borrowed from `related_term` via a direct word-for-word or root-for-root translation. |
| semantic_loan_of | Special case of calques in which the word already existed but a new meaning was added. |
| named_after | Indicates that `term` is based on the name of the person `related_term` (an eponym). |
| phono-semantic_matching_of | Indicates that `term` and `related_term` have very similar sounds and meanings in both languages. |
| etymologically_related_to | A catch-all indicating `term` and `related_term` are etymologically related without any further context provided. |
| blend_of | Indicates that `term` is made up of a blend of `related_term` and the related terms in other `position`s. This differs from a compound in that the beginning of one word is combined with the ending of another. |
| clipping_of | Indicates that `term` is a shortened version of `related_term` without any semantic difference. |
| cognate_of | Indicates that `term` and `related_term` sound/mean similar things, but no direct ancestral relationship exists. |
| group_affix_root | A node that groups together rows that, when combined, form an affix.  |
| group_related_root | A node that groups together rows in which `related_terms` are not just related to the `term`, but to each other as well.. |
| group_derived_root | A node that groups together rows that, when combined, form an unbroken chain of inheritance (in reverse chronological order). |
